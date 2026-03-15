#!/usr/bin/env python3
from pathlib import Path
from ultralytics import YOLO

# Paths
ROOT = Path(__file__).parent
DATA_DIR = ROOT / "dataset_split_rc24_58_fly21_session"  

MODEL_WEIGHTS = "yolo11n-cls.pt"


def main():

    model = YOLO(MODEL_WEIGHTS)  

    
    results = model.train(
        data=str(DATA_DIR),      
        epochs=50,              
        imgsz=256,            
        batch=32,            
        lr0=0.001,                
        optimizer="adam",           
        patience=10,             
        device=0,                
        project="runs_yolo11_cls",
        name="drone_spectrograms_rc_24_58_fly21_session",    # drone_spectrograms_rc_24_fly21_session (more stable training)
        verbose=True,
        pretrained=True,

        crop_fraction=1.0,  # It does not crop, it uses the full spectrogram.
        fliplr=0.0,      # Deactivate horizontal rotation (time reversal)
        flipud=0.0,      # Deactivates vertical rotation (frequency inversion)
        hsv_h=0.0,       # It keeps the Viridis (dB) colors intact
    )

    print("Directorio de resultados:", results.save_dir)

   
    metrics_test = model.val(
        data=str(DATA_DIR),     
        split="test",            
        imgsz=256,
        batch=64,
    )
    
    print("Test top-1 acc:", metrics_test.top1)
    print("Test top-5 acc:", metrics_test.top5)


    sample_img_dir = ROOT / "dataset_split_rc24_58_fly21_session" / "test" / "background"
    sample_img = next(sample_img_dir.glob("*.png"))

    preds = model.predict(source=str(sample_img), imgsz=256)
    probs = preds[0].probs  

    print("Imagen de prueba:", sample_img.name)
    print("Probabilidades (orden model.names):", probs.data.cpu().numpy())
    print("Clase predicha:", probs.top1, "->", model.names[int(probs.top1)])


if __name__ == "__main__":
    main()
