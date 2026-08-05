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
