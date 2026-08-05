import torch
from pathlib import Path
from ultralytics import YOLO

SCRIPT_DIR = Path(__file__).parent
SAMPLE_DIR = SCRIPT_DIR / "sample_images"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

CONF_THRESHOLD = 0.5

model = YOLO("yolov8n.pt")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on: {device.upper()}")
print("Model loaded. Classes it can detect:")
print(model.names)

single_result = model.predict(
    source=str(SAMPLE_DIR / "zidane.jpg"),
    conf=CONF_THRESHOLD,
    save=True,
    project=str(OUTPUT_DIR),
    name="single_image",
    exist_ok=True
)

print("\n--- Single Image Results (zidane.jpg) ---")
for box in single_result[0].boxes:
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    xyxy = box.xyxy[0].tolist()
    print(f"Detected: {model.names[cls_id]:15s} | Confidence: {conf:.2f} | Box: {[round(v, 1) for v in xyxy]}")

image_list = [
    str(SAMPLE_DIR / "zidane.jpg"),
    str(SAMPLE_DIR / "bus.jpg"),
]

multi_results = model.predict(
    source=image_list,
    conf=CONF_THRESHOLD,
    save=True,
    project=str(OUTPUT_DIR),
    name="multiple_images",
    exist_ok=True
)

print("\n--- Multiple Image Results ---")
for i, result in enumerate(multi_results):
    print(f"\nImage: {image_list[i]}")
    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        print(f"  Detected: {model.names[cls_id]:15s} | Confidence: {conf:.2f}")

print(f"\nAll results saved under '{OUTPUT_DIR}'.")
