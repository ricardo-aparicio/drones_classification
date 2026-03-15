# Detection and classification of drones with YOLOv11

## Problem Description
With the rapid proliferation of UAVs (drones), securing airspace requires highly reliable detection and classification methods. Traditional Radio Frequency (RF) fingerprinting faces severe challenges in noisy urban environments—specifically in the 2.4 GHz and 5.8 GHz ISM bands—due to heavy electromagnetic interference from Wi-Fi, Bluetooth, and other devices. Furthermore, modern drones employ complex evasion techniques like Frequency Hopping Spread Spectrum (FHSS) and OFDM modulations, making it exceedingly difficult to differentiate between drones of the same manufacturer (e.g., DJI M30T vs. DJI Mavic 4 Pro) using standard signal processing.

## Proposed Solution
This project transforms raw I/Q RF signals captured via an ADALM-Pluto SDR into 2D spectrogram images, effectively converting a complex Signal Intelligence (SIGINT) challenge into a Computer Vision task. A YOLOv11 image classification model is then trained on these spectrograms to accurately identify the specific drone model or classify the signal as environmental background noise in real-time.

## Advance Presented in this Activity (Preliminary Results)
For this preliminary delivery, the data acquisition, preprocessing, and initial model training pipelines have been completed. A highly curated dataset of over 150,000 spectrogram images was generated, balanced across 5 classes (Autel, FPV, M30T, Mavic 4 Pro, and Background). The current advance includes the successful training of the YOLOv11-cls model, which incorporates "Hard Negative Mining" to proactively filter out massive 5.8 GHz Wi-Fi interference. The preliminary model achieves over 99% Top-1 accuracy on the test set and is capable of real-time inference using a sliding window persistence algorithm to avoid false positives.

## File Structure
```text
├── sample_dataset/                     # Toy dataset (~100 images) to test the pipeline without downloading 2GB
│   ├── test/                           # Sample test images per class
│   ├── train/                          # Sample training images per class
│   └── val/                            # Sample validation images per class
├── data_collection/
│   ├── v2data_acquisition.py           # Captures raw I/Q data from PlutoSDR
│   └── iq_to_spectrogram.py            # Converts I/Q data to spectrograms (Min-Max norm)
├── dataset_preparation/
│   ├── build_spectrograms.py           # Aggregates images from multiple sessions
│   └── make_manual_split_session.py    # Splits data into Train, Val, and Test sets
├── model_training/
│   ├── args.yaml                       # YOLOv11 training hyperparameters
│   ├── train_yolo11_cls.py             # Script to train the YOLOv11 classification model
│   ├── best.pt                         # Final trained YOLOv11 weights (fly21 session)
│   ├── confusion_matrix.png            # Absolute confusion matrix of the test set
│   ├── confusion_matrix_normalized.png # Normalized confusion matrix demonstrating 1.00 diagonal accuracy
│   ├── results.csv                     # Raw training metrics and losses per epoch
│   └── results.png                     # Graphical training/validation loss and accuracy curves
├── inference/
│   └── realtime_yolo11_sdr.py          # Real-time SDR capture and YOLOv11 inference script
```
## Citations and Materials Used

* **YOLOv11 Model:** Jocher, G., et al. (2023). *Ultralytics YOLO* [Computer software]. Available at: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
* **SDR Hardware & Interfacing:** Analog Devices ADALM-Pluto SDR, integrated via the `pyadi-iio` Python library.
* **Signal Processing:** Spectrogram generation and Fast Fourier Transforms (FFT) were implemented using `SciPy` (Virtanen et al., 2020) and `Matplotlib` (Hunter, 2007).

## Note: 
"A sample dataset with 100 images is included to run and test the training scripts (train_yolo11_cls.py). The complete original dataset of 150,000 images exceeds GitHub's limits and is stored locally."
