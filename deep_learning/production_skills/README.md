# Production Machine Learning Skills

While training neural networks is the core of Deep Learning, deploying and maintaining them in an enterprise environment requires a specialized set of MLOps (Machine Learning Operations) skills. This section covers what a Senior MLE actually does day-to-day.

---

## 1. Experiment Tracking (MLflow / Weights & Biases)
In a Jupyter Notebook, you might just print the loss to the console. In production, you might run 50 different experiments simultaneously (testing different learning rates, architectures, and datasets). You cannot track this in an Excel spreadsheet.

**Industry Standard Tools:** MLflow, Weights & Biases (W&B), Neptune.

**What they do:**
- Log hyperparameters (`lr=0.01`, `batch_size=64`).
- Log metrics dynamically (`train_loss`, `val_auc`).
- Save the physical model weights (`.pth` files) linked to that exact experiment.
- Allow teams to visualize and compare all 50 runs on a dashboard to find the best model.

## 2. Model Versioning & Registry
Code is versioned with Git. Data is versioned with tools like DVC. Models are versioned in a **Model Registry**.
When you train a great model, you push it to the Registry (e.g., MLflow Model Registry) as `Version 1`. 
When you deploy to production, the API pulls `Version 1`. 
Next month, you train a better model. You push it as `Version 2`. You can smoothly transition traffic from V1 to V2, and if V2 fails in the real world, you can instantly rollback to V1.

## 3. Hardware & GPU Training
PyTorch runs on CPUs by default. To use a GPU, you must explicitly move the model and the data to the device.
```python
# 1. Detect hardware
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Move Model
model = MyNetwork().to(device)

# 3. Move Data (inside the training loop)
for inputs, targets in dataloader:
    inputs = inputs.to(device)
    targets = targets.to(device)
```
**Multi-GPU Training:** In industry, we use `torch.nn.DataParallel` or `DistributedDataParallel (DDP)` to train massive models across 8+ GPUs simultaneously.

## 4. Checkpointing
Training a large model might take 5 days. If the AWS server crashes on Day 4, you lose everything. 
**Checkpointing** means saving the model weights AND the optimizer state every $N$ epochs.
```python
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss
}
torch.save(checkpoint, 'checkpoint_epoch_10.pth')
```
If the server crashes, you load this file and resume training exactly where you left off.

## 5. Model Serving (Inference)
Once trained, the model must be served to users.
- **REST APIs**: Using FastAPI or Flask. The model is loaded into memory once when the server starts. It listens for JSON requests, converts them to tensors, predicts, and returns JSON.
- **Docker**: The API and model are packaged into a Docker container. This ensures that the exact Python version and CUDA drivers used to train the model are exactly the same in the production environment.
- **ONNX**: PyTorch is great for training, but slow for inference. Models are often exported to ONNX (Open Neural Network Exchange) or TensorRT for massive speedups in production.

## 6. Monitoring & Data Drift
Software APIs fail loudly (HTTP 500 errors). ML APIs fail silently. 
If the distribution of incoming user data changes (e.g., a new demographic starts using the app), the model will continue to return `HTTP 200 OK`, but the predictions will be entirely wrong.
- **Data Drift**: The input features have changed over time.
- **Concept Drift**: The relationship between features and the target has changed (e.g., inflation changes what a "High Salary" means).
Production systems require continuous monitoring of input distributions and prediction distributions, triggering alerts if they deviate significantly from the training data baseline.
