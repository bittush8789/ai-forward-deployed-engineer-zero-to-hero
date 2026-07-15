# ML Module 1: Feature Engineering (Practical ML Focus)

Feature engineering is the process of using domain knowledge of the data to create features that make machine learning algorithms work. It is often said that "better data beats fancier algorithms," and feature engineering is where this truth is put into practice.

---

## 1. Concept Explanation

Feature engineering consists of preparing, cleaning, transforming, and selecting features to maximize model performance.

### A. Missing Value Handling
Data in the wild is frequently incomplete. 
* **Mean/Median Imputation**: Filling missing numerical values with column statistics. Median is preferred for skewed data.
* **Mode/Constant Imputation**: Filling missing categorical values with the most frequent category or an "Unknown" label.
* **Advanced Imputation**: K-Nearest Neighbors (KNN) or Iterative Imputers (MICE) that predict missing values based on other features.

### B. Outlier Detection & Data Cleaning
* **Winsorization**: Capping extreme values at specific percentiles (e.g., 1st and 99th).
* **Trimming**: Deleting records with extreme outliers (only if they are verified data entry errors).

### C. Feature Scaling
Distance-based models (KNN, SVM, K-Means) and gradient-descent models (Neural Networks, Linear Regression) require scaled features.
* **Standardization (StandardScaler)**: Centers data around 0 with a standard deviation of 1.
  $$x_{\text{std}} = \frac{x - \mu}{\sigma}$$
* **Normalization (MinMaxScaler)**: Scales data to a fixed range (typically 0 to 1).
  $$x_{\text{norm}} = \frac{x - x_{\text{min}}}{x_{\text{max}} - x_{\text{min}}}$$

