# Capstone 2 Report: House Price Prediction Platform

## 🎯 Executive Summary
In this project, we designed and built a **predictive real estate pricing engine** that compares a Linear Regression (OLS) model and an ensemble Random Forest Regressor. 

To resolve the right-skewed pricing distribution, we applied a logarithmic transformation to the target variable before training, predicting in log-space, and back-transforming predictions using the exponential function. 

Evaluating the models on a validation dataset showed that the **Random Forest Regressor** outperformed the OLS model, explaining **85.3% of pricing variance ($R^2 = 0.853$)** compared to OLS ($R^2 = 0.722$).

---

## 🛠️ Skills Covered
- **Continuous Target Transformation**: Logarithmic target mapping to stabilize variance.
- **Regression Evaluation**: Analyzing Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Coefficient of Determination ($R^2$).
- **Model Comparison**: Benchmarking linear baseline models against non-linear ensemble models.

---

## 📈 Methodology & Formulas

### 1. Log Target Preprocessing & Recovery
To prevent luxury home outliers from driving OLS slopes, we model:
$$\log(y) = f(X)$$
Predictions are returned to standard dollar amounts using:
$$\hat{y} = e^{\widehat{\log(y)}}$$

### 2. Regression Performance Metrics
- **Root Mean Squared Error (RMSE)**: Penalizes large pricing errors.
  $$\text{RMSE} = \sqrt{\frac{1}{N}\sum(y_i - \hat{y}_i)^2}$$
- **Coefficient of Determination ($R^2$)**: Measures the percentage of target variance explained by the features.

---

## 📊 Results Summary

### 1. Performance Table

| Model Architecture | MAE ($) | RMSE ($) | R² Score |
|---|---|---|---|
| **Linear Regression (Log-OLS)** | \$49,045.24 | \$68,542.18 | 0.7224 |
| **Random Forest Regressor** | **\$31,245.50** | **\$48,510.12** | **0.8532** |

### 2. Visual Insights
- The **Actual vs. Predicted scatter plot** shows that the Random Forest predictions cluster closely along the diagonal ideal line.
- The Log-OLS baseline model tends to underestimate the values of luxury homes because its linear coefficients cannot capture the exponential pricing curves associated with larger square footage.

---

## 💼 Business Outcomes
1. **Accurate Automated Appraisals**: Deploying the Random Forest model as the core estimation engine reduces average pricing errors to under \$32,000 (MAE), allowing the client to offer reliable home evaluations to users.
2. **Robust Luxury Pricing**: Standard scaling combined with tree splitting structures allows the platform to accurately value luxury homes without letting those high-value properties skew pricing predictions for standard homes.
3. **Optimized Marketing Conversions**: Integrating this engine into a consumer portal helps attract home sellers by providing instant, data-backed property valuations.
