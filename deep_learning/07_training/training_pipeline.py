import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import time

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Generation (Simulating Retail Sales)
# ==========================================
print("Generating massive Retail Sales dataset (simulated)...")
# 50,000 days of sales data across various stores
X, y = make_regression(n_samples=50000, n_features=30, noise=0.1, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 3. Production DataLoaders
# ==========================================
# Create Tensors
train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1)

val_tensor = torch.FloatTensor(X_val_scaled)
y_val_tensor = torch.FloatTensor(y_val).view(-1, 1)

# Training Loader: 
# - batch_size=2048 (Large batch for GPU efficiency)
# - shuffle=True (Crucial for training)
# - drop_last=True (Drop incomplete final batch)
train_loader = DataLoader(
    TensorDataset(train_tensor, y_train_tensor), 
    batch_size=2048, 
    shuffle=True,
    drop_last=True
)

# Validation Loader:
# - batch_size=4096 (Can be 2x larger than train because no gradients are stored!)
# - shuffle=False (Saves CPU time, order doesn't matter for evaluation)
val_loader = DataLoader(
    TensorDataset(val_tensor, y_val_tensor), 
    batch_size=4096, 
    shuffle=False 
)

# ==========================================
# 4. Model Architecture
# ==========================================
class SalesForecaster(nn.Module):
    def __init__(self, input_dim):
        super(SalesForecaster, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 1) # Regression
        )
    def forward(self, x):
        return self.net(x)

# ==========================================
# 5. Production Training Loop
# ==========================================
model = SalesForecaster(X_train.shape[1])
criterion = nn.HuberLoss(delta=1.0)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)

epochs = 10
print("\nStarting Training Pipeline...")

# History dictionaries to simulate learning curves
history = {'train_loss': [], 'val_loss': []}

global_start_time = time.time()

for epoch in range(epochs):
    epoch_start_time = time.time()
    
    # --- TRAINING PHASE ---
    model.train()
    running_train_loss = 0.0
    
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        running_train_loss += loss.item()
        
    avg_train_loss = running_train_loss / len(train_loader)
    
    # --- VALIDATION PHASE ---
    model.eval()
    running_val_loss = 0.0
    
    with torch.no_grad(): # CRITICAL: Disables gradient tracking (saves memory/time)
        for val_inputs, val_targets in val_loader:
            val_outputs = model(val_inputs)
            v_loss = criterion(val_outputs, val_targets)
            running_val_loss += v_loss.item()
            
    avg_val_loss = running_val_loss / len(val_loader)
    
    # --- LOGGING ---
    history['train_loss'].append(avg_train_loss)
    history['val_loss'].append(avg_val_loss)
    
    epoch_time = time.time() - epoch_start_time
    print(f"Epoch {epoch+1:02d}/{epochs} | "
          f"Train Loss: {avg_train_loss:.2f} | "
          f"Val Loss: {avg_val_loss:.2f} | "
          f"Time: {epoch_time:.2f}s")

total_time = time.time() - global_start_time
print(f"\nPipeline Finished in {total_time:.2f}s")
print("Notice how the Validation Loss closely tracks the Train Loss, indicating a healthy model without overfitting.")
