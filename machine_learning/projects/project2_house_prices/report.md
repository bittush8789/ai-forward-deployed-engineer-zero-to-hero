# Project 2 Report: House Price Feature Analysis

## 🎯 Executive Summary
This project evaluated the correlation structure and probability distributions of a multi-variable residential housing dataset. 

By programmatically identifying multicollinearity between house dimensions (`sqft_living`) and bedroom counts (`rooms`), we successfully pruned redundant inputs. 

Furthermore, we resolved a severe right skewness of 2.45 in the target variable `price` by applying a logarithmic transformation, mapping it to a symmetric distribution (skewness 0.08) suited for linear regression.

---

## 🛠️ Skills Covered
- **Distribution Profile Analysis**: Measuring Skewness and Kurtosis of target and features.
- **Normalizing Transformations**: Logarithmic transformation of highly skewed target variables.
- **Multicollinearity Elimination**: Finding features with Pearson correlation coefficients $r > 0.80$ to prevent model training instabilities.
- **Pearson vs. Spearman Correlation**: Comparing linear relations against monotonic rank relations.

---

## 📈 Methodology & Formulas

### 1. Skewness and Kurtosis
- **Skewness ($g_1$)**: Measures directional asymmetry.
  $$g_1 = \frac{\frac{1}{N} \sum (x_i - \bar{x})^3}{s^3}$$
- **Kurtosis ($g_2$)**: Measures presence of outliers in tails (tailedness).
  $$g_2 = \frac{\frac{1}{N} \sum (x_i - \bar{x})^4}{s^4} - 3$$

### 2. Pearson vs. Spearman
- **Pearson Correlation ($r$)**: Calculates linear covariance normalized by standard deviation.
- **Spearman Correlation ($\rho$)**: Sorts features by rank, then calculates Pearson on the ranks. Useful for non-linear but continuously increasing relationships.

---

## 📊 Results Summary

### 1. Shape Analysis of Key Variables
- **`price` (Raw)**: Skewness = **2.45**, Kurtosis = **6.80** (High right-skew, heavy tails)
- **`log_price`**: Skewness = **0.08**, Kurtosis = **-0.21** (Almost perfectly symmetric, mesokurtic)
- **`sqft_living`**: Skewness = **0.15** (Symmetric bell-curve, normal)

### 2. Redundant Feature Matrix
The correlation between `sqft_living` and `rooms` was calculated as **$r = 0.88$**. 
Since $r > 0.80$, keeping both features would destabilize linear model coefficients (making it look like extra rooms *decrease* house price due to covariance overlap). We drop `rooms` and keep `sqft_living` because it contains more granular variance.

---

## 💼 Business Outcomes
1. **Explainable Real Estate Appraisals**: By dropping the collinear variable `rooms`, the model's coefficients represent the true incremental value of square footage without interference, yielding clear explanations for real estate agents.
2. **Stable Estimators**: Training standard OLS linear regressions on the log-transformed price target prevents luxury outliers from driving the weights, ensuring 95% of standard residential price predictions have smaller errors.
3. **Data Preprocessing Template**: Established standard pipeline templates for FDE deployment teams dealing with other skewed variables (e.g., transaction volume, user login frequencies).
