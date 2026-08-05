# Day 18 — Smart Parking Occupancy Detection with YOLOv8-OBB

A parking-lot occupancy system that classifies every parking slot as **empty** or **occupied** by fine-tuning a YOLOv8 oriented-bounding-box (OBB) model on the **PKLot** dataset, plus a local training script, a self-contained Colab version, and an inference pipeline that annotates and saves results.

## Project Structure

```
Day_18/
├── config.py                 # Central configuration (paths, thresholds, colors)
├── train.py                  # Local training script — fine-tunes YOLOv8m-OBB on PKLot
├── smart_parking_colab.py    # Self-contained Colab version: mount Drive → extract dataset → train → infer → save results to Drive
├── main.py                   # Inference entry point — runs the trained model on a folder of images
├── preprocessor.py           # Image loading, grayscale conversion, Gaussian blur (feeds the display panel)
├── vehicle_detector.py       # Loads the trained YOLO model and runs OBB slot-status detection
├── visualizer.py             # Draws occupied/vacant overlays + stats box, shows and saves results
├── slot_detector.py          # Classical CV slot-boundary finder (Canny + contours) — not called by main.py
├── occupancy_analyzer.py     # Vehicle-center-inside-slot occupancy check — not called by main.py
└── requirements.txt
```

## Pipeline Overview

**Training**

```
PKLot dataset (OBB-labeled parking-lot images)
        │
        ▼
yolov8m-obb.pt (pretrained)
        │   fine-tune: 50 epochs, imgsz 640, batch 16
        ▼
runs/obb/pklot_training/weights/best.pt
```

**Inference** (`main.py`)

```
Input image
    │
    ├─► preprocessor.py  →  grayscale + blur   (used only for the 3-panel display, not fed to the model)
    │
    └─► vehicle_detector.py  →  YOLO OBB model  →  per-slot: "space-empty" / "space-occupied" + confidence
                │
                ▼
        visualizer.py  →  draw colored polygons + stats box  →  show figure + save to output/
```

## What Is OBB Detection, and Why Use It Here?

Standard YOLO draws axis-aligned rectangles around detections. Parking lots are almost always photographed at an angle, so the slots themselves are rotated relative to the image frame — a regular axis-aligned box either cuts into neighboring slots or leaves a lot of dead space around the one it's meant to cover. **Oriented Bounding Box (OBB)** detection predicts a rotated 4-point quadrilateral per object instead, so each box can hug a slot tightly regardless of camera angle. That's why this project uses `yolov8m-obb.pt` as the base model and the **PKLot.v2-640.yolov8-obb** export (an OBB-formatted version of the classic PKLot dataset, hosted on Roboflow) rather than the standard YOLOv8 detection format.

## Design Note: Two Approaches Live in This Folder, Only One Is Wired Up

Worth flagging, since it isn't obvious from the file names alone: `main.py`'s actual pipeline (via `vehicle_detector.py`) doesn't detect vehicles and slots separately and then check for overlap. Instead, the fine-tuned OBB model predicts each slot's **occupancy status directly** as a 2-class detection problem — class `0` = `space-empty`, class `1` = `space-occupied`. So despite its name, `vehicle_detector.py` is really a slot-status detector, not a vehicle detector.

`slot_detector.py` (classical Canny-edge + contour-based slot-boundary finder) and `occupancy_analyzer.py` (checks whether a detected vehicle's bounding-box center falls inside a slot's contour) implement a different, more traditional two-stage design: find slot boundaries with classical CV, detect vehicles separately, then decide occupancy geometrically. Neither file is imported anywhere else in the folder — they're not part of the pipeline that actually runs. They look like an earlier or exploratory design kept in place after the direct OBB-classification approach was adopted. Worth knowing before reusing or extending this code.

## Dataset

**PKLot v2 (640px, YOLOv8-OBB format)**, via Roboflow.

| Class ID | Label |
|---|---|
| 0 | `space-empty` |
| 1 | `space-occupied` |

`train.py` looks for it at `../PKLot.v2-640.yolov8-obb/data.yaml` (one level above this folder); `smart_parking_colab.py` instead unzips `PKLot.v2-640.yolov8-obb.zip` from Google Drive. **The dataset itself is not included in this repo** — download/export it from Roboflow (or substitute your own PKLot-format export) and place `data.yaml` at that path before running `train.py`.

## Model

- **Base:** `yolov8m-obb.pt` (Ultralytics YOLOv8, medium size, oriented-bounding-box variant)
- **Fine-tuning:** 50 epochs, image size 640×640, batch size 16
- **Output weights:** `runs/obb/pklot_training/weights/best.pt` — also not included in this repo; either train the model yourself or point `config.MODEL_PATH` at your own weights file.

## How to Run

**1. Train (local)**
```bash
pip install -r requirements.txt
python train.py
```
Requires the PKLot dataset at `../PKLot.v2-640.yolov8-obb/` (see Dataset above).

**1b. Train (Google Colab)**
Run `smart_parking_colab.py` cell-by-cell. It mounts your Google Drive, expects `PKLot.v2-640.yolov8-obb.zip` at `/content/drive/MyDrive/`, trains, copies `best.pt` back to Drive, runs inference on the dataset's `test/images`, and saves annotated results to `/content/drive/MyDrive/Day_18_Output`.

**2. Run inference (local)**
```bash
python main.py
```
Create an `images/` folder next to `main.py` and add parking-lot photos to it. Requires `runs/obb/pklot_training/weights/best.pt` to exist (from step 1). For each image, it prints the slot/occupied/empty counts, shows a 3-panel figure (original / grayscale / detected), and saves an annotated copy to `output/`.

## Configuration

All tunable values live in `config.py`:

| Setting | Value | Purpose |
|---|---|---|
| `MODEL_PATH` | `runs/obb/pklot_training/weights/best.pt` | Path to trained weights |
| `INPUT_FOLDER` | `images` | Where `main.py` looks for input images |
| `OUTPUT_FOLDER` | `output` | Where annotated results are saved |
| `CONFIDENCE` | `0.4` | Minimum detection confidence kept |
| `COLOR_OCCUPIED` | red — BGR `(0, 0, 255)` | Overlay color for occupied slots |
| `COLOR_VACANT` | green — BGR `(0, 255, 0)` | Overlay color for empty slots |
| `MIN_SLOT_AREA` / `MAX_SLOT_AREA` | `1000` / `50000` | Area filter used by the classical (unused) `slot_detector.py` |

## Dependencies

| Library | Purpose |
|---|---|
| `ultralytics` | YOLOv8-OBB model — training & inference |
| `opencv-python` | Image I/O, preprocessing, drawing |
| `numpy` | Array/geometry operations |
| `matplotlib` | Side-by-side result visualization |

## Notes

This folder holds the pipeline's source code only — no sample images, trained weights, or output images are committed here, since the dataset and `best.pt` live in Google Drive per the Colab script. To reproduce actual results, you'll need the PKLot Roboflow export and a completed training run.

Being upfront about how this README was put together: it documents what the code does by reading it, not by running it — the PKLot dataset and trained weights aren't available in the environment used to write this. Once you've run training and inference yourself, it's worth swapping in real output images and confidence numbers here, the way the Day 17 README does.