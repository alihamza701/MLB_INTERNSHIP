# DAY 16 — Edge Detection, Morphological Operations & Document Boundary Detection

A set of computer vision scripts built with **OpenCV** and **Python** that cover edge detection techniques, morphological image processing, and automatic document boundary detection.

---

## Project Structure

```
DAY_16/
│
├── Edge_Detection.ipynb                    # Sobel, Laplacian, Canny comparison
├── Morphological_Operations.ipynb          # All 7 morphological operations
├── Document_Boundary_Detection_Tool.ipynb  # Full document boundary detection pipeline
│
├── input_Documents/                        # Input document images (10–15 images)
└── output_images/                          # Saved output images with detected boundaries
```

---

## Pipeline Overview

```
Original Image
      │
      ▼
 Grayscale Conversion
      │
      ▼
 Gaussian Blur  (noise reduction)
      │
      ▼
 Edge Detection  (Sobel / Laplacian / Canny)
      │
      ▼
 Morphological Operations  (close gaps, remove noise)
      │
      ▼
 Contour Detection  (find largest contour = document boundary)
      │
      ▼
 Draw & Save Result
```

---

## The Difference Between Sobel, Laplacian, and Canny

### Sobel
- Computes the **first-order gradient** of the image in the **X direction**, the **Y direction**, and then combines both.
- It is sensitive to **direction** — it can tell you whether an edge is horizontal or vertical.
- Works well for finding **strong, smooth edges** but may miss thin or subtle ones.
- The output is a gradient magnitude image, not a binary edge map.
- **Best for:** Images where you care about edge direction or want a smooth edge response.

### Laplacian
- Computes the **second-order derivative** of the image in all directions at once.
- It is **isotropic** — it treats all directions equally and finds edges regardless of their orientation.
- Very sensitive to **noise**, so it must always be used after blurring.
- Tends to produce **thicker, noisier edges** compared to Canny.
- **Best for:** Detecting edges in all directions in a single pass when direction does not matter.

### Canny
- A **multi-stage algorithm**: Gaussian smoothing → Gradient calculation → Non-Maximum Suppression (NMS) → Double threshold hysteresis.
- **Non-Maximum Suppression** thins the edges down to single-pixel width.
- **Double threshold** (low and high) means only strong edges are kept, and weak edges are kept only if they connect to strong ones.
- Produces the **cleanest, thinnest, most accurate** edges of the three methods.
- **Best for:** Applications that need precise, thin, well-defined edge maps — including document boundary detection.

| Feature | Sobel | Laplacian | Canny |
|---|---|---|---|
| Derivative order | 1st | 2nd | 1st (internally) |
| Direction aware | Yes (X and Y) | No (isotropic) | No |
| Edge thickness | Thick / gradient | Thick / noisy | Thin / precise |
| Noise sensitivity | Medium | High | Low (built-in blur) |
| Output type | Gradient magnitude | Signed values | Binary edge map |
| Best use case | Directional edges | All-direction edges | Precise edge detection |

---

## The Purpose of Each Morphological Operation

All morphological operations work on a binary or grayscale image using a **structuring element (kernel)** — usually a rectangular or circular matrix of ones.

### Erosion
- **Shrinks** the white (foreground) regions by removing pixels at the boundaries.
- Removes small white dots and thin lines from the image.
- **Use:** Eliminate small noise pixels and disconnect weakly connected components.

### Dilation
- **Expands** the white (foreground) regions by adding pixels at the boundaries.
- Fills in small holes and thickens edges.
- **Use:** Connect broken edges or fill small gaps in contours.

### Opening  *(Erosion → Dilation)*
- First erodes, then dilates. This removes small noise without significantly changing the size of larger objects.
- **Use:** Clean up small spurious edge pixels while preserving the main structure.

### Closing  *(Dilation → Erosion)*
- First dilates, then erodes. This fills small holes and gaps inside foreground regions.
- **Use:** Close broken edges and fill gaps in the document boundary contour — very useful in document detection.

### Morphological Gradient  *(Dilation − Erosion)*
- The difference between a dilated and eroded image highlights only the **boundary pixels** of objects.
- **Use:** Extract the outline of shapes — produces a thin border around detected regions.

### Top Hat  *(Original − Opening)*
- Recovers **small bright features** that were removed during the opening step.
- **Use:** Detect small bright spots or text on a darker background.

