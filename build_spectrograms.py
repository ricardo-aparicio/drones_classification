#!/usr/bin/env python3
from pathlib import Path
import shutil

BASE = Path(".")  # carpeta actual: DETECTIONV1/dataset
OUT = BASE / "spectrograms_rc_24_58_fly21"  #spectrograms_rc_24_fly4 con FPV UNOPES

AUTEL_FOLDERS = [ #necesito 17991 por frecuencia
    "autel_envuelo_auto_01", #2999 images dron flying in anechoic chamber with RC
    "autel_envuelo_auto_02", #2999 images in dron flying in anechoic chamber with RC
    "autel_con_rc02_30db", #1499 images with RC
    "autel_envuelo_auto_04", #2999 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_05", #2999 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_06", #1099 images dron flying in anechoic chamber with RC VAL
    "autel_envuelo_auto_07", #1099 images dron flying in anechoic chamber with RC VAL
    "autel_envuelo_auto_08", #349 images dron flying in anechoic chamber with RC TEST
    "autel_envuelo_auto_09", #349 images dron flying in anechoic chamber with RC TEST
    "autel_envuelo_auto_5G_01", #1105 - 166 = 939 images dron flying in anechoic chamber with RC TEST
    "autel_envuelo_auto_5G_02", #2928 - 18 = 2910 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_5G_03", #717 - 108 = 609 images dron flying in anechoic chamber with RC VAL
    "autel_envuelo_auto_5G_04", #1688 - 147 = 1541 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_5G_05", #706 - 64 = 642 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_5G_06", #2893 - 509 = 2384 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_5G_08", #3080 -24 = 3056 images dron flying in anechoic chamber with RC TRAIN
    "autel_envuelo_auto_5G_09", #1399 - 22 = 1377 + 20 = 1397 images dron flying in anechoic chamber with RC VAL
    "autel_envuelo_auto_5G_10", #1399 -18 = 1381 + 120 = 1501 images dron flying in anechoic chamber with RC VAL
    "autel_envuelo_auto_5G_11", #1205 - 2 = 1203 + 130 = 1333 images dron flying in anechoic chamber with RC TEST
    "autel_envuelo_auto_5G_12", #1205 - 2 = 1203 + 40 = 1243 images dron flying in anechoic chamber with RC TEST
    "autel_envuelo_auto_5G_13", #414 images dron flying in anechoic chamber with RC TRAIN
]

