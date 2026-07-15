# Module 10: Probability in Machine Learning (Practical ML Focus)

Machine Learning algorithms are inherently probabilistic. Whether a neural network classifies an image or a logistic regression model predicts customer churn, the output layer represents a conditional probability distribution over classes.

---

## 1. Concept Explanation

### Classification Probabilities
A binary classifier outputs a raw score that is compressed into a probability $P(Y = 1 | X)$ using the **Sigmoid (logistic) function**:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

For multi-class classification (e.g., classifying an image into dog, cat, or bird), we use the **Softmax function** to output a normalized probability distribution over all classes:

$$P(Y = c \mid X) = \frac{e^{z_c}}{\sum_{j=1}^{C} e^{z_j}}$$

### Classification Thresholds & Calibration
* **Default Threshold**: We typically classify a data point as positive ($Y=1$) if $P(Y=1|X) \ge 0.5$.
* **Threshold Optimization**: If false positives are expensive (e.g., blocking legitimate credit cards), we increase the threshold to $0.90$. If false negatives are dangerous (e.g., cancer diagnosis), we lower the threshold to $0.10$.
* **Calibration**: Just because a model outputs "0.80" does not mean it is 80% likely to be true. A model is **calibrated** if, of the samples it predicts with 80% confidence, 80% are indeed positive. We evaluate calibration using **Reliability Diagrams** and correct it using **Platt Scaling** or **Isotonic Regression**.

### Recommendation Systems (Probabilistic Matrix Factorization)
Recommender systems predict the probability that a user $u$ will enjoy item $i$:

$$P(\text{Like} \mid u, i) = \sigma(U_u^T V_i)$$

Where $U_u$ and $V_i$ are latent factor vectors for users and items.

---

## 2. Why It Matters in ML

1. **Risk-Aware Decision Making**: In production, models shouldn't just predict labels; they should report confidence. If a self-driving car classifies a shape as a trash bag with 51% confidence and a human with 49% confidence, it should stop. We need the raw probability values to make risk-minimizing decisions.
2. **Evaluation Metrics**: Probabilistic models are evaluated using metrics that inspect the probabilities themselves, such as **Log Loss (Cross-Entropy)** or **Brier Score**, rather than simple binary accuracy.
3. **Calibrating Ensembles**: Models like Random Forest or SVMs output scores that are not naturally calibrated probabilities. Understanding how to transform these scores into probabilities is crucial for downstream workflows.

---

## 3. Business Example

**Scenario**: A telecom client wants to predict customer churn ($Y=1$) using a classification model.
* **The Problem**: Giving every churning customer a \$100 retention discount is too expensive. We only want to target customers where the discount will prevent churn.
* **The Solution**:
  1. Train a classification model to output the churn probability $P(\text{Churn} | \text{User})$.
  2. Estimate the probability that the customer will accept the offer and stay: $P(\text{Accept} | \text{User})$.
  3. Calculate the Expected Value of sending the offer:
     $$E[\text{Value}] = P(\text{Churn} | X) \times P(\text{Accept} | X) \times (\text{Customer Lifetime Value} - 100) - (1 - P(\text{Churn} | X) \times 0)$$
  4. Only send the retention discount to users where $E[\text{Value}] > 0$.

---

## 4. Dataset Example

Probabilistic churn routing matrix:

| User ID | Churn Probability ($P$) | Customer Value (CLV) | Cost of Retention | Expected Value of Intervention | Action |
|---|---|---|---|---|---|
| U_701 | 0.85 | \$1,200.00 | \$100.00 | \$920.00 | Send Offer |
| U_702 | 0.40 | \$300.00 | \$100.00 | \$20.00 | Send Offer |
| U_703 | 0.12 | \$400.00 | \$100.00 | -\$52.00 | Do Nothing |

---

## 5. Python Example

Using Scikit-Learn to fit a model, extract probabilities, evaluate calibration, and optimize thresholds:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, brier_score_loss

# 1. Create simulated churn data
np.random.seed(42)
n_users = 1000
usage_hours = np.random.normal(40, 10, n_users)
support_tickets = np.random.poisson(2, n_users)

# Churn logic with some noise
z = -0.05 * usage_hours + 0.8 * support_tickets - 1.0
prob_churn = 1 / (1 + np.exp(-z))
churn_label = np.random.binomial(1, prob_churn)

