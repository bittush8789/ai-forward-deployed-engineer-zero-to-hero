# Module 13: FastAPI for AI FDEs

Welcome to **Module 13**. As an AI Forward Deployed Engineer, you rarely deploy Python scripts. You deploy **Microservices**. FastAPI is the modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. It is the absolute industry standard for wrapping AI models and deploying them to production.

---

## 1. Detailed Theory

### REST APIs and HTTP Methods
- **GET**: Retrieve data (e.g., get chat history).
- **POST**: Submit data to be processed (e.g., send a prompt to an LLM).
- **PUT / PATCH**: Update existing data.
- **DELETE**: Remove data.
- **Status Codes**: 200 (OK), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Internal Server Error).

### Pydantic Models (Data Validation)
FastAPI relies entirely on Pydantic. You define the shape of your incoming JSON requests and outgoing JSON responses using Python classes. If a user sends a string where an integer is expected, FastAPI automatically blocks the request and returns a 422 Unprocessable Entity error.

### Dependency Injection
A design pattern baked into FastAPI (`Depends()`). It allows you to declare things your endpoint needs (like a database connection, or an authenticated user token) and FastAPI automatically provides it before the endpoint runs.

### Middleware
Code that runs before every request and after every response. Used for CORS (Cross-Origin Resource Sharing), logging, rate-limiting, and timing.

---

## 2. Architecture Diagram: FastAPI AI Microservice

```mermaid
graph TD
    Client((Client App)) -->|POST /chat (JSON)| A(FastAPI App)
    
    subgraph FastAPI Flow
        A --> B{Middleware: CORS & Auth}
        B --> C{Pydantic Validation}
        C -->|Valid| D[Endpoint logic]
        C -->|Invalid| E[422 Error Response]
        
        D --> F(Depends: DB Session)
        D --> G(Depends: LLM Client)
    end
    
    F --> DB[(PostgreSQL)]
    G --> API[OpenAI API]
    
    D -->|Return Pydantic Model| H[FastAPI serializes to JSON]
    H --> Client
    E --> Client
```

---

## 3. Production Use Cases

1. **AI Model Wrappers**: A data science team trains a custom model in PyTorch. The FDE wraps the inference script in a FastAPI `POST /predict` endpoint, containerizes it with Docker, and deploys it so frontend applications can consume it via HTTP.
2. **Webhook Receivers**: Building endpoints that listen for events from external systems (e.g., a Slack bot sending user messages to your FastAPI server, which processes them via LLM and replies).
3. **Asynchronous RAG Backends**: Using FastAPI's async capabilities to receive a query, search Pinecone, query OpenAI, and stream the text back to a React frontend using Server-Sent Events (SSE).

---

## 4. Real Company Examples

- **Netflix, Uber, Microsoft**: All have adopted FastAPI for their high-performance Python microservices due to its speed (on par with NodeJS/Go) and developer ergonomics.
- **OpenAI**: Many internal tools and enterprise deployment architectures recommended by OpenAI field engineers utilize FastAPI as the core routing layer.

---

## 5. Coding Examples

### The Absolute Basics

*Pre-requisite: `pip install fastapi uvicorn pydantic`*

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Copilot API", version="1.0")

# 1. Pydantic Model for Input Validation
class ChatRequest(BaseModel):
    user_id: str
    message: str
    temperature: float = 0.7 # Default value if omitted

# 2. Pydantic Model for Output
class ChatResponse(BaseModel):
    reply: str
    tokens_used: int

# 3. The Endpoint
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # FastAPI automatically parsed the JSON into the 'request' object!
    print(f"Processing message for {request.user_id} with temp {request.temperature}")
    
    # Mock AI logic
    mock_reply = f"I am an AI. You said: {request.message}"
    
    # Return the Pydantic object (FastAPI turns it back to JSON)
    return ChatResponse(reply=mock_reply, tokens_used=42)

# Run this script directly for testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
*Run it and visit `http://localhost:8000/docs` to see the automatically generated Swagger UI API documentation!*

---

## 6. Hands-on Labs

**Lab: The Health Check Endpoint**
**Objective**: Build a basic GET endpoint.
**Instructions**:
1. Initialize a `FastAPI()` app.
2. Create a `@app.get("/health")` endpoint.
3. The function should simply `return {"status": "healthy", "model_loaded": True}`.
4. Run the app using `uvicorn script_name:app --reload`.
5. Open your browser and navigate to the `/health` URL to see the JSON response.

---

## 7. Assignments

