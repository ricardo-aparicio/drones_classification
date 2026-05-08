#!/usr/bin/env python3
import time
from pathlib import Path

import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from skimage.transform import resize
from ultralytics import YOLO

# =========================
# SDR
# =========================
SDR_IP = "ip:192.168.202.204"
FS = 50e6
RF_BW_HZ = 45e6
GAIN_DB = 30
WINDOW_SAMPLES = 200_000

# =========================
# Bandas y secuencia de escaneo
# =========================
CENTERS_24 = [2.427e9, 2.455e9]
CENTERS_58 = [5.646e9,5.756e9, 5.787e9, 5.818e9]

BANDS = {
    "2.4G": CENTERS_24,
    "5.8G": CENTERS_58,
}

SCAN_SEQUENCE = (
    [("2.4G", i, f) for i, f in enumerate(CENTERS_24)] +
    [("5.8G", i, f) for i, f in enumerate(CENTERS_58)]
)

# =========================
# Timing / retune
# =========================
RETUNE_SLEEP = 0.03   # antes 0.05
LOOP_SLEEP = 0.00     # antes 0.02

def retune_and_flush(sdr, lo_hz: float):
    sdr.rx_lo = int(lo_hz)
    time.sleep(RETUNE_SLEEP)
    _ = sdr.rx()  # flush 1 buffer


# =========================
# Frames
# =========================
FAST_FRAMES = 5
FOCUS_FRAMES = 8
FOCUS_REPEATS = 2
CONFIRM_FRAMES = 15
NEIGHBOR_FRAMES = 6

# =========================
# Suavizado temporal por frecuencia
# =========================
EMA_ALPHA_NEW = 0.65  # peso de la evidencia nueva

# =========================
# Umbrales (perfil long-range)
# =========================
# Etapa "near suspect" -> dispara FOCUS
NEAR_NONBG_CONF_THR = 0.28
NEAR_BEST_NONBG_THR = 0.22
NEAR_BG_GAP_THR = 0.25
NEAR_MARGIN_THR = 0.25

# Etapa sospechosa -> dispara HOLD
SUSPECT_NONBG_CONF_THR = 0.40
SUSPECT_BEST_NONBG_THR = 0.30
SUSPECT_BG_GAP_THR = 0.18
SUSPECT_MARGIN_THR = 0.18

# Confirmación final
CONFIRM_NONBG_CONF_THR = 0.50
CONFIRM_MARGIN_THR = 0.08

BACKGROUND_LABEL = "background"

# =========================
# Modelo
# =========================
ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "runs_yolo11_cls" / "drone_spectrograms_rc24_58_fly24_session_c_unopes" / "weights" / "best.pt"
_CMAP = plt.get_cmap("viridis")


def iq_to_spec_image(iq_seg: np.ndarray) -> np.ndarray:
    f, t, Sxx = spectrogram(
        iq_seg,
        fs=FS,
        window="hann",
        nperseg=1024,
        noverlap=512,
        scaling="density",
        mode="magnitude",
        return_onesided=False,
    )

    Sxx_db = 20 * np.log10(Sxx + 1e-12)

    mn = float(Sxx_db.min())
    mx = float(Sxx_db.max())
    Sxx_norm = (Sxx_db - mn) / (mx - mn + 1e-9)

    spec_256 = resize(
        Sxx_norm,
        (256, 256),
        mode="reflect",
        anti_aliasing=True
    ).astype(np.float32)

    img_rgba = _CMAP(spec_256)
    img_rgb = (img_rgba[:, :, :3] * 255).astype(np.uint8)
    return img_rgb


# =========================
# Helpers
# =========================
def collect_probs_mean_tuned(sdr, model, frames: int) -> tuple[np.ndarray | None, int]:
    probs_acc = None
    n_ok = 0

    for _ in range(frames):
        iq = sdr.rx()
        if len(iq) < WINDOW_SAMPLES:
            continue

        iq_seg = np.asarray(iq[:WINDOW_SAMPLES], dtype=np.complex64)
        img_rgb = iq_to_spec_image(iq_seg)
        results = model.predict(source=img_rgb, imgsz=256, verbose=False)
        probs = results[0].probs.data.cpu().numpy()

        probs_acc = probs.copy() if probs_acc is None else (probs_acc + probs)
        n_ok += 1

    if n_ok == 0 or probs_acc is None:
        return None, 0

    return probs_acc / n_ok, n_ok


def collect_probs_mean(sdr, model, lo_hz: float, frames: int) -> tuple[np.ndarray | None, int]:
    retune_and_flush(sdr, lo_hz)
    return collect_probs_mean_tuned(sdr, model, frames)


