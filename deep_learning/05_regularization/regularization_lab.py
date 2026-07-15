import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import copy

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Noisy Data to force overfitting)
# ==========================================
print("Generating noisy dataset designed to cause overfitting...")
# We use only 1000 samples, but 100 features with lots of noise to encourage memorization.
X, y = make_classification(n_samples=1000, n_features=100, n_informative=10, 
                           n_redundant=0, n_classes=2, flip_y=0.1, random_state=42)

# We need a Validation set to monitor for Early Stopping
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.25, random_state=42) # 0.25 x 0.8 = 0.2

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

train_loader = DataLoader(TensorDataset(torch.FloatTensor(X_train_scaled), torch.FloatTensor(y_train).view(-1, 1)), batch_size=32, shuffle=True)
val_tensor = torch.FloatTensor(X_val_scaled)
y_val_tensor = torch.FloatTensor(y_val).view(-1, 1)
test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Architectures (Overfitter vs Regularized)
# ==========================================
class UnregularizedNet(nn.Module):
    def __init__(self, input_dim):
        super(UnregularizedNet, self).__init__()
        # Massive capacity, no dropout
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
    def forward(self, x):
        return self.net(x)

class RegularizedNet(nn.Module):
    def __init__(self, input_dim):
        super(RegularizedNet, self).__init__()
        # Same capacity, but with Dropout
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.5), # 50% Dropout
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 1)
        )
    def forward(self, x):
        return self.net(x)

# ==========================================
# 4. Training Function with Early Stopping
# ==========================================
def train_and_evaluate(model_type, use_weight_decay=False, use_early_stopping=False):
    print(f"\n--- Training {model_type} (Weight Decay: {use_weight_decay}, Early Stopping: {use_early_stopping}) ---")
    
    if model_type == 'Unregularized':
        model = UnregularizedNet(X_train.shape[1])
    else:
        model = RegularizedNet(X_train.shape[1])
        
    criterion = nn.BCEWithLogitsLoss()
    
    # Weight Decay is applied here
    wd = 1e-2 if use_weight_decay else 0.0
    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=wd)
    
    epochs = 40
    best_val_loss = float('inf')
    best_model_weights = copy.deepcopy(model.state_dict())
    patience = 5
    patience_counter = 0
    stopped_epoch = epochs
    
    for epoch in range(epochs):
        # TRAIN
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            
        # VALIDATE
        model.eval()
        with torch.no_grad():
            val_logits = model(val_tensor)
            val_loss = criterion(val_logits, y_val_tensor).item()
            
            # Calculate Training Loss for monitoring gap
            train_logits = model(torch.FloatTensor(X_train_scaled))
            train_loss = criterion(train_logits, torch.FloatTensor(y_train).view(-1, 1)).item()
            
        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch {epoch+1:02d}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
            
        # EARLY STOPPING LOGIC
        if use_early_stopping:
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_model_weights = copy.deepcopy(model.state_dict())
                patience_counter = 0
            else:
                patience_counter += 1
                
            if patience_counter >= patience:
                print(f"-> Early stopping triggered at epoch {epoch+1}! Restoring best weights.")
                model.load_state_dict(best_model_weights)
                stopped_epoch = epoch + 1
                break
                
    # TEST EVALUATION
    model.eval()
    with torch.no_grad():
        test_logits = model(test_tensor)
        test_preds = (torch.sigmoid(test_logits) >= 0.5).float()
        test_acc = (test_preds == y_test_tensor).float().mean().item()
        
        train_logits = model(torch.FloatTensor(X_train_scaled))
        train_preds = (torch.sigmoid(train_logits) >= 0.5).float()
        train_acc = (train_preds == torch.FloatTensor(y_train).view(-1, 1)).float().mean().item()
        
    print(f"Final Train Accuracy: {train_acc*100:.2f}%")
    print(f"Final Test Accuracy:  {test_acc*100:.2f}%")
    print(f"Generalization Gap:   {(train_acc - test_acc)*100:.2f}% (Lower is better)")

# ==========================================
# 5. Experiment Execution
# ==========================================
if __name__ == "__main__":
    # 1. Unregularized (Will overfit massively: Train 100%, Test ~65%)
    train_and_evaluate('Unregularized', use_weight_decay=False, use_early_stopping=False)
    
    # 2. Regularized with Dropout and Weight Decay (Closes the generalization gap)
    train_and_evaluate('Regularized', use_weight_decay=True, use_early_stopping=False)
    
    # 3. Regularized + Early Stopping (Prevents training from continuing when validation starts degrading)
    train_and_evaluate('Regularized', use_weight_decay=True, use_early_stopping=True)
