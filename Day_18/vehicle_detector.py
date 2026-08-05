from ultralytics import YOLO
import numpy as np
import config

def load_model():
    model = YOLO(config.MODEL_PATH)
    return model

def detect_slots(model, image):
    results = model.predict(image, conf=config.CONFIDENCE, verbose=False)
    slots = []

    for r in results:
        if r.obb is None:
            continue
        for obb in r.obb:
            class_id = int(obb.cls[0])
            conf = float(obb.conf[0])
            points = obb.xyxyxyxy[0].cpu().numpy().reshape(4, 2).astype(int)

            if class_id == 0:
                label = "space-empty"
            else:
                label = "space-occupied"

            slots.append({
                "points": points,
                "label": label,
                "conf": conf
            })

    return slots