M30T_FOLDERS = [
    # --- 2.4G ---
    "m30t_envuelo_10m_train",        #1199
    "m30t_envuelo_10m_val",          #400
    "m30t_envuelo_10m_test",         #400
    "m30t_envuelo_10m_right_train",  #1199
    "m30t_envuelo_10m_right_val",    #400
    "m30t_envuelo_10m_right_test",   #400
    "m30t_envuelo_10m_left_train",   #1199
    "m30t_envuelo_10m_left_val",     #400
    "m30t_envuelo_10m_left_test",    #400

    "m30t_envuelo_20m_train",        #1199
    "m30t_envuelo_20m_val",          #400
    "m30t_envuelo_20m_test",         #400
    "m30t_envuelo_20m_right_train",  #1199
    "m30t_envuelo_20m_right_val",    #400
    "m30t_envuelo_20m_right_test",   #400
    "m30t_envuelo_20m_left_train",   #1199
    "m30t_envuelo_20m_left_val",     #400
    "m30t_envuelo_20m_left_test",    #400

    "m30t_envuelo_auto_train",       #1199
    "m30t_envuelo_auto_val",         #400
    "m30t_envuelo_auto_test",        #400

    "m30t_envuelo_40m_left_train",   #1199
    "m30t_envuelo_40m_left_val",     #400
    "m30t_envuelo_40m_left_test",    #400
    "m30t_envuelo_40m_right_train",  #1199
    "m30t_envuelo_40m_right_val",    #400
    "m30t_envuelo_40m_right_test",   #400

    # --- 5G ---
    "m30t_envuelo_10m_5G_left_train",    #1199
    "m30t_envuelo_10m_5G_left_val",      #400
    "m30t_envuelo_10m_5G_left_test",     #400
    "m30t_envuelo_10m_5G_right_train",   #1199
    "m30t_envuelo_10m_5G_right_val",     #400
    "m30t_envuelo_10m_5G_right_test",    #400
    "m30t_envuelo_10m_5G_center_train",  #1199
    "m30t_envuelo_10m_5G_center_val",    #400
    "m30t_envuelo_10m_5G_center_test",   #400

    "m30t_envuelo_20m_5G_left_train",    #1199
    "m30t_envuelo_20m_5G_left_val",      #400
    "m30t_envuelo_20m_5G_left_test",     #400
    "m30t_envuelo_20m_5G_right_train",   #1199
    "m30t_envuelo_20m_5G_right_val",     #400
    "m30t_envuelo_20m_5G_right_test",    #400
    "m30t_envuelo_20m_5G_center_train",  #1199
    "m30t_envuelo_20m_5G_center_val",    #400
    "m30t_envuelo_20m_5G_center_test",   #400

    "m30t_envuelo_auto_5G_train",     #1199
    "m30t_envuelo_auto_5G_val",       #400
    "m30t_envuelo_auto_5G_test",      #400

    "m30t_envuelo_40m_5G_left_train",   #1199
    "m30t_envuelo_40m_5G_left_val",     #400
    "m30t_envuelo_40m_5G_left_test",    #400
    "m30t_envuelo_40m_5G_right_train",  #1199
    "m30t_envuelo_40m_5G_right_val",    #400
    "m30t_envuelo_40m_5G_right_test",   #400
]

MAVIC4_PRO_FOLDERS = [
    # --- 2.4G ---
    "mavic4pro_envuelo_10m_train",        #1199
    "mavic4pro_envuelo_10m_val",          #400
    "mavic4pro_envuelo_10m_test",         #400
    "mavic4pro_envuelo_10m_right_train",  #1199
    "mavic4pro_envuelo_10m_right_val",    #400
    "mavic4pro_envuelo_10m_right_test",   #400
    "mavic4pro_envuelo_10m_left_train",   #1199
    "mavic4pro_envuelo_10m_left_val",     #400
    "mavic4pro_envuelo_10m_left_test",    #400

    "mavic4pro_envuelo_20m_train",        #1199
    "mavic4pro_envuelo_20m_val",          #400
    "mavic4pro_envuelo_20m_test",         #400
    "mavic4pro_envuelo_20m_right_train",  #1199
    "mavic4pro_envuelo_20m_right_val",    #400
    "mavic4pro_envuelo_20m_right_test",   #400
    "mavic4pro_envuelo_20m_left_train",   #1199
    "mavic4pro_envuelo_20m_left_val",     #400
    "mavic4pro_envuelo_20m_left_test",    #400

    "mavic4pro_envuelo_auto_train",       #1199
    "mavic4pro_envuelo_auto_val",         #400
    "mavic4pro_envuelo_auto_test",        #400

    "mavic4pro_envuelo_40m_left_train",   #1199
    "mavic4pro_envuelo_40m_left_val",     #400
    "mavic4pro_envuelo_40m_left_test",    #400
    "mavic4pro_envuelo_40m_right_train",  #1199
    "mavic4pro_envuelo_40m_right_val",    #400
    "mavic4pro_envuelo_40m_right_test",   #400

    # --- 5G ---
    "mavic4pro_envuelo_10m_5G_left_train",    #1199
    "mavic4pro_envuelo_10m_5G_left_val",      #400
    "mavic4pro_envuelo_10m_5G_left_test",     #400
    "mavic4pro_envuelo_10m_5G_right_train",   #1199
    "mavic4pro_envuelo_10m_5G_right_val",     #400
    "mavic4pro_envuelo_10m_5G_right_test",    #400
    "mavic4pro_envuelo_10m_5G_center_train",  #1199
    "mavic4pro_envuelo_10m_5G_center_val",    #400
    "mavic4pro_envuelo_10m_5G_center_test",   #400

    "mavic4pro_envuelo_20m_5G_left_train",    #1199
    "mavic4pro_envuelo_20m_5G_left_val",      #400
    "mavic4pro_envuelo_20m_5G_left_test",     #400
    "mavic4pro_envuelo_20m_5G_right_train",   #1199
    "mavic4pro_envuelo_20m_5G_right_val",     #400
    "mavic4pro_envuelo_20m_5G_right_test",    #400
    "mavic4pro_envuelo_20m_5G_center_train",  #1199
    "mavic4pro_envuelo_20m_5G_center_val",    #400
    "mavic4pro_envuelo_20m_5G_center_test",   #400

    "mavic4pro_envuelo_40m_5G_left_train",    #1199
    "mavic4pro_envuelo_40m_5G_left_val",      #400
    "mavic4pro_envuelo_40m_5G_left_test",     #400
    "mavic4pro_envuelo_40m_5G_right_train",   #1199
    "mavic4pro_envuelo_40m_5G_right_val",     #400
    "mavic4pro_envuelo_40m_5G_right_test",    #400
    "mavic4pro_envuelo_40m_5G_center_train",  #1199
    "mavic4pro_envuelo_40m_5G_center_val",    #400
    "mavic4pro_envuelo_40m_5G_center_test",   #400
]

