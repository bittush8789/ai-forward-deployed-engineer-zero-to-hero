import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Data Pipeline (Simulated Sequential Text)
# ==========================================
print("Generating simulated text sequences for Sentiment Analysis...")
# Imagine we have a vocabulary of 5,000 words.
# We simulate 2,000 sentences, where each sentence has exactly 20 words (already padded).
# The integers represent word IDs (e.g., 4 = "good", 129 = "terrible").
vocab_size = 5000
seq_length = 20
num_samples = 2000

# Generate random sequences of word IDs
X_train_seq = torch.randint(0, vocab_size, (num_samples, seq_length))

# Generate random binary labels (0 = Negative Sentiment, 1 = Positive Sentiment)
y_train_labels = torch.randint(0, 2, (num_samples, 1)).float()

train_loader = DataLoader(
    TensorDataset(X_train_seq, y_train_labels), 
    batch_size=64, 
    shuffle=True
)

# ==========================================
# 3. Vanilla RNN Architecture
# ==========================================
class SentimentRNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SentimentRNN, self).__init__()
        
        # 1. Embed the integer words into dense vectors
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
        
        # 2. The Recurrent layer
        # batch_first=True makes input/output tensors shape [batch_size, seq_len, features]
        self.rnn = nn.RNN(input_size=embedding_dim, hidden_size=hidden_dim, batch_first=True)
        
        # 3. Classifier Head (Takes the final memory state)
        self.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim)
        )
        
    def forward(self, text_sequence):
        # 1. Embedding [batch_size, seq_len] -> [batch_size, seq_len, embed_dim]
        embedded = self.embedding(text_sequence)
        
        # 2. RNN [batch_size, seq_len, embed_dim] -> output, hidden
        # output contains the memory state for EVERY word in the sequence
        # hidden contains the memory state ONLY for the very last word
        output, hidden = self.rnn(embedded)
        
        # 3. We extract the hidden state. 
        # hidden shape is [num_layers, batch_size, hidden_dim]
        # We squeeze the num_layers dimension (since it's just 1 layer)
        final_memory = hidden.squeeze(0)
        
        # 4. Predict
        return self.fc(final_memory)

# ==========================================
# 4. Training Loop (With Gradient Clipping)
# ==========================================
model = SentimentRNN(vocab_size=vocab_size, embedding_dim=128, hidden_dim=64, output_dim=1)
optimizer = optim.AdamW(model.parameters(), lr=1e-3)
criterion = nn.BCEWithLogitsLoss()

epochs = 5
print("\nStarting Vanilla RNN Training...")
print("WARNING: Vanilla RNNs suffer from vanishing gradients on long sequences. This is just for educational purposes.")

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
        
        # CRITICAL: Gradient Clipping for RNNs
        # This prevents the 'Exploding Gradient' problem inherent to recurrent loops
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
        
        optimizer.step()
        
        running_loss += loss.item()
        
        # Metrics
        preds = (torch.sigmoid(logits) >= 0.5).float()
        correct += (preds == batch_y).sum().item()
        total += batch_y.size(0)
        
    acc = correct / total
    print(f"Epoch {epoch+1:02d}/{epochs} | Loss: {running_loss/len(train_loader):.4f} | Accuracy: {acc*100:.2f}%")

print("\nSuccess: RNN sequence pipeline executed.")
print("In reality, you would replace nn.RNN with nn.LSTM for any production workload.")
