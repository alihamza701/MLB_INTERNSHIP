# Day 9 — Iris Flower Clustering & Visualization

Unsupervised learning on the **Iris Dataset** (built into Scikit-learn) using K-Means clustering and PCA, with visual comparison against the true flower species.

## What is Clustering?

Clustering is an **unsupervised learning** technique that groups data points based purely on similarity in their feature values — without using any labels. The algorithm doesn't know which flower is which species; it only sees the 4 numeric measurements (sepal length/width, petal length/width) and groups flowers that are close together in that 4-dimensional space.

**K-Means** specifically works by:
1. Picking `k` random cluster centers (centroids).
2. Assigning every point to its nearest centroid.
3. Recalculating each centroid as the mean of the points assigned to it.
4. Repeating steps 2–3 until the assignments stop changing.

The result is `k` groups where points within a group are more similar to each other than to points in other groups.

## What is PCA?

**Principal Component Analysis (PCA)** is a dimensionality-reduction technique. It takes a dataset with many features (here, 4) and finds new axes — **principal components** — that capture the maximum possible variance in the data, ordered by importance. By keeping only the top 2 components, we can compress a 4D dataset into a 2D one that's easy to plot, while retaining as much of the original information (variance) as possible.

Importantly, PCA is **not** a clustering method — it doesn't group anything. It's purely a way to compress and visualize high-dimensional data.

## How Did I Determine the Best Value of K?

I used the **Elbow Method**: K-Means was run for `k = 1` through `10`, recording the **inertia** (within-cluster sum of squared distances) at each step. Plotting inertia against `k` shows a sharp drop from `k=1` to `k=3`, after which the curve flattens out significantly — this bend ("elbow") indicates diminishing returns from adding more clusters beyond that point.

Based on the elbow at **k=3**, I chose 3 clusters — which also conveniently matches the known number of Iris species (setosa, versicolor, virginica), even though K-Means never saw those labels.

## Results

**Explained variance from PCA:** PC1 = 72.96%, PC2 = 22.85% → **95.81% of total variance retained in just 2 dimensions.**

**Cluster vs. true species crosstab:**

| Species     | Cluster 0 | Cluster 1 | Cluster 2 |
|-------------|:---------:|:---------:|:---------:|
| setosa      | 0         | **50**    | 0         |
| versicolor  | **39**    | 0         | 11        |
| virginica   | 14        | 0         | **36**    |

## Visualizations

**1. K-Means Clusters** (Petal Length vs Petal Width, colored by assigned cluster):

**2. PCA-Transformed Data** (colored by true species):

**3. Side-by-side comparison** — original features (true species) vs. K-Means clusters vs. PCA-transformed data:

## Insights From the Visualizations

**How many clusters were formed?**
3 — matching both the elbow method's suggestion and the true number of Iris species.

**Did the clusters represent the flower species well?**
Very well for *setosa* — it forms a perfectly isolated cluster (50/50, zero overlap), because its petal measurements are distinctly smaller than the other two species. *Versicolor* and *virginica* overlap somewhat: 25 of the 150 flowers get assigned to the "wrong" cluster relative to their true species, since these two species are genuinely close together in petal length/width — K-Means has no species labels to fall back on, so it draws the boundary purely on geometric distance.

**How did PCA help in visualization?**
PCA compressed 4 features into 2 while keeping 95.81% of the original variance — enough to plot the entire dataset on a single 2D scatter plot without significant information loss. Comparing the PCA plot to the plot using real petal measurements shows the same overall structure (one well-separated group, two overlapping groups) — confirming that PCA preserved the meaningful patterns in the data rather than distorting them. This makes PCA especially useful when a dataset has more than 2–3 features and can't be visualized directly.

## Project Structure

```
Day-9/
├── dataset_exploration.py
├── kmeans_clustering.py
├── pca_script.py
├── mini_project_iris_clustering.py
├── elbow_method.png
├── kmeans_clusters.png
├── pca_visualization.png
├── comparison_plots.png
├── iris_with_clusters.csv
└── README.md
```
