import cv2

def get_center(bbox):
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return cx, cy

def is_occupied(slot_contour, vehicles):
    for v in vehicles:
        cx, cy = get_center(v["bbox"])
        result = cv2.pointPolygonTest(slot_contour, (cx, cy), False)
        if result >= 0:
            return True
    return False

def analyze(slots, vehicles):
    results = []
    for slot in slots:
        occupied = is_occupied(slot, vehicles)
        x, y, w, h = cv2.boundingRect(slot)
        results.append({
            "contour": slot,
            "occupied": occupied,
            "rect": (x, y, w, h)
        })
    return results
