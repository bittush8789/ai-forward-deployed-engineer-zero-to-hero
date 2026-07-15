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
# 2. Data Pipeline (Complex Tabular Data)
# ==========================================
print("Generating complex tabular data for Architecture comparison...")
# We use 10,000 samples and 50 features.
X, y = make_classification(n_samples=10000, n_features=50, n_informative=30, 
                           n_redundant=10, n_classes=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_loader = DataLoader(TensorDataset(torch.FloatTensor(X_train_scaled), torch.FloatTensor(y_train).view(-1, 1)), batch_size=128, shuffle=True)
test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Dynamic Architecture Factory
# ==========================================
class DynamicMLP(nn.Module):
    def __init__(self, input_dim, hidden_layers, output_dim=1, dropout=0.3):
        super(DynamicMLP, self).__init__()
        
        layers = []
        current_dim = input_dim
        
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            current_dim = hidden_dim
            
        layers.append(nn.Linear(current_dim, output_dim))
        self.network = nn.Sequential(*layers)
        
        # Calculate and print total parameters
        total_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print(f"Architecture: {hidden_layers} | Total Parameters: {total_params:,}")
        
    def forward(self, x):
        return self.network(x)

# ==========================================
# 4. Training Function
# ==========================================
def train_and_evaluate(name, hidden_layers):
    print(f"\n--- Training {name} ---")
    model = DynamicMLP(X_train.shape[1], hidden_layers)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    
    epochs = 15
    for epoch in range(epochs):
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            
    # Evaluation
    model.eval()
    with torch.no_grad():
        test_logits = model(test_tensor)
        test_preds = (torch.sigmoid(test_logits) >= 0.5).float()
        test_acc = (test_preds == y_test_tensor).float().mean().item()
        
    print(f"Final Test Accuracy: {test_acc*100:.2f}%")

# ==========================================
# 5. Experiment Execution
# ==========================================
if __name__ == "__main__":
    # 1. Under-parameterized (Too small, can't learn the complex 30 informative features)
    train_and_evaluate("Under-parameterized", [8, 4])
    
    # 2. Over-parameterized / Wide (Massive capacity, 10x slower to train, prone to overfitting)
    train_and_evaluate("Over-parameterized (Wide)", [1024, 1024])
    
    # 3. Funnel Architecture (Industry Standard for Tabular - Compresses features effectively)
    train_and_evaluate("Funnel Architecture (Industry Standard)", [128, 64, 32])
