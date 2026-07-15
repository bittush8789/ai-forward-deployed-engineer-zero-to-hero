# Module 9: Neural Network Debugging

## 1. Industry Explanation
When standard software fails, it throws a Stack Trace (e.g., `NullPointerException at line 42`). When a Neural Network fails, it **fails silently**. It will often compile perfectly, train for 3 days, and output completely useless garbage predictions. 

Debugging deep learning models is the hardest and most valuable skill an MLE can possess. It requires investigating the "silent killers":
- **Vanishing/Exploding Gradients**: The math breaks down in deep layers, preventing weights from updating.
- **Data Leakage**: The model accidentally sees the answer key during training.
- **Label Mismatch**: Data pipeline errors shuffling features without shuffling labels.
- **Dying Activations**: Neurons outputting straight zeros forever.

---

## 2. Why It Matters (The Business Context)
Silent failures cost millions. A major trading firm once deployed a reinforcement learning model that seemed highly profitable in backtesting. However, a data pipeline bug had slightly misaligned the timestamps, allowing the model to "see" 1 second into the future during training (Data Leakage). In production, it immediately started losing hundreds of thousands of dollars per minute because it couldn't see the future anymore. Being able to systematically debug and verify models *before* they hit production is what separates Junior Data Scientists from Senior Applied AI Engineers.

---

## 3. Python Example (Theory / Conceptual)
*Checking for Exploding Gradients.*

```python
import numpy as np

# Imagine these are the gradients calculated during backprop
good_gradients = np.array([0.01, -0.05, 0.02, 0.00])
bad_gradients = np.array([12543.2, -88942.1, 0.0, 99999.9])

def check_gradients(grad_array, threshold=100.0):
    norm = np.linalg.norm(grad_array)
    if norm > threshold:
        print(f"WARNING: Exploding Gradients Detected (Norm: {norm:.2f})")
    else:
        print("Gradients are healthy.")

check_gradients(good_gradients) # Healthy
check_gradients(bad_gradients)  # WARNING!
```

---

## 4. PyTorch Example (Production Grade)
*How to track and debug gradients in PyTorch during the training loop.*

```python
import torch
import torch.nn as nn

model = nn.Linear(10, 1)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# Forward pass
output = model(torch.randn(1, 10))
loss = criterion(output, torch.tensor([[10000.0]])) # Unscaled data causes massive loss

# Backward pass
optimizer.zero_grad()
loss.backward()

# DEBUGGING: Inspect the gradients BEFORE stepping the optimizer
for name, param in model.named_parameters():
    if param.grad is not None:
        grad_norm = param.grad.norm().item()
        if grad_norm > 10.0:
            print(f"Gradient explosion in layer {name}: Norm = {grad_norm:.2f}")

# Industry Fix: Gradient Clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()
```

---

## 5. Business Use Case
**Medical Imaging (Diagnosis Model)**
A healthcare startup built an image classification model to detect tumors in MRI scans. The model achieved 98% accuracy on the test set. However, a Senior MLE decided to run **Saliency Maps** (a debugging technique that highlights which pixels the model looked at to make its decision). 

The Saliency Map revealed that the model wasn't looking at the tumors at all. Instead, it had learned to look at a microscopic text watermark (`Scanner Type: X200`) present only in the images from the hospital with high cancer rates. If deployed, it would have failed on all scans from other hospitals. This is a classic example of **Shortcut Learning**, caught through rigorous visual debugging.

---

## 6. Mini Project: Troubleshooting Lab
Run the accompanying script `troubleshooting_lab.py`.
This script contains a broken training pipeline. It trains but the loss never goes down. Your job is to uncomment the debugging tools to find the root cause (Spoiler: The features are completely detached from the labels due to a shuffling bug).

**To run:**
```bash
python troubleshooting_lab.py
```

---

## 7. Production Considerations
- **The "Overfit a Single Batch" Test**: This is the mandatory first test for any new architecture or data pipeline. You take 1 single batch of data (e.g., 32 rows) and train on it for 200 epochs. The loss should rapidly approach exactly `0.0`. If it does not, you have a fundamental bug in your code (e.g., labels don't match features, optimizer not stepping, wrong loss function).
- **Unit Testing Neural Networks**: You can write `pytest` assertions for your model: `assert not torch.isnan(model(test_batch)).any()` ensures no `NaN` values are ever predicted.

---

## 8. Common Failures
1. **Unscaled Data**: If your loss starts at `999999.0` and immediately goes to `NaN` (Not a Number), your data is not scaled. Neural networks expect inputs to be roughly between `-1.0` and `1.0`. Use `StandardScaler`.
2. **Incorrect Input Shapes**: Passing a shape of `[batch_size]` to a loss function that expects `[batch_size, 1]`. PyTorch will silently "broadcast" the tensors, creating an $N \times N$ matrix, resulting in garbage gradients without throwing an error. Always `view(-1, 1)` your targets.

---

## 9. Debugging Techniques
**Step-by-step Debugging Hierarchy:**
1. **Does it compile?** (Shape mismatch errors).
2. **Does it overfit a single batch?** (Verifies backprop and data alignment).
3. **Is the loss `NaN`?** (Check data scaling and learning rate).
4. **Are the gradients flowing?** (Print `param.grad.norm()` to check for vanishing/exploding gradients).
5. **Is the Train Loss lower than the Validation Loss?** (If Val Loss is lower, you probably have Data Leakage).

---

## 10. Interview Questions

**Q1: You trained a binary classification model. The loss is steadily decreasing, but the accuracy is exactly 50% for 20 epochs straight. What is the most likely cause?**
*Answer*: "The model is likely suffering from a disconnected data pipeline. The features and labels were shuffled independently, so there is no mathematical relationship between the input $X$ and the target $y$. The model is trying to learn, reducing the entropy of its predictions (which lowers the loss slightly), but it's fundamentally just guessing, hence 50% accuracy."

**Q2: How do you identify and fix Exploding Gradients?**
*Answer*: "I identify them by monitoring the L2 norm of the gradients during training. If the norm suddenly spikes to massive values or the loss becomes `NaN`, gradients are exploding. To fix it, I first ensure the input data is scaled properly. If the architecture is deep, I add Batch Normalization. Finally, I use `torch.nn.utils.clip_grad_norm_` to mathematically cap the gradients before the optimizer step."

**Q3: What is Data Leakage and how do you prevent it?**
*Answer*: "Data leakage occurs when information from the Validation or Test set (or information from the future) accidentally 'leaks' into the training process. To prevent it, you must perform all data scaling (`fit_transform`) ONLY on the Training set, and then apply that fitted scaler (`transform`) to the Validation/Test sets. You must also ensure strict temporal splits for time-series data."