### D. Categorical Encoding
* **One-Hot Encoding**: Converts categorical levels into binary columns. Preferred for nominal variables without ordering (e.g., Payment Method). Avoid for high-cardinality features due to dimensionality explosion.
* **Label Encoding**: Assigns an integer value to each category. Useful for ordinal data with inherent order (e.g., Education: High School = 0, Bachelor's = 1, PhD = 2).

### E. Feature Creation
Creating new indicators based on domain logic (e.g., combining `total_spend` and `visit_count` to get `average_spend_per_visit`, or extracting `is_weekend` from a timestamp).

### F. Feature Selection & Importance
* **Filter Methods**: Using statistical tests (ANOVA, Chi-Square, Pearson Correlation) to select features.
* **Wrapper Methods**: Recursively training models and dropping poor features (Recursive Feature Elimination - RFE).
* **Embedded Methods**: Algorithms that naturally perform feature selection (L1/Lasso regularization, Random Forest Feature Importance).

### G. Dimensionality Reduction Basics
* **PCA (Principal Component Analysis)**: A linear technique that projects high-dimensional data onto lower-dimensional orthogonal principal components that maximize variance, reducing features while keeping information.

---

## 2. Why It Matters

1. **Model Convergence**: Unscaled features cause gradient descent steps to bounce back and forth, dragging out training times or preventing neural networks from converging.
2. **Preventing Dimensionality Curse**: Adding too many features increases model complexity exponentially, leading to severe overfitting. Feature selection and PCA prune dimensions to keep models lean.
3. **Representation Capacity**: Creating composite variables (e.g., ratios, aggregations) feeds the model domain knowledge, allowing simple linear models to capture non-linear relationships.

---

## 3. Business Example

**Scenario**: A digital retailer wants to predict whether a cart visitor will complete a purchase.
* **Raw Data**: Contains variables: `signup_date` (timestamp), `payment_method` (credit card, Paypal, wire transfer), `total_price` (ranges \$0 to \$15,000), `support_chat_messages` (contains nulls).
* **Feature Engineering Solution**:
  1. Parse `signup_date` to compute `days_since_signup`.
  2. One-hot encode `payment_method` (yielding 3 binary columns).
  3. Impute null values in `support_chat_messages` with 0 (no message sent).
  4. Standard scale `total_price` to prevent luxury transactions from drowning out checkout clicks.
  5. Combine variables to create `spend_per_day_since_signup`.

---

## 4. Dataset Example

Raw vs Engineered customer variables:

| Customer ID | Pay Method (Raw) | Pay: PayPal (OHE) | Pay: Credit (OHE) | Days Active (Created) | Spend scaled |
|---|---|---|---|---|---|
| C_101 | PayPal | 1 | 0 | 45 | -0.45 |
| C_102 | Credit Card | 0 | 1 | 120 | 1.82 |
| C_103 | PayPal | 1 | 0 | 5 | -0.92 |

---

## 5. Python Example

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

# 1. Create simulated dirty customer dataset
df = pd.DataFrame({
    "total_spend": [150.0, np.nan, 2300.0, 95.0, 450.0],
    "payment_method": ["Credit", "PayPal", "Credit", "PayPal", "Wire"],
    "loyalty_score": [3, 1, 5, 1, 4]
})

# 2. Define pipelines using ColumnTransformer
numerical_cols = ["total_spend"]
categorical_cols = ["payment_method"]

# Numerical Preprocessing: Impute then Scale
num_transformer = StandardScaler()
df_imputed_spend = df["total_spend"].fillna(df["total_spend"].median())
df["total_spend_scaled"] = num_transformer.fit_transform(df_imputed_spend.values.reshape(-1, 1))

# Categorical Preprocessing: One-Hot Encode
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_cats = encoder.fit_transform(df[["payment_method"]])
cat_cols = encoder.get_feature_names_out(["payment_method"])
df_encoded = pd.DataFrame(encoded_cats, columns=cat_cols)

# Combine
final_df = pd.concat([df[["loyalty_score", "total_spend_scaled"]], df_encoded], axis=1)
print("Engineered Dataset:")
print(final_df)
```

---

## 6. Capstone Project Context: Churn Feature Engineering Pipeline

In **Capstone Project 1** (`capstones/capstone1_churn/`), you will build a complete feature engineering pipeline:
1. Impute missing billing records.
2. One-hot encode demographic categories.
3. Construct composite features measuring support ticket densities.
4. Scale inputs using standard scalers.
5. Save the preprocessing states to prevent data leakage in evaluations.

---

## 7. Interview Questions

1. **What is the difference between Standardization (StandardScaler) and Normalization (MinMaxScaler)? When would you use each?**
   *Answer*: Standardization centers the data (mean = 0, std = 1) and does not bound the values, making it ideal for algorithms that assume Gaussian distributions (like Linear/Logistic Regression) and resilient to outliers. Normalization scales values to a hard range $[0, 1]$, which is preferred for algorithms that expect bounded outputs (like Image Processing pixel values) or distance calculations that are highly sensitive to ranges (like KNN and K-Means).
2. **Why is it critical to fit your Scaler only on the training set, rather than the entire dataset?**
   *Answer*: Fitting a scaler on the entire dataset incorporates information from the validation/test sets (like mean and variance limits) into the training processing. This is a classic form of **Data Leakage**, which results in over-optimistic evaluation scores during training that fail to generalize to production.
3. **What is the difference between One-Hot Encoding and Label Encoding? What are the limitations of each?**
   *Answer*: One-Hot Encoding creates a new binary column for each category, which prevents models from assuming mathematical order, but can lead to the "Curse of Dimensionality" on high-cardinality features. Label Encoding maps categories to ascending integers, which is memory-efficient but can lead linear models to incorrectly assume ordinal relationships (e.g. PayPal = 2 is twice as large as Credit Card = 1).

---

## 8. Common Mistakes

- **Standard Scaling One-Hot Encoded columns**: Scaling binary columns (0 and 1) destroys their sparse structure and interpretability. Scalers should only be fit on continuous numerical variables.
- **Dropping rows with missing values blindly**: In production, your model must evaluate *every* request. If you drop rows during training, your model won't know how to handle missing fields during inference, causing system crashes.
- **Assuming PCA always improves model performance**: PCA is a linear transformation that drops low-variance directions. If the predictive signal is in a low-variance direction, PCA will actually degrade performance.

---

## 9. Production Usage

In MLOps pipelines:
* **Feature Stores (e.g., Feast)**: Are used to calculate, store, and serve engineered features. During model inference, instead of recalculating values on the fly, the model queries the Feature Store using a `customer_id` key, retrieving pre-engineered features in sub-millisecond latencies.
* **Pipeline Serialization**: Preprocessing scaling objects must be saved (e.g. serialized as pickle or joblib files) alongside the model binaries. If a model is loaded in production, the exact training-fit scaler must scale the incoming request fields.

---

## 10. AI FDE Perspective

In enterprise engagements, client databases are notoriously messy. You will rarely get clean inputs. 

Always design your feature engineering steps as a **reusable Scikit-Learn ColumnTransformer or Pipeline**. This guarantees that the exact rules you write to clean data during the initial POC can be dropped directly into the client's production Airflow or Spark ingestion systems without requiring engineers to rewrite your code from scratch in SQL or Scala, minimizing translation errors.
