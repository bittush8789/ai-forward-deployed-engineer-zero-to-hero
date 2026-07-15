# Module 8: Model Evaluation

## 1. Industry Explanation
In tutorials, you compile a model and print `accuracy`. In industry, accuracy is often the *least* useful metric. Real-world datasets are heavily imbalanced (e.g., 99% of emails are ham, 1% are spam). If your model predicts "ham" every time, it achieves 99% accuracy but is completely useless.

Model Evaluation in production involves choosing the right statistical metric based on the specific **business cost** of making a mistake.
- **Precision**: When the model claims a condition is true, how often is it actually true? (Used when False Positives are very expensive).
- **Recall**: Out of all the actual true conditions in reality, how many did the model find? (Used when False Negatives are very expensive).
- **F1-Score**: The harmonic mean of Precision and Recall. Used when you want a balanced model.
- **ROC-AUC**: Evaluates the model's ability to rank probabilities, regardless of the specific threshold used to say "Yes/No".
- **Confusion Matrix**: A visual grid showing exactly where the model is making its mistakes (True Positives, False Positives, True Negatives, False Negatives).

---

## 2. Why It Matters (The Business Context)
Consider a **Cancer Detection Model**. 
- A **False Positive** means telling a healthy patient they have cancer. They get stressed and have to do a biopsy (Cost: $2,000 and anxiety).
- A **False Negative** means telling a dying patient they are healthy. They go home and die (Cost: Loss of life and massive lawsuit).

If you optimize this model for Accuracy or Precision, you will miss cancers (False Negatives). As an MLE, you must actively tune this model to maximize **Recall**, ensuring it catches almost every cancer, even if it means accepting a higher rate of False Positives. The business context dictates the metric.

---

## 3. Python Example (Theory / Conceptual)
*Understanding the math behind the confusion matrix.*

```python
# Actual: 1 (Cancer), 0 (Healthy)
y_true = [1, 1, 0, 0, 1]
# Model Predictions
y_pred = [1, 0, 0, 1, 1] 

# True Positives (Model said Cancer, was Cancer): 2
# True Negatives (Model said Healthy, was Healthy): 1
# False Positives (Model said Cancer, was Healthy): 1
# False Negatives (Model said Healthy, was Cancer): 1

TP, TN, FP, FN = 2, 1, 1, 1

precision = TP / (TP + FP)  # 2 / (2 + 1) = 0.66
recall = TP / (TP + FN)     # 2 / (2 + 1) = 0.66
f1 = 2 * (precision * recall) / (precision + recall)

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
```

---

## 4. PyTorch Example (Production Grade)
*PyTorch does not have built-in evaluation metrics like scikit-learn. In industry, we extract the predictions from PyTorch Tensors and pass them to `scikit-learn` or use the `torchmetrics` library.*

```python
import torch
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

# 1. Get raw logits from PyTorch model
# model.eval()
# with torch.no_grad():
#     logits = model(test_data)

logits = torch.tensor([2.5, -1.2, 0.3, 3.1, -0.5])
y_true = torch.tensor([1, 0, 0, 1, 1])

# 2. Convert logits to probabilities
probs = torch.sigmoid(logits).numpy()

# 3. Convert probabilities to binary predictions using a threshold (default 0.5)
preds = (probs >= 0.5).astype(int)
y_true = y_true.numpy()

# 4. Evaluate using scikit-learn
print("ROC-AUC:", roc_auc_score(y_true, probs))
print("Confusion Matrix:\n", confusion_matrix(y_true, preds))
```

---

## 5. Business Use Case
**Fraud Detection System (Banking)**
A bank processes 1 million credit card transactions a day; 100 of them are fraudulent (0.01%). The initial model achieved 99.99% accuracy by simply predicting "Not Fraud" for every transaction. The bank lost $50,000 a day to fraud.

The MLE team shifted the evaluation metric from Accuracy to **ROC-AUC** and plotted the Precision-Recall curve. By lowering the classification threshold from `0.5` to `0.12`, they intentionally increased the False Positive rate (causing some users to get annoyed by "Is this you?" text messages), but increased the **Recall** of actual fraud from 0% to 85%, saving the bank $42,500 daily.

---

## 6. Mini Project: Fraud Evaluation Lab
Run the accompanying script `evaluation_metrics.py`.
This script trains a neural network on a highly imbalanced dataset (simulating fraud). It demonstrates:
1. Why Accuracy is a lying metric.
2. Generating a Classification Report.
3. How to shift the classification threshold to prioritize Recall over Precision.

**To run:**
```bash
python evaluation_metrics.py
```

---

## 7. Production Considerations
- **Threshold Tuning**: In PyTorch, `torch.sigmoid(logits) >= 0.5` is the default, but it's rarely the optimal business threshold. After training, you should write a loop that tests thresholds from 0.01 to 0.99 against your Validation set, calculating the exact dollar-value cost of the resulting False Positives/Negatives at each threshold, and pick the one that maximizes business profit.
- **Model Calibration**: Neural networks are notoriously "uncalibrated". Just because a model outputs a `0.9` probability doesn't mean it's 90% confident. If you need true probabilities (e.g., for betting algorithms), you must apply Platt Scaling or Isotonic Regression after training.

---

## 8. Common Failures
1. **Data Leakage in Evaluation**: If you evaluate your model on data that was used in training, your metrics will look incredible, but the model will fail in production. Always ensure a strict Train/Validation/Test split, especially for time-series data (never predict the past using the future).
2. **Ignoring the Baseline**: An F1-Score of 0.40 sounds terrible, but if a random guess achieves an F1 of 0.01, your model is 40x better than random. Always evaluate your model against a naive baseline (e.g., predicting the majority class every time).

---

## 9. Debugging Techniques
If your ROC-AUC is exactly 0.50:
1. Your model is making completely random guesses.
2. Check if your loss is decreasing. If loss is decreasing but AUC remains 0.50, your labels might be shuffled or disconnected from your features during the DataLoader phase.

If your ROC-AUC is exactly 1.0 (or 0.999):
1. **Stop celebrating. You have Data Leakage.** 
2. The target variable (e.g., `is_fraud`) is accidentally included in the input features (e.g., `fraud_status_code`), allowing the model to just look up the answer.

---

## 10. Interview Questions

**Q1: In an email spam filter, which is worse: a False Positive or a False Negative? Which metric would you optimize?**
*Answer*: "A False Positive is worse. It means sending a crucial work email to the Spam folder, which could cost a user their job. A False Negative just means one spam email makes it to the inbox (a minor annoyance). Therefore, I would optimize for extremely high Precision, ensuring that if we flag an email as spam, we are 99.9% certain."

**Q2: What does the ROC-AUC score actually represent?**
*Answer*: "It represents the probability that the model will rank a randomly chosen positive instance higher than a randomly chosen negative instance. Unlike F1 or Accuracy, ROC-AUC evaluates the raw probabilities without needing to define a specific Yes/No threshold."

**Q3: Your dataset is 99% Class A and 1% Class B. How do you handle this during training and evaluation?**
*Answer*: "During training, I would pass class weights (`pos_weight`) to the Loss Function so the model is heavily penalized for missing Class B. During evaluation, I would completely ignore Accuracy and instead use the Precision-Recall Area Under Curve (PR-AUC) and the F1-Score of the minority class."
