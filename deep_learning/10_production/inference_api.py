import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# ==========================================
# 1. Model Definition (Must match training exactly)
# ==========================================
class ProductionModel(nn.Module):
    def __init__(self, input_dim):
        super(ProductionModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.net(x)

# ==========================================
# 2. Server Initialization & Model Loading
# ==========================================
app = FastAPI(title="Real-Time Neural Network API", version="1.0.0")

# Instantiate the architecture
INPUT_DIM = 5
model = ProductionModel(input_dim=INPUT_DIM)

# SIMULATION: We normally load weights from a .pth file like this:
# model.load_state_dict(torch.load("model_weights.pth"))
# For this lab, we just use the randomly initialized weights.

# CRITICAL: Set the model to evaluation mode!
# If you forget this, Dropout and BatchNorm will corrupt predictions.
model.eval()

# ==========================================
# 3. Pydantic Schemas for Type Validation
# ==========================================
# In production, NEVER trust user input. Validate the payload strictly.
class PredictionRequest(BaseModel):
    user_id: str
    features: list[float]

class PredictionResponse(BaseModel):
    user_id: str
    prediction_probability: float
    is_fraud: bool

# ==========================================
# 4. API Endpoints
# ==========================================
@app.get("/health")
def health_check():
    # Kubernetes checks this to see if the container is alive
    return {"status": "healthy", "model_version": "1.0.0"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # 1. Validate Input Length
    if len(request.features) != INPUT_DIM:
        raise HTTPException(status_code=400, detail=f"Expected {INPUT_DIM} features, got {len(request.features)}")
    
    try:
        # 2. Convert raw list to PyTorch Tensor
        # Notice we use .view(1, -1) to simulate a batch size of 1 [1, 5]
        input_tensor = torch.FloatTensor(request.features).view(1, -1)
        
        # 3. CRITICAL: Run inference without tracking gradients
        with torch.no_grad():
            logits = model(input_tensor)
            probability = torch.sigmoid(logits).item()
            
        # 4. Apply Business Logic (Threshold)
        is_fraud = bool(probability >= 0.85)
        
        # 5. Return JSON response
        return PredictionResponse(
            user_id=request.user_id,
            prediction_probability=probability,
            is_fraud=is_fraud
        )
        
    except Exception as e:
        # Catch unexpected errors (e.g., NaN values causing torch crashes)
        raise HTTPException(status_code=500, detail=f"Inference Error: {str(e)}")

# ==========================================
# 5. Server Execution
# ==========================================
if __name__ == "__main__":
    print("\nStarting Production Inference Server...")
    print("Test it in another terminal with:")
    print('curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d "{\\"user_id\\": \\"u_123\\", \\"features\\": [1.2, -0.5, 3.4, 0.0, -1.1]}"')
    
    # Run the server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
