const dropZone       = document.getElementById("drop-zone");
const fileInput      = document.getElementById("file-input");

const sectionUpload  = document.getElementById("section-upload");
const sectionCorners = document.getElementById("section-corners");
const sectionResults = document.getElementById("section-results");

const canvas         = document.getElementById("canvas");
const ctx            = canvas.getContext("2d");

const btnProcess      = document.getElementById("btn-process");
const btnResetCorners = document.getElementById("btn-reset-corners");
const btnScanAnother  = document.getElementById("btn-scan-another");

const uploadError   = document.getElementById("upload-error");
const uploadLoader  = document.getElementById("upload-loader");
const processError  = document.getElementById("process-error");
const processLoader = document.getElementById("process-loader");

let uploadedFilename = "";
let imageWidth       = 0;
let imageHeight      = 0;
let clickedPoints    = [];
let displayedImage   = null;

const CORNER_LABELS = ["top-left", "top-right", "bottom-right", "bottom-left"];

function showUploadError(msg) {
    uploadError.textContent = msg;
    uploadError.hidden = false;
}

function clearUploadError() {
    uploadError.hidden = true;
    uploadError.textContent = "";
}

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function handleFile(file) {
    clearUploadError();
    uploadLoader.hidden = false;

    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", { method: "POST", body: formData })
        .then(async (res) => {
            const data = await res.json();
            uploadLoader.hidden = true;

            if (!res.ok || data.error) {
                showUploadError(data.error || `Server error (${res.status})`);
                return;
            }

            uploadedFilename = data.filename;
            imageWidth       = data.width;
            imageHeight      = data.height;

            drawImageOnCanvas(data.image);
            resetCorners();

            sectionCorners.hidden = false;
            sectionCorners.scrollIntoView({ behavior: "smooth" });
        })
        .catch((err) => {
            uploadLoader.hidden = true;
            showUploadError(`Could not reach the server. Make sure app.py is running. (${err.message})`);
        });
}

function drawImageOnCanvas(base64) {
    const img = new Image();
    img.onload = () => {
        displayedImage = img;
        const maxW = Math.min(700, img.width);
        const scale = maxW / img.width;
        canvas.width  = Math.round(img.width  * scale);
        canvas.height = Math.round(img.height * scale);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
    img.src = "data:image/png;base64," + base64;
}

function redrawCanvas() {
    if (!displayedImage) return;
    ctx.drawImage(displayedImage, 0, 0, canvas.width, canvas.height);

    clickedPoints.forEach(([ix, iy], index) => {
        const cx = (ix / imageWidth)  * canvas.width;
        const cy = (iy / imageHeight) * canvas.height;

        ctx.beginPath();
        ctx.arc(cx, cy, 7, 0, 2 * Math.PI);
        ctx.fillStyle = "#6c63ff";
        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = "#fff";
        ctx.font = "bold 12px Inter, sans-serif";
        ctx.fillText(CORNER_LABELS[index], cx + 10, cy - 6);
    });
}

function resetCorners() {
    clickedPoints = [];
    btnProcess.disabled = true;
    processError.hidden = true;
    redrawCanvas();
}

btnResetCorners.addEventListener("click", resetCorners);

canvas.addEventListener("click", (e) => {
    if (clickedPoints.length >= 4) return;

    const rect = canvas.getBoundingClientRect();
    const canvasX = e.clientX - rect.left;
    const canvasY = e.clientY - rect.top;
    const imgX = (canvasX / canvas.width)  * imageWidth;
    const imgY = (canvasY / canvas.height) * imageHeight;

    clickedPoints.push([imgX, imgY]);
    redrawCanvas();

    if (clickedPoints.length >= 4) {
        btnProcess.disabled = false;
    }
});

btnProcess.addEventListener("click", () => {
    processError.hidden = true;
    processLoader.hidden = false;
    btnProcess.disabled = true;

    fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            filename: uploadedFilename,
            points: clickedPoints
        })
    })
        .then(async (res) => {
            const data = await res.json();
            processLoader.hidden = true;

            if (!res.ok || data.error) {
                processError.textContent = data.error || `Server error (${res.status})`;
                processError.hidden = false;
                btnProcess.disabled = false;
                return;
            }

            setResult("img-perspective", "dl-perspective", data.perspective,    "perspective.png");
            setResult("img-sharpened",   "dl-sharpened",   data.sharpened,      "sharpened.png");
            setResult("img-contrast",    "dl-contrast",    data.high_contrast,  "high_contrast.png");
            setResult("img-color",       "dl-color",       data.color_enhanced, "color_enhanced.png");

            sectionResults.hidden = false;
            sectionResults.scrollIntoView({ behavior: "smooth" });
        })
        .catch((err) => {
            processLoader.hidden = true;
            processError.textContent = `Could not reach the server. Make sure app.py is running. (${err.message})`;
            processError.hidden = false;
            btnProcess.disabled = false;
        });
});

function setResult(imgId, dlId, base64, filename) {
    const src = "data:image/png;base64," + base64;
    document.getElementById(imgId).src = src;
    const dl = document.getElementById(dlId);
    dl.href = src;
    dl.download = filename;
}

btnScanAnother.addEventListener("click", () => {
    uploadedFilename = "";
    imageWidth = imageHeight = 0;
    displayedImage = null;
    clickedPoints = [];
    fileInput.value = "";

    sectionCorners.hidden = true;
    sectionResults.hidden = true;
    clearUploadError();

    sectionUpload.scrollIntoView({ behavior: "smooth" });
});
