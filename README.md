# RF-Based Drone Detection and Classification with YOLOv11

## 1. Problem Description

The rapid proliferation of unmanned aerial vehicles (UAVs) has created the need for reliable drone detection and classification systems. Traditional RF fingerprinting methods can be difficult to apply in real environments because drone communication signals share the 2.4 GHz and 5.8 GHz ISM bands with Wi-Fi, Bluetooth, and other RF sources.

Modern drones can also use automatic band selection, frequency hopping, and different channel bandwidths, which makes the detection problem more challenging. This project addresses the problem of drone RF detection and classification by transforming raw I/Q samples into spectrogram images and using a YOLOv11 classification model.

## 2. Proposed Solution

This project uses a Software-Defined Radio (SDR) to capture raw I/Q samples from drone communication signals. Each I/Q segment is converted into a 2D spectrogram using the Short-Time Fourier Transform (STFT). These spectrograms are then used as image inputs for a YOLOv11 classification model.

The system can classify RF spectrograms into the following classes:

- Autel
- DJI M30T
- DJI Mavic 4 Pro
- DJI Mavic 3 Pro
- FPV
- Background

The project includes both fixed-frequency inference and multiband real-time scanning.

## 3. Methodology

The complete processing pipeline is:

1. Capture raw I/Q samples using an SDR.
2. Generate spectrogram images from the I/Q samples.
3. Normalize the spectrograms and resize them to 256 × 256 pixels.
4. Train a YOLOv11 classification model using the spectrogram dataset.
5. Evaluate the model using validation and test sets.
6. Run real-time inference using either fixed-frequency scanning or multiband scanning.
7. Apply temporal decision logic to reduce false positives and improve long-range detection.

## 4. Repository Structure

```text
drones_classification/
├── sample_dataset/
│   ├── train/
│   │   ├── autel/
│   │   ├── background/
│   │   ├── fpv/
│   │   ├── m30t/
│   │   ├── mavic3pro/
│   │   └── mavic4pro/
│   ├── val/
│   │   ├── autel/
│   │   ├── background/
│   │   ├── fpv/
│   │   ├── m30t/
│   │   ├── mavic3pro/
│   │   └── mavic4pro/
│   └── test/
│       ├── autel/
│       ├── background/
│       ├── fpv/
│       ├── m30t/
│       ├── mavic3pro/
│       └── mavic4pro/
├── args.yaml
├── best.pt
├── build_spectrograms.py
├── confusion_matrix.png
├── confusion_matrix_normalized.png
├── iq_to_spectrogram.py
├── make_manual_split_session.py
├── realtime_ia_multiband.py
├── realtime_ia_v2_multiband.py
├── realtime_yolo11_sdr.py
├── results.csv
├── results.png
├── train_yolo11_cls.py
└── v2data_acquisition.py
