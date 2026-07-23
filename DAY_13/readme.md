# DAY 13 — Object Detection with YOLOv8

This folder contains my Day 13 task for the internship, where I explored **object detection** using a pre-trained YOLOv8 model on a Face Mask Detection dataset from Kaggle.

## What is Object Detection?

Object detection is a computer vision task where a model doesn't just say *what* is in an image — it also says *where* it is. The model looks at an image and draws a **bounding box** around each object it finds, along with a label (like "person" or "car") and a confidence score (how sure it is). So the output is a list of boxes, labels, and scores for one single image, instead of just one label for the whole picture.

## How is it different from Image Classification?

Image classification only answers **"what is this image of?"** — it looks at the whole picture and gives back one label (or a few, with probabilities), with no information about location. For example, a classifier would just say "this image contains a mask" without showing where the mask is.

Object detection goes a step further and answers **"what objects are in this image, and where exactly are they?"** — it can find and locate multiple objects in the same image, even if there are several people or objects in one picture.

In short:
- **Classification** → one label for the whole image
- **Detection** → multiple labels + bounding box coordinates for each object found

This distinction mattered a lot in my task, because the dataset I ended up using (folders of `with_mask` / `without_mask` images with no bounding box coordinates) is actually structured for **classification**, not detection — so part of my learning here was realizing which task a dataset is actually set up for.

## What is YOLO?

YOLO stands for **"You Only Look Once."** It's a family of object detection models that can look at an entire image in a single pass and predict all the bounding boxes and class labels at once, which makes it very fast compared to older detection methods that scanned an image piece by piece.

In this task I used **YOLOv8**, built by Ultralytics, specifically the pre-trained `yolov8n.pt` model ("n" = nano, the smallest and fastest version). This model comes already trained on the **COCO dataset**, which has 80 everyday object classes such as `person`, `car`, `dog`, `chair`, etc. I did not train it myself — I just loaded the pre-trained weights and ran it on my images.

## Which dataset i used?

I used a **Face Mask Detection** dataset from Kaggle, made up of two folders of face images:
- `with_mask` (3,517 images)
- `without_mask` (3,217 images)

This dataset only has whole-image labels (which folder an image is in) and does **not** include bounding box coordinates, so it isn't in true YOLO detection format — it's better suited to an image classification setup.

## What objects were detected?

Since the pre-trained `yolov8n.pt` model was trained on COCO, and COCO has no "mask" or "no mask" class, the model could only detect the generic classes it already knows. In practice, this meant it detected **`person`** in the face images — it drew a bounding box around the person/face in each picture, but it had no way of labeling whether they were wearing a mask or not, since that class simply doesn't exist in COCO's 80 categories.

## My observations about the detection results

- The pre-trained model was reliable at finding and boxing the `person` class in the sample images, even across a mix of `with_mask` and `without_mask` photos.
- It never once produced a "mask" or "no mask" label — confirming that a pre-trained COCO model can only output the classes it was originally trained on, no matter what dataset you feed it.
- Confidence scores varied per image — boxes with lower confidence were generally on smaller or partially visible faces.
- Because my dataset only had whole-image class folders and no bounding box `.txt` labels, it wasn't actually set up as a YOLO detection dataset. To get real `with_mask` / `without_mask` predictions, the right approach would be to either:
  1. Fine-tune a YOLOv8 **classification** model (`yolov8n-cls.pt`) directly on the `with_mask` / `without_mask` folders, since that's the format they're already in, or
  2. Re-label the images with bounding boxes and train a proper YOLOv8 **detection** model, if I wanted both the location and the mask/no-mask label together.
- This task taught me the practical difference between classification-ready data and detection-ready data, and why a pre-trained model's output is limited by the classes it was originally trained on.
