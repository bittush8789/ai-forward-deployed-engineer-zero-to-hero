import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (WITH A DELIBERATE BUG)
# ==========================================
print("Generating data...")
X, y = make_classification(n_samples=5000, n_features=20, n_classes=2, random_state=42)

# --- THE BUG IS HERE ---
# A Junior Engineer tried to shuffle the data manually before splitting, 
# but they shuffled the features and labels INDEPENDENTLY.
# This breaks the relationship between X and y. The model will never learn.
np.random.shuffle(X)
np.random.shuffle(y)
# -----------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_loader = DataLoader(
    TensorDataset(torch.FloatTensor(X_train_scaled), torch.FloatTensor(y_train).view(-1, 1)), 
    batch_size=64, shuffle=True
)
test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Model Architecture
# ==========================================
class DebugNet(nn.Module):
    def __init__(self, input_dim):
        super(DebugNet, self).__init__()
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
# 4. Training Function (With Debugging Tools)
# ==========================================
model = DebugNet(X_train.shape[1])
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

epochs = 10
print("\nStarting Training... (Notice how accuracy is stuck around 50%)")

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        logits = model(batch_X)
        loss = criterion(logits, batch_y)
        loss.backward()
        
        # --- DEBUGGING TOOL 1: Check Gradients ---
        # Uncomment this to verify gradients are flowing correctly.
        # If gradients are healthy, the architecture is fine. The problem is the data.
        """
        for name, param in model.named_parameters():
            if param.grad is not None:
                grad_norm = param.grad.norm().item()
                if grad_norm == 0.0:
                    print(f"Warning: Dead Gradients in {name}")
                elif grad_norm > 100.0:
                    print(f"Warning: Exploding Gradients in {name}")
        """
        
        optimizer.step()
        running_loss += loss.item()
        
        preds = (torch.sigmoid(logits) >= 0.5).float()
        correct += (preds == batch_y).sum().item()
        total += batch_y.size(0)
        
    acc = correct / total
    print(f"Epoch {epoch+1:02d} | Loss: {running_loss/len(train_loader):.4f} | Accuracy: {acc*100:.2f}%")

print("\nDEBUGGING EXERCISE:")
print("1. The architecture is standard. The optimizer is standard.")
print("2. The loss goes down very slightly, but accuracy is exactly random (50%).")
print("3. This happens because the model is trying to learn, but there is no pattern to learn.")
print("4. Look at the 'Data Pipeline' section in the code to find and fix the independent shuffling bug.")
