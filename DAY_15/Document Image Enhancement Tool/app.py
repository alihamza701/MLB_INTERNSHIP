import os
import uuid
import json
import base64

import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
UPLOAD_FOLDER = "uploads"
OUTPUT_SIZE = 500

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File is too large. Maximum allowed size is 10 MB."}), 413


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": f"Server error: {str(e)}"}), 500


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def apply_perspective(image, pts):
    pts_dst = np.float32([
        [0, 0],
        [OUTPUT_SIZE, 0],
        [OUTPUT_SIZE, OUTPUT_SIZE],
        [0, OUTPUT_SIZE]
    ])
    matrix = cv2.getPerspectiveTransform(pts, pts_dst)
    return cv2.warpPerspective(image, matrix, (OUTPUT_SIZE, OUTPUT_SIZE))


def apply_sharpening(image):
    kernel = np.array([
        [0, -1,  0],
        [-1,  5, -1],
        [0, -1,  0]
    ])
    return cv2.filter2D(image, -1, kernel)


def apply_contrast_brightness(image, alpha=1.0, beta=3):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def apply_color_enhancement(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.6, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)
    hsv = hsv.astype("uint8")
    vivid = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lab = cv2.cvtColor(vivid, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    vivid = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    kernel = np.array([
        [0, -1,  0],
        [-1,  5, -1],
        [0, -1,  0]
    ])
    vivid = cv2.filter2D(vivid, -1, kernel)
    return vivid


def image_to_base64(image):
    _, buffer = cv2.imencode(".png", image)
    return base64.b64encode(buffer).decode("utf-8")


def validate_points(points, img_width, img_height):
    if len(points) != 4:
        return False, "Exactly 4 corner points are required."
    for i, pt in enumerate(points):
        if len(pt) != 2:
            return False, f"Point {i+1} must have exactly 2 values (x, y)."
        x, y = pt
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            return False, f"Point {i+1} coordinates must be numbers."
        if not (0 <= x <= img_width and 0 <= y <= img_height):
            return False, f"Point {i+1} is outside image boundaries."
    return True, "OK"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided."}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected."}), 400

        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400

        safe_name = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{safe_name}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(save_path)

        image = cv2.imread(save_path)
        if image is None:
            os.remove(save_path)
            return jsonify({"error": "Could not read the image. Is it a valid image file?"}), 400

        h, w = image.shape[:2]
        img_b64 = image_to_base64(image)

        return jsonify({
            "image": img_b64,
            "width": w,
            "height": h,
            "filename": unique_name
        })

    except Exception as e:
        return jsonify({"error": f"Upload error: {str(e)}"}), 500


@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received."}), 400

        filename = data.get("filename", "")
        points = data.get("points", [])

        filename = os.path.basename(filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        if not os.path.exists(filepath):
            return jsonify({"error": "Image not found. Please upload again."}), 404

        image = cv2.imread(filepath)
        if image is None:
            os.remove(filepath)
            return jsonify({"error": "Could not read the image."}), 400

        h, w = image.shape[:2]

        is_valid, msg = validate_points(points, w, h)
        if not is_valid:
            os.remove(filepath)
            return jsonify({"error": msg}), 400

        pts = np.array(points, dtype="float32")
        pts = order_points(pts)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        perspective_gray = apply_perspective(gray, pts)
        perspective_color = apply_perspective(image, pts)

        sharpened     = apply_sharpening(perspective_gray)
        high_contrast = apply_contrast_brightness(perspective_gray)
        color_enhanced = apply_color_enhancement(perspective_color)

        os.remove(filepath)

        return jsonify({
            "perspective":    image_to_base64(perspective_gray),
            "sharpened":      image_to_base64(sharpened),
            "high_contrast":  image_to_base64(high_contrast),
            "color_enhanced": image_to_base64(color_enhanced)
        })

    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
