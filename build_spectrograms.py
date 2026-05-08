#!/usr/bin/env python3
from pathlib import Path
import shutil

BASE = Path(".")  # DETECTIONV1/dataset
OUT = BASE / "spectrograms_rc_24_58_fly24_c_unopes" 

AUTEL_FOLDERS = [ 
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

MAVIC3_PRO_FOLDERS = [
#     # --- 2.4G ---
    "mavic3pro_envuelo_10m_center_train", #1999 2.442 GHz
    "mavic3pro_envuelo_10m_center_val",   #500 2.442 GHz
    "mavic3pro_envuelo_10m_center_test",  #500 2.442 GHz 
    "mavic3pro_envuelo_10m_right_train",  #1999 2.442 GHz 
    "mavic3pro_envuelo_10m_right_val",    #500 2.442 GHz 
    "mavic3pro_envuelo_10m_right_test",   #499 2.442 GHz 
    "mavic3pro_envuelo_10m_left_train",   #1999 2.442 GHz 
    "mavic3pro_envuelo_10m_left_val",     #500 2.442 GHz 
    "mavic3pro_envuelo_10m_left_test",    #499 2.442 GHz 

    "mavic3pro_envuelo_20m_center_train", #1999 2.442 GHz 
    "mavic3pro_envuelo_20m_center_val",   #500 2.442 GHz 
    "mavic3pro_envuelo_20m_center_test",  #499 2.442 GHz 
    "mavic3pro_envuelo_20m_right_train",  #1999 2.442 GHz 
    "mavic3pro_envuelo_20m_right_val",    #500 2.442 GHz 
    "mavic3pro_envuelo_20m_right_test",   #499 2.442 GHz 
    "mavic3pro_envuelo_20m_left_train",   #1999 2.442 GHz 
    "mavic3pro_envuelo_20m_left_val",     #500 2.442 GHz 
    "mavic3pro_envuelo_20m_left_test",    #499 2.442 GHz 

    # --- 5G ---
    "mavic3pro_envuelo_10m_5G_left_train",    #1999 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_left_val",      #500 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_left_test",     #499 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_right_train",   #1999 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_right_val",     #500 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_right_test",    #499 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_center_train",  #1999 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_center_val",    #500 5.787 GHz 
    "mavic3pro_envuelo_10m_5G_center_test",   #499 5.787 GHz 

    "mavic3pro_envuelo_20m_5G_left_train",    #1999 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_left_val",      #500 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_left_test",     #499 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_right_train",   #1999 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_right_val",     #500 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_right_test",    #499 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_center_train",  #1999 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_center_val",    #500 5.787 GHz 
    "mavic3pro_envuelo_20m_5G_center_test",   #499 5.787 GHz 
]

FPV_FOLDERS = [
    "dron_unopes_2", #1499 images in anechoic chamber without RC
    "dron_unopes_3", #1499 images in anechoic chamber with RC
    "dron_unopes_5", #1499 images in anechoic chamber with RC
    "dron_unopes_13", #1499 images in anechoic chamber with RC
    "dron_unopes_15", #1499 images in real ambient environment with RC, spinning propellers
    "fpv_train",  #2499 images (nuevas)
    "fpv_val",    #1499 images (nuevas)
    "fpv_test",   #1499 images (nuevas)

]

BACKGROUND_FOLDERS = [
    "ruido_camara01_30db", #1499 - 600 = 899 images in anechoic chamber 2.442 GHZ TRAIN 
    "background_24G_real_01", #1999 - 1100 = 899 images in real ambient environment with 2.442 GHz signal TRAIN 
    "background_24G_real_02", #1999 - 1200 = 799 images in real ambient environment with 2.442 GHz signal VAL 
    "background_24G_real_03", #1999 - 1200 = 799 images in real ambient environment with 2.442 GHz signal (outside, with more interference) TEST 
    "background_24G_real_04", #3999 - 2100 = 1899 TRAIN 2.442 GHz 
    "background_24G_real_05", #3999 - 2100 = 1899 TRAIN 2.442 GHz 
    "background_24G_real_06", #999 - 400 = 599 VAL 2.442 GHz 
    "background_24G_real_07", #999 - 400 = 599 TEST 2.442 GHz 
    "background_24G_real_08", #999 - 400 = 599 VAL 2.442 GHz 
    "background_24G_real_09", #999 - 400 = 599 TEST 2.442 GHz 
    "background_24G_real_10", #700 TRAIN 2.427 GHz ADENTRO
    "background_24G_real_10b", #1400 TRAIN 2.427 GHz AFUERA 
    "background_24G_real_10c", #400 TRAIN 2.427 GHz ADENTRO 
    "background_24G_real_11", #150 TEST 2.427 GHz AFUERA
    "background_24G_real_11a", #700 TEST 2.427 GHz AFUERA 
    "background_24G_real_12", #150 VAL 2.427 GHz ADENTRO
    "background_24G_real_12b", #400 VAL 2.427 GHz ADENTRO 
    "background_24G_real_12c", #300 VAL 2.427 GHz AFUERA 
    "background_24G_real_13", #700 TRAIN 2.455 GHz ADENTRO
    "background_24G_real_13b", #1400 TRAIN 2.455 GHz AFUERA 
    "background_24G_real_13c", #400 TRAIN 2.455 GHz ADENTRO 
    "background_24G_real_14", #150 TEST 2.455 GHz AFUERA
    "background_24G_real_14a", #700 TEST 2.455 GHz AFUERA 
    "background_24G_real_15", #150 VAL 2.455 GHz ADENTRO
    "background_24G_real_15b", #400 VAL 2.455 GHz ADENTRO 
    "background_24G_real_15c", #300 VAL 2.455 GHz AFUERA 
    "background_5G_real_01", # 1999 - 1100 = 899 images in real ambient environment with 5.787 GHz signal TRAIN 
    "background_5G_real_02", # 1999 - 1200 = 799 images in real ambient environment with 5.787 GHz signal VAL 
    "background_5G_real_03", # 1999 -1200 = 799 images in real ambient environment with 5.787 GHz signal (outside, with more interference) TEST 
    "background_5G_real_04", #3999 - 2100 = 1899 TRAIN 5.787 GHz 
    "background_5G_real_05", #999 - 400 = 599 VAL 5.787 GHz 
    "background_5G_real_06", #999 - 400 = 599 TEST 5.787 GHz 
    "background_5G_real_07", #3999 - 2100 = 1899 TRAIN 5.787 GHz 
    "background_5G_real_08", #999 - 400 = 599 VAL 5.787 GHz 
    "background_5G_real_09", #999 - 400 = 599 TEST 5.787 GHz 
    "background_negatives_01", #1499 - 600 = 899 images in real ambient environment without drones in 5.787 GHz with some interference TRAIN
    "background_5G_real_10", #700 images in real ambient environment without drones in 5.756 GHz TRAIN ADENTRO
    "background_5G_real_10b", #1400 images in real ambient environment without drones in 5.756 GHz TRAIN AFUERA 
    "background_5G_real_10c", #400 images in real ambient environment without drones in 5.756 GHz TRAIN ADENTRO 
    "background_5G_real_11", #150 images in real ambient environment without drones in 5.756 GHz TEST AFUERA
    "background_5G_real_11a", #700 images in real ambient environment without drones in 5.756 GHz TEST AFUERA 
    "background_5G_real_12", #150 images in real ambient environment without drones in 5.756 GHz VAL ADENTRO
    "background_5G_real_12b", #400 images in real ambient environment without drones in 5.756 GHz VAL ADENTRO 
    "background_5G_real_12c", #300 images in real ambient environment without drones in 5.756 GHz VAL AFUERA 
    "background_5G_real_13", #700 images in real ambient environment without drones in 5.818 GHz TRAIN ADENTRO
    "background_5G_real_13b", #1400 images in real ambient environment without drones in 5.818 GHz TRAIN AFUERA 
    "background_5G_real_13c", #400 images in real ambient environment without drones in 5.818 GHz TRAIN ADENTRO 
    "background_5G_real_14", #150 images in real ambient environment without drones in 5.818 GHz VAL ADENTRO
    "background_5G_real_14b", #400 images in real ambient environment without drones in 5.818 GHz VAL ADENTRO 
    "background_5G_real_14c", #300 images in real ambient environment without drones in 5.818 GHz VAL AFUERA 
    "background_5G_real_15", #150 images in real ambient environment without drones in 5.818 GHz TEST AFUERA
    "background_5G_real_15a", #700 images in real ambient environment without drones in 5.818 GHz TEST AFUERA 
    "background_5G_real_16", #700 images in real ambient environment without drones in 5.645 GHz TRAIN ADENTRO
    "background_5G_real_16b", #1400 images in real ambient environment without drones in 5.645 GHz TRAIN AFUERA 
    "background_5G_real_16c", #400 images in real ambient environment without drones in 5.645 GHz TRAIN ADENTRO 
    "background_5G_real_17", #150 images in real ambient environment without drones in 5.645 GHz VAL ADENTRO
    "background_5G_real_17b", #400 images in real ambient environment without drones in 5.645 GHz VAL ADENTRO 
    "background_5G_real_17c", #300 images in real ambient environment without drones in 5.645 GHz VAL AFUERA 
    "background_5G_real_18", #150 images in real ambient environment without drones in 5.645 GHz TEST AFUERA
    "background_5G_real_18a", #700 images in real ambient environment without drones in 5.645 GHz TEST AFUERA 
    "background_5G_5645_hardneg_train", #700 images in real ambient environment without drones in 5.645 GHz TRAIN ADENTRO
    "background_5G_5645_hardneg_val", #150 images in real ambient environment without drones in 5.645 GHz VAL ADENTRO
    "background_5G_5645_hardneg_test", #150 images in real ambient environment without drones in 5.645 GHz TEST AFUERA

]

CLASS_MAP = {
    "autel": AUTEL_FOLDERS,
    "m30t": M30T_FOLDERS,
    "mavic4pro": MAVIC4_PRO_FOLDERS,
    "mavic3pro": MAVIC3_PRO_FOLDERS,
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
