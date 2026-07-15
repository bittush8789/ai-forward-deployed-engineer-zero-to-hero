import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score
import numpy as np

# ==========================================
# 1. Configuration & Reproducibility
# ==========================================
# In production, always set seeds so your training is reproducible.
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Synthetic Churn Data)
# ==========================================
print("Generating synthetic Customer Churn data...")
# Simulating a dataset of 10,000 customers, 20 features (usage metrics, tenure, etc.)
X, y = make_classification(n_samples=10000, n_features=20, n_informative=15, 
                           n_classes=2, weights=[0.8, 0.2], random_state=42)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CRITICAL: Neural Networks require scaled data. 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert numpy arrays to PyTorch Tensors
X_train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1) # Reshape to [batch_size, 1]
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# Create DataLoaders for batching
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# ==========================================
# 3. Model Architecture
# ==========================================
class ChurnPredictorDNN(nn.Module):
    def __init__(self, input_dim):
        super(ChurnPredictorDNN, self).__init__()
        # Dense network with Batch Normalization and Dropout for stability
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            # Output layer (1 neuron for binary classification)
            nn.Linear(32, 1) 
            # Note: No Sigmoid here! We output raw logits.
        )
        
    def forward(self, x):
        return self.net(x)

model = ChurnPredictorDNN(input_dim=X_train.shape[1])

# ==========================================
# 4. Loss & Optimizer
# ==========================================
# BCEWithLogitsLoss is numerically stable compared to Sigmoid + BCELoss
# We use pos_weight to handle the imbalanced dataset (20% churners)
pos_weight = torch.tensor([(y_train == 0).sum() / (y_train == 1).sum()])
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# AdamW optimizer is the industry standard (better weight decay than Adam)
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)

# ==========================================
# 5. Training Loop
# ==========================================
epochs = 20
print("\nStarting Training...")
for epoch in range(epochs):
    model.train() # Set model to training mode (enables Dropout/BatchNorm)
    epoch_loss = 0.0
    
    for batch_X, batch_y in train_loader:
        # 1. Zero gradients
        optimizer.zero_grad()
        
        # 2. Forward pass
        predictions = model(batch_X)
        
        # 3. Calculate Loss
        loss = criterion(predictions, batch_y)
        
        # 4. Backward pass (calculate gradients)
        loss.backward()
        
        # 5. Update weights
        optimizer.step()
        
        epoch_loss += loss.item()
        
    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss/len(train_loader):.4f}")

# ==========================================
# 6. Evaluation
# ==========================================
print("\nStarting Evaluation...")
model.eval() # Set to evaluation mode (disables Dropout/BatchNorm)
with torch.no_grad(): # Disable gradient calculation for speed & memory efficiency
    test_logits = model(X_test_tensor)
    
    # Convert logits to probabilities using Sigmoid
    test_probs = torch.sigmoid(test_logits)
    
    # Convert probabilities to binary predictions (threshold = 0.5)
    test_preds = (test_probs >= 0.5).float()

# Calculate Metrics
acc = accuracy_score(y_test, test_preds.numpy())
prec = precision_score(y_test, test_preds.numpy())
rec = recall_score(y_test, test_preds.numpy())

print(f"Test Accuracy:  {acc:.4f}")
print(f"Test Precision: {prec:.4f}")
print(f"Test Recall:    {rec:.4f}")
print("\nSuccess: End-to-end binary classification model trained and evaluated!")
