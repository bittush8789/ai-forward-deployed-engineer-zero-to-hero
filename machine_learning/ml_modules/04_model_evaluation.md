# ML Module 4: Model Evaluation (Practical ML Focus)

Model evaluation is the process of using different evaluation metrics to understand a machine learning model's performance, strengths, and weaknesses. A model that looks perfect on paper can fail in production if evaluated incorrectly.

---

## 1. Concept Explanation

Evaluation metrics differ based on the machine learning task (Classification vs. Regression) and validation strategies.

### A. Classification Evaluation Metrics
Based on the **Confusion Matrix**, which tabulates True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN):
- **Accuracy**: The proportion of total correct predictions.
  $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
- **Precision**: The proportion of predicted positive cases that were actually positive. High precision is critical when false positives are costly (e.g. spam filtering).
  $$\text{Precision} = \frac{TP}{TP + FP}$$
- **Recall (Sensitivity)**: The proportion of actual positive cases that were correctly identified. High recall is critical when false negatives are dangerous (e.g. cancer detection).
  $$\text{Recall} = \frac{TP}{TP + FN}$$
- **F1-Score**: The harmonic mean of Precision and Recall, providing a single metric that balances both.
  $$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **ROC-AUC**: Receiver Operating Characteristic area under the curve. Plots True Positive Rate vs. False Positive Rate across all decision thresholds. AUC ranges from 0.5 (random guess) to 1.0 (perfect classifier).

### B. Regression Evaluation Metrics
- **MAE (Mean Absolute Error)**: Average absolute difference between predicted and actual values. Robust to outliers.
  $$\text{MAE} = \frac{1}{N} \sum |y_i - \hat{y}_i|$$
- **MSE (Mean Squared Error)**: Average squared difference. Heavily penalizes large errors, making it useful for mathematical optimization.
- **RMSE (Root Mean Squared Error)**: Square root of MSE. Returns metric to original target units.
- **R² Score (Coefficient of Determination)**: The proportion of variance in the target variable that is predictable from the features. Ranges from $-\infty$ to 1.0. An $R^2$ of 0.80 means the model explains 80% of the variance.

### C. Validation Strategies
* **Train-Test Split**: Dividing data (typically 80/20) to evaluate model performance on unseen data.
* **K-Fold Cross Validation**: Splitting data into $K$ parts. The model is trained $K$ times, each time using a different fold as the test set and the remaining $K-1$ folds as the training set, averaging the evaluation scores.
* **Stratified K-Fold**: Ensures each fold contains approximately the same percentage of target classes as the complete dataset. Crucial for imbalanced classification.

---

## 2. Why It Matters

1. **Unbalanced Class Handling**: If churn rate is 1%, a dummy model predicting "No Churn" achieves 99% accuracy. Evaluating with F1-Score or ROC-AUC reveals the model's true performance immediately.
2. **Business Alignment**: Different metrics map to different business goals. A fraud detection system prioritizes **Recall** (catching every fraud), while a marketing campaign prioritizes **Precision** (avoiding wasting budgets on wrong leads).
3. **Overfitting Detection**: Comparing training metrics against cross-validation metrics allows you to spot when a model is memorizing noise (underfitting vs. overfitting).

---

## 3. Business Example

**Scenario**: A medical tech firm builds a model to classify high-risk patients for emergency care interventions.
* **The Danger**: A False Negative (missing a patient who needs help) leads to serious health risks. A False Positive (sending emergency care to a healthy patient) incurs minor administrative costs.
* **The Evaluation Metric Choice**:
  * The business team must optimize for **Recall**.
  * They select a model that achieves 98% Recall, even if its Precision drops to 45% (meaning many false alarms are sent).
  * If they optimized for Accuracy or Precision, the model would miss high-risk patients to keep its error counts low.

---

## 4. Dataset Example

Confusion Matrix inputs:

| | Predicted: Positive | Predicted: Negative |
|---|---|---|
| **Actual: Positive** | 80 (True Positive) | 20 (False Negative) |
| **Actual: Negative** | 10 (False Positive) | 890 (True Negative) |

- Accuracy = $(80+890)/1000 = \textbf{97.0\%}$
- Precision = $80/(80+10) = \textbf{88.9\%}$
- Recall = $80/(80+20) = \textbf{80.0\%}$

