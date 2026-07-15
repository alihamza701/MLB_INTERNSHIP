# Day 11 — CNN Image Classification (Fashion MNIST)

Two notebooks in this folder cover CNN fundamentals and a full image classification pipeline on the **Fashion MNIST** dataset:
- `CNN_practice.ipynb` — a first, simpler CNN to practice the basic building blocks.
- `Fashion_MNIST_Classifier.ipynb` — the more complete classifier, including validation tracking, dropout, and full evaluation (confusion matrix, correct/incorrect sample inspection).

## Why CNNs Are Better Than ANNs for Image Data

A plain ANN can only accept 1D input, so an image has to be **flattened** first — a 28×28 image becomes a flat list of 784 numbers. This throws away spatial structure: the network has no way of knowing that a pixel is right next to another one, since they just become two unrelated numbers in a long row. It also means every pixel gets its own set of weights, so parameter counts explode quickly on larger images.

CNNs solve both problems:
- They keep the image in its **2D grid form** as it passes through the network, preserving spatial relationships between neighboring pixels.
- They use **filters that slide across the whole image**, reusing the same small set of weights everywhere rather than learning a separate weight for every pixel position. This means far fewer parameters, faster training, and much better generalization on image data.

## The Purpose of Convolution and Pooling Layers

**Convolution layers** slide small filters (e.g. 3×3) across the image, computing a dot product at each position. Each filter learns to detect a specific visual pattern — edges, curves, textures — and produces a **feature map** showing where that pattern was found in the image. A layer typically has many filters (e.g. 16, 32, 64), so it produces many feature maps, each highlighting a different feature.

**Pooling layers** shrink those feature maps down, reducing the amount of data flowing through the network and making it more tolerant to small shifts or distortions in the image:
- **Max Pooling** keeps the strongest (maximum) value in each small window — preserves the sharpest signal.
- **Average Pooling** takes the average value in each window — produces a smoother, blurrier summary.

Both notebooks in this folder use a mix of the two: `CNN_practice.ipynb` uses Max Pooling only, while `Fashion_MNIST_Classifier.ipynb` uses Max Pooling after the first convolution and Average Pooling after the second, as a deliberate comparison of both approaches.

## Model Architecture

### `Fashion_MNIST_Classifier.ipynb` (main / final model)

```
Conv2D(32 filters, 3x3, relu)        -> (26, 26, 32)
MaxPooling2D(2x2)                    -> (13, 13, 32)
Conv2D(64 filters, 3x3, relu)        -> (11, 11, 64)
AveragePooling2D(2x2)                -> (5, 5, 64)
Flatten()                            -> 1600 values
Dense(128, relu)
Dropout(0.3)
Dense(10, softmax)
```
**Total parameters: 225,034**

- **Dropout(0.3)** randomly disables 30% of neurons in the dense layer during each training step — this is a regularization technique specifically included to reduce overfitting.
- Optimizer: `adam`, Loss: `sparse_categorical_crossentropy` (correct choice, since labels are integers 0–9, not one-hot encoded).
- Trained for **10 epochs**, batch size **64**, with a **10% validation split**.

### `CNN_practice.ipynb` (earlier practice version)

```
Conv2D(16 filters, 3x3, same padding, relu)  -> (28, 28, 16)
MaxPooling2D(2x2)                            -> (14, 14, 16)
Flatten()                                    -> 3136 values
Dense(128, relu)
Dense(64, relu)
Dense(10, softmax)
```
A simpler, single-convolution version used to first practice the core building blocks (Conv → Pool → Flatten → Dense → Output) before building the more complete model above. Trained for 10 epochs, batch size 32, with no validation split.

## Final Training and Testing Accuracy

| Notebook | Training Accuracy | Test Accuracy | Training Loss | Test Loss |
|---|:---:|:---:|:---:|:---:|
| `CNN_practice.ipynb` | 97.61% | 91.41% | 0.067 | 0.325 |
| `Fashion_MNIST_Classifier.ipynb` | 93.63% | 90.23% | 0.171 | 0.301 |

**Training vs. Validation Accuracy (from `Fashion_MNIST_Classifier.ipynb`):**

![Training and Validation Accuracy](training_curves.png)

Training and validation accuracy track closely together across all 10 epochs, with validation actually slightly ahead of training in the earlier epochs (likely due to Dropout making training accuracy look artificially lower during training itself, since dropout is disabled during evaluation). This is a healthy curve — no dramatic overfitting, though the gap starts to widen slightly by epoch 8-10.

**Confusion Matrix:**

![Confusion Matrix](confusion_matrix.png)

The model performs strongly on visually distinct classes (Trouser, Sandal, Bag, Sneaker, Ankle boot all show a bright, clean diagonal). The clearest weak spot is the **Shirt** class, which gets confused with T-shirt/top, Pullover, and Coat — all similar upper-body garments with overlapping silhouettes at 28×28 resolution.

## Challenges Faced and How They Were Solved (or Identified)

1. **Choosing the right loss function for integer labels.** Since `y_train`/`y_test` are plain integers (0–9) rather than one-hot vectors, `sparse_categorical_crossentropy` was used instead of `categorical_crossentropy` — using the wrong one would have thrown a shape-mismatch error during training.

2. **Comparing Max vs. Average Pooling directly.** Rather than guessing which pooling type works better, `Fashion_MNIST_Classifier.ipynb` deliberately uses one of each (Max after the first conv layer, Average after the second) so both could be observed in the same model.

3. **Overfitting risk with a fairly large Dense layer (128 units) feeding into only 10 output classes.** Dropout(0.3) was added specifically to address this, randomly deactivating 30% of neurons during training so the network can't over-rely on any single path through the dense layer.

4. **A normalization step that didn't actually apply.** Worth flagging for the next iteration: in `Fashion_MNIST_Classifier.ipynb`, the normalization line is written as:
   ```python
   X_train.astype(float)/255.0
   y_train.astype(float)/255.0
   ```
   Neither line is assigned back to a variable, so `X_train` and `y_train` are **not actually modified** — the model ends up training on raw pixel values (0–255) rather than normalized ones (0–1). The model still reached 90%+ accuracy despite this, which shows CNNs can be somewhat robust to unnormalized inputs, but the fix is a one-line change:
   ```python
   X_train = X_train.astype(float) / 255.0
   X_test = X_test.astype(float) / 255.0
   ```
   (Note: labels `y_train`/`y_test` should never be normalized/divided at all — they're class indices, not pixel intensities. That line should simply be removed.)

## Project Structure

```
Day-11/
├── CNN_practice.ipynb
├── Fashion_MNIST_Classifier.ipynb
├── sample_images.png
├── training_curves.png
├── confusion_matrix.png
├── correct_predictions.png
├── incorrect_predictions.png
└── README.md
```

## 
* Short video of training and testing of the model
https://drive.google.com/file/d/1V3xAceCIcKgKKy-PxGRAFd3rGrvfbfnq/view?usp=sharing
