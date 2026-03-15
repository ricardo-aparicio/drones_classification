#!/usr/bin/env python3
import time
from pathlib import Path

import numpy as np
import adi                      # pyadi-iio
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from skimage.transform import resize
from ultralytics import YOLO


# Parámetros de RF 
SDR_IP          = "ip:192.168.201.204"
CENTER_FREQ_HZ  = 5.787e9       # 2.442 GHz #5.645 #5.787  #5746 a 5786 anchos de los DJI - HSB 5.786
FS              = 50e6          # 50 MS/s
RF_BW_HZ        = 45e6
GAIN_DB         = 30

# Tamaño de ventana para el espectrograma
WINDOW_SAMPLES  = 200_000

# Modelo YOLO entrenado
ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "runs_yolo11_cls" / "drone_spectrograms_rc_24_58_fly21_session" / "weights" / "best.pt"  
# drone_spectrograms_rc_24_fly12_session # drone_spectrograms_rc_24_58_fly16_session

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
     Sxx_norm = (Sxx_db - Sxx_db.min()) / (Sxx_db.max() - Sxx_db.min() + 1e-9)

     spec_256 = resize(Sxx_norm, (256, 256), mode="reflect", anti_aliasing=True).astype(np.float32)

     cmap = plt.get_cmap("viridis")
     img_rgba = cmap(spec_256)
     img_rgb = (img_rgba[:, :, :3] * 255).astype(np.uint8)
     return img_rgb

# def iq_to_spec_image(iq_seg: np.ndarray) -> np.ndarray:
#     f, t, Sxx = spectrogram(
#         iq_seg,
#         fs=FS,
#         window="hann",
#         nperseg=1024,
#         noverlap=512,
#         scaling="density",
#         mode="magnitude",
#         return_onesided=False,
#     )

#     # dB
#     Sxx_db = 20 * np.log10(Sxx + 1e-12)

#     # Normalización robusta por percentiles
#     p_low, p_high = 5, 99.5
#     lo = np.percentile(Sxx_db, p_low)
#     hi = np.percentile(Sxx_db, p_high)

#     # Clip para que spikes no dominen el rango
#     Sxx_db = np.clip(Sxx_db, lo, hi)

#     # Normalizar a [0,1]
#     Sxx_norm = (Sxx_db - lo) / (hi - lo + 1e-9)

#     spec_256 = resize(Sxx_norm, (256, 256), mode="reflect", anti_aliasing=True).astype(np.float32)

#     cmap = plt.get_cmap("viridis")
#     img_rgba = cmap(spec_256)
#     img_rgb = (img_rgba[:, :, :3] * 255).astype(np.uint8)
#     return img_rgb

def main():

    # Configurar SDR
    print("[*] Conectando al SDR...")
    sdr = adi.Pluto(SDR_IP)

    sdr.rx_lo = int(CENTER_FREQ_HZ)
    sdr.sample_rate = int(FS)
    sdr.rx_rf_bandwidth = int(RF_BW_HZ)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = GAIN_DB

    # Buffer de recepción ~ tamaño de ventana
    sdr.rx_buffer_size = WINDOW_SAMPLES

    print("[*] SDR configurado:")
    print("    LO  =", sdr.rx_lo)
    print("    Fs  =", sdr.sample_rate)
    print("    BW  =", sdr.rx_rf_bandwidth)
    print("    G   =", sdr.rx_hardwaregain_chan0)

  
    # Cargar modelo YOLO
    print("[*] Cargando modelo YOLO:", MODEL_PATH)
    model = YOLO(str(MODEL_PATH))
    class_names = model.names
    print("[*] Clases del modelo:", class_names)

    print("\n[***] Detección en tiempo (casi) real iniciada.")
    print(f"      Enciende/apaga el dron cerca de {CENTER_FREQ_HZ/1e9:.3f} GHz y observa las predicciones.")
    print("      Ctrl+C para detener.\n")

    try:
        while True:
            # 1) Capturar un bloque de IQ
            iq = sdr.rx()  # numpy array complejo

            if len(iq) < WINDOW_SAMPLES:
                continue

            iq_seg = np.asarray(iq[:WINDOW_SAMPLES], dtype=np.complex64)

            # 2) IQ -> espectrograma -> imagen 256x256
            img_rgb = iq_to_spec_image(iq_seg)

            # 3) Predicción con YOLOv11n-Cls
            results = model.predict(
                source=img_rgb,
                imgsz=256,
                verbose=False
            )
            probs = results[0].probs

            top1 = int(probs.top1)
            conf = float(probs.top1conf)
            label = class_names[top1]

            probs_vec = probs.data.cpu().numpy()

            # 4) Mostrar resultado en consola
            print(f"[PRED] Clase={label:10s}  conf={conf:.3f}  "
                  f"probs={probs_vec}", flush=True)

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n[!] Detección detenida por el usuario.")


if __name__ == "__main__":
    main()