---

## 5. Python Example

Using Scikit-Learn to evaluate classification metrics and run Stratified K-Fold validation:

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# 1. Create imbalanced dataset (90% class 0, 10% class 1)
X, y = make_classification(n_samples=500, n_features=5, weights=[0.9, 0.1], random_state=42)

# 2. Initialize classifier
model = LogisticRegression()

# 3. Stratified K-Fold Cross Validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring="roc_auc")

print(f"Stratified 5-Fold ROC-AUC Scores: {scores}")
print(f"Mean ROC-AUC: {scores.mean():.4f} (Std Dev: {scores.std():.4f})\n")

# 4. Local Classification Report
model.fit(X, y)
y_preds = model.predict(X)
probs = model.predict_proba(X)[:, 1]

print("Classification Report:")
print(classification_report(y, y_preds, target_names=["Majority", "Minority"]))
print(f"ROC-AUC: {roc_auc_score(y, probs):.4f}")
```

---

## 6. Capstone Project Context: Model Comparison Dashboard

In **Capstone Project 4** (`capstones/capstone4_segmentation/`) and **Project 5** (`capstones/capstone5_pipeline/`), you will:
1. Train multiple candidate models.
2. Compile their evaluations (Precision, Recall, F1, MSE, R²) into comparative tables.
3. Automatically plot ROC-AUC curves comparing models side-by-side.
4. Export the metrics report to disk for stakeholder review.

---

## 7. Interview Questions

1. **Why is the F1-Score computed as the Harmonic Mean rather than the Arithmetic Mean of Precision and Recall?**
   *Answer*: The harmonic mean penalizes extreme values. If a model has a Precision of 1.0 and a Recall of 0.0, the Arithmetic Mean is 0.5, which looks deceptively decent. The Harmonic Mean yields an F1-Score of 0.0, correctly reflecting that the model has zero recall and is useless for the positive class.
2. **What does an $R^2$ score of -0.05 indicate about a regression model?**
   *Answer*: An $R^2$ score can be negative. A score of 0.0 indicates that the model predicts as well as a baseline that always predicts the mean of the target. A negative $R^2$ indicates that the model's predictions are worse than simply predicting the mean, meaning the model has fit patterns completely incorrectly.
3. **What is the difference between K-Fold and Stratified K-Fold? When is K-Fold dangerous?**
   *Answer*: K-Fold randomly splits the dataset into folds. Stratified K-Fold ensures that the ratio of target classes in each fold matches the ratio in the full dataset. K-Fold is dangerous when dealing with imbalanced datasets (e.g. fraud detection); a random split might result in some folds containing zero fraud cases, causing model evaluation to fail.

---

## 8. Common Mistakes

- **Evaluating imbalanced classification with Accuracy**: Assuming a model with 98% accuracy on a dataset with 2% positive cases is performing well. Always look at Precision, Recall, and AUC.
- **Comparing RMSE between different target variables**: RMSE is dependent on the scale of the target variable. You cannot compare the RMSE of a house price prediction model (in dollars) with the RMSE of a age prediction model (in years). Use $R^2$ for scale-independent comparisons.
- **Reporting train metrics instead of test metrics**: Reporting training set metrics to stakeholders. Models can easily memorize the training set, leading to over-optimistic performance figures that will degrade in production.

---

## 9. Production Usage

In MLOps pipelines:
* **Model Promotion Gates**: During CI/CD runs, automated tests train and evaluate new model candidates. If the candidate model's cross-validated F1-Score exceeds the currently deployed model's score by a specified threshold (e.g. > 0.01), it is promoted to the model registry; otherwise, deployment is blocked.

---

## 10. AI FDE Perspective

In enterprise settings, business stakeholders rarely understand ROC-AUC or F1-Score. 

As an FDE, you must translate these statistical metrics into business metrics. Do not say: "The model achieved an AUC of 0.82." Instead, present a trade-off table: "At this decision threshold, the model will catch 80% of fraud cases, saving \$50,000/month, while generating 50 false alarms per day." Framed in terms of cost and workload impact, business leaders can easily make decisions.
