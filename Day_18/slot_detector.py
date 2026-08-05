import cv2
import numpy as np
import config

def find_slots(blurred):
    edges = cv2.Canny(blurred, 50, 150)

    kernel = np.ones((5, 5), np.uint8)
    morphed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    slots = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < config.MIN_SLOT_AREA or area > config.MAX_SLOT_AREA:
            continue

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

        if len(approx) >= 4:
            slots.append(approx)

    return slots, edges, morphed
