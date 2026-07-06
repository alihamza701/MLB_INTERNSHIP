# 📊 Student Performance Analysis using Python

## Overview

This project focuses on analyzing a student performance dataset using **Python**, **Pandas**, and **Matplotlib**. The objective was to clean the dataset, perform exploratory data analysis (EDA), create meaningful visualizations, and extract useful insights about student performance.

---

## Data Cleaning Steps Performed

The following preprocessing and data cleaning tasks were completed before performing the analysis:

* Identified and handled missing (null) values in multiple columns.
* Removed duplicate student records to improve data quality.
* Renamed columns to make them more descriptive and easier to use.
* Calculated a new **Average_Score** column by averaging the marks obtained in all subjects.
* Created a **Performance** column based on the average score using the following categories:

  * Excellent (≥ 90)
  * Good (80–89)
  * Average (70–79)
  * Needs Improvement (< 70)
* Verified the data types of all columns before analysis.
* Saved the cleaned dataset for future analysis.

---

## Data Visualizations Created

Several visualizations were created to better understand the dataset:

### 1. Bar Chart

* Displayed the average score of each student.
* Also used to visualize the top-performing students.
* Purpose: To compare student performance easily.

### 2. Histogram

* Displayed the distribution of students' average scores.
* Purpose: To understand how student scores are distributed and identify concentration ranges.

### 3. Scatter Plot

* Compared **Python** marks with **Machine Learning** marks.
* Purpose: To identify whether students who performed well in Python also performed well in Machine Learning.

### 4. Pie Chart

* Visualized the distribution of students across different performance categories.
* Purpose: To understand the proportion of Excellent, Good, Average, and Needs Improvement students.

### 5. Box Plot

* Displayed the distribution of marks across all subjects.
* Purpose: To identify the spread of marks and detect potential outliers.

---

## Key Insights

### 1. Most students performed satisfactorily.

The majority of students were classified as **Pass**, with relatively fewer students falling into the **Needs Improvement** category, indicating an intentionally imbalanced dataset.

### 2. Positive relationship between technical subjects.

The scatter plot suggested that students scoring higher in **Python** generally also achieved higher marks in **Machine Learning**, indicating a positive relationship between the two subjects.

### 3. Presence of outliers and data quality issues.

The dataset contained missing values, duplicate records, and several outliers. Cleaning these issues was necessary before conducting reliable analysis and visualization.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib

---

## Learning Outcomes

Through this project, I gained practical experience in:

* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* Feature engineering
* Data visualization using Matplotlib
* Extracting insights from real-world datasets
* Working with structured datasets using Pandas
