# Module 15: PyTorch in Production

## 1. Industry Explanation
PyTorch won the academic AI war. Almost 90% of AI research papers use PyTorch. Because of this, it is now the dominant framework in industry for training state-of-the-art models (like Llama-3). 

However, PyTorch's greatest strength (its dynamic, Python-first execution graph) is also its greatest weakness in production. Python is slow, and running heavy neural networks natively in Python via Flask/FastAPI is a bottleneck for high-traffic enterprise applications.

**The Industry Solution:**
In production, we decouple the training environment from the serving environment. We train the model in native PyTorch, but we serve it using specialized, high-performance engines like **TorchServe**, **ONNX Runtime**, or **TensorRT**.

---

## 2. Why It Matters (The Business Context)
Imagine you are building a recommendation engine for a streaming service. You train a massive PyTorch model.
If you deploy it naively using `Flask + torch.load()`, each recommendation might take 300ms. If you have 50,000 concurrent users, your AWS bill will skyrocket because you need thousands of servers to handle the load without crashing.

By exporting the PyTorch model to **ONNX (Open Neural Network Exchange)**, it is converted into a highly optimized C++ graph. Running that exact same model through ONNX Runtime reduces the latency to 30ms. You just increased your server throughput by 10x, saving the business millions of dollars in cloud compute costs.

---

## 3. Python Example (Theory / Conceptual)
*The fundamental building block of PyTorch: Autograd (Automatic Differentiation).*

```python
import torch

# In PyTorch, everything is a Tensor. 
# requires_grad=True tells PyTorch to track every mathematical operation on this tensor.
x = torch.tensor([2.0], requires_grad=True)

# We define a function (Forward Pass)
# y = 3x^2 + 4x + 2
y = 3 * (x ** 2) + 4 * x + 2

# We want to know the derivative of y with respect to x (dy/dx).
# dy/dx = 6x + 4. Evaluated at x=2, the gradient should be 6(2) + 4 = 16.

# Backward Pass (PyTorch does the calculus automatically)
y.backward()

# Print the gradient
print(f"Gradient dy/dx at x=2 is: {x.grad.item()}") # Output: 16.0
```
*In production inference, we DO NOT want this tracking happening. This is why we use `with torch.no_grad():` to save memory.*

---

## 4. PyTorch Example (Production Grade)
*Exporting a trained PyTorch model to ONNX for high-performance serving.*

```python
import torch
import torch.nn as nn

# 1. Define and train your model in PyTorch
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)
        
    def forward(self, x):
        return self.fc(x)

model = SimpleNet()
model.eval() # CRITICAL: Set to eval mode before exporting!

# 2. Create a "dummy" input tensor that matches the shape of your production data
# e.g., Batch Size 1, 10 Features
dummy_input = torch.randn(1, 10)

# 3. Export to ONNX
# PyTorch runs the dummy input through the model, traces the operations, and writes them to a C++ file.
torch.onnx.export(
    model,                      # The model being exported
    dummy_input,                # Model input (or a tuple for multiple inputs)
    "production_model.onnx",    # Where to save the file
    export_params=True,         # Store the trained weights inside the file
    opset_version=12,           # The ONNX version to use
    do_constant_folding=True,   # Optimizes constant operations for speed
    input_names=['input'],      # The model's input names
    output_names=['output'],    # The model's output names
    dynamic_axes={'input': {0: 'batch_size'},    # Allow variable batch sizes in production
                  'output': {0: 'batch_size'}}
)
print("Model successfully exported to ONNX format!")
```

---

## 5. Business Use Case
**AI Inference Platform (TorchServe)**
A retail company deployed 5 different PyTorch models (Demand Forecasting, Fraud Detection, Customer Churn, Recommendation, and Product Categorization).
Initially, each model was wrapped in its own custom FastAPI Docker container. The MLOps team was overwhelmed trying to manage 5 different codebases, scaling rules, and API endpoints.

They migrated to **TorchServe**, PyTorch's official production serving engine. TorchServe allows you to package the `.pth` files and deploy them behind a single, highly optimized, multi-threaded Java server. It automatically provides Health Checks, Metrics (Prometheus), Dynamic Batching (grouping requests together for GPU efficiency), and Model Versioning out of the box, standardizing the entire AI deployment process.

---

## 6. Mini Project: ONNX Export and Inference
Run the accompanying script `inference_platform.py`.
This script simulates the industry transition from Training to Production:
1. It creates a PyTorch model and exports it to ONNX.
2. It uses `onnxruntime` (a highly optimized C++ backend) to run inference on the ONNX file, bypassing Python's sluggishness.

**To run:**
```bash
# Requires: pip install onnx onnxruntime
python inference_platform.py
```

---

## 7. Production Considerations
- **TorchScript / JIT**: If you don't want to use ONNX, PyTorch has its own native optimization called TorchScript. You use `torch.jit.trace` or `torch.jit.script` to convert your Python code into a serialized format that can be loaded natively into C++ applications using `libtorch`.
- **Dynamic Batching**: If a GPU receives 1 request, it takes 10ms. If a GPU receives 32 requests in a batch, it takes 11ms. In production, you *must* use a serving layer that collects incoming API requests for ~20ms, groups them into a batch, sends them to the GPU once, and distributes the answers.

---

## 8. Common Failures
1. **Dynamic Control Flow in ONNX**: ONNX traces a static graph. If your PyTorch `forward()` function has a dynamic `if` statement (e.g., `if x.sum() > 0: do_something()`), `torch.onnx.export` will only trace the path that the *dummy_input* took. The other path will be permanently deleted from the production model. If you have dynamic control flow, you must use TorchScript (`torch.jit.script`) instead of ONNX.
2. **Device Mismatch**: When loading a `.pth` file saved on a GPU into a CPU server, PyTorch will crash. You must explicitly tell PyTorch to map the tensors to the CPU during loading: `torch.load("model.pth", map_location=torch.device('cpu'))`.

---

## 9. Interview Questions

**Q1: Why do we use ONNX instead of deploying native PyTorch models via Flask?**
*Answer*: "Native PyTorch models run in Python, which is subject to the Global Interpreter Lock (GIL) and is inherently slow. ONNX creates a standardized, static computation graph that can be executed by highly optimized, multi-threaded C++ runtimes (like ONNX Runtime or TensorRT). This significantly reduces inference latency and increases server throughput, reducing cloud costs."

**Q2: What is the difference between `model.train()` and `model.eval()`?**
*Answer*: "These methods toggle the behavior of specific layers like Dropout and Batch Normalization. `model.train()` ensures Dropout randomly zeroes out neurons and Batch Norm calculates new mini-batch statistics. `model.eval()` disables Dropout and forces Batch Norm to use the running statistics it learned during training. Forgetting `model.eval()` in production will completely corrupt your predictions."

**Q3: How do you handle a PyTorch model whose output shape depends on the input batch size when exporting to ONNX?**
*Answer*: "During the `torch.onnx.export` call, I would use the `dynamic_axes` parameter. I would specify that the 0th dimension (the batch size) for both the `input_names` and `output_names` is dynamic. This tells the ONNX runtime to accept variable batch sizes during production inference, rather than strictly expecting the exact batch size of the dummy input."
