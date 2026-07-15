import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (House Prices with Outliers)
# ==========================================
print("Generating synthetic House Price data...")
# 10,000 houses, 15 features (sqft, bedrooms, etc.)
X, y = make_regression(n_samples=10000, n_features=15, noise=0.1, random_state=42)

# Shift and scale y to look like real house prices (in $1000s)
y = (y - y.min()) / (y.max() - y.min()) * 500 + 100 # Range roughly $100k - $600k

# Introduce extreme outliers (e.g., Billionaire Mansions)
# These 50 houses are priced at $10,000k ($10M) to $50,000k ($50M)
outlier_indices = np.random.choice(len(y), 50, replace=False)
y[outlier_indices] = np.random.uniform(10000, 50000, 50)

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
class HousePricePredictor(nn.Module):
    def __init__(self, input_dim):
        super(HousePricePredictor, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            # Output layer: 1 neuron, NO activation (Regression)
            nn.Linear(32, 1)
        )
        
    def forward(self, x):
        return self.net(x)

# ==========================================
# 4. Training Function
# ==========================================
def train_and_evaluate(loss_function, name):
    print(f"\n--- Training with {name} ---")
    model = HousePricePredictor(X_train.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    epochs = 20
    for epoch in range(epochs):
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = loss_function(predictions, batch_y)
            loss.backward()
            optimizer.step()
            
    # Evaluation
    model.eval()
    with torch.no_grad():
        test_preds = model(test_tensor).numpy()
        
    y_true = y_test_tensor.numpy()
    
    # We evaluate both models using MAE to see how well they predict "normal" houses
    mae = mean_absolute_error(y_true, test_preds)
    rmse = np.sqrt(mean_squared_error(y_true, test_preds))
    
    print(f"Test MAE (Mean Error in $1000s): ${mae:.2f}k")
    print(f"Test RMSE: ${rmse:.2f}k")
    
    # Check predictions on normal houses vs outliers
    normal_mask = y_true < 1000
    outlier_mask = y_true >= 1000
    
    normal_mae = mean_absolute_error(y_true[normal_mask], test_preds[normal_mask])
    print(f"--> Error on NORMAL houses: ${normal_mae:.2f}k")
    
    if outlier_mask.sum() > 0:
        outlier_mae = mean_absolute_error(y_true[outlier_mask], test_preds[outlier_mask])
        print(f"--> Error on OUTLIER houses: ${outlier_mae:.2f}k")

# ==========================================
# 5. Experiment Execution
# ==========================================
if __name__ == "__main__":
    print("Notice how MSE ruins predictions for normal houses because it over-optimizes for the $50M mansions.")
    
    # 1. MSE Loss
    train_and_evaluate(nn.MSELoss(), "MSELoss (L2)")
    
    # 2. MAE Loss
    train_and_evaluate(nn.L1Loss(), "L1Loss (MAE)")
    
    # 3. Huber Loss (Best of both worlds)
    train_and_evaluate(nn.HuberLoss(delta=1.0), "HuberLoss (Robust)")
