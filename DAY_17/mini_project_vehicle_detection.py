import sys
import torch
from pathlib import Path
from ultralytics import YOLO

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs"
IMAGE_DIR = SCRIPT_DIR / "sample_images"

CONF_THRESHOLD = 0.5

model = YOLO("yolov8n.pt")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on: {device.upper()}")

VEHICLE_CLASSES = {"car", "bus", "truck", "motorcycle", "bicycle", "train"}

image_files = [
    str(IMAGE_DIR / f) for f in IMAGE_DIR.iterdir()
    if f.suffix.lower() in {".jpg", ".jpeg", ".png"}
]

if not image_files:
    print(f"[ERROR] No images found in '{IMAGE_DIR}'. "
          "Please add .jpg/.jpeg/.png files or update IMAGE_DIR.")
    sys.exit(1)

results = model.predict(
    source=image_files,
    conf=CONF_THRESHOLD,
    save=True,
    project=str(OUTPUT_DIR),
    name="mini_project_vehicle_detection",
    exist_ok=True
)

print("===== Mini Project: Vehicle Detection Results =====\n")

vehicle_detections = 0
total_detections = 0

for path, result in zip(image_files, results):
    print(f"Image: {path}")
    for box in result.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        confidence = float(box.conf[0])
        total_detections += 1

        tag = " <-- VEHICLE" if class_name in VEHICLE_CLASSES else ""
        print(f"  {class_name:12s} | confidence: {confidence:.2f}{tag}")

        if class_name in VEHICLE_CLASSES:
            vehicle_detections += 1
    print()

print(f"Total objects detected across all images: {total_detections}")
print(f"Of which vehicle-class objects: {vehicle_detections}")
print(f"\nAnnotated output images saved to {OUTPUT_DIR / 'mini_project_vehicle_detection'}")
