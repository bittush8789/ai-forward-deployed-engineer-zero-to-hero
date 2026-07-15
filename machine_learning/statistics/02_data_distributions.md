# Module 2: Data Distribution (Practical ML Focus)

In Machine Learning, we don't just care about summary metrics; we care about the *shape* of the data. The probability distribution of a feature determines how models interpret it and whether our mathematical assumptions hold true.

---

## 1. Concept Explanation

### The Normal (Gaussian) Distribution
The Normal distribution is a bell-shaped, symmetric distribution where the mean, median, and mode are all equal. It is defined by its mean ($\mu$) and standard deviation ($\sigma$).
* **The Empirical Rule (68-95-99.7 Rule)**:
  - **68.2%** of the data falls within $\pm 1\sigma$ of the mean.
  - **95.4%** of the data falls within $\pm 2\sigma$ of the mean.
  - **99.7%** of the data falls within $\pm 3\sigma$ of the mean.
  
Any value beyond $\pm 3\sigma$ in a truly normal distribution is highly rare ($< 0.3\%$ probability) and often treated as an anomaly.

### Skewness
Skewness measures the asymmetry of a distribution around its mean.
* **Symmetrical Distribution**: Skewness is near 0.
* **Positive (Right) Skew**: The tail on the right side of the distribution is longer/fatter. The mean is typically greater than the median (e.g., income, asset prices).
* **Negative (Left) Skew**: The tail on the left side is longer/fatter. The mean is typically less than the median (e.g., age of retirement, death rates).

### Kurtosis
Kurtosis measures the "tailedness" of a distribution, indicating the presence of extreme values or outliers.
* **Mesokurtic (Kurtosis ≈ 0)**: Normal distribution.
* **Leptokurtic (Kurtosis > 0 / "Heavy-tailed")**: Tall, thin peak with fat tails. This indicates a high probability of extreme values (outliers), common in financial returns.
* **Platykurtic (Kurtosis < 0 / "Light-tailed")**: Flat, wide peak with thin tails. Indicates fewer extreme outliers.

---

## 2. Why It Matters in ML

1. **Model Assumptions**: Algorithms like Linear Regression, Logistic Regression, and LDA assume that residuals (errors) are normally distributed.
2. **Feature Transformations**: Highly skewed features can degrade linear and distance-based model performance (e.g., KNN, K-Means). We apply transformations like Logarithm ($\log(x)$), Square Root ($\sqrt{x}$), or Box-Cox/Yeo-Johnson to force highly skewed distributions to look more normal.
3. **Anomaly Detection**: In cybersecurity or infrastructure monitoring, we model normal behavior as a Gaussian distribution. Production data points that fall outside the $\pm 3\sigma$ range are flagged as anomalies.
4. **Target Variable Conditioning**: If your target variable $y$ is highly skewed (e.g., insurance claim values), predicting it directly can result in massive errors on high-value points. Predicting $\log(y)$ instead stabilizes model gradients.

---

## 3. Business Example

**Scenario**: An HR analytics platform needs to identify salary inequities and detect anomalous compensation packages for an enterprise client.
* **The Problem**: Employee salaries are typically right-skewed. Executives make $500,000+ while mid-level staff make $70,000. Running simple regression models to predict salary based on performance indicators will perform poorly on standard staff due to the leverage of executive outliers.
* **The Solution**:
  1. Measure skewness. If skewness $> 1.0$, apply a logarithmic transformation to the salary column.
  2. The log-transformed salary follows a normal distribution, stabilizing the regression weights.
  3. Predictions are made in the log space and then back-transformed ($e^{\hat{y}}$) to standard currency values.

---

## 4. Dataset Example

A company's salary structure before and after a log-transform shows how skewness is compressed:

| Employee ID | Department | Base Salary ($) | $\log(\text{Salary})$ |
|-------------|------------|-----------------|----------------------|
| E_101       | Dev        | 85,000.00       | 11.35                |
| E_102       | QA         | 70,000.00       | 11.15                |
| E_103       | Support    | 55,000.00       | 10.91                |
| E_104       | CEO        | 750,000.00      | 13.52                |
| E_105       | Dev        | 92,000.00       | 11.42                |

The raw salary ratio between CEO and Support is **13.6x**. In log space, the ratio is compressed to **1.2x**, removing the disproportionate leverage of extreme values.

