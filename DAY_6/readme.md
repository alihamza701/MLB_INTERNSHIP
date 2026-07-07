# Day 6 — Student Performance: Regression Model

## Mini Project
Built on the Student Performance Analysis dataset from Day 4, this time training 
a regression model to predict a student's exam score as a numeric value, based 
on other features in the dataset.

## 📹 Explanation Recording

A walkthrough explaining this project — the preprocessing steps, train-test 
split, model training, and evaluation results — is available here:

🔗 [Watch the explanation recording](https://drive.google.com/drive/folders/1HeTusTf-8DBT7INl9IcBGVjB9ihceu5C?usp=sharing
)

## What I Learned About Data Preprocessing

- Machine learning models can't work directly with text/categorical data (like 
  gender or grade level) — these need to be converted into numeric form before 
  they can be fed into a model
- Used **encoding** to convert categorical columns (e.g. gender, grade) into 
  numeric representations:
  - **Label Encoding** — assigns each category a number (e.g. Male → 0, Female → 1)
  - **One-Hot Encoding** — creates a separate binary column for each category, 
    avoiding the model wrongly assuming an order/ranking between categories
- Learned that choosing the wrong encoding method can introduce bias — for 
  example, Label Encoding a column with no natural order (like grade names) can 
  make the model incorrectly assume one category is "greater than" another

## Why Train-Test Splitting Is Important

- Splitting the dataset into a **training set** and a **test set** lets you 
  evaluate the model on data it has never seen before, rather than just 
  memorizing the training data
- Without this split, a model could achieve a very high score on the data it 
  was trained on but still fail badly on new, unseen students — this is called 
  **overfitting**
- A typical split (e.g. 80% train / 20% test) balances giving the model enough 
  data to learn patterns, while still holding back enough data to fairly judge 
  how well it generalizes
- Used `train_test_split()` from `sklearn.model_selection` to perform this split

## Evaluation Metrics Used

Since this was a **regression** problem (predicting a continuous exam score, 
not a category), classification metrics like accuracy don't apply. Instead, 
used regression-specific metrics:

- **Mean Squared Error (MSE)** — average of the squared differences between 
  predicted and actual scores; penalizes larger errors more heavily
- **Root Mean Squared Error (RMSE)** — square root of MSE, brought back into 
  the same unit as the original scores (marks), making it easier to interpret
- **R² Score (Coefficient of Determination)** — indicates how much of the 
  variation in exam scores the model explains; closer to 1 means a better fit

## My Model's Performance and Observations

- *(Fill in your actual numbers here once you run the model, e.g.:)*
  - MSE: `___`
  - RMSE: `___`
  - R² Score: `___`
- Observed that [note here whether predictions were close to actual scores, 
  or whether certain students' scores were consistently over/under-predicted]
- [Note here if any single feature seemed to influence predictions the most — 
  e.g. did encoded gender or grade seem to matter much, or did numeric subject 
  scores dominate the prediction?]

## Challenges I Faced During Implementation

- Deciding between Label Encoding and One-Hot Encoding for categorical columns, 
  and understanding when each is appropriate
- Making sure the train-test split was applied *after* encoding, so both sets 
  had features in the same numeric format
- Interpreting regression metrics correctly — unlike classification accuracy, 
  MSE/RMSE values don't have a fixed "good" threshold and need to be judged 
  relative to the scale of the target variable (exam scores out of 100)

## Key Takeaway
Encoding categorical data correctly and splitting data before training are both 
essential steps that directly affect whether a model's evaluation results can 
be trusted — skipping either one can make a model look better (or worse) than 
it actually is.
