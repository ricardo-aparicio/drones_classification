#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(".")
INPUT_DIR = ROOT / "spectrograms_rc_24_58_fly21"
OUTPUT_DIR = ROOT / "dataset_split_rc24_58_fly21_session"

MANUAL_SPLITS = {
    "autel": {
        # sesión de 2.4G y de 5.8G para Validación
        "val":  ["autel_con_rc02_30db", "autel_envuelo_auto_5G_03","autel_envuelo_auto_06","autel_envuelo_auto_07","autel_envuelo_auto_5G_09","autel_envuelo_auto_5G_10"],
        # sesión de 2.4G y de 5.8G para Test
        "test": ["autel_envuelo_auto_01", "autel_envuelo_auto_5G_01","autel_envuelo_auto_08","autel_envuelo_auto_09","autel_envuelo_auto_5G_11","autel_envuelo_auto_5G_12"]
    },                                     
    "m30t": {
        "val": [
        # --- 2.4G ---
            "m30t_envuelo_10m_val",
            "m30t_envuelo_10m_right_val",
            "m30t_envuelo_10m_left_val",

            "m30t_envuelo_20m_val",
            "m30t_envuelo_20m_right_val",
            "m30t_envuelo_20m_left_val",

            "m30t_envuelo_auto_val",

            "m30t_envuelo_40m_left_val",
            "m30t_envuelo_40m_right_val",

            # --- 5G ---
            "m30t_envuelo_10m_5G_left_val",
            "m30t_envuelo_10m_5G_right_val",
            "m30t_envuelo_10m_5G_center_val",

            "m30t_envuelo_20m_5G_left_val",
            "m30t_envuelo_20m_5G_right_val",
            "m30t_envuelo_20m_5G_center_val",

            "m30t_envuelo_auto_5G_val",

            "m30t_envuelo_40m_5G_left_val",
            "m30t_envuelo_40m_5G_right_val",
        ],
        "test": [
        # --- 2.4G ---
            "m30t_envuelo_10m_test",
            "m30t_envuelo_10m_right_test",
            "m30t_envuelo_10m_left_test",

            "m30t_envuelo_20m_test",
            "m30t_envuelo_20m_right_test",
            "m30t_envuelo_20m_left_test",

            "m30t_envuelo_auto_test",

            "m30t_envuelo_40m_left_test",
            "m30t_envuelo_40m_right_test",

            # --- 5G ---
            "m30t_envuelo_10m_5G_left_test",
            "m30t_envuelo_10m_5G_right_test",
            "m30t_envuelo_10m_5G_center_test",

            "m30t_envuelo_20m_5G_left_test",
            "m30t_envuelo_20m_5G_right_test",
            "m30t_envuelo_20m_5G_center_test",

            "m30t_envuelo_auto_5G_test",

            "m30t_envuelo_40m_5G_left_test",
            "m30t_envuelo_40m_5G_right_test",
        ]
    },

    "mavic4pro": {
        "val": [
        # --- 2.4G ---
            "mavic4pro_envuelo_10m_val",
            "mavic4pro_envuelo_10m_right_val",
            "mavic4pro_envuelo_10m_left_val",

            "mavic4pro_envuelo_20m_val",
            "mavic4pro_envuelo_20m_right_val",
            "mavic4pro_envuelo_20m_left_val",

            "mavic4pro_envuelo_auto_val",

            "mavic4pro_envuelo_40m_left_val",
            "mavic4pro_envuelo_40m_right_val",

            # --- 5G ---
            "mavic4pro_envuelo_10m_5G_left_val",
            "mavic4pro_envuelo_10m_5G_right_val",
            "mavic4pro_envuelo_10m_5G_center_val",

            "mavic4pro_envuelo_20m_5G_left_val",
            "mavic4pro_envuelo_20m_5G_right_val",
            "mavic4pro_envuelo_20m_5G_center_val",

            "mavic4pro_envuelo_40m_5G_left_val",
            "mavic4pro_envuelo_40m_5G_right_val",
            "mavic4pro_envuelo_40m_5G_center_val",
        ],
        "test": [
        # --- 2.4G ---
            "mavic4pro_envuelo_10m_test",
            "mavic4pro_envuelo_10m_right_test",
            "mavic4pro_envuelo_10m_left_test",

            "mavic4pro_envuelo_20m_test",
            "mavic4pro_envuelo_20m_right_test",
            "mavic4pro_envuelo_20m_left_test",

            "mavic4pro_envuelo_auto_test",

            "mavic4pro_envuelo_40m_left_test",
            "mavic4pro_envuelo_40m_right_test",

            # --- 5G ---
            "mavic4pro_envuelo_10m_5G_left_test",
            "mavic4pro_envuelo_10m_5G_right_test",
            "mavic4pro_envuelo_10m_5G_center_test",

            "mavic4pro_envuelo_20m_5G_left_test",
            "mavic4pro_envuelo_20m_5G_right_test",
            "mavic4pro_envuelo_20m_5G_center_test",

            "mavic4pro_envuelo_40m_5G_left_test",
            "mavic4pro_envuelo_40m_5G_right_test",
            "mavic4pro_envuelo_40m_5G_center_test",
        ]
    },
    "fpv": {
        "val":  ["dron_unopes_3"],
        "test": ["dron_unopes_5"]
    },
    "background": {
        "val":  ["background_24G_real_02", "background_5G_real_02","background_24G_real_06","background_24G_real_08","background_5G_real_05","background_5G_real_08"],
        "test": ["background_24G_real_03", "background_5G_real_03","background_24G_real_07","background_24G_real_09","background_5G_real_06","background_5G_real_09"]
    }
}

