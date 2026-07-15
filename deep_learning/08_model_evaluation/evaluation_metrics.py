import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import numpy as np

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Highly Imbalanced Fraud Data)
# ==========================================
print("Generating highly imbalanced Fraud dataset (95% Legit, 5% Fraud)...")
X, y = make_classification(n_samples=10000, n_features=20, n_informative=15, 
                           n_classes=2, weights=[0.95, 0.05], random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_loader = DataLoader(
    TensorDataset(torch.FloatTensor(X_train_scaled), torch.FloatTensor(y_train).view(-1, 1)), 
    batch_size=128, shuffle=True
)
test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Model Architecture
# ==========================================
class FraudNet(nn.Module):
    def __init__(self, input_dim):
        super(FraudNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x)

# ==========================================
# 4. Training Function
# ==========================================
model = FraudNet(X_train.shape[1])

# CRITICAL: We pass pos_weight to heavily penalize missing the 5% Fraud cases.
# Without this, the model just predicts 0 (Legit) every time to get 95% accuracy.
pos_weight = torch.tensor([(y_train == 0).sum() / (y_train == 1).sum()])
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

optimizer = optim.Adam(model.parameters(), lr=1e-3)

print("\nTraining Model...")
epochs = 15
for epoch in range(epochs):
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch_X), batch_y)
        loss.backward()
        optimizer.step()

# ==========================================
# 5. Production Evaluation (The right way)
# ==========================================
print("\n--- Model Evaluation ---\n")
model.eval()
with torch.no_grad():
    test_logits = model(test_tensor)
    test_probs = torch.sigmoid(test_logits).numpy().flatten()
    
y_true = y_test_tensor.numpy().flatten()

# 1. Why Accuracy is a Lie
naive_preds = np.zeros_like(y_true)
print(f"Naive Baseline Accuracy (Predict everything is Legit): {(naive_preds == y_true).mean()*100:.2f}%\n")

# 2. Evaluate with Default Threshold (0.5)
default_preds = (test_probs >= 0.5).astype(int)
print("=== Default Threshold (0.5) ===")
print("Confusion Matrix:")
print(confusion_matrix(y_true, default_preds))
print("\nClassification Report:")
print(classification_report(y_true, default_preds, target_names=['Legit', 'Fraud']))

# 3. Evaluate with Adjusted Threshold (Optimize for Recall)
# Let's say a False Negative (missed fraud) costs $1,000.
# A False Positive (annoying a legit customer) costs $5.
# We want to catch ALMOST ALL fraud, so we lower the threshold.
custom_threshold = 0.2
custom_preds = (test_probs >= custom_threshold).astype(int)

print(f"\n=== Custom Threshold ({custom_threshold}) ===")
print("Confusion Matrix:")
print(confusion_matrix(y_true, custom_preds))
print("\nClassification Report:")
print(classification_report(y_true, custom_preds, target_names=['Legit', 'Fraud']))

# 4. Global Metric
print("\nROC-AUC Score (Evaluates raw probabilities, independent of threshold):")
print(f"{roc_auc_score(y_true, test_probs):.4f}")
