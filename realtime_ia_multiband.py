#!/usr/bin/env python3
import time
from pathlib import Path

import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from skimage.transform import resize
from ultralytics import YOLO

# SDR
SDR_IP = "ip:192.168.202.204"
FS = 50e6
RF_BW_HZ = 45e6
GAIN_DB = 45
WINDOW_SAMPLES = 200_000

# Bands and scanning sequence
CENTERS_24 = [2.427e9, 2.455e9]
CENTERS_58 = [5.756e9, 5.787e9, 5.818e9]

BANDS = {
    "2.4G": CENTERS_24,
    "5.8G": CENTERS_58,
}

SCAN_SEQUENCE = (
    [("2.4G", i, f) for i, f in enumerate(CENTERS_24)] +
    [("5.8G", i, f) for i, f in enumerate(CENTERS_58)]
)

# Timing / retune
RETUNE_SLEEP = 0.05      # seconds for the LO to stabilize
LOOP_SLEEP = 0.02   

def retune_and_flush(sdr, lo_hz: float):
    sdr.rx_lo = int(lo_hz)
    time.sleep(RETUNE_SLEEP)
    _ = sdr.rx()  # flush 1 buffer 


# Frames
FAST_FRAMES     = 5
CONFIRM_FRAMES  = 15
NEIGHBOR_FRAMES = 10      


# Thresholds
SUSPECT_NONBG_CONF_THR = 0.25   
SUSPECT_BG_CONF_LOW     = 0.55   
SUSPECT_TOP2_THR        = 0.35 
SUSPECT_MARGIN_THR      = 0.10

# Confirmation
CONFIRM_NONBG_CONF_THR = 0.50
CONFIRM_MARGIN_THR     = 0.10


BACKGROUND_LABEL = "background"


# Model
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

    spec_256 = resize(Sxx_norm, (256, 256), mode="reflect", anti_aliasing=True).astype(np.float32)

    img_rgba = _CMAP(spec_256)                    
    img_rgb = (img_rgba[:, :, :3] * 255).astype(np.uint8)
    return img_rgb


# Helpers
def collect_probs_mean_tuned(sdr, model, frames: int) -> tuple[np.ndarray | None, int]:
    probs_acc = None
    n_ok = 0

    for _ in range(frames):
        iq = sdr.rx()
        if len(iq) < WINDOW_SAMPLES:
            continue

        iq_seg = np.asarray(iq[:WINDOW_SAMPLES], dtype=np.complex64)
        img_rgb = iq_to_spec_image(iq_seg)
        img_bgr = img_rgb[:, :, ::-1]  # RGB -> BGR for OpenCV  
        results = model.predict(source=img_bgr, imgsz=256, verbose=False)
        probs = results[0].probs.data.cpu().numpy()  # (nc,)

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

    label1 = class_names[top1]
    label2 = class_names[top2]
    margin = conf1 - conf2

    return {
        "top1": top1, "conf1": conf1, "label1": label1,
        "top2": top2, "conf2": conf2, "label2": label2,
        "margin": margin,
        "probs": probs_mean,
    }

def is_suspect(s: dict) -> bool:
    # Case 1: top1 is NOT background with moderate confidence
    if s["label1"] != BACKGROUND_LABEL and s["conf1"] >= SUSPECT_NONBG_CONF_THR:
        return True

    # Case 2: top1 is background, but weak, and there is strong competition
    if s["label1"] == BACKGROUND_LABEL:
        if s["conf1"] < SUSPECT_BG_CONF_LOW and (s["conf2"] >= SUSPECT_TOP2_THR or s["margin"] < SUSPECT_MARGIN_THR):
            return True

    # Case 3: very small margin, highly ambiguous, with decent confidence
    if s["conf1"] > 0.35 and s["margin"] < SUSPECT_MARGIN_THR:
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

# Main
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
    print(f"      FAST={FAST_FRAMES}  CONFIRM={CONFIRM_FRAMES}  NEIGH={NEIGHBOR_FRAMES}")
    print("      Ctrl+C para detener.\n")

    try:
        while True:
            for band, idx, lo_hz in SCAN_SEQUENCE:
                retune_and_flush(sdr, lo_hz)
                # 1) SCAN
                probs_mean, n_ok = collect_probs_mean_tuned(sdr, model, FAST_FRAMES)
                if probs_mean is None:
                    continue

                s_fast = summarize_probs(probs_mean, class_names)
                print(
                    f"[SCAN] {band} FREC={lo_hz/1e9:.3f} "
                    f"PRED1={s_fast['label1']:10s} {s_fast['conf1']:.3f} | "
                    f"PRED2={s_fast['label2']:10s} {s_fast['conf2']:.3f} | "
                    f"margin={s_fast['margin']:.3f} | frames={n_ok}",
                    flush=True
                )

                # 2) suspect -> confirm on the same LO
                if is_suspect(s_fast):
                    probs_c, n_ok_c = collect_probs_mean_tuned(sdr, model, CONFIRM_FRAMES)
                    if probs_c is None:
                        continue
                    s_conf = summarize_probs(probs_c, class_names)

                    print(
                        f"[HOLD] {band} FREC={lo_hz/1e9:.3f} "
                        f"PRED1={s_conf['label1']:10s} {s_conf['conf1']:.3f} | "
                        f"PRED2={s_conf['label2']:10s} {s_conf['conf2']:.3f} | "
                        f"margin={s_conf['margin']:.3f} | frames={n_ok_c}",
                        flush=True
                    )

                    # 3) confirmed event, then checks neighboring frequencies for similar evidence
                    if is_confirmed(s_conf):
                        neigh = neighbor_indices(band, idx)
                        if neigh:
                            print(
                                f"[EVENT] CONFIRMED BAND={band} FREC={lo_hz/1e9:.3f} "
                                f"PRED1={s_conf['label1']} conf={s_conf['conf1']:.3f} "
                                f"PRED2={s_conf['label2']} conf2={s_conf['conf2']:.3f} "
                                f"margin={s_conf['margin']:.3f}",
                                flush=True
                            )

                        for j in neigh:
                            lo_nb = BANDS[band][j]
                            probs_n, n_ok_n = collect_probs_mean(sdr, model, lo_nb, NEIGHBOR_FRAMES)
                            if probs_n is None:
                                continue
                            s_nb = summarize_probs(probs_n, class_names)

                            print(
                                f"[NEIG] {band} LO={lo_nb/1e9:.3f} "
                                f"top1={s_nb['label1']:10s} {s_nb['conf1']:.3f} | "
                                f"top2={s_nb['label2']:10s} {s_nb['conf2']:.3f} | "
                                f"margin={s_nb['margin']:.3f} | frames={n_ok_n}",
                                flush=True
                            )

                if LOOP_SLEEP > 0:
                    time.sleep(LOOP_SLEEP)

    except KeyboardInterrupt:
        print("\n[!] Escaneo detenido por el usuario.")

if __name__ == "__main__":
    main()
