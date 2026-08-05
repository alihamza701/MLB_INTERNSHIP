import torch
from pathlib import Path
from ultralytics import YOLO

SCRIPT_DIR = Path(__file__).parent
SAMPLE_DIR = SCRIPT_DIR / "sample_images"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

CONF_THRESHOLD = 0.5

IMAGE_PATHS = [
    str(SAMPLE_DIR / "zidane.jpg"),
    str(SAMPLE_DIR / "bus.jpg"),
]

model = YOLO("yolov8n.pt")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on: {device.upper()}")

results = model.predict(
    source=IMAGE_PATHS,
    conf=CONF_THRESHOLD,
    save=True,
    project=str(OUTPUT_DIR),
    name="own_images",
    exist_ok=True
)

for path, result in zip(IMAGE_PATHS, results):
    print(f"\n================  {path}  ================")
    print(f"Number of objects detected: {len(result.boxes)}")

    for box in result.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = [round(v, 1) for v in box.xyxy[0].tolist()]

        print(f"  Object: {class_name:12s} | Confidence: {confidence:.2f} | "
              f"Bounding Box: (x1={x1}, y1={y1}, x2={x2}, y2={y2})")

print(f"\nAnnotated images saved to {OUTPUT_DIR / 'own_images'}")
