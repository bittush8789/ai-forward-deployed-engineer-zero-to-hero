# Module 10: Production Neural Networks

## 1. Industry Explanation
Training a neural network is only 20% of the job. The remaining 80% is figuring out how to get that network to serve predictions to users reliably, securely, and cheaply.

In industry, there are two primary ways to deploy a Neural Network:
- **Batch Inference**: The model runs on a schedule (e.g., every midnight), predicting on millions of rows of data at once, and saves the predictions to a database (like Snowflake or BigQuery). Users then query the database, not the model. This is cheap and highly scalable.
- **Real-Time Inference (Online)**: The model is wrapped in an API (like FastAPI or Flask). When a user clicks a button, a request is sent to the API, the model makes a prediction in milliseconds, and returns it. This is expensive, complex, but necessary for things like Fraud Detection or TikTok recommendations.

---

## 2. Why It Matters (The Business Context)
If your model requires 5 seconds to run inference, and you deploy it as a Real-Time API for a mobile app, the users will uninstall your app. 
If you deploy a Real-Time API when you only actually needed Batch Inference (e.g., predicting Churn for tomorrow), you will spend $5,000/month keeping GPU servers online 24/7 waiting for requests, instead of $50/month spinning up a server for 1 hour at midnight. Designing the production architecture correctly saves the business massive amounts of money.

---

## 3. Python Example (Theory / Conceptual)
*The difference between Batch and Real-Time.*

```python
# 1. Batch Inference (e.g., Airflow Job at Midnight)
def run_batch_job(model, data_lake):
    new_users = data_lake.get_users_from_today()
    # Process 100,000 users at once (Highly efficient)
    predictions = model.predict(new_users, batch_size=1024)
    data_lake.save_predictions(predictions)

# 2. Real-Time Inference (e.g., FastAPI Endpoint)
def handle_api_request(model, user_json):
    # Process exactly 1 user on-demand (High overhead)
    features = extract_features(user_json)
    prediction = model.predict(features)
    return {"status": 200, "prediction": prediction}
```

---

## 4. PyTorch Example (Production Grade)
*Saving and Loading a PyTorch model properly for production.*

```python
import torch
import torch.nn as nn

model = nn.Linear(10, 1)

# 1. THE WRONG WAY (Pickling the entire object)
# If you refactor your code and move the class definition, this file breaks permanently.
torch.save(model, "bad_model.pth")

# 2. THE RIGHT WAY (Saving the State Dictionary)
# This only saves the raw weights (the numbers). It is robust and future-proof.
torch.save(model.state_dict(), "good_model.pth")

# --- In your Production Inference Server ---
# You must instantiate the architecture first, then load the weights into it.
prod_model = nn.Linear(10, 1)
prod_model.load_state_dict(torch.load("good_model.pth"))

# CRITICAL: Always set to eval mode before serving requests!
prod_model.eval()
```

---

## 5. Business Use Case
**Real-Time Price Estimation (Real Estate Platform)**
A real estate platform allows users to type in their house details to get an instant estimated sale price. The MLE team built a massive PyTorch model and deployed it via a Flask API on a CPU server. Because the model was so large, each request took 800ms. When the marketing team ran a Super Bowl ad, 10,000 users hit the API simultaneously. The server couldn't handle the sequential load and crashed, resulting in a blank screen for millions of viewers.

The team rebuilt the architecture using **FastAPI** (which handles asynchronous requests) and added **Dynamic Batching** (the API waits 50ms to collect multiple incoming requests, batches them together, sends the batch through the model once, and distributes the answers back). Inference time dropped to 80ms, and the server survived the next traffic spike effortlessly.

---

## 6. Mini Project: Production Neural Network API
Run the accompanying script `inference_api.py`.
This script simulates a production environment:
1. It defines a model and creates "fake" pre-trained weights.
2. It sets up a high-performance **FastAPI** server.
3. It exposes a `/predict` endpoint that takes JSON, converts it to a PyTorch Tensor, runs inference, and returns a JSON response.

**To run:**
```bash
# This requires uvicorn and fastapi: pip install fastapi uvicorn
python inference_api.py
```
*(Once running, you can test it by opening a new terminal and running the `curl` command printed in the console).*

---

## 7. Production Considerations
- **ONNX (Open Neural Network Exchange)**: In advanced production systems, you don't actually deploy PyTorch code. You export your PyTorch model to the ONNX format (`torch.onnx.export`). ONNX is a standardized, highly optimized C++ runtime that can run inference 2x-5x faster than native PyTorch on CPUs.
- **Monitoring (Model Drift)**: Your API must log every input it receives and every prediction it makes. After 3 months, user behavior might change (Data Drift). If you don't monitor the statistical distribution of the incoming API requests, your model will silently start making terrible predictions.

---

## 8. Common Failures
1. **Forgetting `torch.no_grad()`**: If your inference API does not use `with torch.no_grad():` during the forward pass, PyTorch will build a massive computational graph in RAM for every single user request, preparing for a backward pass that will never happen. The server will run out of memory and crash within an hour.
2. **Batch Size Mismatch**: During training, your batch size was 64. In real-time inference, your batch size is 1. If you used `nn.BatchNorm1d`, and you forget to call `model.eval()`, the layer will try to calculate the mean and variance of a single row, resulting in `NaN` or a division by zero error.

---

## 9. Debugging Techniques
If your API predictions don't match your Jupyter Notebook predictions:
1. **Check `model.eval()`**: Did you set the model to evaluation mode?
2. **Check the Scaler**: Are you applying the exact same `StandardScaler` (loaded from a `.pkl` file) in the API that you used during training? A neural network expects age to be `0.5`, not `35`. If you pass raw `35` to the API, the output will be garbage.
3. **Check Data Types**: Pandas might cast a boolean to an integer during training, while the JSON payload in the API passes a boolean. Ensure strict type checking in your API (e.g., using Pydantic).

---

## 10. Interview Questions

**Q1: What is the difference between `torch.save(model)` and `torch.save(model.state_dict())`?**
*Answer*: "`torch.save(model)` uses Python's pickle module to serialize the entire object, including the exact directory path and class structure. If you move or rename the file, it breaks. `torch.save(model.state_dict())` only saves a dictionary mapping each layer's name to its learned tensor weights. It is the industry standard because it's completely decoupled from the codebase structure."

**Q2: Why is it critical to use `with torch.no_grad():` during inference?**
*Answer*: "By default, PyTorch tracks every operation to build a computational graph for backpropagation. This consumes significant memory and CPU time. Since we don't update weights during inference, we use `torch.no_grad()` to disable this tracking, drastically reducing memory usage and speeding up the forward pass."

**Q3: Explain the concept of Data Drift and how it affects a production model.**
*Answer*: "Data Drift occurs when the statistical properties of the incoming production data change over time, diverging from the data the model was trained on. For example, a fraud model trained in 2019 might fail in 2024 because fraud tactics changed. The model's code is fine, but its predictions degrade silently. It requires continuous monitoring of input distributions to trigger retraining."
