# Phase 3: Machine Learning Foundations & Core Pipelines

Welcome to the Practical Machine Learning curriculum. This phase is designed for AI Forward Deployed Engineers (FDEs), Machine Learning Engineers, and Data Scientists who want to master the mathematical foundations, algorithm selection, preprocessing techniques, hyperparameter optimization, and production pipeline deployment of ML models.

---

## 🗺️ Curriculum Overview

This phase is split into three core disciplines, supplemented by **10 Hands-on Projects/Capstones** and an **Interactive Course Hub Dashboard**.

### 📊 Part 1: Statistics & Probability (Math Foundation)
1. **[Descriptive Statistics](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/statistics/01_descriptive_stats.md)**: Foundation metrics (mean, median, IQR, std dev, outliers).
2. **[Data Distribution](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/statistics/02_data_distributions.md)**: Shapes of data (Normal, skewness, kurtosis) and scaling transforms.
3. **[Correlation Analysis](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/statistics/03_correlation_analysis.md)**: Pearson/Spearman correlation for feature redundancy.
4. **[Sampling & Inference](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/statistics/04_sampling_inference.md)**: Confidence intervals, Z-tests, and A/B Testing.
5. **[Statistics for ML](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/statistics/05_statistics_for_ml.md)**: Preprocessing, missing values, winsorization.
6. **[Probability Fundamentals](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/probability/06_prob_fundamentals.md)**: Conditional probability, clickstreams, and independence.
7. **[Bayes' Theorem](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/probability/07_bayes_theorem.md)**: Priors, posteriors, Laplace smoothing, and spam filters.
8. **[Random Variables](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/probability/08_random_variables.md)**: Expected values, revenue forecasting, CLV.
9. **[Probability Distributions](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/probability/09_prob_distributions.md)**: Binomial success, Poisson rates, capacity sizing.
10. **[Probability in ML](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/probability/10_prob_in_ml.md)**: Calibration, sigmoid/softmax, classification thresholds.

### 🤖 Part 2: Machine Learning Core (Production Focus)
1. **[Module 1: Feature Engineering](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/ml_modules/01_feature_engineering.md)**: Missing value treatment, outlier mitigation, scaling, one-hot encoding, feature selection, dimensionality reduction.
2. **[Module 2: Supervised Learning](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/ml_modules/02_supervised_learning.md)**: Regression (Linear, Tree, Forest, XGBoost) and Classification (Logistic, Tree, Forest, XGBoost, SVM).
3. **[Module 3: Unsupervised Learning](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/ml_modules/03_unsupervised_learning.md)**: Clustering (K-Means, Hierarchical, DBSCAN), Dimensionality Reduction (PCA), and Anomaly Detection (Isolation Forest).
4. **[Module 4: Model Evaluation](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/ml_modules/04_model_evaluation.md)**: Classification metrics (Accuracy, Precision, Recall, F1, ROC-AUC), Regression metrics (MAE, MSE, RMSE, R²), and Cross Validation.
5. **[Module 5: Hyperparameter Tuning](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/ml_modules/05_hyperparameter_tuning.md)**: GridSearchCV, RandomizedSearchCV, bias-variance tradeoff, and regularization.
6. **[Module 6: Scikit-Learn Pipelines](file:///d:/ai-forward-deployed-engineer-zero-to-hero/machine_learning/ml_modules/06_scikit_learn.md)**: Architecture, estimators, custom transformers, Pipeline chains, and model persistence (Joblib).

---

## 🛠️ Setup & Execution

### 1. Install Dependencies
First, install the required packages using pip:
```bash
pip install -r requirements.txt
```

### 2. Run Mini-Projects & Capstones
Each project contains a self-contained `run_project.py` or `run_capstone.py` script that generates data, runs analysis, displays results, and saves charts:

#### 📊 Part 1 Mini-Projects:
- **Project 1: Customer Spending Analysis**
  `python projects/project1_customer_spending/run_project.py`
- **Project 2: House Price Analysis**
  `python projects/project2_house_prices/run_project.py`
- **Project 3: Marketing Campaign A/B Testing**
  `python projects/project3_marketing_ab_test/run_project.py`
- **Project 4: Email Spam Detection**
  `python projects/project4_email_spam/run_project.py`
- **Project 5: Customer Churn Prediction**
  `python projects/project5_customer_churn/run_project.py`

#### 🤖 Part 2 Capstone Projects:
- **Capstone 1: Customer Churn Prediction System**
  `python capstones/capstone1_churn/run_capstone.py`
- **Capstone 2: House Price Prediction Platform**
  `python capstones/capstone2_house_prices/run_capstone.py`
- **Capstone 3: Fraud Detection System**
  `python capstones/capstone3_fraud/run_capstone.py`
- **Capstone 4: Customer Segmentation Engine**
  `python capstones/capstone4_segmentation/run_capstone.py`
- **Capstone 5: End-to-End ML Pipeline**
  `python capstones/capstone5_pipeline/run_capstone.py`

---

## 🌐 Interactive Web Hub (Course Dashboard)

To explore interactive calculators, quizzes, and live data visualizations:
1. Locate the directory `machine_learning/course_hub/`.
2. Open `index.html` in your favorite web browser (double-click it, or run a local python web server).
   *To launch a local server:*
   ```bash
   python -m http.server 8000
   ```
   Then navigate to `http://localhost:8000/machine_learning/course_hub/`.