**Assignment: Secured AI Generation Endpoint**
1. Create a FastAPI app.
2. Create a Pydantic model `GenerateRequest` with `prompt` (str) and `max_words` (int).
3. Create a `POST /generate` endpoint.
4. Add a query parameter for authentication: `def generate(req: GenerateRequest, api_key: str):`.
5. Inside the endpoint, if `api_key != "secret123"`, raise an `HTTPException(status_code=401, detail="Unauthorized")`. (Import `HTTPException` from `fastapi`).
6. If authorized, return a mock generated string clipped to `max_words`.

---

## 8. Interview Questions

1. **Why is FastAPI faster than traditional frameworks like Flask or Django?**
   *Answer Hint: It is built on Starlette and Asyncio, allowing non-blocking I/O natively. It also uses Pydantic (written in Rust) for incredibly fast data validation and serialization.*
2. **What is the purpose of Pydantic in FastAPI?**
   *Answer Hint: Data parsing, type coercion, and validation. It guarantees that the data entering your endpoint exactly matches the types defined in your Python class. If it doesn't, Pydantic throws a 422 error before your code even runs.*
3. **What is Swagger UI and how does FastAPI integrate with it?**
   *Answer Hint: Swagger UI is an interactive, visual documentation for APIs. FastAPI automatically generates the OpenAPI schema based on your Python type hints and serves the Swagger UI at the `/docs` endpoint with zero extra configuration.*

---

## 9. Best Practices (FDE Standards)

- **Use Routers for Large Apps**: Don't put 50 endpoints in `main.py`. Use `APIRouter` to split your app into logical modules (e.g., `routers/auth.py`, `routers/agents.py`) and include them in `main.py`.
- **Dependency Injection for DBs**: Always use `Depends(get_db)` to pass database sessions into endpoints. This ensures connections are closed properly and allows easy mocking during unit tests.
- **CORS Middleware**: If a React frontend is calling your FastAPI backend, you must configure `CORSMiddleware` in FastAPI to allow cross-origin requests, otherwise the browser will block them.

---

## 10. Common Mistakes

- **Blocking the Event Loop**: 
  ```python
  @app.get("/slow")
  async def slow_endpoint():
      time.sleep(5) # BUG! Freezes the entire server.
      return {"done": True}
  ```
  *Fix: If you must run synchronous blocking code, define the endpoint as `def` instead of `async def`. FastAPI will automatically run it in an external thread pool to prevent blocking!*
- **Returning standard dictionaries instead of Pydantic models**: While allowed, it removes the type safety and automatic documentation benefits of FastAPI. Always use `response_model=...`.

---

## 11. End-to-End Project: Production-Ready RAG API Service

**Scenario**: You are structuring the foundational API for a Retrieval-Augmented Generation application. It includes Dependency Injection, Pydantic validation, and simulated Vector DB lookups.

**Code:**
```python
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
import uvicorn
import time

app = FastAPI(title="Enterprise RAG Backend")

# --- Dependencies ---
# Simulated database connection
class MockVectorDB:
    def search(self, query: str):
        time.sleep(0.5) # Simulate latency
        return ["Doc1: Company policy", "Doc2: Q3 Revenue"]

def get_vector_db():
    db = MockVectorDB()
    try:
        yield db # Pass the DB to the endpoint
    finally:
        # Cleanup code runs after the endpoint finishes
        print("[CLEANUP] Closing DB connection")

# Simulated Auth Dependency
def verify_token(x_token: str = Header(...)):
    if x_token != "super-secret-fde-token":
        raise HTTPException(status_code=401, detail="Invalid X-Token header")
    return x_token

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="The user's question")
    top_k: int = Field(default=3, le=10, description="Number of docs to retrieve")

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# --- Endpoints ---
@app.post("/api/v1/ask", response_model=QueryResponse, tags=["AI Agents"])
async def ask_agent(
    request: QueryRequest, 
    db: MockVectorDB = Depends(get_vector_db),
    token: str = Depends(verify_token)
):
    print(f"Authenticated request via token. Searching for '{request.query}'...")
    
    # 1. Retrieve context
    docs = db.search(request.query)
    
    # 2. Simulate LLM Generation with context
    llm_answer = f"Based on {len(docs)} documents, the answer is Yes."
    
    return QueryResponse(answer=llm_answer, sources=docs)

if __name__ == "__main__":
    print("Run using: uvicorn script_name:app --reload")
    # Uncomment to run programmatically
    # uvicorn.run(app, host="127.0.0.1", port=8000)
```
