import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import numpy as np

# ==========================================
# 1. Configuration & Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Customer Support Ticket Routing)
# ==========================================
print("Generating synthetic Support Ticket Routing data...")
# Simulating 5,000 text embeddings (e.g., from BERT) classifying into 4 support departments
# Departments: 0: Billing, 1: Technical Support, 2: Sales, 3: Account Recovery
n_classes = 4
X, y = make_classification(n_samples=5000, n_features=50, n_informative=40, 
                           n_classes=n_classes, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_tensor = torch.FloatTensor(X_train_scaled)
# CRITICAL: CrossEntropyLoss expects target labels to be LongTensors of class indices (0 to C-1)
y_train_tensor = torch.LongTensor(y_train) 
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.LongTensor(y_test)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# ==========================================
# 3. Model Architecture
# ==========================================
class TicketRouterDNN(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(TicketRouterDNN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.4),
            
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.4),
            
            # Output layer neurons must equal num_classes
            nn.Linear(64, num_classes) 
            # Note: No Softmax here! CrossEntropyLoss handles it internally.
        )
        
    def forward(self, x):
        return self.net(x)

model = TicketRouterDNN(input_dim=X_train.shape[1], num_classes=n_classes)

# ==========================================
# 4. Loss & Optimizer
# ==========================================
# CrossEntropyLoss expects raw unnormalized logits
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001)

# ==========================================
# 5. Training Loop
# ==========================================
epochs = 20
print("\nStarting Training...")
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
        
    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss/len(train_loader):.4f}")

# ==========================================
# 6. Evaluation
# ==========================================
print("\nStarting Evaluation...")
model.eval()
with torch.no_grad():
    test_logits = model(X_test_tensor)
    
    # In multi-class, we take the index of the highest logit as the predicted class
    # torch.argmax returns the index of the maximum value along the specified dimension (dim=1)
    test_preds = torch.argmax(test_logits, dim=1)

# Generate detailed classification report
target_names = ['Billing', 'Technical Support', 'Sales', 'Account Recovery']
print("\nClassification Report:")
print(classification_report(y_test, test_preds.numpy(), target_names=target_names))
print("Success: End-to-end multi-class classification model trained and evaluated!")
