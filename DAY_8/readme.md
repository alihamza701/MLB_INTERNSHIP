# Day 8 — Breast Cancer Prediction System

A complete classification pipeline built on the **Breast Cancer Wisconsin Diagnostic Dataset** (built into Scikit-learn), covering data exploration, baseline modeling, and hyperparameter tuning with Logistic Regression.

## Dataset Overview

- 569 samples, 30 numeric features (all `float64`), no missing values.
- Target distribution: **357 benign (1)**, **212 malignant (0)** — a moderate class imbalance, which is why accuracy alone isn't a sufficient evaluation metric here.

## What I Learned About Model Evaluation

A single metric doesn't tell the full story, especially for a diagnostic task like this:

- **Accuracy** — overall correctness, but can hide poor performance on the minority class (malignant, in this dataset).
- **Precision** — of everything predicted malignant, how many actually were. High precision matters when false alarms are costly.
- **Recall** — of everything that was actually malignant, how many were caught. This matters most here — a missed cancer diagnosis (false negative) is far more dangerous than a false alarm.
- **F1-Score** — the harmonic mean of precision and recall, useful when both matter and you need one number to compare models.
- **Confusion Matrix / Classification Report** — shows performance broken down *per class*, which is essential with imbalanced data — the baseline and tuned models in this project actually showed different strengths depending on which class you look at (see comparison below).

**Key lesson**: two models can have the same accuracy but very different tradeoffs between false positives and false negatives — you have to look at the per-class breakdown to know which model is actually safer for this problem.

## What Hyperparameter Tuning Is and Why It Matters

Hyperparameters (`C`, `penalty`, `solver`, `max_iter` for Logistic Regression) are settings chosen *before* training — they aren't learned from data, unlike model coefficients. The default values are generic and may not suit a specific dataset.

**GridSearchCV** automates the search: it exhaustively tries every combination in a defined grid, using 5-fold cross-validation to score each combination fairly (rather than relying on one lucky/unlucky train-test split). It matters because:

- The regularization strength (`C`) directly controls the underfitting/overfitting tradeoff.
- Different `solver`s handle the optimization differently and can materially change which features get weighted (especially with `l1` vs `l2` penalty).
- Manually guessing good values is inefficient; GridSearchCV finds the best-performing combination systematically.

**Real lesson learned from this project**: hyperparameter tuning is also fragile to input errors. A single typo in the `solver` list (`'linlinear'` instead of `'liblinear'`) silently failed half the grid search fits — GridSearchCV didn't crash, it just scored those combinations as `NaN` and moved on. This produced a *worse* "best" result than what was actually possible. Always sanity-check that your grid actually ran the number of fits you expect, and watch for `FitFailedWarning` in the output.

## Best Parameters Found by GridSearchCV


*(from the corrected `Final_prediction_Pipeline.ipynb`, where the full grid ran successfully)*

## Baseline vs. Tuned Model Comparison

| Metric              | Baseline Model | Tuned Model (corrected) |
|---------------------|:--------------:|:------------------------:|
| Accuracy            | 0.9649          | **0.9825**               |
| Precision (class 0 / malignant) | 0.97 | 0.98                      |
| Recall (class 0 / malignant)    | 0.91 | 0.98                      |
| Precision (class 1 / benign)    | 0.95 | 0.99                      |
| Recall (class 1 / benign)       | 0.99 | 0.99                      |
| F1-Score (weighted avg)         | 0.96 | 0.98                      |

## Key Observations

- **Tuning improved every metric**, but the biggest jump was **recall on the malignant class** (0.91 → 0.98) — this is the most clinically important improvement, since it means fewer missed cancer cases.
- The baseline model already had perfect recall on the *benign* class (0.99–1.0) but was noticeably weaker at catching malignant cases — tuning closed that gap significantly.
- GridSearchCV selected `l1` penalty with `liblinear` solver and a relatively high `C=100` (low regularization) — meaning the tuned model benefited from being allowed to fit the training data more closely, with `l1` also performing implicit feature selection.
- **A typo in the solver name silently degraded an earlier grid search run** (`Hyperparameter_Tuning.ipynb`), causing half the parameter combinations to fail without stopping the script. This is a good reminder to check for `FitFailedWarning` messages rather than assuming a completed run means a *correct* run.
- Feature scaling was **not applied** in this version of the pipeline — since `liblinear`/`l1` still performed well, it worked here, but adding a `StandardScaler` step would likely make results more stable across solvers and is generally recommended for Logistic Regression, given how differently-scaled the raw features are (e.g. `mean area` in the hundreds/thousands vs `mean smoothness` under 1).
