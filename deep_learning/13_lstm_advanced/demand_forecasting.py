import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import math

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Multivariate Time Series)
# ==========================================
print("Generating simulated Retail Time-Series Data...")

# Let's simulate 2 years of daily data (730 days) for 3 features:
# Feature 0: Temperature (seasonality)
# Feature 1: Marketing Spend (random spikes)
# Feature 2: Target (Sales)
days = 730
time = np.arange(days)
temperature = np.sin(time * (2 * np.pi / 365)) * 20 + 60 + np.random.normal(0, 2, days)
marketing = np.random.exponential(100, days)

# Sales are driven by temperature, marketing, and a general upward trend
sales = (temperature * 5) + (marketing * 1.5) + (time * 0.1) + np.random.normal(0, 10, days)

raw_data = np.stack([temperature, marketing, sales], axis=1)

# CRITICAL: CHRONOLOGICAL SPLIT (NO SHUFFLING)
# We train on the first 80%, test on the final 20%
split_idx = int(days * 0.8)
train_data_raw = raw_data[:split_idx]
test_data_raw = raw_data[split_idx:]

# CRITICAL: SCALE TARGETS TO [0, 1] (LSTMs use Tanh internally)
scaler = MinMaxScaler()
# We fit ONLY on the training data to prevent Lookahead Bias
train_scaled = scaler.fit_transform(train_data_raw)
test_scaled = scaler.transform(test_data_raw)

# The Sliding Window Function
def create_sequences(data, seq_length):
    X = []
    y = []
    # We stop at len(data) - seq_length so we always have a target
    for i in range(len(data) - seq_length):
        X.append(data[i : i+seq_length]) # All features for past N days
        y.append(data[i+seq_length, 2])  # Feature 2 (Sales) for the Next Day
    return np.array(X), np.array(y)

seq_length = 14 # Look back 2 weeks
X_train, y_train = create_sequences(train_scaled, seq_length)
X_test, y_test = create_sequences(test_scaled, seq_length)

train_loader = DataLoader(
    TensorDataset(torch.FloatTensor(X_train), torch.FloatTensor(y_train).view(-1, 1)),
    batch_size=32, shuffle=True
)
test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# ==========================================
# 3. Multivariate LSTM Architecture
# ==========================================
class DemandForecasterLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(DemandForecasterLSTM, self).__init__()
        
        # batch_first=True -> [batch_size, seq_len, features]
        self.lstm = nn.LSTM(
            input_size=input_dim, 
            hidden_size=hidden_dim, 
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # out shape: [batch, seq_len, hidden_dim]
        # hn shape: [num_layers, batch, hidden_dim]
        out, (hn, cn) = self.lstm(x)
        
        # Extract the hidden state of the LAST time step, from the LAST layer
        final_memory = hn[-1, :, :]
        
        return self.fc(final_memory)

# ==========================================
# 4. Training Loop
# ==========================================
# input_dim = 3 (Temp, Marketing, Sales)
model = DemandForecasterLSTM(input_dim=3, hidden_dim=64, num_layers=2, output_dim=1)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

epochs = 15
print("\nStarting LSTM Training (Multivariate Forecasting)...")

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)
        loss.backward()
        
        # Prevent Exploding Gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        running_loss += loss.item()
        
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1:02d}/{epochs} | MSE Loss: {running_loss/len(train_loader):.4f}")

# ==========================================
# 5. Evaluation & Inverse Scaling
# ==========================================
model.eval()
with torch.no_grad():
    test_preds_scaled = model(test_tensor).numpy()

# We need to invert the scaling to understand the error in Real Dollars/Units
# To inverse_transform, the scaler needs an array of the exact same shape it was fitted on (3 features).
# We create a dummy array, slot our predictions into the Sales column, and inverse transform.
dummy_array = np.zeros((len(test_preds_scaled), 3))
dummy_array[:, 2] = test_preds_scaled.flatten()
test_preds_real = scaler.inverse_transform(dummy_array)[:, 2]

dummy_array_true = np.zeros((len(y_test), 3))
dummy_array_true[:, 2] = y_test
y_test_real = scaler.inverse_transform(dummy_array_true)[:, 2]

# Calculate MAE in real units
mae = np.mean(np.abs(test_preds_real - y_test_real))
print(f"\nSuccess: LSTM trained and evaluated.")
print(f"Mean Absolute Error (in raw Sales Units): {mae:.2f}")
