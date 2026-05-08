# RF-Based Drone Detection and Classification with YOLOv11

## 1. Project Overview

This repository presents a radio-frequency (RF) drone detection and classification system based on Software-Defined Radio (SDR), spectrogram image processing, and a YOLOv11 image classification model.

The main objective is to detect and classify drone communication signals operating mainly in the 2.4 GHz and 5.8 GHz ISM bands. Instead of using optical images from a camera, this project captures raw I/Q samples from an SDR, converts them into spectrogram images, and classifies those spectrograms using a deep learning model.

This approach converts an RF signal classification problem into a computer vision problem.

---

## 2. Problem Description

The rapid proliferation of unmanned aerial vehicles (UAVs) has created the need for reliable drone detection and classification systems. Many commercial drones communicate with their remote controllers using the 2.4 GHz and 5.8 GHz bands, which are also used by Wi-Fi, Bluetooth, and other RF devices.

This makes drone detection challenging because:

- Drone signals can overlap with other RF sources.
- The RF environment changes depending on location and interference.
- Drones may use automatic band selection.
- Some drones can change channel position or frequency band during operation.
- Signals become weaker and more intermittent as distance increases.
- Drones from the same manufacturer may have similar RF signatures.

This project addresses these challenges by using RF spectrograms and a YOLOv11 classification model to distinguish drone emissions from background RF activity.

---

## 3. Proposed Solution

The proposed solution consists of the following pipeline:

1. Capture raw I/Q samples using an SDR.
2. Convert the I/Q samples into spectrogram images using the Short-Time Fourier Transform (STFT).
3. Normalize and resize the spectrograms to 256 × 256 pixels.
4. Train a YOLOv11 classification model using the generated spectrogram dataset.
5. Evaluate the model using train, validation, and test partitions.
6. Run real-time inference using either:
   - fixed-frequency scanning, or
   - adaptive multiband scanning.
7. Apply temporal decision logic to improve detection stability and reduce false positives.

The system can classify RF spectrograms into the following classes:

- Autel
- DJI M30T
- DJI Mavic 4 Pro
- DJI Mavic 3 Pro
- FPV
- Background

---

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
├── .gitignore
├── README.md
├── args.yaml
├── best.pt
├── build_spectrograms.py
├── confusion_matrix.png
├── confusion_matrix_normalized.png
├── final_comparisson.png
├── fixed_frequency_scan_comparison.png
├── iq_to_spectrogram.py
├── logs_escaneos.html
├── logs_escaneos_text.txt
├── make_manual_split_session.py
├── multiband_scan_comparison.png
├── multiband_v2.png
├── realtime_ia_multiband.py
├── realtime_ia_v2_multiband.py
├── realtime_yolo11_sdr.py
├── results.csv
├── results.png
├── train_yolo11_cls.py
└── v2data_acquisition.py
```

---

## 5. Main Files

| File | Description |
|---|---|
| `v2data_acquisition.py` | Captures raw I/Q samples from the SDR. |
| `iq_to_spectrogram.py` | Converts I/Q samples into spectrogram images. |
| `build_spectrograms.py` | Aggregates spectrogram images from different capture sessions. |
| `make_manual_split_session.py` | Creates train, validation, and test dataset partitions. |
| `train_yolo11_cls.py` | Trains the YOLOv11 classification model. |
| `args.yaml` | Stores YOLOv11 training configuration and hyperparameters. |
| `best.pt` | Trained YOLOv11 classification weights. |
| `realtime_yolo11_sdr.py` | Performs fixed-frequency real-time inference. |
| `realtime_ia_multiband.py` | Original multiband scanning implementation. |
| `realtime_ia_v2_multiband.py` | Improved multiband scanner with FOCUS, EMA, and best non-background logic. |
| `confusion_matrix.png` | Absolute confusion matrix from model evaluation. |
| `confusion_matrix_normalized.png` | Normalized confusion matrix from model evaluation. |
| `results.csv` | Training metrics per epoch. |
| `results.png` | Training and validation curves. |
| `fixed_frequency_scan_comparison.png` | Presentation table comparing fixed-frequency scanning results. |
| `multiband_scan_comparison.png` | Presentation table comparing original multiband scanning results. |
| `multiband_v2.png` | Presentation table comparing improved multiband v2 scanning results. |
| `final_comparisson.png` | Final comparison table between fixed-frequency, original multiband, and improved multiband v2 strategies. |
| `logs_escaneos.html` | Organized and color-coded scan logs for presentation. |
| `logs_escaneos_text.txt` | Organized text version of scan logs. |

---

## 6. Dataset Description

The complete dataset was generated from real SDR captures of drone RF emissions and environmental background signals.

The full dataset includes spectrograms from:

- Drone signals in the 2.4 GHz band.
- Drone signals in the 5.8 GHz band.
- Different channel positions.
- Different drone operating modes.
- Indoor and outdoor background RF activity.
- Drone flights with the aircraft linked to the remote controller.
- Drone flights with propellers active.

Due to GitHub storage limitations, the full dataset is not included in this repository. Instead, a smaller `sample_dataset/` is provided to demonstrate the required folder structure and to allow the training and inference scripts to be tested.

The expected dataset format follows the Ultralytics classification structure:

```text
dataset/
├── train/
│   ├── autel/
│   ├── background/
│   ├── fpv/
│   ├── m30t/
│   ├── mavic3pro/
│   └── mavic4pro/
├── val/
│   ├── autel/
│   ├── background/
│   ├── fpv/
│   ├── m30t/
│   ├── mavic3pro/
│   └── mavic4pro/
└── test/
    ├── autel/
    ├── background/
    ├── fpv/
    ├── m30t/
    ├── mavic3pro/
    └── mavic4pro/
