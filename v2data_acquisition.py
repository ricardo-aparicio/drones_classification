#!/usr/bin/env python3
import numpy as np
import adi  # pyadi-iio
import time
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT 

sdr = adi.Pluto("ip:192.168.201.204")

#5.787 GHz
sdr.rx_lo = int(5.787e9)     #5.787 5.658 5.650_2 5.645_3,5 (con RC) (la buena) 5.640_4 850_6 900_7 (dron.rc) _8 (sin dron)
sdr.sample_rate = int(50e6)    #900_9 (dron) #900_10 (dron y RC) #900_11 (RC) 5.645_12,13 (con RC, helices camara)
sdr.rx_rf_bandwidth = int(45e6)  #900_14 (con RC, helices camara) 5.645_15 (con RC, volando camara) 900_16 (con RC, volando camara)
sdr.gain_control_mode_chan0 = "manual"  #5.787 AUTEL 5.725 - 5.85 ; DJIM30T 5.787 (5.786 HSB); MAVIC4PRO (5.786 HSB)
sdr.rx_hardwaregain_chan0 = 30  


OUT_FILE = DATA_DIR / "background_negatives_01.bin"    # mavic4pro_envuelo_10m_5G_rigth.bin mavic4pro_envuelo_10m_5G_center.bin 

DURATION_SEC   = 3       
CHUNK_SAMPLES  = 1_000_000   

# ----------------------------------------

def capture_samples(filename, duration_sec):
    fs = sdr.sample_rate
    target_samples = int(fs * duration_sec)

    print(f"Capturando ~{duration_sec:.2f} s "
          f"({target_samples/1e6:.2f} M muestras) en {filename}")

    samples_written = 0

    with open(filename, "wb") as f:
        t0 = time.time()
        while samples_written < target_samples:
           
            this_block = min(CHUNK_SAMPLES, target_samples - samples_written)
            sdr.rx_buffer_size = this_block
            iq = sdr.rx()

            iq_c64 = np.asarray(iq, dtype=np.complex64)
            iq_c64.tofile(f)

            samples_written += len(iq_c64)
            print(f"\r  -> {samples_written/1e6:7.2f} M muestras", end="")

        t1 = time.time()

    real_sec = samples_written / fs
    print(f"\nListo. Guardadas {samples_written} muestras "
          f"(~{real_sec:.3f} s) en {filename}. "
          f"Tiempo real: {t1-t0:.1f} s")

if __name__ == "__main__":
    capture_samples(OUT_FILE, DURATION_SEC)
