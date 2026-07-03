# Day 4 — Student Performance Analysis (Mini Project)

## Mini Project
Performed exploratory data analysis on a student performance dataset containing 
marks across multiple subjects, using Pandas and NumPy to load, analyze, and 
export the results.

## What I Learned About NumPy

- How NumPy underpins Pandas — Series and DataFrame columns are built on NumPy 
  arrays under the hood, which is why vectorized operations (like summing across 
  columns) are so much faster than manual loops
- Generating realistic numeric data using `np.random.normal()` for a natural, 
  skewed distribution — instead of `np.random.randint()`, which produces a flat, 
  unrealistic uniform spread
- Using `np.clip()` to keep generated values within a valid range (e.g. marks 
  between 0–100)
- Selecting random indices with `np.random.choice()` to inject controlled outliers 
  (a few weak and a few exceptional scorers) into a dataset

## What I Learned About Pandas

- Loading data with `pd.read_csv()` and inspecting it using `.head()`, `.shape`, 
  `.describe()`, and `.columns`
- The difference between `df.iloc[]` (position-based indexing) and `df.loc[]` 
  / direct column selection (label-based) — mixing these up causes errors
- Filtering rows with multiple conditions requires wrapping **each condition in 
  its own parentheses** and using `&` instead of `and`:
```python
  df[(df['Name'] == 'Ali') & (df['Score'] > 50)]
```
- Calculating column-wise and row-wise aggregates using `.sum(axis=1)`, `.mean()`
- Sorting and selecting top-N rows using `.sort_values()` and `.head()`, instead 
  of manually looping and tracking indices
- Saving processed results with `.to_csv("filename.csv", index=False)`

## Key Insights I Found From the Dataset

- Subject averages varied meaningfully once the dataset had a realistic, skewed 
  distribution instead of a uniform one — English had the highest average score, 
  while Science had the lowest
- Only a small number of students accounted for the lowest scores (below 40), 
  confirming the dataset had genuine low-performing outliers rather than an 
  evenly spread population
- The top 5 performing students were consistent across subjects, suggesting 
  strong overall performers rather than students who excelled in just one subject
- A meaningful number of students scored below the class average, which is 
  expected in any normal-ish distribution — roughly half the class should fall 
  below the mean when the data isn't artificially uniform

## Challenges I Faced During Implementation

- **Uniform vs. realistic data:** My first version of the dataset used random 
  integers, giving a flat/uniform distribution with no meaningful "top" or 
  "below average" students. Fixed by generating scores from a normal distribution 
  with injected outliers instead
- **Task Understanding:** Today few tasks were confusing me , so i had to ask my mentor for the clarification
  ,that helped me to step on to next task quickly.
- **Boolean filtering errors:** Wrote conditions like 
  `df[df['Name'] == 'x' & df['Score'] > 50]` without wrapping each condition in 
  parentheses — Python's operator precedence tried to evaluate `&` before the 
  comparisons, causing a `TypeError`
- **Incorrect indexing:** Tried using `df[y, 2:6]` to select rows/columns by 
  position, which isn't valid Pandas syntax — needed `.iloc[y, 2:6]` instead
- **Dictionary logic errors:** Tried to `.update()` a dictionary key that didn't 
  exist yet (`summation[x].update(...)`), and tried to slice a dictionary like a 
  list (`summation[0:4]`) — dictionaries aren't ordered/sliceable the way lists 
  are, so I had to convert to a sorted list of tuples first, or better, let 
  Pandas handle sorting natively with `.sort_values()`
- **Reinventing what Pandas already does:** Initially wrote manual loops to sum 
  and sort values, which was slower and more error-prone than using Pandas' 
  built-in vectorized methods (`.sum(axis=1)`, `.sort_values()`, `.head()`)

## Key Takeaway
Pandas and NumPy provide vectorized, built-in methods for almost every common 
data operation — looping manually with tracked indices is usually a sign there's 
a cleaner, faster, less bug-prone Pandas equivalent available.
