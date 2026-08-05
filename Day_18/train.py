from pathlib import Path
from ultralytics import YOLO

DATA_YAML = str(Path(__file__).parent.parent / "PKLot.v2-640.yolov8-obb" / "data.yaml")

model = YOLO("yolov8m-obb.pt")

model.train(
    data=DATA_YAML,
    epochs=50,
    imgsz=640,
    batch=16,
    name="pklot_training"
)

print("Training done. Best weights saved at: runs/obb/pklot_training/weights/best.pt")
