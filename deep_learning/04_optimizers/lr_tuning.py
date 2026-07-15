import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
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
# 2. Data Pipeline (Customer Segmentation)
# ==========================================
print("Generating highly sparse Customer Segmentation data...")
# We use 500 features to simulate sparse user event logs (e.g., clicked_button_X)
X, y = make_classification(n_samples=8000, n_features=500, n_informative=20, 
                           n_classes=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1)
train_dataset = TensorDataset(train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)

test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Model Architecture
# ==========================================
class SegmentationNet(nn.Module):
    def __init__(self, input_dim):
        super(SegmentationNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )
        
    def forward(self, x):
        return self.net(x)

# ==========================================
# 4. Training Function with Optimizer Choice
# ==========================================
def train_model(optimizer_name, lr):
    print(f"\n--- Training with {optimizer_name} (Initial LR={lr}) ---")
    model = SegmentationNet(X_train.shape[1])
    criterion = nn.BCEWithLogitsLoss()
    
    if optimizer_name == 'SGD':
        optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
        scheduler = None
    elif optimizer_name == 'Adam':
        optimizer = optim.Adam(model.parameters(), lr=lr)
        scheduler = None
    elif optimizer_name == 'AdamW_with_Scheduler':
        optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
        # Reduce LR by factor of 0.5 if loss plateaus for 2 epochs
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2, verbose=True)
    
    epochs = 15
    start_time = time.time()
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            
        avg_loss = epoch_loss / len(train_loader)
        
        # Step the scheduler if it exists
        if scheduler:
            scheduler.step(avg_loss)
            
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f}")
            
    training_time = time.time() - start_time
    
    # Evaluation
    model.eval()
    with torch.no_grad():
        test_logits = model(test_tensor)
        test_preds = (torch.sigmoid(test_logits) >= 0.5).float()
        acc = (test_preds == y_test_tensor).float().mean().item()
        
    print(f"Time Taken: {training_time:.2f}s")
    print(f"Final Test Accuracy: {acc*100:.2f}%")

# ==========================================
# 5. Experiment Execution
# ==========================================
if __name__ == "__main__":
    # 1. Standard SGD (Struggles with sparse features without heavy tuning)
    train_model('SGD', lr=0.01)
    
    # 2. Adam (Standard default, fast convergence)
    train_model('Adam', lr=0.001)
    
    # 3. AdamW with LR Scheduler (Industry Best Practice)
    train_model('AdamW_with_Scheduler', lr=0.01)