FPV_FOLDERS = [
    "dron_unopes_2", #1499 images in anechoic chamber without RC
    "dron_unopes_3", #1499 images in anechoic chamber with RC
    "dron_unopes_5", #1499 images in anechoic chamber with RC
    "dron_unopes_13", #1499 images in anechoic chamber with RC
    "dron_unopes_15", #1499 images in real ambient environment with RC, spinning propellers

]

BACKGROUND_FOLDERS = [
    "ruido_camara01_30db", #1499 images in anechoic chamber
    "background_24G_real_01", #1999 images in real ambient environment with 2.4G signal
    "background_24G_real_02", #1999 images in real ambient environment with 2.4G signal
    "background_24G_real_03", #1999 images in real ambient environment with 2.4G signal (outside, with more interference)
    "background_24G_real_04", #3999 TRAIN
    "background_24G_real_05", #3999 TRAIN
    "background_24G_real_06", #999 VAL
    "background_24G_real_07", #999 TEST
    "background_24G_real_08", #999 VAL
    "background_24G_real_09", #999 TEST
    "background_5G_real_01", # 1999 images in real ambient environment with 5G signal
    "background_5G_real_02", # 1999 images in real ambient environment with 5G signal
    "background_5G_real_03", # 1999 images in real ambient environment with 5G signal (outside, with more interference)
    "background_5G_real_04", #3999 TRAIN
    "background_5G_real_05", #999 VAL
    "background_5G_real_06", #999 TEST
    "background_5G_real_07", #3999 TRAIN
    "background_5G_real_08", #999 VAL
    "background_5G_real_09", #999 TEST
    "background_negatives_01", #1499 images in real ambient environment without drones in 5.787 GHz with some interference
]

CLASS_MAP = {
    "autel": AUTEL_FOLDERS,
    "m30t": M30T_FOLDERS,
    "mavic4pro": MAVIC4_PRO_FOLDERS,
    "fpv": FPV_FOLDERS,
    "background": BACKGROUND_FOLDERS,
}

def main():
    for cls, folders in CLASS_MAP.items():
        dest = OUT / cls
        dest.mkdir(parents=True, exist_ok=True)
        print(f"[{cls}] -> {dest}")

        for folder_name in folders:
            src_dir = BASE / folder_name
            if not src_dir.is_dir():
                print(f"  [WARN] {src_dir} no existe, lo salto")
                continue

            for img_path in src_dir.glob("*.png"):
                new_name = f"{folder_name}_{img_path.name}"
                dst_path = dest / new_name
                shutil.copy2(img_path, dst_path)

            print(f"  Copiado {folder_name}")

if __name__ == "__main__":
    main()
