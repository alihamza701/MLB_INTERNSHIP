# 📄 Document Scanner Web App

A simple web app that lets you upload a photo of a document, click its 4 corners, and get a perspective-corrected, sharpened scan — all in your browser.

Built with **Python + Flask + OpenCV**.

---

## ✨ Features

- 📤 Drag & drop or click-to-upload image
- 🖱️ Click 4 corners of your document on the image
- 📐 Perspective correction (straightens skewed documents)
- 🔪 Sharpening filter (crisper text)
- ☀️ Brightness/contrast boost
- ⬇️ Download any of the 3 output images

## 🔒 Security Features

- File extension whitelist (only image files accepted)
- 10 MB upload size limit
- Secure filename sanitization (prevents path traversal)
- Coordinate validation (prevents malicious JSON payloads)
- Automatic temp file cleanup after processing

---

## 🚀 How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/document-scanner.git
cd document-scanner
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

**4. Open your browser**
```
http://localhost:5000
```

---

## 📁 Project Structure

```
document-scanner/
├── app.py              ← Flask backend (routes + OpenCV logic)
├── requirements.txt    ← Python dependencies
├── static/
│   ├── style.css       ← Styling (dark mode)
│   └── script.js       ← Frontend logic (upload, canvas, corner clicks)
└── templates/
    └── index.html      ← Main HTML page
```

---

## 🖼️ How It Works

1. Upload a photo of a document (e.g. a receipt, book page, ID card)
2. Click the **4 corners** of the document in the image
3. Click **Process Document**
4. Download your corrected scan

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework |
| `opencv-python` | Image processing |
| `numpy` | Array operations |
