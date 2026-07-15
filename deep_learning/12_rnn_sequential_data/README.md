# Module 12: Recurrent Neural Networks (Sequential Data)

## 1. Industry Explanation
Standard Neural Networks (MLPs) and CNNs assume that all inputs are independent of each other. They have no concept of "Time" or "Order". If you feed the sentence *"I am not happy, I am sad"* into an MLP, it just sees the words as a bag of features. It doesn't know that "not" comes right before "happy", reversing its meaning.

**Recurrent Neural Networks (RNNs)** are designed for Sequential Data (Text, Time-Series, Audio, User Clickstreams). They have an internal "Memory" (Hidden State). As they process a sequence step-by-step, they update this hidden state, passing information from the past into the present calculation.

**Industry Shift:** 
While vanilla RNNs were groundbreaking, **they are almost never used in modern production systems today** due to severe limitations (vanishing gradients over long sequences). They have been completely replaced by LSTMs, GRUs, and Transformers. However, understanding the core RNN concept (the hidden state loop) is mandatory for passing MLE interviews and understanding why LSTMs/Transformers exist.

---

## 2. Why It Matters (The Business Context)
Before RNNs/LSTMs, businesses analyzed text using "Bag of Words" or TF-IDF. This worked for simple spam filters, but failed miserably on complex sentiment analysis. 
Consider a customer review: *"The food was incredibly slow to arrive, though I suppose the taste was okay."* 
A simple model sees "incredibly", "okay", and "taste", and predicts positive sentiment. An RNN reads it sequentially, maintaining the context of "slow to arrive", allowing it to correctly classify it as a negative, frustrating experience.

---

## 3. Python Example (Theory / Conceptual)
*The core loop of a Recurrent Neural Network.*

```python
import numpy as np

# Sequential Input: 3 words, each represented by a 2D embedding vector
word_embeddings = [
    np.array([0.1, 0.5]), # Word 1: "I"
    np.array([0.9, -0.2]), # Word 2: "am"
    np.array([0.4, 0.8])  # Word 3: "sad"
]

# Initialize Hidden State (Memory) to zeros
hidden_state = np.array([0.0, 0.0])

# Weights
W_x = np.array([[0.5, 0.2], [0.1, 0.8]]) # Weight for input
W_h = np.array([[0.4, 0.6], [0.3, 0.7]]) # Weight for previous hidden state

def tanh_activation(x):
    return np.tanh(x)

# The Recurrent Loop
for t, word in enumerate(word_embeddings):
    # The new hidden state is a combination of the Current Word AND the Previous Memory
    combined = np.dot(word, W_x) + np.dot(hidden_state, W_h)
    hidden_state = tanh_activation(combined)
    print(f"Time Step {t} Memory: {hidden_state}")

print("Final Output sent to classifier:", hidden_state)
```

---

## 4. PyTorch Example (Production Grade)
*Implementing a text classification RNN using PyTorch `nn.RNN` and `nn.Embedding`.*

```python
import torch
import torch.nn as nn

class SimpleTextRNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SimpleTextRNN, self).__init__()
        
        # 1. Embedding Layer: Converts integer word IDs into dense vectors
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # 2. RNN Layer: batch_first=True makes inputs [batch, seq_len, features]
        self.rnn = nn.RNN(embedding_dim, hidden_dim, batch_first=True)
        
        # 3. Classifier Head
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, text_sequence):
        # text_sequence shape: [batch_size, sequence_length]
        
        # embedded shape: [batch_size, sequence_length, embedding_dim]
        embedded = self.embedding(text_sequence)
        
        # output contains the hidden states for ALL time steps
        # hidden contains ONLY the final time step's hidden state
        output, hidden = self.rnn(embedded)
        
        # We only care about the final hidden state to make our classification
        # hidden shape is [num_layers, batch_size, hidden_dim]. We squeeze it to [batch_size, hidden_dim]
        final_memory = hidden.squeeze(0)
        
        return self.fc(final_memory)
```

---