def summarize_probs(probs_mean: np.ndarray, class_names: dict) -> dict:
    top1 = int(np.argmax(probs_mean))
    conf1 = float(probs_mean[top1])

    tmp = probs_mean.copy()
    tmp[top1] = -1.0
    top2 = int(np.argmax(tmp))
    conf2 = float(probs_mean[top2])

    bg_idx = next(i for i, n in class_names.items() if n == BACKGROUND_LABEL)
    bg_conf = float(probs_mean[bg_idx])

    nonbg = probs_mean.copy()
    nonbg[bg_idx] = -1.0
    best_nonbg = int(np.argmax(nonbg))
    best_nonbg_conf = float(probs_mean[best_nonbg])

    label1 = class_names[top1]
    label2 = class_names[top2]
    best_nonbg_label = class_names[best_nonbg]

    margin = conf1 - conf2
    bg_gap = bg_conf - best_nonbg_conf  # si es pequeño, el no-background va cerca del background

    return {
        "top1": top1,
        "conf1": conf1,
        "label1": label1,
        "top2": top2,
        "conf2": conf2,
        "label2": label2,
        "margin": margin,
        "bg_conf": bg_conf,
        "best_nonbg": best_nonbg,
        "best_nonbg_label": best_nonbg_label,
        "best_nonbg_conf": best_nonbg_conf,
        "bg_gap": bg_gap,
        "probs": probs_mean,
    }


def update_ema(history: dict, key: float, probs: np.ndarray) -> np.ndarray:
    if key not in history:
        history[key] = probs.copy()
    else:
        history[key] = EMA_ALPHA_NEW * probs + (1.0 - EMA_ALPHA_NEW) * history[key]
    return history[key]


def is_near_suspect(s: dict) -> bool:
    # top1 no background aunque sea débil
    if s["label1"] != BACKGROUND_LABEL and s["conf1"] >= NEAR_NONBG_CONF_THR:
        return True

    # background gana, pero el mejor no-background está cerca
    if s["best_nonbg_conf"] >= NEAR_BEST_NONBG_THR and s["bg_gap"] <= NEAR_BG_GAP_THR:
        return True

    # caso ambiguo general
    if s["conf1"] >= 0.35 and s["margin"] <= NEAR_MARGIN_THR:
        return True

    return False


def is_suspect(s: dict) -> bool:
    # top1 no background con confianza moderada
    if s["label1"] != BACKGROUND_LABEL and s["conf1"] >= SUSPECT_NONBG_CONF_THR:
        return True

    # background gana, pero el mejor no-background va muy cerca
    if s["best_nonbg_conf"] >= SUSPECT_BEST_NONBG_THR and s["bg_gap"] <= SUSPECT_BG_GAP_THR:
        return True

    # margen ambiguo
    if s["conf1"] >= 0.35 and s["margin"] <= SUSPECT_MARGIN_THR:
        return True

    return False


def is_confirmed(s: dict) -> bool:
    return (
        s["label1"] != BACKGROUND_LABEL and
        s["conf1"] >= CONFIRM_NONBG_CONF_THR and
        s["margin"] >= CONFIRM_MARGIN_THR
    )


def neighbor_indices(band: str, idx: int) -> list[int]:
    centers = BANDS[band]
    out = []
    if idx - 1 >= 0:
        out.append(idx - 1)
    if idx + 1 < len(centers):
        out.append(idx + 1)
    return out


def weighted_merge(prob_items: list[tuple[np.ndarray, int]]) -> tuple[np.ndarray | None, int]:
    if not prob_items:
        return None, 0

    acc = None
    n_total = 0

    for probs, n in prob_items:
        if probs is None or n <= 0:
            continue
        if acc is None:
            acc = probs * n
        else:
            acc += probs * n
        n_total += n

    if acc is None or n_total == 0:
        return None, 0

    return acc / n_total, n_total


