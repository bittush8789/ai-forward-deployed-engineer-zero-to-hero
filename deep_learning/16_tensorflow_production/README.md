# Module 16: TensorFlow in Production

## 1. Industry Explanation
If PyTorch won the academic AI war, **TensorFlow (TF)** won the early enterprise war. Developed by Google, TensorFlow was built from the ground up for massive distributed training and robust production serving.

While many companies are migrating to PyTorch for *training* because it's easier to debug, TensorFlow's production ecosystem (`TensorFlow Serving`, `TensorFlow Lite` for mobile, `TensorFlow.js` for browsers) remains heavily entrenched in legacy enterprise systems.

**Key Ecosystem Components:**
- **Keras:** The high-level, human-readable API for building neural networks. In TF 2.0, Keras became the official frontend for TensorFlow.
- **tf.data:** The industry-standard pipeline for loading terabytes of data asynchronously from disk to GPU without bottlenecking.
- **TensorFlow Serving (TFS):** Google's production server. You export a `SavedModel`, put it in a Docker container, and TFS automatically creates a gRPC/REST API capable of handling 100,000+ requests per second.

---

## 2. Why It Matters (The Business Context)
You are an MLE at Spotify. You have 10 terabytes of user listening history stored in AWS S3. 
If you try to load this into a Pandas DataFrame or standard PyTorch DataLoader, your server will crash with an Out-of-Memory (OOM) error. 

By using `tf.data.Dataset`, you can create a pipeline that streams the data directly from S3, prefetches the next batch into CPU RAM while the GPU is processing the current batch, and applies data augmentation dynamically. This ensures your expensive GPUs are utilized at 100% capacity, saving millions in compute time.

---

## 3. Python Example (Theory / Conceptual)
*The difference between eager execution and graph execution.*

```python
import tensorflow as tf

# 1. Eager Execution (Like standard Python/PyTorch)
# Easy to debug, but slow.
def eager_math(x):
    if tf.reduce_sum(x) > 0:
        return x * 2
    return x * 0

# 2. Graph Execution (@tf.function)
# TensorFlow reads your Python code and compiles it into a static C++ graph.
# Harder to debug, but highly optimized and much faster for production.
@tf.function
def graph_math(x):
    if tf.reduce_sum(x) > 0:
        return x * 2
    return x * 0

tensor = tf.constant([1.0, 2.0, 3.0])
print(graph_math(tensor))
```

---

## 4. TensorFlow Example (Production Grade)
*Building a robust `tf.data` pipeline and compiling a Keras model.*

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 1. Simulate a large dataset (e.g., millions of image paths and labels)
X = tf.random.normal((10000, 28, 28, 1))
y = tf.random.uniform((10000,), maxval=10, dtype=tf.int32)

# 2. Build the tf.data Pipeline
dataset = tf.data.Dataset.from_tensor_slices((X, y))

# The holy grail of TF performance:
dataset = dataset.shuffle(buffer_size=1024) # Shuffle data
dataset = dataset.batch(64)                 # Group into batches
dataset = dataset.cache()                   # Cache data in RAM after first epoch
dataset = dataset.prefetch(tf.data.AUTOTUNE)# Prepare next batch while GPU is busy

# 3. Build a Keras Model
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# 4. Compile and Train
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# model.fit(dataset, epochs=5) # Train using the highly optimized pipeline
```

---

## 5. Business Use Case
**Mobile Image Classifier (TensorFlow Lite)**
A farming startup wants an app where users point their phone camera at a crop to detect diseases instantly, even without an internet connection (offline inference).

PyTorch and standard TensorFlow models are hundreds of megabytes—too large for a mobile app. The MLE team trains an `EfficientNet` in Keras, and uses the `TFLiteConverter`. They apply **Quantization**, converting the 32-bit float weights into 8-bit integers. 
The model size shrinks from 120MB to 15MB, and the inference speed on the phone's ARM processor increases by 3x, with almost zero loss in accuracy.

---

## 6. Mini Project: TF Serving Export
Run the accompanying script `tf_serving_export.py`.
This script simulates the end of a training run:
1. It builds a Keras model.
2. It exports the model into the `SavedModel` format required by TensorFlow Serving.
3. It demonstrates how to structure the versioning directories so TFS can hot-swap models without downtime.

**To run:**
```bash
# Requires: pip install tensorflow
python tf_serving_export.py
```

---

## 7. Production Considerations
- **TensorBoard**: TensorFlow's visualization suite is the industry standard for debugging training runs. You add a `keras.callbacks.TensorBoard` to your `model.fit()` call. It logs your loss curves, gradient histograms, and the actual computational graph. You can then view it in your browser (`tensorboard --logdir logs/`).
- **Distributed Strategy**: To train on 8 GPUs simultaneously, you wrap your model creation in a `tf.distribute.MirroredStrategy().scope()`. TensorFlow automatically handles syncing the gradients and broadcasting the weights.

---

## 8. Common Failures
1. **OOM due to Batch Size**: If you get `ResourceExhaustedError: OOM when allocating tensor`, your batch size is too large for your GPU's VRAM. Reduce the batch size in `dataset.batch()`.
2. **`tf.function` Retracing**: If you pass NumPy arrays or Python lists of different sizes into a function decorated with `@tf.function`, TensorFlow will trigger a C++ compilation ("retracing") for *every single unique shape*. This will cause training to freeze and consume all CPU RAM. Always pass `tf.Tensor` objects with consistent shapes.

---

## 9. Interview Questions

**Q1: Explain the purpose of `tf.data.AUTOTUNE` in a TensorFlow pipeline.**
*Answer*: "During training, the CPU reads data from the disk, and the GPU performs matrix math. If the CPU is slow, the GPU sits idle waiting for data (a massive bottleneck). `dataset.prefetch(tf.data.AUTOTUNE)` tells TensorFlow to dynamically calculate how many batches it should load into CPU memory in the background *while* the GPU is currently training, ensuring the GPU never starves for data."

**Q2: What is a `SavedModel` in TensorFlow?**
*Answer*: "Unlike PyTorch which saves a `.pth` file containing only weights, a `SavedModel` is a complete directory containing both the weights AND the static C++ computation graph. This allows the model to be loaded by TensorFlow Serving, C++, Java, or Go environments completely independently of the original Python code."

**Q3: How would you deploy a deep learning model to an iOS or Android device?**
*Answer*: "I would train the model in Keras, then use the TensorFlow Lite Converter to export it as a `.tflite` file. During conversion, I would apply Post-Training Quantization to convert the weights from Float32 to Int8, which reduces the file size by 4x and speeds up inference on mobile hardware."
