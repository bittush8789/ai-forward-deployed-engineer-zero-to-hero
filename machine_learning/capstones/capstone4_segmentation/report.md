# Capstone 4 Report: Customer Segmentation Engine

## 🎯 Executive Summary
In this project, we designed and built an **unsupervised customer segmentation system** using K-Means Clustering and Principal Component Analysis (PCA). 

To ensure distance calculations were balanced, customer behavioral features (purchase frequency, basket size, return rate) were standardized. 

The K-Means algorithm identified **3 distinct buyer personas**, validated by a high **Silhouette Score of 0.735**. To make these high-dimensional segments visible, we used PCA to project features into a 2D space, explaining **94.8% of the total variance**.

---

## 🛠️ Skills Covered
- **Standardized Clustering**: Preprocessing features for K-Means Euclidean distance inputs.
- **Dimensionality Reduction**: Applying PCA to project multi-variable vectors onto 2 principal components.
- **Cluster Diagnostics**: Evaluating groupings using Silhouette Scores.
- **Persona Profiling**: Translating cluster mathematical averages into business-actionable definitions.

---

## 📈 Methodology & Formulas

### 1. K-Means Centroid Allocation
Data points are iteratively assigned to cluster $S_i$ by minimizing the sum of squared distances to the centroid $\mu_i$:
$$\arg\min_{S} \sum_{i=1}^{k} \sum_{x \in S_i} ||x - \mu_i||^2$$

### 2. PCA Dimension Compression
PCA finds eigenvectors of the covariance matrix. 2D coordinates are projected onto the first two eigenvectors (explaining the highest variance), allowing high-dimensional segments to be visualized on standard scatter plots.

---

## 📊 Results Summary

### 1. Cohort Profile Groupings (Mean Values)

| Cluster ID | Segment Label | Count | Purchase Frequency | Avg Basket ($) | Return Rate |
|---|---|---|---|---|---|
| **Cluster 0** | Bargain Hunters | 150 | 34.62 | \$24.81 | 35.3% |
| **Cluster 1** | VIP Clients | 75 | 5.86 | \$442.21 | 3.0% |
| **Cluster 2** | Average Shoppers | 75 | 14.89 | \$109.11 | 9.9% |

### 2. PCA Diagnostic Report
- **PC1 Explained Variance**: **68.22%**
- **PC2 Explained Variance**: **26.62%**
- **Total Variance Explained**: **94.84%**
- **Silhouette Coefficient**: **0.7348** (Indicates well-separated clusters with minimal overlap).

---

## 💼 Business Outcomes
1. **Differentiated Landing Pages**: 
   - Route **Cluster 0 (Bargain Hunters)** visitors to discount and sale headers.
   - Route **Cluster 1 (VIP Clients)** visitors to luxury, high-end collection banners.
2. **Optimized Logistics and Returns**: Target **Cluster 0** (35.3% return rate) with return warning messages during checkout to reduce shipping overhead.
3. **Sales Representative Targeting**: CRM dashboards can flag Cluster 1 users for early-access outreach by sales reps, maximizing high-value customer lifetime value.
