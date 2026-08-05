import cv2
import os
import matplotlib.pyplot as plt
import config

def draw_slots(image, slots):
    for slot in slots:
        points = slot["points"]
        label = slot["label"]

        if label == "space-occupied":
            color = config.COLOR_OCCUPIED
            text = "Occupied"
        else:
            color = config.COLOR_VACANT
            text = "Empty"

        cv2.polylines(image, [points], True, color, 2)

        cx = int(points[:, 0].mean())
        cy = int(points[:, 1].mean())
        cv2.putText(image, text, (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image

def draw_stats(image, slots):
    total = len(slots)
    occupied = sum(1 for s in slots if s["label"] == "space-occupied")
    vacant = total - occupied

    cv2.rectangle(image, (5, 5), (230, 90), (0, 0, 0), -1)
    cv2.putText(image, f"Total   : {total}",    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(image, f"Occupied: {occupied}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    cv2.putText(image, f"Empty   : {vacant}",   (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

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

def save_image(image, filename):
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    path = os.path.join(config.OUTPUT_FOLDER, "result_" + filename)
    cv2.imwrite(path, image)
    print("Saved:", path)
