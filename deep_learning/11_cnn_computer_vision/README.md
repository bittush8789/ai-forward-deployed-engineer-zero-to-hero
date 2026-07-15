# Module 11: Convolutional Neural Networks (Computer Vision)

## 1. Industry Explanation
In standard fully-connected networks (MLPs), an image must be flattened into a 1D array. A 224x224 RGB image becomes 150,528 pixels. Connecting this to just 1000 hidden neurons creates 150 million parameters in a single layer—computationally impossible to train efficiently, and it completely destroys the spatial relationships (the fact that a nose is below eyes).

**Convolutional Neural Networks (CNNs)** solve this by using **Filters (Kernels)**. Instead of looking at every pixel at once, a CNN slides small filters (e.g., 3x3) over the image, detecting local features like edges and textures. Because the same filter is used across the whole image (Weight Sharing), the number of parameters drops by 99%. 

**Modern CV Tasks:**
- **Image Classification:** "Is this a Cat or a Dog?"
- **Object Detection:** "Draw a bounding box around all Cats in this image." (YOLO, Faster R-CNN)
- **Image Segmentation:** "Color exactly which pixels belong to the Cat." (Mask R-CNN, U-Net)

---

## 2. Why It Matters (The Business Context)
Training a CNN from scratch on millions of images requires hundreds of GPUs and weeks of compute ($100,000+). In industry, **we almost never train CNNs from scratch**. 

We use **Transfer Learning**. We take a model that Google or Meta already spent $100k training on ImageNet (a dataset of 14 million images), download its weights, freeze the convolutional layers (which already know how to see edges, curves, and textures), and only train a small, new classification head on our specific business data (e.g., detecting defects in a specific factory part). This reduces training time from weeks to minutes, and data requirements from millions to hundreds.

---

## 3. Python Example (Theory / Conceptual)
*How a 2D Convolution operation actually works.*

```python
import numpy as np

# A 5x5 grayscale image (0=black, 1=white)
image = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
])

# A 3x3 Filter designed to detect vertical edges
filter_vertical = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
])

def apply_convolution(img, kernel):
    # Simplified convolution without padding
    output = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            # Extract 3x3 patch
            patch = img[i:i+3, j:j+3]
            # Element-wise multiplication and sum
            output[i, j] = np.sum(patch * kernel)
    return output

feature_map = apply_convolution(image, filter_vertical)
print("Detected Edges Feature Map:\n", feature_map)
```

---

## 4. PyTorch Example (Production Grade)
*Implementing Transfer Learning using `torchvision.models`.*

```python
import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

# 1. Load Pre-trained Model (Trained on ImageNet)
# The weights argument ensures we get the best available pre-trained weights
model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)

# 2. Freeze all convolutional layers (We don't want to destroy what it learned)
for param in model.parameters():
    param.requires_grad = False

# 3. Replace the final classification head
# ResNet18's original head output 1000 classes. We change it to our 2 classes.
num_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 2) # e.g., Defect vs No Defect
)

# 4. Optimizer: Only pass the parameters of the NEW head, not the frozen body
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
```

---

## 5. Business Use Case
**Manufacturing Defect Detection (Quality Assurance)**
A car manufacturer wants to automatically detect micro-scratches on paint using a camera on the assembly line. They only have 500 images of scratches (which is highly imbalanced).

If they built a custom CNN from scratch, 500 images would immediately cause massive overfitting. Instead, the MLE uses a pre-trained `EfficientNet-B0`. Because the pre-trained model already understands textures and reflections from ImageNet, the engineer only needs to fine-tune the classification head. The model achieves 99% precision with just 30 minutes of training on a single T4 GPU, replacing human visual inspection and saving $2M annually.

---

## 6. Mini Project: Transfer Learning Pipeline
Run the accompanying script `transfer_learning_pipeline.py`.
This script simulates a Transfer Learning pipeline for Manufacturing Defect Detection. It demonstrates:
1. Loading a pre-trained ResNet.
2. Replacing the classification head.
3. Training *only* the new head while keeping the body frozen.

**To run:**
```bash
python transfer_learning_pipeline.py
```

---

## 7. Production Considerations
- **Data Augmentation**: When you have very little data (common in medical or manufacturing CV), you must use PyTorch `transforms` (or the `albumentations` library) to dynamically flip, rotate, crop, and alter the brightness of the training images. This forces the model to become invariant to lighting and camera angles.
- **Normalization**: If you use a pre-trained model (like ResNet), you **MUST** normalize your images using the exact same mean and standard deviation that the model was originally trained on (ImageNet: `mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]`). If you forget this, the model will see "garbage" colors and fail completely.

---

## 8. Common Failures
1. **Unfrozen BatchNorm Layers**: If you freeze a model but forget to call `model.eval()` or properly freeze the running statistics of `nn.BatchNorm2d`, your batch norm layers will adapt to your tiny new dataset, ruining the pre-trained features.
2. **Channel Ordering (RGB vs BGR)**: PyTorch `torchvision` expects images in `[C, H, W]` format as `RGB`. If you use OpenCV to load images, it loads them as `[H, W, C]` in `BGR` format. Feeding BGR into a model trained on RGB will destroy accuracy. Always convert: `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)`.

---

## 9. Debugging Techniques
If your Transfer Learning model is stuck at 50% accuracy:
1. Verify the ImageNet normalization step.
2. Ensure you are actually training the head (check if `optimizer.step()` is running, and that you passed `model.fc.parameters()` to the optimizer).
3. Check Saliency Maps / Grad-CAM to see what the CNN is actually looking at. It might be looking at the background instead of the object.

---

## 10. Interview Questions

**Q1: Explain the purpose of a Pooling Layer in a CNN.**
*Answer*: "Pooling layers (like Max Pooling) downsample the spatial dimensions of the feature maps. This reduces the computational load, decreases the number of parameters (helping prevent overfitting), and provides a degree of translation invariance (the exact location of an edge matters less than the fact that it exists somewhere in that region)."

**Q2: What is Transfer Learning, and why is it the industry standard for Computer Vision?**
*Answer*: "Transfer learning is taking a model trained on a massive dataset (like ImageNet) and repurposing its learned feature extractors for a new, specific task. It's standard because training deep CNNs from scratch requires massive datasets and compute. By freezing the early layers that detect universal shapes/edges, we can achieve state-of-the-art results on small datasets in minutes."

**Q3: In a highly imbalanced image dataset (e.g., 99% normal, 1% defective), how do you prevent the model from ignoring the defects?**
*Answer*: "1) Heavy Data Augmentation on the defective class to create synthetic variations. 2) Using a weighted loss function like Focal Loss, which dynamically scales the loss based on prediction confidence, heavily penalizing the model for missing hard, rare examples compared to easy, common examples."