---

## 5. Python Example

```python
import numpy as np
import pandas as pd
import scipy.stats as stats

# 1. Create a right-skewed salary dataset (Log-Normal Distribution)
np.random.seed(42)
raw_salaries = np.random.lognormal(mean=11.2, sigma=0.6, size=500)
df = pd.DataFrame({"salary": raw_salaries})

# 2. Analyze Shape Metrics
raw_skew = df["salary"].skew()
raw_kurt = df["salary"].kurtosis()

print(f"Raw Salary - Skewness: {raw_skew:.2f} (Right-skewed if > 1.0)")
print(f"Raw Salary - Kurtosis: {raw_kurt:.2f} (Heavy-tailed if > 3.0)\n")

# 3. Apply Log Transformation to normalize distribution
df["log_salary"] = np.log(df["salary"])

log_skew = df["log_salary"].skew()
log_kurt = df["log_salary"].kurtosis()

print(f"Log Salary - Skewness: {log_skew:.2f} (Symmetric if near 0.0)")
print(f"Log Salary - Kurtosis: {log_kurt:.2f} (Normal if near 0.0)")

# 4. Outlier detection in Normalized Space (Z-Score method)
df["z_score"] = (df["log_salary"] - df["log_salary"].mean()) / df["log_salary"].std()
anomalies = df[np.abs(df["z_score"]) > 3.0]
print(f"\nNumber of salary anomalies found via 3-sigma rule: {len(anomalies)}")
```

---

## 6. Mini Project Context: Employee Salary Distribution Analysis

In `projects/project2_house_prices/`, you will analyze feature distributions and apply transformations. For salaries, the logic is identical. 
In the visualizations:
- Highly skewed distributions will show a long right tail in histograms.
- After log transformations, the distribution takes a clean bell curve.

---

## 7. Interview Questions

1. **What is the difference between positive skewness and negative skewness? Draw/describe their tails.**
   *Answer*: Positive skewness is right-skewed, meaning the distribution has a long tail pointing to the right (larger values). The mean is pulled toward the right tail and is usually greater than the median. Negative skewness is left-skewed, meaning the tail points to the left (smaller values), pulling the mean below the median.
2. **If your model is a decision tree, do you need to log-transform highly skewed features? Why?**
   *Answer*: No. Tree-based models (like Decision Trees, Random Forests, XGBoost) split features based on ordering (rank) rather than numerical distance or scale. They are completely invariant to monotonic transformations like logarithms. Feature transformation is primarily necessary for linear models, neural networks, support vector machines, and distance-based clustering (K-Means).
3. **What does a high kurtosis tell you about the risk of a model?**
   *Answer*: High kurtosis (leptokurtic) means the data has heavy tails, indicating that extreme events occur far more frequently than would be expected under a normal distribution. In financial risk forecasting or predictive maintenance, models that assume normality will severely underestimate the frequency of these catastrophic failures.

---

## 8. Common Mistakes

- **Assuming all data must be normal**: Do not transform features blindly. Check the model type first. Linear/distance models benefit from normalized features; trees do not.
- **Log-transforming zero or negative numbers**: The logarithm of zero or negative numbers is undefined. If a feature contains zeros, use $\log(x + 1)$ (known as `np.log1p`) or a Yeo-Johnson transform.
- **Forgetting to invert the target variable prediction**: If you log-transform the target variable $y$ before training, your model will predict $\log(y)$. You *must* take the exponential of the predictions ($e^{\hat{y}}$) to report the final metrics to the business stakeholders.

---

## 9. Production Usage & MLOps

In production, models can fail silently if user input distributions change.
* **Drift Detection**: Run statistical tests like the **Kolmogorov-Smirnov (KS) test** weekly to compare the distribution of inference inputs against the training baseline. If the distributions differ significantly (p-value < 0.05), trigger an alert to retrain the model.

---

## 10. AI FDE Perspective

In client engagements, you will often build forecasting systems for sales, demand, or cloud usage. Clients will expect simple averages to work, but enterprise demand is heavily skewed (e.g., massive spikes on Black Friday). 

Always map out skewness and kurtosis in your initial data profiling reports. If client data is highly kurtotic, advise them against linear regression models, and propose models designed for heavy tails or extreme value theory, positioning yourself as an architect rather than just an implementation engineer.
