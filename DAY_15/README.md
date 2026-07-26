# DAY 15 — Document Scanner & Image Enhancement Tool

A web-based document scanner built with **Python**, **Flask**, and **OpenCV**. Upload a photo of any document, select its 4 corners, and the app applies perspective correction along with multiple image enhancement techniques to produce a clean, readable scan.

---

## How It Works

1. Upload a photo of a document (receipt, ID card, book page, etc.)
2. Click the **4 corners** of the document in the image
3. Click **Process Document**
4. Download any of the 4 enhanced outputs

---

## Transformations Implemented

### 1. Perspective Correction (Homography Transform)

The core transformation of the entire pipeline. The user manually selects the four corners of the document in the original photo. Using `cv2.getPerspectiveTransform()` and `cv2.warpPerspective()`, the selected region is mathematically mapped onto a flat, square output of fixed size (500×500 pixels).

**How it works:**
- The 4 clicked points are sorted into a consistent order: top-left → top-right → bottom-right → bottom-left
- A 3×3 transformation matrix (homography) is computed that maps the source quadrilateral to a destination rectangle
- The image is warped using this matrix so the document fills the entire output

---

### 2. Sharpening (Laplacian Kernel Filter)

A 3×3 convolution kernel is applied to the grayscale perspective-corrected image using `cv2.filter2D()`.

**Kernel used:**
```
 0  -1   0
-1   5  -1
 0  -1   0
```

This is a high-pass filter that enhances edges by subtracting the surrounding pixel values from the centre. Text edges and fine details become crisper and more defined, making the document easier to read.

---

### 3. Brightness / Contrast Boost (`convertScaleAbs`)

Applied to the grayscale output using `cv2.convertScaleAbs(image, alpha=1.0, beta=3)`.

- `alpha` controls contrast (multiplier on pixel values)
- `beta` adds a flat brightness offset to every pixel

This lifts the overall brightness of the document slightly, which helps on images taken in dim or uneven lighting. The output is a cleaner, less washed-out version of the scan.

---

### 4. Colour Enhancement (HSV + CLAHE + Sharpening)

Applied to the **colour** (BGR) version of the perspective-corrected image. Three stages are combined:

**Stage 1 — Saturation Boost (HSV)**
The image is converted to HSV colour space. The saturation channel (S) is multiplied by 1.6 (60% boost) and the value/brightness channel (V) is lifted by 10%. This makes colours more vivid and punchy without looking artificial.

**Stage 2 — CLAHE (Contrast Limited Adaptive Histogram Equalisation)**
The image is converted to LAB colour space. CLAHE is applied only to the L (luminance) channel using `cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))`. Unlike global histogram equalisation, CLAHE works on small local tiles, which means it brings out detail in both dark and bright areas simultaneously without over-exposing highlights.

**Stage 3 — Sharpening**
The same Laplacian sharpening kernel from transformation #2 is applied to the colour-enhanced image. This gives the final output crisp edges with vibrant, clear colours.

---

## Purpose of Each Enhancement Technique

| Technique | Purpose |
|---|---|
| **Perspective Correction** | Removes the physical skew and angle distortion from a handheld photo, producing a straight, flat document view |
| **Sharpening** | Improves readability of text by making character edges more defined |
| **Brightness / Contrast Boost** | Compensates for dark or unevenly lit source images |
| **Colour Enhancement (HSV + CLAHE)** | Restores natural colour fidelity and recovers detail lost in shadow or highlight regions |

---

## Which Transformation Had the Biggest Impact

**Perspective Correction had by far the biggest impact on document quality.**

Without it, the other enhancements are largely cosmetic. A document photographed at an angle — which is almost always the case in real use — is geometrically distorted: text lines appear slanted, margins are uneven, and the content is harder to read or digitize. Perspective correction fixes the root problem.

The transformation converts an angled, trapezoid-shaped capture into a proper rectangular document, which alone makes the output usable. The sharpening and colour enhancements build on top of this corrected base to improve visual quality further, but they cannot compensate for geometric distortion on their own.

In terms of visual improvement ranking:
1. **Perspective Correction** — foundational, fixes geometry
2. **CLAHE (in Colour Enhancement)** — biggest quality jump after perspective, recovers local contrast
3. **Sharpening** — noticeably crisps up text edges
4. **Brightness/Contrast Boost** — subtle improvement for dark images

---

## Challenges Faced During Implementation

### 1. Replacing Colab-Specific Code with a Web Interface
The original script ran in Google Colab and used `cv2_imshow()` and `eval_js()` to display images and capture clicks — features that only exist inside a Colab notebook. Rebuilding this interaction for a standard browser required designing a canvas-based click system in JavaScript and communicating the coordinates back to the Flask backend via a POST request.

### 2. Coordinate Scaling Between Canvas and Original Image
When an image is displayed on a `<canvas>` element in the browser, it is scaled down to fit the screen. The pixel coordinates of a user's click refer to the *displayed* canvas, not the *original* image. Converting display coordinates back to image coordinates required computing a scale factor (`canvas.width / imageWidth`) and applying it to every click point before sending them to the server.

### 3. Consistent Corner Ordering
`cv2.getPerspectiveTransform()` requires the 4 source points to be in a specific order (top-left, top-right, bottom-right, bottom-left). If the user clicks in a different order, the transform produces an incorrect or flipped result. This was solved by implementing an `order_points()` function that sorts any 4 points by their coordinate sums and differences, reliably assigning each point to its correct corner regardless of click order.

### 4. OpenCV Compatibility on Cloud Servers
`opencv-python` (the standard package) attempts to load display libraries (`libGL`, `libgthread`) that are not available on headless Linux cloud servers. The solution was to switch to `opencv-python-headless`, which provides the full OpenCV API without any display dependencies, making it suitable for server-side deployment.

### 5. Silent JavaScript Errors Causing Upload Failures
Early in development, removing the corner hint element from the HTML without also removing its JavaScript references caused a `ReferenceError` at page load. Because the error occurred before the `fetch()` call, every upload silently failed and showed only a generic error message. The fix required tracing the error source and removing all stale DOM references from the script.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Image Processing | OpenCV, NumPy |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Canvas Interaction | HTML5 Canvas API |

---

## Run Locally

```bash
git clone https://github.com/alihamza701/MLB_INTERNSHIP.git
cd "MLB_INTERNSHIP/DAY_15/Document Image Enhancement Tool"
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.