## 5. Business Use Case
**Chat Message Classification (Trust & Safety)**
A gaming company needs to filter highly toxic messages in real-time chat. A traditional model flagged the word "kill" automatically. Players typing *"I need to kill the boss in the next room"* were being banned unfairly (False Positives).

The MLE team trained an RNN on the sequence of words. The RNN learned that the context of "the boss" or "a monster" coming after the word "kill" neutralized the toxicity. By capturing the sequence, False Positives dropped by 80%, drastically reducing the number of angry support tickets from banned players.

---

## 6. Mini Project: Sentiment Analysis Pipeline
Run the accompanying script `sentiment_analysis.py`.
This script simulates text processing for an RNN:
1. It simulates tokenizing words into integer IDs.
2. It passes the sequences through an Embedding layer.
3. It trains a Vanilla RNN on the sequence.

**To run:**
```bash
python sentiment_analysis.py
```

---

## 7. Production Considerations
- **Padding and Packing**: Sequences in a batch are rarely the same length (e.g., one review is 5 words, another is 50). In PyTorch, you must pad the short ones with `0`s to make a perfect rectangle tensor. However, computing the RNN on 45 zeros wastes GPU time. In production, you use `torch.nn.utils.rnn.pack_padded_sequence` to tell PyTorch to skip the padding during calculation.
- **Out of Vocabulary (OOV)**: Users will inevitably type words the model has never seen (e.g., slang). The Embedding layer will crash if it receives an unknown ID. You must reserve an `<UNK>` token (e.g., ID 1) in your vocabulary, and map any unknown word to this ID during preprocessing.

---

## 8. Common Failures
1. **Vanishing Gradients in Time (The Death of Vanilla RNNs)**: If a sentence is 100 words long, the gradient has to backpropagate through 100 matrix multiplications. Because the activation function is `tanh` (values < 1), multiplying 100 fractions together results in $0.000000001$. The early words in the sentence receive no weight updates. The network develops "amnesia" and forgets the start of the sentence. **This is why we use LSTMs.**
2. **Exploding Gradients**: Occasionally, the multiplications result in numbers $> 1$, shooting the gradient to infinity (`NaN`). You must strictly use `torch.nn.utils.clip_grad_norm_` when training recurrent models.

---

## 9. Debugging Techniques
If your RNN predicts the exact same output regardless of the input sentence:
1. **Check your Hidden State slicing**: Are you accidentally passing the *first* hidden state to the classifier instead of the *last* hidden state? (e.g., doing `output[:, 0, :]` instead of `output[:, -1, :]`).
2. **Check sequence lengths**: If you padded your sequences to length 100, but a sentence was only 5 words long, the *last* hidden state will actually be the result of passing 95 zeros through the network. You must extract the hidden state exactly at the step before the padding starts.

---

## 10. Interview Questions

**Q1: Explain the Vanishing Gradient problem specifically in the context of Recurrent Neural Networks.**
*Answer*: "In an RNN, backpropagation happens 'through time' (BPTT). The gradient is multiplied by the same weight matrix for every time step in the sequence. If the largest singular value of this matrix is less than 1, the gradient decays exponentially as it travels back to earlier time steps. This prevents the network from learning long-term dependencies, as early words get zero gradient updates."

**Q2: What is an Embedding Layer and why is it better than One-Hot Encoding?**
*Answer*: "One-hot encoding represents a word as a massive vector of mostly zeros with a single 1 (e.g., size 50,000 for an English vocabulary). It is highly inefficient and treats all words as completely independent. An Embedding layer learns a dense, low-dimensional representation (e.g., size 256) where words with similar meanings are clustered together mathematically, allowing the network to generalize better."

**Q3: How do you handle batches of text where sentences are different lengths?**
*Answer*: "I pad the shorter sentences with a special `<PAD>` token so they form a rectangular tensor required for batch matrix operations. To ensure the model doesn't process or learn from the padding, I use PyTorch's `pack_padded_sequence` before passing it to the RNN, which optimizes the computation and ensures the hidden state is extracted at the true end of each sentence."