```

---

## 7. Spectrogram Generation

Each RF capture consists of complex I/Q samples. These samples are transformed into spectrogram images using STFT.

The general conversion process is:

```text
I/Q samples → STFT → magnitude spectrogram → dB scale → normalization → 256 × 256 RGB image
```

The spectrograms are generated using:

- `scipy.signal.spectrogram`
- Hann window
- `nperseg = 1024`
- `noverlap = 512`
- Magnitude mode
- Viridis colormap
- 256 × 256 image size

The same spectrogram generation pipeline is used for both offline dataset creation and real-time inference.

This consistency is important because the model should receive images during inference that are generated using the same processing method used during training.

---

## 8. YOLOv11 Training Configuration

The model was trained using YOLOv11 classification mode.

Main training configuration:

```yaml
task: classify
model: yolo11n-cls.pt
epochs: 50
patience: 10
batch: 32
imgsz: 256
optimizer: adam
lr0: 0.001
pretrained: true
crop_fraction: 1.0
fliplr: 0.0
flipud: 0.0
hsv_h: 0.0
hsv_s: 0.0
hsv_v: 0.0
```

Most data augmentation parameters were disabled because the color distribution, time-frequency structure, and spatial layout of the spectrograms are part of the RF signature.

For example:

- Horizontal flipping could alter the time structure of the signal.
- Vertical flipping could invert the frequency structure.
- Color augmentation could modify the dB-related color representation of the spectrogram.

To train the model:

```bash
python3 train_yolo11_cls.py
```

---

## 9. Real-Time Fixed-Frequency Inference

The file `realtime_yolo11_sdr.py` performs real-time inference at one fixed SDR center frequency.

This approach is useful when the expected drone channel is already known.

Example:

```bash
python3 realtime_yolo11_sdr.py
```

Typical use cases:

- Testing a drone forced to 2.4 GHz.
- Monitoring a known 2.455 GHz channel.
- Monitoring a known 5.8 GHz channel.
- Comparing model behavior against multiband scanning.
- Validating whether the RF signature is detectable at a specific frequency.

Main advantage:

```text
Highest sensitivity when the correct frequency is known.
```

Main limitation:

```text
It does not automatically monitor other possible drone bands.
```

---

## 10. Original Multiband Inference

The file `realtime_ia_multiband.py` implements the original multiband scanning strategy.

It scans several candidate frequencies in the 2.4 GHz and 5.8 GHz bands and uses a temporal confirmation strategy.

The basic decision flow is:

```text
SCAN → HOLD → EVENT CONFIRMED → NEIGHBOR CHECK
```

This approach allows the system to monitor several possible drone communication channels instead of staying fixed on one frequency.

Example:

```bash
python3 realtime_ia_multiband.py
```

Main advantage:

```text
It provides automatic multiband coverage.
```

Main limitation:

```text
The evidence can be diluted across the scan cycle, especially at longer distances.
```

In other words, the original multiband scanner can observe weak evidence in some bands, but because it must move across several frequencies, it may not remain long enough in the most promising band to confirm weak long-range signals.

---

## 11. Improved Multiband v2 Inference

The file `realtime_ia_v2_multiband.py` is the improved version of the multiband scanner.

It was developed to improve long-range detection and avoid losing weak drone evidence across the scan cycle.

The improved decision flow is:

```text
SCAN → FOCUS → HOLD → EVENT CONFIRMED → NEIGHBOR CHECK
```

Main improvements:

- Adds a `FOCUS` stage before final confirmation.
- Uses the best non-background class to detect weak drone evidence.
- Applies Exponential Moving Average (EMA) memory per frequency.
- Uses temporal evidence accumulation.
- Keeps multiband operation while improving sensitivity.
- Uses RGB spectrograms directly to match the fixed-frequency inference pipeline.

The `FOCUS` stage is important because weak drone signals may appear as secondary predictions behind `background`. Instead of immediately discarding those cases, the v2 scanner stays longer in the promising sub-band and collects more evidence before deciding.

Example:

```bash
python3 realtime_ia_v2_multiband.py
```

Main advantage:

```text
Best balance between autonomous multiband monitoring and long-range detection performance.
```

---

## 12. Experimental Findings

Three scanning strategies were compared:

1. Fixed-frequency scanning with `realtime_yolo11_sdr.py`
2. Original multiband scanning with `realtime_ia_multiband.py`
3. Improved multiband scanning with `realtime_ia_v2_multiband.py`

### 12.1 Fixed-Frequency Scanner

The fixed-frequency scanner produced strong detections when the SDR was tuned to the correct drone operating frequency.

This method is highly sensitive because all the observation time is spent on one frequency. However, it requires prior knowledge of the target frequency.

For example, when the drone was operating near the selected center frequency, the fixed-frequency scanner repeatedly classified the spectrograms as the correct drone class.

### 12.2 Original Multiband Scanner

The original multiband scanner provided wider frequency coverage by monitoring several sub-bands in 2.4 GHz and 5.8 GHz.

However, it struggled to sustain detection evidence at longer range, especially for Mavic 4 Pro. In some cases, the drone signal appeared as weak or secondary evidence, but the detection was not stable enough to generate repeated confirmed events.

This showed that multiband coverage alone was not enough. The scanner also needed a better strategy to remain longer in promising sub-bands.

### 12.3 Improved Multiband v2 Scanner

The improved v2 multiband scanner produced the best overall multiband results.

In recent field tests, Mavic 4 Pro detections were repeatedly confirmed around:

```text
5.818 GHz
```

The neighboring frequency:

```text
5.787 GHz
```

often appeared as supporting evidence.

A key result was obtained at:

```text
200 m altitude × 400 m distance
```

where the improved v2 scanner confirmed Mavic 4 Pro detections using only:

```text
30 dB SDR gain
```

This suggests that the main improvement came from the scanning logic, especially the `FOCUS` stage and temporal evidence accumulation, rather than only from increasing SDR gain.

---

## 13. Result Figures

The repository includes the following result figures:

| Figure | Description |
|---|---|
| `confusion_matrix.png` | Absolute confusion matrix from YOLOv11 evaluation. |
| `confusion_matrix_normalized.png` | Normalized confusion matrix. |
| `results.png` | Training and validation curves. |
| `fixed_frequency_scan_comparison.png` | Summary of fixed-frequency scan performance. |
| `multiband_scan_comparison.png` | Summary of original multiband scan performance. |
| `multiband_v2.png` | Summary of improved multiband v2 scan performance. |
| `final_comparisson.png` | Final comparison between the three scanning strategies. |

These figures were added to make the repository easier to review and to support the project presentation.

---

## 14. Organized Logs

The files:

```text
logs_escaneos.html
logs_escaneos_text.txt
```

contain organized scan logs used for presentation.

The HTML version includes colored labels for:

- `EVENT CONFIRMED`
- `FOCUS`
- `HOLD`
- `SCAN`
- `NEIG`
- Drone predictions
- Background predictions

The final Mavic3Pro test logs were excluded from the presentation version to keep the comparison focused on the main Mavic4Pro and Autel experiments.

The organized logs are useful to explain how the decision logic behaves during real-time detection, especially when comparing the original multiband scanner against the improved v2 scanner.

---

## 15. Requirements

Recommended Python packages:

```bash
pip install ultralytics numpy scipy matplotlib scikit-image pillow pyadi-iio
```

If GPU acceleration is required, install the correct PyTorch version for the local CUDA environment from the official PyTorch installation instructions.

A virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 16. Hardware Requirements

The project requires:

- SDR compatible with `pyadi-iio`
- Antenna covering 2.4 GHz and 5.8 GHz
- Computer running Python 3.10 or newer
- Optional NVIDIA GPU for faster YOLO inference

Typical SDR configuration:

```text
Sample rate: 50 MS/s
RF bandwidth: 45 MHz
Manual gain: 30–45 dB depending on the experiment
```

The real-time scripts were developed for SDR-based acquisition using Python and `pyadi-iio`.

---

## 17. How to Run

Clone the repository:

```bash
git clone https://github.com/ricardo-aparicio/drones_classification.git
cd drones_classification
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install ultralytics numpy scipy matplotlib scikit-image pillow pyadi-iio
```

Train YOLOv11 with the sample dataset:

```bash
python3 train_yolo11_cls.py
```

Run fixed-frequency inference:

```bash
python3 realtime_yolo11_sdr.py
```

Run the original multiband scanner:

```bash
python3 realtime_ia_multiband.py
```

Run the improved multiband v2 scanner:

```bash
python3 realtime_ia_v2_multiband.py
```

---

## 18. Notes Before Running Real-Time Scripts

Before running the real-time scripts, verify:

1. The SDR is connected and reachable.
2. The SDR IP address in the script matches your device.
3. The antenna supports the selected frequency band.
4. The model path points to the correct `best.pt` file.
5. The Python environment has the required packages installed.

The SDR IP address may need to be modified in the scripts, for example:

```python
SDR_IP = "ip:192.168.202.204"
```

---

## 19. Limitations

- The full dataset is not included due to repository size limitations.
- Real-time inference requires SDR hardware.
- Detection performance depends on antenna gain, SDR gain, line of sight, drone distance, drone altitude, drone orientation, and RF interference.
- Fixed-frequency scanning performs best when the correct operating frequency is known.
- Multiband scanning is more autonomous, but it must divide observation time across multiple frequencies.
- Long-range detection can become intermittent when the RF signal is weak or when the drone changes operating band.
- Some drones from the same manufacturer may show similar RF patterns, which can cause classification confusion.

---

## 20. Future Work

Future improvements may include:

- Adding more outdoor background samples.
- Testing additional drone models and communication modes.
- Improving the adaptive multiband decision logic.
- Adding cooldown logic for sub-bands that repeatedly trigger `FOCUS` but do not confirm.
- Evaluating additional SDR gain settings and antenna configurations.
- Comparing YOLOv11 with other deep learning models for spectrogram classification.
- Exploring RF-based drone localization or direction finding.
- Testing the system in more complex RF environments.

---

## 21. Conclusion

This project demonstrates that RF drone detection can be approached as a computer vision problem by converting I/Q samples into spectrogram images.

The fixed-frequency scanner provides strong detection when the correct frequency is known. The original multiband scanner adds autonomous frequency coverage but can lose weak evidence at longer range. The improved `realtime_ia_v2_multiband.py` scanner provides the best overall balance because it keeps multiband coverage while adding temporal evidence accumulation through the `FOCUS` stage.

The final result shows that the improved multiband v2 strategy is more suitable for realistic drone monitoring scenarios where the operating frequency is not always known in advance.

---

## 22. References and Tools

- Ultralytics YOLOv11
- Analog Devices SDR hardware
- `pyadi-iio`
- SciPy signal processing tools
- Matplotlib
- scikit-image
- Python
