import torch
import torch.nn as nn
import os
import time
import numpy as np

# ==========================================
# 1. Define the PyTorch Model
# ==========================================
class ProductionClassifier(nn.Module):
    def __init__(self):
        super(ProductionClassifier, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(20, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )
        
    def forward(self, x):
        return self.net(x)

# ==========================================
# 2. Export to ONNX (The Industry Standard)
# ==========================================
print("--- Step 1: Exporting PyTorch Model to ONNX ---")
model = ProductionClassifier()

# CRITICAL: Always set to eval before exporting!
model.eval()

# We need a dummy input tensor that matches the shape of our expected production data
# Batch Size: 1, Features: 20
dummy_input = torch.randn(1, 20)

onnx_filename = "classifier.onnx"

try:
    # Export the model
    torch.onnx.export(
        model,
        dummy_input,
        onnx_filename,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    print(f"Success: Model exported to {onnx_filename}")
    print(f"File Size: {os.path.getsize(onnx_filename) / 1024:.2f} KB\n")
except Exception as e:
    print(f"Warning: ONNX export failed (this is expected if running in a restricted environment). Error: {e}")


# ==========================================
# 3. Simulate High-Performance Inference
# ==========================================
print("--- Step 2: High-Performance ONNX Inference ---")

# We will simulate incoming API requests
num_requests = 100
test_data = np.random.randn(num_requests, 20).astype(np.float32)

try:
    import onnxruntime as ort
    
    if not os.path.exists(onnx_filename):
        raise FileNotFoundError(f"Missing {onnx_filename}")
        
    # Load the ONNX model into the highly optimized C++ runtime
    ort_session = ort.InferenceSession(onnx_filename)
    
    print("Executing 100 requests through ONNX Runtime...")
    start_time = time.time()
    
    for i in range(num_requests):
        # Extract 1 row for the API request
        request = test_data[i:i+1]
        
        # Run Inference
        # We must pass a dictionary mapping the 'input_name' to the NumPy array
        ort_inputs = {ort_session.get_inputs()[0].name: request}
        ort_outs = ort_session.run(None, ort_inputs)
        
    end_time = time.time()
    print(f"Success! Total Inference Time (100 requests): {(end_time - start_time)*1000:.2f} ms")
    print(f"Average Latency: {((end_time - start_time)*1000)/num_requests:.2f} ms per request")

except ImportError:
    print("\n[Simulation Mode]")
    print("The 'onnxruntime' library is not installed in this environment.")
    print("In a production environment, ONNX Runtime executes the static graph in C++,")
    print("often resulting in a 2x-5x speedup compared to running native PyTorch.")
    print("\nTo run this locally, install: pip install onnx onnxruntime")

# Clean up
if os.path.exists(onnx_filename):
    os.remove(onnx_filename)