df = pd.DataFrame({
    "usage_hours": usage_hours,
    "support_tickets": support_tickets,
    "churn": churn_label
})

# 2. Split and Train Logistic Regression
X = df[["usage_hours", "support_tickets"]]
y = df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# 3. Extract Probabilities
# predict_proba returns [P(class_0), P(class_1)]
probs = model.predict_proba(X_test)[:, 1]

# 4. Evaluate Probabilistic Performance
loss = log_loss(y_test, probs)
brier = brier_score_loss(y_test, probs)

print(f"Log Loss: {loss:.4f} (Lower is better)")
print(f"Brier Score: {brier:.4f} (Mean squared error of probabilities)")

# 5. Threshold Optimization
# If we care about high-precision churn detection, change threshold from 0.5 to 0.75
custom_threshold = 0.75
custom_preds = (probs >= custom_threshold).astype(int)
print(f"Number of predicted churners at 0.50 threshold: {sum(probs >= 0.5)}")
print(f"Number of predicted churners at 0.75 threshold: {sum(custom_preds)}")
```

---

## 6. Mini Project Context: Customer Churn Prediction

In `projects/project5_customer_churn/`, you will:
1. Build a complete customer churn prediction pipeline.
2. Preprocess numerical and categorical features.
3. Train classifiers to generate calibrated probabilities.
4. Run threshold tuning experiments to optimize business revenue.
5. Save ROC-AUC and Precision-Recall curve diagrams to analyze performance.

---

## 7. Interview Questions

1. **What is Log Loss (Cross-Entropy)? Why is it preferred over accuracy when training classification models?**
   *Answer*: Log Loss penalizes models based on the confidence of their predictions. If a model predicts a user will churn with 99% confidence but the user doesn't, the Log Loss penalty is extremely high (near infinity). Accuracy only checks if the predicted class matches the actual class, completely ignoring model confidence. Log Loss ensures the model outputs well-calibrated probabilities.
2. **What is Sigmoid vs Softmax? When is each used?**
   *Answer*: Sigmoid maps any real-valued number to a range $[0, 1]$, making it ideal for binary classification (predicting yes/no). Softmax is used in multi-class classification; it takes a vector of raw scores (logits) and maps them to a probability distribution where the sum of all elements is exactly 1.0.
3. **What is probability calibration, and why does it matter?**
   *Answer*: Calibration means that the predicted probability matches the actual frequency of occurrences. If a model predicts a credit card transaction has a 90% chance of being fraud, and we look at 100 transactions with that prediction, exactly 90 of them should be actual fraud. It matters because downstream decision engines (e.g., transaction blocking limits) rely on the literal dollar-value risks computed from these probabilities.

---

## 8. Common Mistakes

- **Confusing confidence with accuracy**: Assuming a model with 95% accuracy always outputs 95% confident predictions, or vice versa.
- **Using raw model output scores as probabilities**: Support Vector Machines (SVMs) and Random Forests do not naturally output probabilities. If you call their prediction score methods, you must pass them through a calibration layer (e.g., Scikit-Learn's `CalibratedClassifierCV`) before using them in risk calculators.
- **Selecting 0.5 as the default threshold for imbalanced classes**: If churn rate is 1%, a model predicting "0.0" for everyone achieves 99% accuracy. For rare classes, you *must* select a threshold that balances precision and recall rather than relying on the default 0.5 split.

---

## 9. Production Usage & MLOps

In credit underwriting systems:
* Models predict the probability of default ($P(\text{Default} | \text{Applicant})$). Rather than a binary output, the loan approval engine takes this probability and calculates the interest rate required to offset the default risk, adjusting prices automatically for each risk tier.

---

## 10. AI FDE Perspective

In business-to-business AI deployments, your client will often have a legacy rule-based system. 

By building your ML model to output probabilities rather than hard decisions, you can run a **hybrid decision pipeline**. If $P(\text{Fraud}) < 0.1$, approve automatically. If $P(\text{Fraud}) > 0.9$, block automatically. If the probability is in the middle ($0.1 \le P \le 0.9$), route the transaction to a human analyst. This approach reduces human review workloads by 80% while retaining human oversight for ambiguous cases, which is highly appealing to enterprise clients.
