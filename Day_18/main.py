import os
import sys
import cv2

import config
import preprocessor
import vehicle_detector
import visualizer

if not os.path.isdir(config.INPUT_FOLDER):
    print(f"[ERROR] Input folder '{config.INPUT_FOLDER}' not found.")
    sys.exit(1)

model = vehicle_detector.load_model()

image_files = os.listdir(config.INPUT_FOLDER)

for filename in image_files:
    if not filename.endswith(".jpg") and not filename.endswith(".png"):
        continue

    path = os.path.join(config.INPUT_FOLDER, filename)
    image = preprocessor.load_image(path)

    if image is None:
        print("Could not load:", filename)
        continue

    print("Processing:", filename)

    gray, blurred = preprocessor.preprocess(image)

    slots = vehicle_detector.detect_slots(model, image)
    print("  Slots detected:", len(slots))

    occupied = sum(1 for s in slots if s["label"] == "space-occupied")
    empty = len(slots) - occupied
    print("  Occupied:", occupied)
    print("  Empty   :", empty)

    result = image.copy()
    result = visualizer.draw_slots(result, slots)
    result = visualizer.draw_stats(result, slots)

    visualizer.show_figure(image, gray, result, filename)
    visualizer.save_image(result, filename)
