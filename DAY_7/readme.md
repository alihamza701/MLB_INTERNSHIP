# Day 7 — Classification: Logistic Regression & Decision Tree

## Mini Project
Applied classification algorithms across two datasets — used the **Wine dataset** 
for the classification script, and the **Iris dataset** for the two accompanying 
tasks. Trained and evaluated both **Logistic Regression** and **Decision Tree** 
models.

## What is Classification?

Classification is a supervised machine learning technique used to predict a 
**category or class label**, rather than a continuous number. The model learns 
from labeled training data and then assigns new, unseen data points to one of a 
fixed set of classes.

Examples:
- Predicting whether a wine sample belongs to a specific quality/type class 
  (Wine dataset)
- Predicting which species a flower belongs to — Setosa, Versicolor, or 
  Virginica (Iris dataset)
- Predicting pass/fail, spam/not spam, disease/no disease

## Difference Between Regression and Classification

| Aspect | Regression | Classification |
|---|---|---|
| Output type | Continuous numeric value | Discrete category/class label |
| Example | Predicting an exam score (e.g. 78.5) | Predicting a flower species (e.g. Setosa) |
| Evaluation metrics | MSE, RMSE, R² | Accuracy, Precision, Recall, F1 Score |
| Goal | Minimize the numeric error between predicted and actual values | Correctly assign the right class label |

In short: **regression answers "how much?"**, while **classification answers 
"which category?"**

## Evaluation Metrics Used

- **Accuracy** — the proportion of total predictions the model got correct
- **Precision** — of all the samples the model predicted as a given class, how 
  many were actually that class (measures false positives)
- **Recall** — of all the samples that actually belong to a given class, how 
  many did the model correctly identify (measures false negatives)
- **F1 Score** — the harmonic mean of Precision and Recall, useful when you 
  need a single balanced metric between the two

## Model Performance and Observations

**Results (both Logistic Regression and Decision Tree, on the Iris dataset):**
- Accuracy: 1.0
- Precision: 1.0
- Recall: 1.0
- F1 Score: 1.0

**Observations:**
- Both models achieved a perfect score across every metric. Initially treated 
  this as suspicious, since a perfect 1.0 across all four metrics for two 
  different models often signals a data leakage bug rather than genuine 
  performance
- Verified this wasn't the case by checking the pipeline directly: 
  `train_test_split()` was called before any model fitting, no scaling or 
  preprocessing was applied that could leak test information into training, 
  and the test set (30 samples) had a reasonable, non-degenerate class balance 
  (11/10/9 across the three species)
- Concluded the perfect score is genuine in this specific case — Iris is a 
  small (150 rows), well-studied, near-linearly-separable dataset, and 
  achieving 100% accuracy on it is a commonly reproduced result, not unique to 
  this run
- Key lesson: a perfect score should always be verified against the pipeline 
  (split order, preprocessing, class balance) rather than accepted or rejected 
  on instinct alone — in this case verification confirmed the result was valid

## Challenges I Faced During Implementation

- Understanding the conceptual difference between regression and classification 
  metrics, and knowing which apply to which type of problem
- Learning to critically verify an unusually perfect result instead of just 
  assuming it was either automatically correct or automatically a bug — and 
  developing a concrete checklist (split order, preprocessing, test set 
  balance) to actually confirm which one it was

## Key Takeaway
Classification and regression solve fundamentally different types of 
prediction problems and require different evaluation metrics. A perfect score 
isn't inherently wrong — on small, clean datasets like Iris it can be entirely 
genuine — but it's worth verifying the pipeline (train-test split order, 
preprocessing steps, and test set class balance) before trusting it, rather 
than assuming either success or a hidden bug.
