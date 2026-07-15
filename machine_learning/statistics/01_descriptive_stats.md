# Module 1: Descriptive Statistics (Practical ML Focus)

Descriptive statistics is the art of summarizing and describing the key characteristics of a dataset. As a Machine Learning Engineer or AI Forward Deployed Engineer (FDE), you cannot train robust models without first understanding the scale, central tendencies, and variability of your data.

---

## 1. Concept Explanation

Descriptive statistics are split into two main categories:
1. **Measures of Central Tendency**: Where is the "center" of the data?
2. **Measures of Dispersion (Spread)**: How spread out are the data points around that center?

### Central Tendency
- **Mean (Average)**: The sum of all values divided by the number of values. Highly sensitive to extreme values (outliers).
  $$\mu = \frac{1}{N} \sum_{i=1}^{N} x_i$$
- **Median**: The middle value when the dataset is ordered from smallest to largest. If the size is even, it is the average of the two middle values. Highly robust to outliers.
- **Mode**: The most frequently occurring value in the dataset. Useful for categorical data or discrete numerical counts.

### Dispersion
- **Variance ($\sigma^2$)**: The average of the squared differences from the mean. It measures the overall spread.
  $$\sigma^2 = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2$$
- **Standard Deviation ($\sigma$)**: The square root of the variance. It is in the same unit as the original data, making it highly interpretable.
  $$\sigma = \sqrt{\sigma^2}$$
- **Percentiles**: The value below which a percentage of data falls. For example, the 90th percentile is the value greater than 90% of the data points.
- **Quartiles**: Values that divide the data into four equal parts:
  - **Q1 (25th Percentile)**: First quartile.
  - **Q2 (50th Percentile)**: Second quartile (Median).
  - **Q3 (75th Percentile)**: Third quartile.
- **Interquartile Range (IQR)**: The distance between the 75th and 25th percentiles.
  $$\text{IQR} = Q3 - Q1$$
  IQR is the basis for the classical Tukey box-plot outlier detection rule: any value below $Q1 - 1.5 \times \text{IQR}$ or above $Q3 + 1.5 \times \text{IQR}$ is labeled an outlier.

---

## 2. Why It Matters in ML

1. **Feature Scale**: Models like Linear Regression, Support Vector Machines (SVM), and Neural Networks are highly sensitive to the scale of features. Standard deviation and variance help us decide if standard scaling (Z-score normalization) is needed.
2. **Loss Function Design**: Understanding dispersion guides your choice of loss functions. For instance, Mean Absolute Error (MAE) optimizes for the median, while Mean Squared Error (MSE) optimizes for the mean.
3. **Outlier Mitigation**: Linear models can be severely skewed by outliers. Detecting them using the IQR method allows us to clip, impute, or drop extreme values before training.
4. **Data Quality Checks**: If your data's mean or standard deviation shifts dramatically between training and production, it indicates **data drift**, which will degrade model performance.

---

## 3. Business Example

**Scenario**: A fintech client wants to build a credit risk scoring model. They provide customer monthly credit card transaction values.
* **The Problem**: A few wealthy customers spend $1,000,000/month, while the average customer spends $1,500/month.
* **The Solution**:
  * Using the **Mean** to represent "typical" customer spending yields $8,500/month (skewed by the high spenders).
  * Using the **Median** yields $1,450/month (a realistic representation of the target audience).
  * Identifying the outliers using the **IQR method** allows the credit scoring model to place these extreme high-value transactions into a separate high-net-worth segment rather than letting them skew the default probability model.

---

## 4. Dataset Example

Let's look at a typical tabular representation of customer transactions in an enterprise database:

| Customer ID | Age | Monthly Spend ($) | Transaction Count | Tier |
|-------------|-----|-------------------|-------------------|------|
| C_001       | 28  | 450.00            | 12                | Free |
| C_002       | 42  | 2300.00           | 45                | Gold |
| C_003       | 35  | 120.00            | 3                 | Free |
| C_004       | 51  | 145000.00         | 188               | Plat |
| C_005       | 22  | 95.00             | 8                 | Free |

In this dataset, Customer `C_004` represents a classic spending outlier ($145,000.00).

---

## 5. Python Example

Here is how you analyze this data using **NumPy** and **Pandas** to detect outliers and inspect central tendencies.

