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
# 2. Data Pipeline (Synthetic Data)
# ==========================================
print("Generating synthetic data for Activation Comparison...")
# We generate a complex, non-linear dataset
X, y = make_classification(n_samples=5000, n_features=20, n_informative=10, 
                           n_classes=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_dataset = TensorDataset(torch.FloatTensor(X_train_scaled), torch.FloatTensor(y_train).view(-1, 1))
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)

test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Model Architecture with Swappable Activations
# ==========================================
class ActivationTestNet(nn.Module):
    def __init__(self, activation_name):
        super(ActivationTestNet, self).__init__()
        
        # Select activation based on input
        if activation_name == 'Sigmoid':
            self.act = nn.Sigmoid()
        elif activation_name == 'ReLU':
            self.act = nn.ReLU()
        elif activation_name == 'LeakyReLU':
            self.act = nn.LeakyReLU(0.01)
        elif activation_name == 'GELU':
            self.act = nn.GELU()
        else:
            raise ValueError("Unknown activation")
            
        # A deep network to demonstrate vanishing gradients with Sigmoid
        self.net = nn.Sequential(
            nn.Linear(20, 128),
            self.act,
            nn.Linear(128, 128),
            self.act,
            nn.Linear(128, 64),
            self.act,
            nn.Linear(64, 32),
            self.act,
            nn.Linear(32, 1)
        )
        
        # Dead Neuron tracking
        self.dead_neurons_count = 0
        self.total_neurons_checked = 0
        
        # Register hook on the second hidden layer
        self.net[3].register_forward_hook(self.check_dead_neurons)

    def check_dead_neurons(self, module, input_tensor, output_tensor):
        # Count how many activations in this batch were exactly 0.0
        # (This applies mainly to ReLU)
        if isinstance(module, nn.ReLU):
            zeros = (output_tensor <= 0.0).float().sum().item()
            total = output_tensor.numel()
            self.dead_neurons_count += zeros
            self.total_neurons_checked += total

    def forward(self, x):
        return self.net(x)

# ==========================================
# 4. Training Function
# ==========================================
def train_and_evaluate(activation_name, lr=0.01):
    print(f"\n--- Training with {activation_name} (LR={lr}) ---")
    model = ActivationTestNet(activation_name)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    
    epochs = 15
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        
        # Reset dead neuron counters for the epoch
        model.dead_neurons_count = 0
        model.total_neurons_checked = 0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss/len(train_loader):.4f}")
            
    # Evaluation
    model.eval()
    with torch.no_grad():
        test_logits = model(test_tensor)
        test_preds = (torch.sigmoid(test_logits) >= 0.5).float()
        acc = (test_preds == y_test_tensor).float().mean().item()
        
    print(f"Final Test Accuracy: {acc*100:.2f}%")
    
    if activation_name == 'ReLU' and model.total_neurons_checked > 0:
        dead_pct = (model.dead_neurons_count / model.total_neurons_checked) * 100
        print(f"Estimated Dead Neurons (Layer 2): {dead_pct:.2f}%")

# ==========================================
# 5. Experiment Execution
# ==========================================
if __name__ == "__main__":
    # 1. Sigmoid - Suffers from Vanishing Gradients (Network is too deep)
    train_and_evaluate('Sigmoid', lr=0.1)
    
    # 2. ReLU with standard LR
    train_and_evaluate('ReLU', lr=0.01)
    
    # 3. ReLU with HIGH LR (Demonstrates Dying ReLU)
    train_and_evaluate('ReLU', lr=0.5)
    
    # 4. LeakyReLU with HIGH LR (Recovers from high LR better than ReLU)
    train_and_evaluate('LeakyReLU', lr=0.5)
    
    # 5. GELU (Modern standard)
    train_and_evaluate('GELU', lr=0.01)
