# Module 3: Loss Functions

## 1. Industry Explanation
A **Loss Function** (or Cost Function/Objective Function) is the compass that guides the neural network during training. It calculates a single scalar value representing the "error" between the model's predictions and the actual ground truth. Backpropagation then uses this error to update the network's weights.

In industry, choosing a loss function isn't arbitrary; it is strictly dictated by the **business problem** and the **shape of the output layer**:
- **Regression (Predicting a continuous number, e.g., Price, LTV, Age)**: Use Mean Squared Error (MSE), Mean Absolute Error (MAE), or Huber Loss.
- **Binary Classification (Yes/No, Spam/Ham, Churn/Retain)**: Use Binary Cross Entropy (BCE).
- **Multi-Class Classification (Dog/Cat/Bird)**: Use Categorical Cross Entropy (CCE).

---

## 2. Why It Matters (The Business Context)
Using the wrong loss function can lead to models that technically train but solve the wrong business problem. 
For example, if you are predicting House Prices, using MSE penalizes large errors heavily (because the error is squared). If your model predicts a $10M mansion as $5M, the huge penalty will distort your entire model to focus on mansions. If the business goal is to accurately price median homes for normal users, **MAE (Mean Absolute Error)** or **Huber Loss** is a much better choice, as it doesn't overreact to massive outliers.

---

## 3. Python Example (Theory / Conceptual)
*Understanding the math behind MSE and BCE.*

```python
import numpy as np

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def binary_cross_entropy(y_true, y_pred):
    # Add epsilon to prevent log(0)
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

y_true_reg = np.array([100.0, 200.0, 300.0])
y_pred_reg = np.array([110.0, 190.0, 300.0])
print(f"MSE Loss: {mean_squared_error(y_true_reg, y_pred_reg):.2f}")

y_true_clf = np.array([1, 0, 1])
y_pred_clf = np.array([0.9, 0.1, 0.8])
print(f"BCE Loss: {binary_cross_entropy(y_true_clf, y_pred_clf):.4f}")
```

---

## 4. PyTorch Example (Production Grade)
*In PyTorch, loss functions are instantiated as objects and called on the predictions.*

```python
import torch
import torch.nn as nn

# 1. Regression (Output layer has 1 neuron, NO activation)
mse_loss = nn.MSELoss()
mae_loss = nn.L1Loss() # L1 Loss is the PyTorch name for MAE

# 2. Binary Classification (Output has 1 neuron, raw logits)
# BCEWithLogitsLoss applies Sigmoid internally (numerically stable)
bce_loss = nn.BCEWithLogitsLoss() 

# 3. Multi-Class (Output has N neurons, raw logits)
# CrossEntropyLoss applies LogSoftmax internally
cce_loss = nn.CrossEntropyLoss() 

# Example: BCE
logits = torch.tensor([2.5, -1.2, 0.3]) # Raw model outputs
targets = torch.tensor([1.0, 0.0, 1.0])
loss = bce_loss(logits, targets)
```

---

## 5. Business Use Case
**Demand Forecasting (Retail)**
A supermarket chain predicts the daily demand for perishable goods like milk. Initially, the MLE team used MSE as the loss function. However, MSE punished the model symmetrically (under-predicting by 10 gallons was penalized exactly the same as over-predicting by 10 gallons). 

In reality, throwing away 10 spoiled gallons (over-predicting) costs the business $20, but running out of milk (under-predicting) costs $50 in lost revenue and customer trust. The team switched to a custom **Asymmetric Loss Function** (a modified MAE) that penalized under-predictions 2.5x more heavily than over-predictions. The model's raw accuracy dropped slightly, but it increased overall store profitability by 12%.

---

## 6. Mini Project: House Price Prediction (Loss Selection)
Run the accompanying script `loss_selection.py`.
This project trains a Neural Network to predict House Prices. We train two identical models:
1. Trained with **MSELoss** (Mean Squared Error)
2. Trained with **L1Loss** (Mean Absolute Error)

We then evaluate how they perform on a dataset that contains extreme outliers (billion-dollar mansions).

**To run:**
```bash
python loss_selection.py
```

---

## 7. Production Considerations
- **Class Imbalance**: In fraud detection, 99.9% of transactions are legitimate. Standard BCE will achieve 99.9% accuracy by predicting "Not Fraud" every time. In PyTorch, you must pass a `pos_weight` to `BCEWithLogitsLoss` to penalize missing a fraud case heavily.
- **`reduction='mean'` vs `reduction='sum'`**: By default, PyTorch loss functions return the mean loss of the batch. This is usually what you want because it keeps the learning rate stable regardless of batch size. If you use `reduction='sum'`, a larger batch will produce a massive loss, causing exploding gradients.

---

## 8. Common Failures
1. **Using BCELoss instead of BCEWithLogitsLoss**: If your network ends with `nn.Sigmoid()`, and you use `nn.BCELoss()`, the loss calculation can suffer from floating-point rounding errors when the sigmoid output is extremely close to 0 or 1, resulting in `NaN` loss. Always output logits and use `BCEWithLogitsLoss`.
2. **Target Shape Mismatches in BCE**: `BCEWithLogitsLoss` requires the `target` tensor to have the exact same shape as the `input` tensor (e.g., both must be `[batch_size, 1]`). If the target is `[batch_size]`, PyTorch will broadcast the tensors, creating an invisible $N \times N$ matrix and returning garbage gradients.

---

## 9. Debugging Techniques
If your loss is `NaN` (Not a Number) on the very first epoch:
1. **Check for NaNs in Data**: `assert not torch.isnan(inputs).any()`
2. **Check Loss Function Inputs**: Are you passing logits to a loss function that expects probabilities? Or probabilities to a loss function that expects logits?
3. **Exploding Gradients**: The loss function might be returning a massive number that overflows `float32`. Use gradient clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`.

---

## 10. Interview Questions

**Q1: What is the difference between BCEWithLogitsLoss and CrossEntropyLoss in PyTorch?**
*Answer*: "`BCEWithLogitsLoss` is for binary or multi-label classification (where classes are not mutually exclusive). It expects an output layer of size 1 (or size N for multi-label) and applies a Sigmoid internally. `CrossEntropyLoss` is for multi-class classification (mutually exclusive classes). It expects an output layer of size C (number of classes) and applies a LogSoftmax internally."

**Q2: When predicting human age, would you use MSE or MAE? Why?**
*Answer*: "MAE (Mean Absolute Error) is usually better. If I predict someone is 25 but they are 35, the error is 10. With MAE, the penalty is 10. With MSE, the penalty is 100. MSE disproportionately punishes large errors, making the model highly sensitive to outliers. Since age errors scale linearly in human perception, MAE aligns better with reality."

**Q3: Your classification loss is decreasing steadily, but your accuracy is stuck at 50%. What's happening?**
*Answer*: "The model is likely making the same predictions but becoming more 'confident' in them (e.g., moving a prediction from 0.51 to 0.99 for a class, which lowers Cross Entropy Loss), but it's not actually crossing the decision boundary for new, correct predictions. This often indicates the learning rate is too small to escape a local minimum, or there's an issue with class imbalance."
