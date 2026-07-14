# Day 10 — Build Your First Artificial Neural Network

An ANN built with TensorFlow/Keras to classify clothing images from the **Fashion MNIST** dataset.

## Dataset

- 60,000 training images, 10,000 test images.
- Each image: 28×28 grayscale (pixel values 0–255).
- 10 balanced classes (6,000 images each): T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot.

## Preprocessing

Pixel values were normalized from the raw **0–255** range down to **0–1** by dividing by 255. Neural networks train faster and more stably on small, consistently-scaled inputs — large raw pixel values can cause unstable gradients during training.

## Model Architecture

A simple, fully-connected ANN (no convolutional layers):

```
Flatten(28, 28)        →  784 input values
Dense(128, relu)       →  100,480 params
Dense(64, relu)        →  8,256 params
Dense(10, softmax)     →  650 params (one output per class)
```
**Total: 109,386 trainable parameters**

- `relu` activations in hidden layers introduce non-linearity, letting the network learn complex patterns.
- `softmax` on the output layer converts raw scores into a probability distribution over the 10 classes.
- Compiled with the **Adam** optimizer and **sparse categorical crossentropy** loss (appropriate for integer-encoded, multi-class labels).

## Training

Trained for **10 epochs**, batch size 32, with 10% of training data held out for validation.

| Metric              | Value   |
|---------------------|:-------:|
| Final Training Accuracy   | 91.08% |
| Final Validation Accuracy | 88.68% |
| **Test Accuracy**         | **88.09%** |
| Test Loss                 | 0.3412 |

Training accuracy climbs steadily across all 10 epochs, while validation accuracy tracks a bit behind it — a normal, mild sign of overfitting rather than a red flag. The loss curves show the same pattern in reverse.

## Predictions

A sample of test images with the model's predicted label vs. the actual label:

## Insights

- A basic 2-hidden-layer ANN reaches ~88% test accuracy on Fashion MNIST without any convolutional layers — a solid baseline, though CNNs typically push well past 90%+ on this dataset since they can exploit spatial structure in images that a flattened ANN discards.
- The small, fairly stable gap between training and validation accuracy suggests the model isn't overfitting badly at 10 epochs — training much longer without regularization (dropout, early stopping) would likely widen that gap.
- Misclassifications tend to cluster among visually similar classes (e.g., "Shirt" vs "T-shirt/top" vs "Pullover" vs "Coat" — all upper-body garments with similar silhouettes), which makes sense since the model only sees raw pixel intensities, not higher-level shape features.

## Project Structure

```
Day-10/
├── fashion_mnist_ann.py
├── sample_images.png
├── accuracy_loss_curves.png
├── sample_predictions.png
└── README.md
```
