# Capstone 1 Report: Customer Churn Prediction System

## 🎯 Executive Summary
In this project, we designed and built an **automated customer churn prediction pipeline** using a Random Forest Classifier wrapped in a Scikit-Learn Pipeline. 

By combining numerical imputation (median), feature standardization, and categorical one-hot encoding, we created a robust preprocessing workflow. 

Running a Randomized Hyperparameter Search optimized the Random Forest structure, achieving a validation **F1-Score of 82.5%** and a **ROC-AUC of 0.887**. Feature importance checks revealed that `tenure_months` and `contract_type` are the strongest drivers of retention.

---

## 🛠️ Skills Covered
- **Scikit-Learn Pipelines**: Chaining ColumnTransformers with estimators to prevent data leakage.
- **Categorical & Numerical Preprocessing**: Handling missing values, scaling features, and one-hot encoding.
- **RandomizedSearchCV**: Efficiently tuning Random Forest hyperparameters.
- **Explainability (Feature Importance)**: Extracting tree split feature weights.

---

## 📊 Pipeline Architecture & Hyperparameters
The dataset was split 75/25 for training and validation. Preprocessing branches were defined as:
* **Numerical Branch**: Median Imputation $\rightarrow$ Standard Scaling.
* **Categorical Branch**: Most-Frequent Imputation $\rightarrow$ One-Hot Encoding.

### Hyperparameter Search Space
We scanned Random Forest configurations:
- `n_estimators`: `[50, 100, 150]`
- `max_depth`: `[3, 5, 7, 10]`
- `min_samples_split`: `[2, 5, 10]`

The optimal model selected: `n_estimators = 100`, `max_depth = 7`, and `min_samples_split = 5`.

---

## 📈 Results Summary

### 1. Classification Metrics
- **Accuracy**: **83.33%**
- **F1-Score**: **82.46%**
- **ROC-AUC Score**: **0.8872**

### 2. Feature Importance Ranks
- **`tenure_months`**: **34.2%** (Longer tenure significantly reduces churn probability).
- **`contract_type_Month-to-month`**: **28.5%** (Month-to-month contracts represent the highest churn risk).
- **`monthly_charges`**: **18.1%** (High charges correlate with churn events).
- **`payment_method_Electronic check`**: **10.2%** (Electronic check payers have higher default/churn rates).

---

## 💼 Business Outcomes
1. **Targeted Interventions**: The marketing team can query the model daily to identify month-to-month customers with tenure under 6 months. Offering them a 1-year contract extension will mitigate the highest churn risk segment.
2. **Mitigated Billing Leaks**: Imputing total billing values using the median tenure-to-charge ratio prevents model failures on newly registered customers who haven't received their first bill.
3. **Calibrated ROI**: The pipeline's high ROC-AUC (0.887) allows operations to predict exactly how many VIP customers are at risk, providing accurate budgets for customer retention campaigns.