### Black Hat  *(Closing − Original)*
- Recovers **small dark features** that were removed during the closing step.
- **Use:** Detect small dark spots or thin dark lines on a bright background.

| Operation | Formula | Effect |
|---|---|---|
| Erosion | — | Shrinks foreground |
| Dilation | — | Grows foreground |
| Opening | Erosion → Dilation | Removes small noise |
| Closing | Dilation → Erosion | Fills small gaps/holes |
| Gradient | Dilation − Erosion | Outlines object borders |
| Top Hat | Original − Opening | Finds small bright features |
| Black Hat | Closing − Original | Finds small dark features |

---

## Which Combination of Techniques Gave the Best Results

After testing across all image conditions (straight scans, mobile photos, tilted documents, shadowed and blurred images), the following pipeline gave the best overall results:

```
Grayscale  →  Gaussian Blur (5×5)  →  Canny (50, 150)  →  MORPH_CLOSE (5×5 kernel)  →  Largest Contour
```

**Why this combination works best:**

- **Gaussian Blur (5×5)** smooths out noise and minor texture variations before edge detection, reducing false edges.
- **Canny** produces the thinnest and most accurate edge map, which means the contour finder has cleaner boundaries to work with.
- **MORPH_CLOSE** after Canny fills in small gaps in the document boundary that Canny may break due to low contrast areas or shadows. This connects broken edge segments into a complete closed contour.
- **Largest contour** selection reliably picks the document because the document boundary is almost always the biggest connected shape in the image.

**What did not work as well:**

- Sobel edges are too thick and noisy for clean contour detection — many false contours appear.
- Laplacian without very strong blurring produces too much internal texture noise, making it hard to isolate the document boundary.
- Using Opening instead of Closing breaks the boundary contour further rather than healing it.

---

## Challenges Faced While Detecting Document Boundaries

### 1. Shadows and Uneven Lighting
When a document has shadows (common in mobile phone photos), the Canny edge detector picks up the shadow boundary instead of the paper boundary. This creates extra edges inside the image that compete with the real document boundary.

**Approach:** Increasing the Canny lower threshold reduces weak shadow edges. Adaptive thresholding before edge detection also helps.

### 2. Low Contrast Between Document and Background
When the document is white and the surface beneath it is also light-coloured (like a white desk), the edges at the boundary are very faint. Canny may miss them entirely.

**Approach:** Applying histogram equalisation (`cv2.equalizeHist`) before blurring boosts contrast and makes the boundary edges more visible.

### 3. Tilted and Crumpled Documents
Tilted documents produce a rotated rectangular contour. If the document is crumpled or folded, the contour is no longer a clean quadrilateral and `approxPolyDP` may not approximate it well.

**Approach:** Using `cv2.convexHull` on the largest contour gives a better outer boundary even for slightly crumpled pages.

### 4. Background Clutter
When the document is placed on a busy background (keyboard, patterned tablecloth), many contours appear and the document boundary is not always the largest one by area.

**Approach:** Sorting contours by area and filtering out ones that are too small or touch the image border helps narrow down the real document contour.

### 5. Blurred Images
Slightly blurred images (from camera shake or out-of-focus shots) produce soft, wide edges rather than sharp ones. After Canny, the edges are broken into fragments and the boundary contour is incomplete.

**Approach:** A larger Gaussian kernel (7×7 or 9×9) paradoxically helps by averaging out the blur further, making the remaining strong edges cleaner. MORPH_CLOSE with a larger kernel (7×7) then reconnects the fragments.

---

## Setup

```bash
pip install opencv-python numpy matplotlib
```

## Usage

1. Put your document images inside the `input_Documents/` folder.
2. Open and run any of the three notebooks in order:
   - `Edge_Detection.ipynb` — explore Sobel, Laplacian, Canny
   - `Morphological_Operations.ipynb` — explore all morphological operations
   - `Document_Boundary_Detection_Tool.ipynb` — run the full detection pipeline
3. Results are saved to `output_images/`.

---

## Dependencies

| Library | Version |
|---|---|
| opencv-python | 4.x |
| numpy | 1.x |
| matplotlib | 3.x |

---

## Dataset

The `input_Documents/` folder contains 10–15 document images covering different real-world conditions:

- Straight flat scanned documents
- Mobile phone photos of documents
- Tilted or rotated documents
- Documents with shadows or uneven lighting
- Slightly blurred or out-of-focus documents
