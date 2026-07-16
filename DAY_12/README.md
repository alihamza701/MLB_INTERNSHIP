# Cats vs Dogs Classification — Transfer Learning with MobileNetV2

## What is Transfer Learning?

Transfer learning is the practice of taking a model that has already been trained on a large dataset (here, MobileNetV2 pretrained on ImageNet's 1.4 million images across 1,000 classes) and reusing the feature representations it has already learned, instead of training a new model from scratch on your own smaller dataset.

The intuition: the early and middle layers of a CNN trained on a huge diverse image dataset learn general-purpose visual features — edges, textures, corners, shapes, fur patterns, eyes, and other mid-level features — that are useful for almost any image classification task, not just the original 1,000 ImageNet classes. Only the final task-specific layers actually need to be relearned.

In this project specifically:
- The **convolutional base** of MobileNetV2 (all its inverted residual blocks) is kept frozen — its ImageNet-trained weights are used as a fixed feature extractor.
- A small **custom classification head** (Global Average Pooling → Dropout → Dense with sigmoid) is added on top and trained from scratch to map those general features onto the specific cat-vs-dog decision.

This lets a dataset with only a few thousand images (Cats vs Dogs) reach strong accuracy, which would be very difficult training a CNN of this depth from random initialization on a dataset that size.

## Why choose MobileNetV2?

- **Parameter efficiency.** MobileNetV2 uses depthwise separable convolutions and inverted residual blocks, giving it roughly 3.4M parameters — a fraction of VGG16 (~138M) or ResNet50 (~25.6M) — while still reaching competitive ImageNet accuracy. For a binary classification task like cats vs dogs, that lighter feature extractor is more than sufficient and far cheaper to run.
- **Fast to fine-tune and iterate on.** With the base frozen, only the small head is trainable, so training epochs are quick — useful for experimenting with different head designs and hyperparameters within a limited time.
- **Practical/deployment relevance.** MobileNetV2 was designed for mobile and edge inference, which matches the kind of lightweight, deployable models relevant to real-world computer vision work.
- **Built-in Keras support.** `tf.keras.applications.MobileNetV2` ships with ImageNet weights and a matching `preprocess_input` function, making the pretrained-weights + correct-normalization setup straightforward and less error-prone than a custom implementation.

## What experiments did i perform to improve accuracy?

> _Fill in with what you actually tried — suggested experiments to run and report on below:_

- [ ] **Baseline:** frozen base + GAP + Dropout(0.2) + Dense(1, sigmoid), trained for `[N]` epochs at learning rate `[X]`. Baseline validation accuracy: `[__]`.
- [ ] **Learning rate tuning:** tried learning rates `[e.g. 1e-3, 1e-4, 1e-5]` — result: `[which worked best and why]`.
- [ ] **Dropout rate:** tried `[e.g. 0.2, 0.3, 0.5]` — result: `[effect on train/val gap]`.
- [ ] **Data augmentation:** added `[e.g. RandomFlip, RandomRotation, RandomZoom]` before the base model — result: `[did it reduce overfitting]`.
- [ ] **Batch size:** tried `[e.g. 16, 32, 64]` — result: `[effect on training stability/speed]`.
- [ ] **Fine-tuning:** unfroze the top `[N]` layers of the base model after initial head training, retrained with a lower learning rate (`[e.g. 1e-5]`) — result: `[accuracy change]`.
- [ ] **Input resolution:** tried `[e.g. 128 vs 160 vs 224]` — result: `[accuracy/speed tradeoff]`.

## Final validation accuracy

> _Replace with your actual result from `model.evaluate(val_ds)`:_

**Validation accuracy: `[__.__%]`**
**Validation loss: `[_.____]`**

## Key challenges and lessons learned

> _A few common ones to start from — replace/expand with what you actually ran into:_

- **Preprocessing mismatch.** MobileNetV2 expects inputs scaled to `[-1, 1]` via `mobilenet_v2.preprocess_input`, not the more common `/255.0` scaling to `[0, 1]`. Using the wrong normalization doesn't throw an error — it just quietly caps accuracy, which makes it an easy bug to miss.
- **No premade validation split.** The `cats_vs_dogs` TFDS dataset only ships a single `train` split, so the train/validation split had to be carved out manually using slice syntax (`train[:80%]`, `train[80%:]`) rather than relying on a built-in split.
- **Freezing BatchNorm correctly.** Setting `base_model.trainable = False` alone isn't enough — `base_model(inputs, training=False)` is also needed at call time, otherwise BatchNorm layers keep updating their running statistics during training and slowly corrupt the pretrained feature extractor.
- **Overfitting on a frozen-head setup.** `[Describe what you observed in your accuracy/loss curves — e.g. training accuracy climbing faster than validation, and what you changed in response.]`

---
*Part of the MLB AI/Computer Vision Internship — Day [12].*
