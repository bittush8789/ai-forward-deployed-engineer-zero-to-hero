import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import torchvision.models as models
import numpy as np

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Simulating Image Batches)
# ==========================================
print("Generating synthetic image batches for Defect Detection...")
# Simulating a batch of 128 images. 
# PyTorch expects shape: [Batch_Size, Channels, Height, Width]
# Standard ResNet expects 3 channels (RGB) and 224x224 images.
batch_size = 128
X_train_images = torch.randn(batch_size, 3, 224, 224) 

# Simulating labels: 0 (Normal), 1 (Defect)
y_train_labels = torch.randint(0, 2, (batch_size, 1)).float()

train_loader = DataLoader(
    TensorDataset(X_train_images, y_train_labels), 
    batch_size=32, 
    shuffle=True
)

# ==========================================
# 3. Transfer Learning Architecture
# ==========================================
print("Loading ResNet18 Architecture...")
# IN PRODUCTION: Use weights=models.ResNet18_Weights.IMAGENET1K_V1
# For this lab simulation, we use weights=None to avoid massive internet downloads.
model = models.resnet18(weights=None)

# Step 1: Freeze all layers in the base model
for param in model.parameters():
    param.requires_grad = False
    
# Step 2: Replace the final Fully Connected (fc) layer
# ResNet18's original head has `in_features=512`
num_features = model.fc.in_features

# We replace it with a new, UNFREEZEN head for our binary classification task
model.fc = nn.Sequential(
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 1) # 1 Output for Binary Classification (Defect vs No Defect)
)

# Verify which parameters are trainable
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"Total Parameters: {total_params:,}")
print(f"Trainable Parameters: {trainable_params:,} (Only the new head!)")

# ==========================================
# 4. Training Loop (Fine-Tuning)
# ==========================================
# CRITICAL: We only pass model.fc.parameters() to the optimizer.
# Passing model.parameters() would waste CPU/GPU cycles trying to update frozen weights.
optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)
criterion = nn.BCEWithLogitsLoss()

epochs = 5
print("\nStarting Transfer Learning Fine-Tuning...")

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        
        # Forward pass
        logits = model(batch_X)
        loss = criterion(logits, batch_y)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        # Metrics
        preds = (torch.sigmoid(logits) >= 0.5).float()
        correct += (preds == batch_y).sum().item()
        total += batch_y.size(0)
        
    acc = correct / total
    print(f"Epoch {epoch+1:02d}/{epochs} | Loss: {running_loss/len(train_loader):.4f} | Accuracy: {acc*100:.2f}%")

print("\nSuccess: Transfer Learning pipeline executed.")
print("The model's convolutional base remained frozen, while the new head learned to classify the synthetic data.")
