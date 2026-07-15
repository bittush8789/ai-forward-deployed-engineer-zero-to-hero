# Deep Learning Interview Preparation (MLE / AI Engineer)

This guide focuses on the questions asked for **Senior Machine Learning Engineer** and **Applied AI Engineer** roles. Unlike Data Science interviews (which focus on stats/SQL) or Research Scientist interviews (which focus on math/proofs), MLE interviews focus on **Architecture, Debugging, and System Design**.

---

## 1. Fundamentals & Architecture

**Q: Explain the Bias-Variance Tradeoff in the context of deep neural networks.**
> **A:** Deep neural networks have immense capacity, naturally leaning towards low bias (they can fit complex data easily) but extremely high variance (they memorize noise and overfit). The entire job of an MLE is to manage this high variance using regularization techniques (Dropout, Weight Decay, Early Stopping) and gathering massive amounts of data.

**Q: Why do we use ReLU instead of Sigmoid in hidden layers?**
> **A:** Sigmoid squashes outputs between 0 and 1, meaning its maximum derivative is 0.25. During backpropagation in deep networks, multiplying these small derivatives causes the gradient to vanish exponentially, stalling training. ReLU has a derivative of 1 for positive inputs, allowing gradients to flow unimpeded through deep layers, enabling faster and deeper training.

**Q: What is the "Dying ReLU" problem, and how do you fix it?**
> **A:** It happens when a large learning rate updates a neuron's weights so much that it always outputs a negative value. Because the derivative of ReLU for negative values is 0, the neuron can never update its weights again; it is "dead". To fix it, you can lower the learning rate, use Batch Normalization, or switch to Leaky ReLU (which has a small positive slope for negative inputs).

**Q: What is the purpose of Batch Normalization?**
> **A:** It addresses Internal Covariate Shift. As weights update in earlier layers, the distribution of inputs to later layers changes constantly, slowing down training. Batch Norm standardizes the outputs of a layer to have a mean of 0 and variance of 1 across the mini-batch. This smooths the loss landscape, allows for much higher learning rates, and acts as a mild regularizer.

---

## 2. Optimization & Loss Functions

**Q: What is the difference between Adam and SGD with Momentum? Which do you prefer in production?**
> **A:** Adam maintains a per-parameter learning rate that adapts based on the first and second moments of the gradients, leading to very fast convergence with minimal tuning. SGD applies the same learning rate to all parameters but uses momentum to barrel through local minima. In production, I start with **AdamW** because the engineering time saved by not tuning the learning rate manually is highly valuable, and AdamW fixes the weight decay bugs present in standard Adam.

**Q: You are predicting human age from a photo. Would you use MSE (Mean Squared Error) or MAE (Mean Absolute Error)?**
> **A:** MAE. If the true age is 30, and the model predicts 40, the error is 10. With MAE, the penalty is 10. With MSE, the penalty is 100. MSE disproportionately punishes large errors, making the model highly sensitive to outliers. Since age errors scale linearly in human perception, MAE (or Huber Loss) aligns better with reality.

**Q: Explain the difference between `BCEWithLogitsLoss` and `CrossEntropyLoss` in PyTorch.**
> **A:** `BCEWithLogitsLoss` is for binary or multi-label classification. It expects an output layer of size 1 (or size N for multi-label) and applies a Sigmoid internally for numerical stability. `CrossEntropyLoss` is for multi-class classification (mutually exclusive classes like Cat vs Dog). It expects an output layer of size C (number of classes) and applies a LogSoftmax internally.

---

## 3. Debugging & Troubleshooting

**Q: You train a binary classification model. The loss decreases slightly, but accuracy is exactly 50% for 20 epochs straight. What happened?**
> **A:** The model is likely suffering from a disconnected data pipeline. The features and labels were shuffled independently, so there is no mathematical relationship between $X$ and $y$. The model is trying to learn, but it's fundamentally just guessing, hence 50% accuracy.

**Q: How do you identify and fix Exploding Gradients?**
> **A:** I identify them by monitoring the loss (it becomes `NaN`) or the L2 norm of the gradients during training. To fix it, I first ensure the input data is scaled properly (e.g., StandardScaler). If the architecture is deep, I add Batch Normalization. Finally, I use gradient clipping (`torch.nn.utils.clip_grad_norm_`) to mathematically cap the gradients before the optimizer step.

**Q: Your model achieves 99% accuracy on the test set, but 50% in production. Name 3 possible reasons.**
> **1. Data Leakage:** The test set accidentally contained information from the future or overlap with the training set.
> **2. Train/Serving Skew:** The production API is applying different preprocessing (or missing scaling) compared to the Jupyter Notebook used for training.
> **3. Concept Drift:** The model was trained on historical data, and the real-world environment has fundamentally changed since then.

---

## 4. Production System Design

**Q: You need to deploy a heavy PyTorch model that takes 500ms to run inference, but the business SLA requires a response time under 100ms. What are your architectural options?**
> **1. Dynamic Batching:** Instead of processing 1 request immediately, have the API wait 20ms to collect multiple incoming requests, pass them through the model as a batch, and distribute the answers. This massively increases throughput.
> **2. Model Conversion:** Export the PyTorch model to ONNX or TensorRT to optimize it for CPU/GPU inference, often yielding 2x-5x speedups.
> **3. Model Compression:** Apply techniques like Quantization (converting 32-bit floats to 8-bit integers) or Knowledge Distillation (training a smaller model to mimic the heavy model).
> **4. Caching:** If the same requests happen frequently, put a Redis cache in front of the API so the model doesn't even need to run.
