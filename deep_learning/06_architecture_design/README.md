# Module 6: Neural Network Architecture Design

## 1. Industry Explanation
Architecture design is the process of deciding the physical structure of your neural network: how many layers (depth), how many neurons per layer (width), and how those layers connect. 

In academia, researchers spend years inventing novel architectures (like ResNet or Transformers) to beat benchmarks by 0.1%. In industry, **Applied AI Engineers rarely invent new architectures from scratch**. Instead, they:
1. Start with known, proven baseline architectures for their specific data modality (e.g., MLPs for Tabular data, ResNet for Images, BERT for Text).
2. Tune the **Depth** and **Width** based on the complexity of the dataset and the latency requirements of production inference.
3. Add structural components like Batch Normalization and skip connections to stabilize training.

---

## 2. Why It Matters (The Business Context)
Choosing the right architecture is a balancing act between **Capacity** (the model's ability to learn complex patterns), **Compute Cost** (how expensive it is to train and run), and **Latency** (how fast it makes predictions).

If you deploy a 150-layer massive neural network to recommend products to users on a website, it might be highly accurate, but if it takes 500ms to return a prediction, users will leave the site before the page loads. The business loses money. An MLE must design an architecture that maximizes accuracy while staying strictly under a latency SLA (Service Level Agreement, e.g., < 50ms per request).

---

## 3. Python Example (Theory / Conceptual)
*Calculating the number of trainable parameters. A larger network has more capacity but requires more data to avoid overfitting.*

```python
def calculate_parameters(input_dim, hidden1, hidden2, output_dim):
    # Weights + Biases for each layer
    layer1_params = (input_dim * hidden1) + hidden1
    layer2_params = (hidden1 * hidden2) + hidden2
    output_params = (hidden2 * output_dim) + output_dim
    
    total = layer1_params + layer2_params + output_params
    return total

print(f"Small Network Params: {calculate_parameters(50, 64, 32, 1)}")
# Output: 5,345
print(f"Deep Network Params:  {calculate_parameters(50, 1024, 512, 1)}")
# Output: 577,537 (100x more expensive to train)
```

---

## 4. PyTorch Example (Production Grade)
*A scalable, parameterized architecture factory pattern used in industry codebases.*

```python
import torch
import torch.nn as nn

class DynamicMLP(nn.Module):
    def __init__(self, input_dim, hidden_layers, output_dim, dropout_rate=0.3):
        super(DynamicMLP, self).__init__()
        
        layers = []
        current_dim = input_dim
        
        # Iteratively build the architecture based on a list of hidden dimensions
        # Example hidden_layers: [512, 256, 128]
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            current_dim = hidden_dim
            
        # Final output layer
        layers.append(nn.Linear(current_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x)

# Instantiating a "Wide" vs "Deep" network
wide_model = DynamicMLP(100, [1024, 1024], 1)
deep_model = DynamicMLP(100, [256, 128, 64, 32, 16], 1)
```

---

## 5. Business Use Case
**Employee Attrition Prediction (HR Analytics)**
A large enterprise wants to predict which high-performing employees are likely to quit in the next 6 months. The dataset has only 10,000 rows (employees) but 150 features (salary, tenure, manager reviews, commute distance). 

The initial MLE team built a massive architecture: `[1024, 512, 256]`. The model had 700,000 parameters and completely memorized the 10,000 rows, performing terribly in production. 

A Senior Engineer redesigned the architecture using an industry rule of thumb for tabular data: a "Funnel" architecture that starts slightly larger than the input dimension and halves at each step: `[256, 128, 64]`. This reduced the parameters by 90%, forcing the network to compress the data into meaningful representations (a bottleneck), which drastically improved the model's ability to predict real-world attrition.

---

## 6. Mini Project: Architecture Tuning
Run the accompanying script `architecture_tuning.py`.
This script attempts to solve a classification problem using three different architectural paradigms:
1. **Under-parameterized**: Too small to learn the complex patterns.
2. **Over-parameterized (Too Wide)**: Massive capacity, prone to overfitting if not regulated heavily.
3. **Funnel Architecture (Industry Standard)**: Balanced capacity that compresses features effectively.

**To run:**
```bash
python architecture_tuning.py
```

---

## 7. Production Considerations
- **Depth vs Width**: For tabular data (Excel-style data), deeper is rarely better. Most tabular MLPs max out at 2 to 4 hidden layers. For unstructured data (Images, Text), depth is crucial for learning hierarchical features (e.g., Edges -> Shapes -> Faces).
- **Batch Normalization**: Always place `nn.BatchNorm1d` *before* the activation function in dense layers. It normalizes the inputs to the activation, ensuring gradients don't vanish or explode, which allows you to use much deeper architectures safely.

---

## 8. Common Failures
1. **Curse of Dimensionality in Linear Layers**: If you flatten a $224 \times 224$ image, your input dimension is 50,176. A single dense hidden layer of 1024 neurons will create $50,176 \times 1024 = 51,380,224$ parameters in just *one layer*. This is why we never use standard MLPs for images, and instead use Convolutional Neural Networks (CNNs) which share weights.
2. **Information Bottlenecks**: If you compress your architecture too quickly (e.g., `input(500) -> hidden(4) -> hidden(256)`), the network loses all information in the tiny middle layer and can never recover it, leading to a permanent stall in training.

---

## 9. Debugging Techniques
If your model's training loss won't go down:
1. **Check Capacity**: Your architecture might be too small. Double the width of your hidden layers and see if it can overfit a single batch.
2. **Check for Bottlenecks**: Ensure you don't have a layer that is suspiciously small early in the network.
3. **Add Batch Norm**: If the network is deep (4+ layers), vanishing gradients might be preventing the first few layers from learning. Adding Batch Normalization fixes this 90% of the time.

---

## 10. Interview Questions

**Q1: How do you decide on the number of hidden layers and neurons for a completely new tabular dataset?**
*Answer*: "I don't guess. I start with a proven baseline: a 2 or 3-layer funnel architecture (e.g., if input is 100, hidden layers of 128 -> 64 -> 32). I run a quick training loop. If the model severely underfits, I increase capacity. If it overfits, I increase regularization. I let the empirical validation metrics drive the architectural choices."

**Q2: What is the purpose of Batch Normalization in deep architectures?**
*Answer*: "It addresses Internal Covariate Shift. As weights update in earlier layers, the distribution of inputs to later layers changes constantly, slowing down training. Batch Norm standardizes the outputs of a layer to have a mean of 0 and variance of 1 across the mini-batch, which smooths the loss landscape, allows for higher learning rates, and acts as a mild regularizer."

**Q3: When would you choose a 'Wide' architecture over a 'Deep' architecture?**
*Answer*: "Wide architectures (fewer layers, many neurons) are great for memorizing highly sparse, linear relationships, often used in recommendation systems (like YouTube's Wide & Deep model). Deep architectures (many layers, fewer neurons) are necessary when you need to learn hierarchical, compositional features, like in computer vision or natural language processing."
