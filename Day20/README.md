# 🎮 Remote Instance Segmentation with YOLOv8

A Google Colab notebook that trains a **YOLOv8n-seg** model to perform **instance segmentation** on a single custom class — the **TV Remote** — using two different training strategies and compares their results.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Approaches](#approaches)
- [Training Configuration](#training-configuration)
- [Results](#results)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Requirements](#requirements)

---

## 🧾 Overview

This project is **Day 20** of a hands-on deep learning challenge. The goal is to build an instance segmentation pipeline that can detect and segment a TV remote in images. Two training strategies are explored and compared:

1. **Training from scratch** — no pretrained weights, learned entirely from the custom dataset.
2. **Fine-tuning** — starting from COCO-pretrained YOLOv8n-seg weights and adapting to the custom class.

---

## 📦 Dataset

> 📁 Dataset and training results are available on Google Drive: *(link to be added)*

- **Class:** `Remote` (single class, index `0`)
- **Total images:** 50
  - Train: 40 images
  - Val: 10 images
- **Annotation format:** COCO JSON → converted to YOLO segmentation format using `ultralytics.data.converter.convert_coco`
- **Split ratio:** 80/20 (train/val), with `SEED=42` for reproducibility
- **Image size:** 640 × 640

---

## ⚙️ Approaches

### Approach 1 — Train from Scratch
- Model initialized with **random weights** (`pretrained=False`)
- Trained for **200 epochs**
- Optimizer: AdamW (auto-selected, `lr=0.002`, `momentum=0.9`)
- Output saved to: `runs/segment/scratch_remote/`

### Approach 2 — Fine-tune from COCO Weights
- Model initialized from **pretrained `yolov8n-seg.pt`** (COCO weights)
- Trained for **100 epochs**
- Transfer learning from general features to the Remote class
- Output saved to: `runs/segment/finetune_remote/`

---

## 🔧 Training Configuration

| Parameter         | Value              |
|-------------------|--------------------|
| Model             | `yolov8n-seg`      |
| Image Size        | `640`              |
| Batch Size        | `8`                |
| Epochs (Scratch)  | `200`              |
| Epochs (Finetune) | `100`              |
| Val Fraction      | `0.2`              |
| Seed              | `42`               |
| Device            | Tesla T4 (Colab)   |
| Augmentations     | Mosaic, Flip, HSV, Blur, CLAHE |

---

## 📊 Results

> 📁 Training plots, confusion matrices, and model weights are available on Google Drive: *(link to be added)*

Results include:
- `box_loss`, `seg_loss`, `cls_loss`, `dfl_loss` curves across epochs
- Per-epoch **mAP@50** and **mAP@50-95** for both Box and Mask heads
- Prediction visualizations on validation images

---

## 📁 Project Structure

```
Day20.ipynb              ← Main Colab notebook
README.md                ← This file
```

Inside the Colab runtime (ephemeral):
```
/content/
├── raw_dataset/
│   └── dataset/
│       ├── images/
│       └── annotations.json    ← COCO format
├── converted/
│   └── labels/annotations/     ← YOLO seg format (.txt)
├── dataset/
│   ├── images/train/ & val/
│   ├── labels/train/ & val/
│   └── data.yaml
└── runs/segment/
    ├── scratch_remote/          ← Approach 1 outputs
    └── finetune_remote/         ← Approach 2 outputs
```

---

## ▶️ How to Run

1. **Open in Google Colab** — upload `Day20.ipynb` or open from GitHub.
2. **Mount Google Drive** — the notebook loads `dataset.zip` from `MyDrive/dataset.zip`.
3. **Run all cells sequentially:**
   - Cell 1: Install Ultralytics & verify environment
   - Cell 2: Set hyperparameters
   - Cell 3: Mount Drive & extract dataset
   - Cell 4: Convert COCO annotations → YOLO format
   - Cell 5: Train/val split
   - Cell 6: Generate `data.yaml`
   - Cell 7: Visualize sample annotations
   - Cell 8+: Train from scratch (Approach 1)
   - Later cells: Fine-tune from pretrained weights (Approach 2)

> ⚠️ Make sure your `dataset.zip` contains an `images/` folder and a single `annotations.json` (COCO format) at the dataset root.

---

## 📦 Requirements

All dependencies are installed inside the notebook:

```bash
pip install ultralytics
```

| Library       | Purpose                         |
|---------------|---------------------------------|
| `ultralytics` | YOLOv8 training & inference     |
| `torch`       | Deep learning backend           |
| `opencv-cv2`  | Image loading & visualization   |
| `matplotlib`  | Plotting annotations & results  |
| `numpy`       | Array operations                |

---

## 🧠 Key Learnings

- How to convert **COCO JSON** annotations to **YOLO segmentation** `.txt` format.
- The impact of **pretraining** vs. training from scratch on small datasets (~50 images).
- How YOLOv8's **instance segmentation head** (mask coefficients + prototypes) works.
- Using Ultralytics' built-in **train/val pipeline** with automatic optimizer selection.
