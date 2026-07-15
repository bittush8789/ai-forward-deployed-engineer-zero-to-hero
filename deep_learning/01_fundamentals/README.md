# Module 1: Neural Network Fundamentals

## 1. Industry Explanation
In academia, a neural network is often described as a universal function approximator inspired by the human brain. In the **industry**, a neural network is a highly scalable feature extraction and mapping engine. It takes raw, unstructured or structured data (pixels, text, tabular rows) and learns hierarchical representations to map inputs to a specific business metric (e.g., probability of a user clicking an ad, or the expected price of a house). 

The core architecture consists of:
- **Inputs**: The raw features passed into the network.
- **Hidden Layers**: Dense (fully connected) layers where the network learns non-linear relationships.
- **Outputs**: The final prediction (e.g., a single probability for binary classification).
- **Forward Pass**: The flow of data from inputs through hidden layers to the output.
- **Loss Function**: The mathematical measurement of how wrong the network's predictions are compared to the ground truth.
- **Backpropagation**: The engine of learning. It calculates the gradient (direction of error) for every weight in the network.
- **Activation Functions**: Functions that introduce non-linearity, allowing the network to learn complex patterns instead of just drawing straight lines.

---

## 2. Why It Matters (The Business Context)
Traditional Machine Learning (like Random Forests or XGBoost) is incredibly powerful for tabular data but requires extensive manual **feature engineering**. 

Neural Networks matter because they perform **automatic feature engineering**. Given enough data and compute, a neural network can find complex, non-linear interactions between variables that a human data scientist might never think to engineer. In production, this means:
- Less time spent manually crafting features.
- The ability to ingest raw text, images, and audio directly.
- Highly scalable training (can be distributed across clusters of GPUs).

---

## 3. Python Example (Theory / Conceptual)
*To understand the forward pass, here is a simplified version built entirely in raw Python without ML frameworks.*

```python
import numpy as np

# 1. Initialize Inputs and Weights
X = np.array([0.5, 0.2])          # 2 input features
W1 = np.array([[0.1, 0.3],        # Weights for Layer 1
               [0.2, 0.4]])
b1 = np.array([0.01, 0.01])       # Bias for Layer 1

W2 = np.array([0.5, 0.6])         # Weights for Output Layer
b2 = np.array([0.05])             # Bias for Output Layer

# 2. Forward Pass
# Layer 1
z1 = np.dot(X, W1) + b1
a1 = np.maximum(0, z1)            # ReLU Activation

# Output Layer
z2 = np.dot(a1, W2) + b2
output = 1 / (1 + np.exp(-z2))    # Sigmoid Activation for probability

print(f"Prediction Probability: {output[0]:.4f}")
```

---

## 4. PyTorch Example (Production Grade)
*In industry, we use PyTorch. Here is how a production-grade Dense Neural Network is defined.*

```python
import torch
import torch.nn as nn

class ProductionDNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(ProductionDNN, self).__init__()
        
        # Define architecture
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),  # Crucial for training stability
            nn.ReLU(),
            nn.Dropout(0.2),             # Regularization to prevent overfitting
            
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(hidden_dim // 2, output_dim)
        )

    def forward(self, x):
        # The forward pass
        # Note: We output raw logits, NOT probabilities. 
        # The loss function (BCEWithLogitsLoss) will handle the sigmoid internally for numerical stability.
        return self.network(x)

# Instantiate the model
model = ProductionDNN(input_dim=10, hidden_dim=64, output_dim=1)
print(model)
```

---

## 5. Business Use Case
**Customer Churn Prediction in SaaS**
A B2B SaaS company is losing 5% of its user base monthly. A traditional Logistic Regression model is only achieving 65% recall on churners. By feeding raw usage logs (daily logins, feature clicks, support tickets) directly into a Deep Neural Network, the company can learn complex behavioral sequences that precede a cancellation, improving recall to 85% and saving millions in retained Annual Recurring Revenue (ARR).

---

## 6. Mini Project: Build First Neural Network
We have provided two complete, runnable Python scripts in this directory that represent your first hands-on projects:

1. **`binary_classification.py`**: A Customer Churn Prediction model predicting if a customer will leave (1) or stay (0).
2. **`multi_class.py`**: A Customer Support Ticket router that classifies text embeddings into multiple departments.

**To run these:**
```bash
python binary_classification.py
python multi_class.py
```
*(Review the code inside these files to see how data loading, training loops, and evaluation metrics are structured in industry).*

---

## 7. Production Considerations
When taking a neural network from a Jupyter Notebook to a production API, consider:
- **Numerical Stability**: Never use `nn.Sigmoid()` as the last layer followed by `BCELoss()`. It causes floating-point underflow. Always output raw logits and use `BCEWithLogitsLoss()`.
- **Data Scaling**: Neural networks are extremely sensitive to unscaled data. If Age is 0-100 and Salary is 0-200,000, the gradients for Salary will explode. Always use `StandardScaler` or `MinMaxScaler`.
- **Determinism**: PyTorch training is non-deterministic by default due to GPU operations. Always set seeds for reproducibility: `torch.manual_seed(42)`.

---

## 8. Common Failures
1. **Shape Mismatches**: The most common error in Deep Learning. `RuntimeError: mat1 and mat2 shapes cannot be multiplied`. This happens when the output dimension of Layer $N$ doesn't match the input dimension of Layer $N+1$, or when your batch size is misaligned.
2. **Forgetting to Zero Gradients**: In PyTorch, gradients accumulate. If you forget `optimizer.zero_grad()` in your training loop, your model will step in the wrong direction and loss will explode.
3. **Forgetting `model.eval()`**: If you evaluate your model without setting `model.eval()`, Dropout and BatchNorm layers will behave as if they are still training, causing highly erratic predictions during inference.

---

## 9. Debugging Techniques
- **Overfit a single batch**: The fastest way to verify your architecture and backprop implementation is to take a single batch of data (e.g., 32 rows) and train on it for 100 epochs. The loss should rapidly approach zero. If it doesn't, your model is fundamentally broken (e.g., bad learning rate, wrong loss function).
- **Check weight initialization**: If loss is stuck on epoch 1, print `model.layer.weight.grad`. If gradients are `None` or exactly `0.0`, backpropagation is broken (likely due to a detached tensor or a dead activation function).

---

## 10. Interview Questions

**Q1: Explain Backpropagation to a non-technical Product Manager.**
*Answer*: "Imagine adjusting the recipe of a complex soup. You taste it (calculate loss) and it's too salty. Backpropagation is the process of figuring out exactly which ingredients contributed to the saltiness, and automatically telling the chefs to reduce those specific ingredients for the next batch."

**Q2: Why do we use mini-batches instead of training on the entire dataset at once?**
*Answer*: "Three reasons: Memory constraints (you can't fit 1TB of data on a 16GB GPU), computational efficiency (matrix multiplications are highly optimized for specific batch sizes), and regularization (the noise introduced by mini-batches helps the model escape local minima and generalize better)."

**Q3: What is the difference between a parameter and a hyperparameter?**
*Answer*: "Parameters (weights and biases) are learned by the network during training via backpropagation. Hyperparameters (learning rate, batch size, number of layers) are set by the engineer before training begins."