# =========================
# Main
# =========================
def main():
    print("[*] Conectando al SDR...")
    sdr = adi.Pluto(SDR_IP)

    sdr.sample_rate = int(FS)
    sdr.rx_rf_bandwidth = int(RF_BW_HZ)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = GAIN_DB
    sdr.rx_buffer_size = WINDOW_SAMPLES

    print("[*] SDR configurado:")
    print("    Fs  =", sdr.sample_rate)
    print("    BW  =", sdr.rx_rf_bandwidth)
    print("    G   =", sdr.rx_hardwaregain_chan0)

    print("[*] Cargando modelo YOLO:", MODEL_PATH)
    model = YOLO(str(MODEL_PATH))
    class_names = model.names
    print("[*] Clases del modelo:", class_names)

    print("\n[***] Escaneo multi-banda iniciado.")
    print(
        f"      FAST={FAST_FRAMES}  FOCUS={FOCUS_FRAMES}x{FOCUS_REPEATS}  "
        f"CONFIRM={CONFIRM_FRAMES}  NEIGH={NEIGHBOR_FRAMES}"
    )
    print("      Ctrl+C para detener.\n")

    # memoria EMA por LO
    history_ema: dict[float, np.ndarray] = {}

    try:
        while True:
            for band, idx, lo_hz in SCAN_SEQUENCE:
                # 1) retune + SCAN corto
                retune_and_flush(sdr, lo_hz)
                probs_fast, n_ok_fast = collect_probs_mean_tuned(sdr, model, FAST_FRAMES)
                if probs_fast is None:
                    continue

                s_fast = summarize_probs(probs_fast, class_names)

                ema_probs = update_ema(history_ema, lo_hz, probs_fast)
                s_ema = summarize_probs(ema_probs, class_names)

                print(
                    f"[SCAN] {band} FREC={lo_hz/1e9:.3f} "
                    f"PRED1={s_fast['label1']:10s} {s_fast['conf1']:.3f} | "
                    f"PRED2={s_fast['label2']:10s} {s_fast['conf2']:.3f} | "
                    f"best_nonbg={s_fast['best_nonbg_label']:10s} {s_fast['best_nonbg_conf']:.3f} | "
                    f"bg_gap={s_fast['bg_gap']:.3f} | "
                    f"margin={s_fast['margin']:.3f} | frames={n_ok_fast}",
                    flush=True
                )

                # 2) si está cerca de sospecha -> FOCUS en el mismo LO
                focus_summary = s_fast
                if is_near_suspect(s_fast) or is_near_suspect(s_ema):
                    focus_items = [(probs_fast, n_ok_fast)]

                    for _ in range(FOCUS_REPEATS):
                        probs_f, n_ok_f = collect_probs_mean_tuned(sdr, model, FOCUS_FRAMES)
                        if probs_f is not None and n_ok_f > 0:
                            focus_items.append((probs_f, n_ok_f))

                    probs_focus, n_ok_focus = weighted_merge(focus_items)
                    if probs_focus is not None:
                        focus_summary = summarize_probs(probs_focus, class_names)

                        ema_focus = update_ema(history_ema, lo_hz, probs_focus)
                        s_ema_focus = summarize_probs(ema_focus, class_names)

                        print(
                            f"[FOCUS] {band} FREC={lo_hz/1e9:.3f} "
                            f"PRED1={focus_summary['label1']:10s} {focus_summary['conf1']:.3f} | "
                            f"PRED2={focus_summary['label2']:10s} {focus_summary['conf2']:.3f} | "
                            f"best_nonbg={focus_summary['best_nonbg_label']:10s} {focus_summary['best_nonbg_conf']:.3f} | "
                            f"bg_gap={focus_summary['bg_gap']:.3f} | "
                            f"margin={focus_summary['margin']:.3f} | frames={n_ok_focus}",
                            flush=True
                        )

                        # 3) HOLD / CONFIRM si después de FOCUS ya se ve sospechoso
                        if is_suspect(focus_summary) or is_suspect(s_ema_focus):
                            probs_c, n_ok_c = collect_probs_mean_tuned(sdr, model, CONFIRM_FRAMES)
                            if probs_c is None:
                                continue

                            s_conf = summarize_probs(probs_c, class_names)
                            update_ema(history_ema, lo_hz, probs_c)

                            print(
                                f"[HOLD] {band} FREC={lo_hz/1e9:.3f} "
                                f"PRED1={s_conf['label1']:10s} {s_conf['conf1']:.3f} | "
                                f"PRED2={s_conf['label2']:10s} {s_conf['conf2']:.3f} | "
                                f"best_nonbg={s_conf['best_nonbg_label']:10s} {s_conf['best_nonbg_conf']:.3f} | "
                                f"bg_gap={s_conf['bg_gap']:.3f} | "
                                f"margin={s_conf['margin']:.3f} | frames={n_ok_c}",
                                flush=True
                            )

                            # 4) evento confirmado + vecinos
                            if is_confirmed(s_conf):
                                print(
                                    f"[EVENT] CONFIRMED BAND={band} FREC={lo_hz/1e9:.3f} "
                                    f"PRED1={s_conf['label1']} conf={s_conf['conf1']:.3f} "
                                    f"PRED2={s_conf['label2']} conf2={s_conf['conf2']:.3f} "
                                    f"best_nonbg={s_conf['best_nonbg_label']} best_nonbg_conf={s_conf['best_nonbg_conf']:.3f} "
                                    f"margin={s_conf['margin']:.3f}",
                                    flush=True
                                )

                                neigh = neighbor_indices(band, idx)
                                for j in neigh:
                                    lo_nb = BANDS[band][j]
                                    probs_n, n_ok_n = collect_probs_mean(sdr, model, lo_nb, NEIGHBOR_FRAMES)
                                    if probs_n is None:
                                        continue

                                    s_nb = summarize_probs(probs_n, class_names)
                                    update_ema(history_ema, lo_nb, probs_n)

                                    print(
                                        f"[NEIG] {band} LO={lo_nb/1e9:.3f} "
                                        f"top1={s_nb['label1']:10s} {s_nb['conf1']:.3f} | "
                                        f"top2={s_nb['label2']:10s} {s_nb['conf2']:.3f} | "
                                        f"best_nonbg={s_nb['best_nonbg_label']:10s} {s_nb['best_nonbg_conf']:.3f} | "
                                        f"bg_gap={s_nb['bg_gap']:.3f} | "
                                        f"margin={s_nb['margin']:.3f} | frames={n_ok_n}",
                                        flush=True
                                    )

                if LOOP_SLEEP > 0:
                    time.sleep(LOOP_SLEEP)

    except KeyboardInterrupt:
        print("\n[!] Escaneo detenido por el usuario.")


if __name__ == "__main__":
    main()