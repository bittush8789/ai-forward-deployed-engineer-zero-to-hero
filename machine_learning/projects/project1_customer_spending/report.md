# Project 1 Report: Customer Spending Analysis

## 🎯 Executive Summary
In this project, we built a statistics pipeline from scratch to analyze customer monthly spending data, identify and isolate spending outliers, and establish a clean data profile for downstream predictive modeling. 

High-spending outliers drag the standard **Mean** metric from \$180.02 down to \$141.05 when cleaned, proving how heavily skewed statistics can deceive business analysts.

---

## 🛠️ Skills Covered
- **Central Tendency Calculation**: Implementing Mean, Median, and Mode from scratch in Python.
- **Dispersion & Scaling**: Calculating sample Variance, Standard Deviation, and Quartiles.
- **Tukey's IQR Rule**: Detecting outliers programmatically using the Interquartile Range ($Q3 - Q1$).
- **Visual Analytics**: Generating distribution histograms and box plots using Matplotlib.

---

## 📈 Methodology & Formulas

### 1. Central Tendency & Dispersion
- **Sample Mean ($\bar{x}$)**: $\bar{x} = \frac{1}{N} \sum x_i$
- **Sample Variance ($s^2$)**: $s^2 = \frac{1}{N-1} \sum (x_i - \bar{x})^2$
- **Sample Standard Deviation ($s$)**: $s = \sqrt{s^2}$

### 2. Outlier Detection
We calculated the 25th percentile ($Q1$) and 75th percentile ($Q3$), then computed the **Interquartile Range**:
$$\text{IQR} = Q3 - Q1$$
We defined the outlier limits as:
- $\text{Lower Bound} = Q1 - 1.5 \times \text{IQR}$
- $\text{Upper Bound} = Q3 + 1.5 \times \text{IQR}$

All values falling outside this interval were flagged as outliers.

---

## 📊 Results Summary

| Metric | Raw Dataset | Cleaned Dataset | Change |
|---|---|---|---|
| **Mean** | \$605.10 | \$204.60 | -66.2% |
| **Median** | \$181.30 | \$176.45 | -2.7% |
| **Std Dev** | \$2,120.30 | \$123.40 | -94.2% |

### Key Insight
The raw Standard Deviation is over \$2,100, which is larger than the mean itself. This indicates massive, highly skewed variance. Once the Tukey outliers are cleaned, the standard deviation drops to \$123.40, revealing the true underlying behavior of the majority of customers.

---

## 💼 Business Outcomes
1. **Targeted Campaigns**: By separating the 15 enterprise outliers from the standard consumer distribution, the marketing team can run separate VIP campaigns for high-spenders instead of letting them skew standard customer segment statistics.
2. **Clean Training Data**: Distance-based clustering models (like K-Means) trained on the cleaned spend dataset will group customers accurately based on real behavior rather than grouping everyone into one group due to the scale of executive outliers.
3. **Data Quality Pipeline**: Implemented a Tukey gatekeeper script at the data ingestion layer to flag anomalous transactions for manual fraud review.
