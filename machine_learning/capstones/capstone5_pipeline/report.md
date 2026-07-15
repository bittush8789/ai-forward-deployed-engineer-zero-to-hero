# Capstone 5 Report: End-to-End Production ML Pipeline

## 🎯 Executive Summary
In this project, we built a **production-ready end-to-end machine learning pipeline** that encapsulates feature imputation, scaling, one-hot encoding, and random forest classification into a single Scikit-Learn Pipeline object. 

The pipeline was serialized to disk as a `.joblib` binary file. We successfully reloaded the binary to serve predictions on raw, uncleaned mock client requests (resolving missing fields automatically). 

Additionally, we designed a mock **MLOps Monitoring script** that checks for feature drift in incoming cohorts, generating an alert when average income shifted by 26% compared to the training baseline.

---

## 🛠️ Skills Covered
- **Scikit-Learn ColumnTransformer**: Building parallel numerical and categorical preprocessing pipelines.
- **Model Serialization (Joblib)**: Persisting models to disk for production APIs.
- **Production Inference Routing**: Calling predictions on raw, un-preprocessed inputs.
- **MLOps Drift Monitoring**: Tracking statistical shifts in production features to signal retraining schedules.

---

## 📈 Methodology & Formulas

### 1. Preprocessing Pipeline Architecture
- **Numeric Pipeline**: Median Imputer $\rightarrow$ StandardScaler.
- **Categorical Pipeline**: Most-Frequent Imputer $\rightarrow$ OneHotEncoder.
- **Estimator**: Random Forest Classifier.

### 2. Feature Drift Calculation
To track shifts in incoming batch data, we calculate the percentage deviation of the batch mean ($\bar{x}_{\text{batch}}$) against the training baseline mean ($\mu_{\text{baseline}}$) for each continuous feature:
$$\text{Shift} = \frac{|\bar{x}_{\text{batch}} - \mu_{\text{baseline}}|}{\mu_{\text{baseline}}}$$
If $\text{Shift} > 15\%$, a drift alert is raised.

---

## 📊 Results Summary

### 1. API Inference Outcome
- **Incoming Mock Request**: `{"age": NaN, "income": 120000.0, "account_type": "Business"}`
- **Imputation Action**: Age was imputed automatically with the training median (**38.0**).
- **Model Class Output**: **PREMIUM** (Class 1)
- **Model Probability Score**: **74.15%**

### 2. MLOps Drift Check Log
- **`age`**: Baseline: **37.95** | Batch: **38.45** | Shift: **1.32%** (Safe)
- **`income`**: Baseline: **65,245.12** | Batch: **82,142.50** | Shift: **25.90%** (⚠ Drift Alert!)

---

## 💼 Business Outcomes
1. **Zero Preprocessing Redundancy**: Software engineers do not need to replicate data cleansing code in the API layer. The single joblib file handles all cleaning, encoding, scaling, and classification, reducing deployment bugs.
2. **Automated Drift Alerts**: The MLOps check prevents model degradation by alerting engineers when the incoming demographic shifts (e.g. during a luxury marketing campaign), triggering an automated model retraining run.
3. **Calibrated API Responses**: Emitting raw probabilities alongside binary classification labels allows front-end dashboards to show confidence levels or flag borderline files for human review.