def main():

    if OUTPUT_DIR.exists():
        print(f"[*] Limpiando directorio existente: {OUTPUT_DIR}")
        shutil.rmtree(OUTPUT_DIR)
    
    for split in ["train", "val", "test"]:
        (OUTPUT_DIR / split).mkdir(parents=True, exist_ok=True)

    if not INPUT_DIR.exists():
        print(f"[!] Error: No se encontró el directorio base {INPUT_DIR}")
        return

    # Contadores
    stats = {"train": 0, "val": 0, "test": 0}

    # 2. Process each class (autel, m30t, mavic4pro, fpv, background)
    for class_dir in INPUT_DIR.iterdir():
        if not class_dir.is_dir():
            continue
            
        class_name = class_dir.name
        print(f"\n[*] Procesando clase: {class_name}")

        # Crear subcarpetas para la clase dentro de train, val y test
        for split in ["train", "val", "test"]:
            (OUTPUT_DIR / split / class_name).mkdir(parents=True, exist_ok=True)

        # Cargar las listas de sesiones asignadas a val y test para esta clase
        val_sessions = MANUAL_SPLITS.get(class_name, {}).get("val", [])
        test_sessions = MANUAL_SPLITS.get(class_name, {}).get("test", [])

        contadores_clase = {"train": 0, "val": 0, "test": 0}

       
        for img_path in class_dir.glob("*.png"):
            filename = img_path.name
            
            # va a 'train'
            split_dest = "train" 
            
            # Verificamos si el nombre del archivo empieza con alguna sesión de Validación
            for val_ses in val_sessions:
                if filename.startswith(val_ses):
                    split_dest = "val"
                    break
                    
            # Si no se fue a Validación, verificamos si va a Test
            if split_dest == "train": 
                for test_ses in test_sessions:
                    if filename.startswith(test_ses):
                        split_dest = "test"
                        break
            
            # 3. Copiar la imagen a su destino final
            dst_path = OUTPUT_DIR / split_dest / class_name / filename
            shutil.copy2(img_path, dst_path)
            
            # Actualizar contadores
            contadores_clase[split_dest] += 1
            stats[split_dest] += 1
            
        # Imprimir resumen de la clase
        print(f"  -> Train: {contadores_clase['train']} imágenes")
        print(f"  -> Val:   {contadores_clase['val']} imágenes")
        print(f"  -> Test:  {contadores_clase['test']} imágenes")

    # 5. Reporte final
    print("\n" + "="*50)
    print(" PARTICIÓN COMPLETADA CON ÉXITO")
    print("="*50)
    print(f" Total Train: {stats['train']} imágenes")
    print(f" Total Val:   {stats['val']} imágenes")
    print(f" Total Test:  {stats['test']} imágenes")
    print(f" Directorio listo para YOLO: {OUTPUT_DIR}")
    print("="*50)

if __name__ == "__main__":
    main()