```python
import numpy as np
import pandas as pd

# 1. Create simulated customer spend data
data = {
    "customer_id": ["C_001", "C_002", "C_003", "C_004", "C_005", "C_006", "C_007", "C_008"],
    "monthly_spend": [450.0, 2300.0, 120.0, 145000.0, 95.0, 500.0, 600.0, 750.0]
}
df = pd.DataFrame(data)

# 2. Compute central tendencies
mean_spend = df["monthly_spend"].mean()
median_spend = df["monthly_spend"].median()
mode_spend = df["monthly_spend"].mode()[0]

print(f"Mean Spend: ${mean_spend:,.2f}")      # Output: $18,726.88 (highly skewed)
print(f"Median Spend: ${median_spend:,.2f}")  # Output: $550.00 (representative)
print(f"Mode Spend: ${mode_spend:,.2f}")      # Output: $95.00 (first value)

# 3. Compute dispersion metrics
variance_spend = df["monthly_spend"].var()
std_dev_spend = df["monthly_spend"].std()
q1 = df["monthly_spend"].quantile(0.25)
q3 = df["monthly_spend"].quantile(0.75)
iqr = q3 - q1

print(f"\nStandard Deviation: ${std_dev_spend:,.2f}")
print(f"IQR: ${iqr:,.2f}")

# 4. Tukey's outlier detection rule
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[(df["monthly_spend"] < lower_bound) | (df["monthly_spend"] > upper_bound)]
clean_df = df[(df["monthly_spend"] >= lower_bound) & (df["monthly_spend"] <= upper_bound)]

print(f"\nOutlier Threshold: Spend > ${upper_bound:,.2f} or Spend < ${lower_bound:,.2f}")
print("Detected Outliers:")
print(outliers)
```

---

## 6. Mini Project Context: Customer Spending Analysis

In the hands-on project located in `projects/project1_customer_spending/`, you will build a production-like pipeline that:
1. Generates 1,000 transaction records with realistic spending profiles (log-normal distribution) and explicit outliers.
2. Implements descriptive metrics calculations from scratch to build your intuition.
3. Automatically generates an outlier report and cleanses the dataset.
4. Generates box plots and distribution charts to visualize the outliers.

---

## 7. Interview Questions

1. **Why is the median preferred over the mean in datasets with high skewness, like household incomes?**
   *Answer*: The mean incorporates every value in the calculation. A single extremely high value (e.g., a billionaire in a small town) will drag the mean upwards, misrepresenting the average resident. The median, being the positional middle value, is unaffected by extreme values on either tail.
2. **What is the mathematical relation between standard deviation and variance? Why do we use both?**
   *Answer*: Variance is the average squared distance from the mean, whereas standard deviation is the square root of variance. We use variance in mathematical optimization (it has clean derivative properties), but we use standard deviation for reporting because it shares the same unit as the original features (e.g., dollars instead of dollars-squared).
3. **If a feature has a variance of 0, what does it mean for your machine learning model?**
   *Answer*: A variance of 0 means all data points have the exact same value. In machine learning, this feature contains no information (entropy is 0) and has no predictive power. It should be removed during feature selection to reduce model dimensionality and training time.

---

## 8. Common Mistakes

- **Treating outliers as noise to always be deleted**: Sometimes outliers are the most valuable data points (e.g., cyber attacks, fraud transactions, equipment failures). Never delete outliers blindly without checking the business domain context.
- **Reporting only the mean**: Reporting a single "average revenue" to stakeholders without mentioning the standard deviation or range can hide the fact that a few accounts generate 99% of the revenue, introducing massive business concentration risk.
- **Confusing Sample vs. Population Variance**: In Python, `pandas.var()` defaults to *sample variance* (divides by $N-1$, known as Bessel's correction), while `numpy.var()` defaults to *population variance* (divides by $N$). This mismatch can lead to unit testing failures.

---

## 9. Production Usage & MLOps

In production pipelines:
- **Data Validation**: Tools like **Great Expectations** use descriptive statistics to validate incoming data. You can set rules like: `expect_column_mean_to_be_between("monthly_spend", min_value=100, max_value=2500)`.
- **Model Drift Monitoring**: By scheduling daily cron jobs to compute the median and standard deviation of inferred features, you can detect when production user behaviors deviate from what the model saw during training.

---

## 10. AI FDE Perspective

As an AI Forward Deployed Engineer, you will often receive un-curated datasets from enterprise clients containing corrupted strings, database anomalies, and human entry errors. 

Before running any algorithms, your first deliverable during client discovery workshops should always be a descriptive statistics dashboard. Showing the client that 5% of their transaction amounts are negative or that their "User Age" column has a maximum value of 999 builds immediate technical trust and aligns assumptions early in the deployment process.
