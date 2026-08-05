!pip install ultralytics roboflow opencv-python-headless matplotlib -q


from google.colab import drive
drive.mount("/content/drive")


import zipfile
import os

zip_path = "/content/drive/MyDrive/PKLot.v2-640.yolov8-obb.zip"
extract_path = "/content/Dataset"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as f:
    f.extractall(extract_path)

print("Dataset extracted:", os.listdir(extract_path))

dataset_yaml = extract_path + "/data.yaml"
print("data.yaml path:", dataset_yaml)


from ultralytics import YOLO

model = YOLO("yolov8m-obb.pt")

model.train(
    data=dataset_yaml,
    epochs=50,
    imgsz=640,
    batch=16,
    name="pklot_training",
    device=0
)

print("Training complete!")


import shutil

shutil.copy(
    "runs/obb/pklot_training/weights/best.pt",
    "/content/drive/MyDrive/best.pt"
)

print("best.pt saved to Google Drive!")


from ultralytics import YOLO

model = YOLO("runs/obb/pklot_training/weights/best.pt")

print("Model loaded successfully!")


import cv2

def load_image(path):
    image = cv2.imread(path)
    return image

def to_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def apply_blur(gray):
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def preprocess(image):
    gray = to_grayscale(image)
    blurred = apply_blur(gray)
    return gray, blurred

print("Preprocessor functions ready!")


import numpy as np

def detect_slots(model, image):
    results = model.predict(image, conf=0.4, verbose=False)
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

print("Slot detection function ready!")


import matplotlib.pyplot as plt

COLOR_OCCUPIED = (0, 0, 255)
COLOR_VACANT   = (0, 255, 0)

def draw_slots(image, slots):
    for slot in slots:
        points = slot["points"]
        label  = slot["label"]

        if label == "space-occupied":
            color = COLOR_OCCUPIED
            text  = "Occupied"
        else:
            color = COLOR_VACANT
            text  = "Empty"

        cv2.polylines(image, [points], True, color, 2)

        cx = int(points[:, 0].mean())
        cy = int(points[:, 1].mean())
        cv2.putText(image, text, (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image

def draw_stats(image, slots):
    total    = len(slots)
    occupied = sum(1 for s in slots if s["label"] == "space-occupied")
    vacant   = total - occupied

    cv2.rectangle(image, (5, 5), (230, 90), (0, 0, 0), -1)
    cv2.putText(image, f"Total   : {total}",    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(image, f"Occupied: {occupied}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),     1)
    cv2.putText(image, f"Empty   : {vacant}",   (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),     1)

    return image

def show_figure(original, gray, result, name):
    plt.figure(figsize=(14, 4))
    plt.suptitle(name)

    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap="gray")
    plt.title("Grayscale")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Detected Slots")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

print("Visualization functions ready!")


import os

INPUT_FOLDER  = "/content/Dataset/test/images"
OUTPUT_FOLDER = "/content/output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

image_files = os.listdir(INPUT_FOLDER)

for filename in image_files:
    if not filename.endswith(".jpg") and not filename.endswith(".png"):
        continue

    path  = os.path.join(INPUT_FOLDER, filename)
    image = load_image(path)

    if image is None:
        print("Could not load:", filename)
        continue

    print("Processing:", filename)

    gray, blurred = preprocess(image)

    slots = detect_slots(model, image)
    print("  Slots detected:", len(slots))

    occupied = sum(1 for s in slots if s["label"] == "space-occupied")
    empty    = len(slots) - occupied
    print("  Occupied:", occupied, "| Empty:", empty)

    result = image.copy()
    result = draw_slots(result, slots)
    result = draw_stats(result, slots)

    show_figure(image, gray, result, filename)

    out_path = os.path.join(OUTPUT_FOLDER, "result_" + filename)
    cv2.imwrite(out_path, result)
    print("  Saved:", out_path)


import shutil

shutil.copytree(
    "/content/output",
    "/content/drive/MyDrive/Day_18_Output"
)

print("All output images saved to Google Drive!")
