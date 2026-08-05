# Day 17 — Object Detection using YOLO

Exploring the Ultralytics YOLO package for object detection: basic inference, testing on images, and a mini project applying a pre-trained model to vehicle detection.

## What is Object Detection?

Object detection is a computer vision task that does two things at once for every object in an image:
1. **Classifies** what the object is (e.g. "person", "bus", "car").
2. **Localizes** where it is, by drawing a bounding box around it.

A single image can contain multiple objects, of multiple classes, and the model must find and label all of them — not just describe the image as a whole.

## How is it Different from Image Classification?

**Image Classification** assigns a single label to an entire image (e.g. "this image contains a dog"). It assumes one main subject and gives no location information.

**Object Detection** goes further: it finds *every* object in the image, tells you *what* each one is, *where* it is (bounding box coordinates), and *how confident* the model is in each individual prediction. An image can have zero, one, or many detected objects, each handled independently.

| | Image Classification | Object Detection |
|---|---|---|
| Output | One label for the whole image | Multiple labels + boxes |
| Location info | No | Yes (bounding boxes) |
| Multiple objects | Not handled | Explicitly handled |

## What is YOLO?

**YOLO (You Only Look Once)** is a family of real-time object detection models. Unlike older approaches that scanned an image in multiple passes, YOLO processes the entire image in a single forward pass through the network — predicting all bounding boxes and class labels simultaneously. This makes it fast enough for real-time use (video, webcams, live camera feeds) while still being accurate.

This project uses **YOLOv8n** ("nano") from the `ultralytics` Python package — the smallest and fastest variant, pre-trained on the **COCO dataset** (80 everyday object classes: people, vehicles, animals, furniture, food, etc.).

## Which Dataset Did I Use?

**Vehicle Detection.**

Note on dataset sourcing: this project was built in a sandboxed environment without direct access to Roboflow Universe or Kaggle (network access is restricted to package-hosting sites only). Vehicle Detection was chosen specifically because it doesn't require a specialized downloaded dataset to produce meaningful results — YOLOv8n's pre-training on COCO already includes vehicle classes (**car, bus, truck, motorcycle, bicycle, train**), so running inference directly on public sample images still demonstrates genuine, correct-domain vehicle detection.

Sample images used (from the official [Ultralytics assets repo](https://github.com/ultralytics/assets), the standard images used in YOLO documentation/demos):
- `bus.jpg` — a street scene with a bus and several pedestrians.
- `zidane.jpg` — two people on a sports sideline (used for general practice, not the vehicle mini-project).

**To reproduce this with a real downloaded Roboflow/Kaggle dataset:** download any of the recommended datasets (PPE, Helmet, Vehicle, Fruit, Face Mask) in YOLO format, then point the script's `IMAGE_DIR` at the dataset's `images/` folder — everything else in the pipeline works the same way, since it doesn't depend on any bus.jpg-specific logic.

## What Objects Were Detected?

From `bus.jpg` (the vehicle detection mini-project image):

| Object | Confidence |
|--------|:----------:|
| bus | 0.84 |
| person | 0.89 |
| person | 0.88 |
| person | 0.88 |
| person | 0.44 |

From `zidane.jpg` (general practice image):

| Object | Confidence |
|--------|:----------:|
| person | 0.83 |
| person | 0.83 |
| tie | 0.28 |

## Observations About the Detection Results

- The model correctly identified the **bus** with high confidence (0.84) and drew a tight bounding box around it, despite the bus taking up a large, irregular portion of the frame.
- All clearly-visible people were detected with high confidence (0.83–0.89). The one low-confidence person detection (0.44) corresponds to a partially cropped figure at the edge of the frame — the model is less certain when an object is only partially visible.
- The "tie" detection at just 0.28 confidence is a good example of a **borderline detection** — low enough that a real application might filter it out using a confidence threshold (e.g. only keep detections above 0.5).
- Since this is a general-purpose COCO-pretrained model rather than one fine-tuned specifically for vehicles, it correctly caught the bus but wouldn't reliably distinguish finer-grained vehicle types (e.g. it might not tell a delivery van from a regular car) — that level of specificity is what a domain-specific dataset and fine-tuning would add.
- Inference is fast: around 150–200ms per image on CPU with the "nano" model, which is why YOLO models are popular for real-time or near-real-time applications.

## Project Structure

```
Day-17/
├── yolo_practice.py                      # Practice 1: load model, single + multiple image detection
├── object_detection_own_images.py        # Practice 2: test on images, inspect boxes/confidence
├── mini_project_vehicle_detection.py     # Mini project: vehicle detection pipeline
├── sample_images/
│   ├── bus.jpg
│   └── zidane.jpg
├── output_images/
│   ├── practice1_single_zidane.jpg
│   ├── practice1_multi_zidane.jpg
│   ├── practice1_multi_bus.jpg
│   ├── practice2_own_zidane.jpg
│   ├── practice2_own_bus.jpg
│   ├── miniproject_vehicle_zidane.jpg
│   └── miniproject_vehicle_bus.jpg
└── README.md
```

## How to Run

```bash
pip install ultralytics
python yolo_practice.py
python object_detection_own_images.py
python mini_project_vehicle_detection.py
```

The first run will automatically download the `yolov8n.pt` pre-trained weights (~6MB) from Ultralytics' GitHub releases.

To test on your own personal photos: edit `IMAGE_PATHS` in `object_detection_own_images.py` (or `IMAGE_DIR` in the mini project script) to point at your own image files instead of the sample images.
