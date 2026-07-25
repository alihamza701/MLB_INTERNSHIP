# DAY 14 — Image Processing with OpenCV

This folder contains my Day 14 task, where I practiced basic image processing operations using **OpenCV** in Python, across two notebooks: `Image_Processing_Toolkit.ipynb` and `OpenCV_Practice_Programs.ipynb`.

## The difference between BGR and RGB

Most people are used to images being stored as **RGB** (Red, Green, Blue) — that's the order used by most image viewers, browsers, and libraries like Matplotlib and PIL.

OpenCV, however, reads and stores color images in **BGR** (Blue, Green, Red) order instead — the same three channels, just in reverse order. This is a historical quirk of OpenCV, not a different format.

This matters in practice: if you load an image with `cv2.imread()` and then try to display it with a library that expects RGB (like Matplotlib's `plt.imshow()`), the colors will look wrong — blues and reds get swapped. That's why, whenever I needed to hand an OpenCV image to a non-OpenCV tool, I had to convert it first with something like `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)`. Since I displayed images using `cv2_imshow()` (Colab's own display helper for OpenCV images), which expects BGR, I didn't need to convert colors for on-screen viewing.

## What grayscale images are and why they are used

A grayscale image only stores **brightness/intensity** information (from black to white) instead of separate color channels — so instead of 3 numbers per pixel (B, G, R), there's just **1 number per pixel**.

I converted my image to grayscale using:

```python
grayscale = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
```

Grayscale is used a lot in image processing because:
- It's **simpler and faster** to process — 1 channel instead of 3 means less data and less computation.
- Many classic computer vision techniques (edge detection, thresholding, feature matching, etc.) only care about shapes and brightness patterns, not color, so grayscale is enough and removes unnecessary complexity.
- It reduces file size and memory usage.

## Which OpenCV functions I used

Across the two notebooks, I practiced the following OpenCV operations:

- `cv2.imread()` — load an image from disk
- `cv2_imshow()` (Colab's display helper) — show an image in the notebook
- `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` — convert a color image to grayscale
- `cv2.resize()` — resize an image to a specific width/height
- **NumPy array slicing** (e.g. `image1[0:100, 0:100]`) — crop specific regions out of an image
- `cv2.rotate()` with `cv2.ROTATE_90_CLOCKWISE`, `cv2.ROTATE_180`, `cv2.ROTATE_90_COUNTERCLOCKWISE` — rotate images
- `cv2.flip()` — flip an image horizontally (`1`) or vertically (`0`)
- `cv2.rectangle()` — draw a rectangle on an image
- `cv2.circle()` — draw a circle on an image
- `cv2.line()` — draw a straight line
- `cv2.polylines()` — draw a custom multi-point shape (using a NumPy array of points)
- `cv2.putText()` — draw text on an image
- `cv2.imwrite()` — save a processed image to disk
- `os.makedirs()` — create an output folder to save results into (used alongside OpenCV, not an OpenCV function itself)

`OpenCV_Practice_Programs.ipynb` also prints out basic image info (`image1.shape` for height/width/channels, and `image1.size`) before processing.

## Challenges I faced and how I solved them

- **Same image object gets modified across cells:** OpenCV's drawing functions (`cv2.rectangle`, `cv2.circle`, `cv2.line`, `cv2.polylines`, `cv2.putText`) draw directly onto the image array **in place**, rather than returning a new copy. Since I reused the same `img_for_shapes` variable across several cells, each new shape got added on top of the previous ones instead of starting from a blank image each time. I used this on purpose to build up one combined image with all the shapes on it, but it's an important thing to be careful about — if you only want one shape at a time, you need to reload or copy the original image first.
- **Output folder didn't exist yet:** `cv2.imwrite()` silently fails (returns `False`) if the folder you're saving to doesn't exist. I fixed this by always calling `os.makedirs(output_dir, exist_ok=True)` before saving, so the folder gets created if it isn't there already, and the script doesn't error out if it is.
- **Colors looked different than expected:** Since OpenCV works in BGR instead of RGB, colors passed into functions like `cv2.rectangle()` and `cv2.circle()` (e.g. `(0, 200, 0)`) needed to be thought of as **(Blue, Green, Red)**, not (Red, Green, Blue). Mixing this up meant shapes came out a different color than intended, so I had to keep the BGR order in mind every time I picked a color tuple.
