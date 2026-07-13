# Module 14: Testing for AI FDEs

Welcome to **Module 14**. You cannot deploy code to a client's production environment based on "it worked on my machine." Testing guarantees that changes to your prompt templates, routing logic, or data models do not break the entire enterprise system. We use `pytest`—the industry standard for Python testing.

---

## 1. Detailed Theory

### The Testing Pyramid
- **Unit Tests**: Testing small, isolated blocks of code (a single function or class method). Fast and cheap.
- **Integration Tests**: Testing how multiple components work together (e.g., testing if the FastAPI endpoint successfully connects to the real Database). Slower.
- **End-to-End (E2E) Tests**: Simulating a real user interacting with the whole system. Slow and brittle.

### Pytest Fundamentals
- `pytest` auto-discovers tests: It looks for files named `test_*.py` and runs any function inside them starting with `test_`.
- **Assertions**: Standard Python `assert` statements (`assert result == expected`). Pytest intercepts these to provide detailed failure messages.

### Fixtures
A way to provide a fixed baseline for tests. Used to inject dependencies (like a mock database connection, or a test client) into your test functions automatically. Setup and Teardown logic happens here.

### Mocking and Patching
When writing Unit Tests, you **must not** hit real external APIs (OpenAI costs money, is slow, and introduces network flakiness). You use `unittest.mock.patch` to intercept the API call and return a fake, predetermined response instantly.

---

## 2. Architecture Diagram: Mocking AI Calls in Testing

```mermaid
graph TD
    A[Pytest Runner] --> B(test_agent_routing)
    B --> C(Agent Logic)
    
    C -- Attempts to call OpenAI --> D{Patch/Mock Interceptor}
    
    D -.->|Real API (Blocked)| E[OpenAI Server]
    D -->|Returns Mock Data| C
    
    C --> F(Assert expected routing output)
    F --> A
    
    style D fill:#f96,stroke:#333
    style E fill:#d3d3d3,stroke-dasharray: 5 5
```

---

## 3. Production Use Cases

1. **Prompt Regression Testing**: Before deploying a new system prompt, running 100 historical queries through the mocked LLM to ensure the parsed JSON output structure hasn't broken.
2. **Endpoint Validation (FastAPI `TestClient`)**: Spinning up a fake in-memory server during CI/CD to throw thousands of malformed JSON payloads at your endpoints to ensure Pydantic catches them properly.
3. **Database State Testing**: Using fixtures to spin up a temporary SQLite database, insert mock users, run the application logic, assert the logic worked, and destroy the database—all in milliseconds.

---

## 4. Real Company Examples

- **All Enterprise AI Teams**: CI/CD (Continuous Integration/Continuous Deployment) pipelines via GitHub Actions will strictly run `pytest` on every Pull Request. If test coverage drops, or a test fails, the code cannot be merged.
- **LangChain**: Has thousands of unit tests heavily relying on mocking to simulate various LLM provider responses to ensure their abstraction layers work universally.

---

## 5. Coding Examples

*Pre-requisite: `pip install pytest httpx`*

### Basic Unit Testing
```python
# file: calculator.py
def token_cost(tokens: int, price_per_k: float) -> float:
    return (tokens / 1000) * price_per_k

# file: test_calculator.py
# (Run in terminal by typing `pytest`)
from calculator import token_cost

def test_token_cost_calculation():
    # Setup
    tokens = 2500
    price = 0.02
    
    # Execute
    result = token_cost(tokens, price)
    
    # Assert
    assert result == 0.05
    
def test_token_cost_zero():
    assert token_cost(0, 0.02) == 0.0
```

### Advanced Mocking (The FDE Bread and Butter)
```python
# file: ai_agent.py
import requests

def fetch_external_context(query: str):
    # This hits the real internet! We don't want this in tests.
    response = requests.get(f"https://api.mockdata.com/search?q={query}")
    return response.json()

def build_prompt(query: str):
    context = fetch_external_context(query)
    return f"Context: {context['data']}. User says: {query}"

# file: test_agent.py
from unittest.mock import patch
from ai_agent import build_prompt

# The @patch decorator intercepts 'requests.get' where it is used in 'ai_agent.py'
@patch('ai_agent.requests.get')
def test_build_prompt(mock_get):
    # 1. Setup the Mock Behavior
    mock_get.return_value.json.return_value = {"data": "Mocked context data"}
    
    # 2. Execute the function (it will hit the mock, not the internet)
    result = build_prompt("Hello")
    
    # 3. Assertions
    assert "Mocked context data" in result
    assert "Hello" in result
    # Verify the mock was actually called correctly
    mock_get.assert_called_once_with("https://api.mockdata.com/search?q=Hello")
```

---

## 6. Hands-on Labs

**Lab: FastAPI Test Client**
**Objective**: Test a web endpoint without running the server.
**Instructions**:
1. In a file, create a tiny FastAPI app with `@app.get("/ping")` returning `{"status": "pong"}`.
2. In the same file, import `TestClient` from `fastapi.testclient`.
3. Create `client = TestClient(app)`.
4. Write a test function: `def test_ping():`
5. Inside, do `response = client.get("/ping")`.
6. Assert `response.status_code == 200` and `response.json() == {"status": "pong"}`.

---

## 7. Assignments

**Assignment: Test Driven Development (TDD) for Document Parsing**
1. Write the test *first*: `def test_parse_document_metadata():`
2. Create mock input: `doc = "AUTHOR: Alice | DATE: 2023 | CONTENT: Testing"`
3. Assert that calling `parse(doc)` returns `{"author": "Alice", "date": "2023", "text": "Testing"}`.
4. Run the test (it will fail because `parse` doesn't exist).
5. Now, write the `parse` function using `str.split()` to make the test pass!

---

## 8. Interview Questions

1. **Why must we mock LLM API calls in unit tests?**
   *Answer Hint: Determinism, Speed, and Cost. Unit tests must be fast (run in milliseconds) and deterministic (always pass if the code is correct). LLMs are slow, cost money, and return non-deterministic (random) text that makes assertions impossible.*
2. **What is a Pytest Fixture?**
   *Answer Hint: A function decorated with `@pytest.fixture` that sets up state (like a database connection) and passes it into test functions as an argument. It replaces repetitive `setUp()` methods.*
3. **What is Test Coverage?**
   *Answer Hint: The percentage of your application's source code lines that are executed during the automated tests. A coverage of 80%+ is typically standard for enterprise applications.*

---

## 9. Best Practices (FDE Standards)

- **Test Edge Cases**: Don't just test the "Happy Path". Test what happens when the LLM returns an empty string, or malformed JSON, or when the Vector DB times out.
- **Keep Tests Independent**: Test A should never rely on the outcome or state of Test B. They should be able to run in any order, or in parallel.
- **Descriptive Test Names**: Name tests explicitly: `test_vector_search_returns_empty_list_on_db_timeout`. If a test fails in CI/CD, the name should tell you exactly what broke.

---

## 10. Common Mistakes

- **Testing the Mock**: Writing a test where you mock a function, call the mocked function directly, and assert it returns what you told it to return. You tested nothing. You must call *your application code* that relies on the mock.
- **Patching the wrong path**: If you are testing `my_module.py` which does `from external_lib import func`, you must `@patch('my_module.func')`, NOT `@patch('external_lib.func')`.

---

## 11. End-to-End Project: Fully Tested Backend Service

**Scenario**: You have a core function that formats user messages into an LLM payload. You will write the function and a suite of Pytest fixtures and tests for it.

**Code (`test_payload_builder.py`):**
```python
import pytest

# --- The Application Code ---
class PayloadError(Exception):
    pass

def build_llm_payload(user_query: str, history: list, system_prompt: str) -> dict:
    if not user_query.strip():
        raise PayloadError("Query cannot be empty.")
        
    messages = [{"role": "system", "content": system_prompt}]
    
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    messages.append({"role": "user", "content": user_query})
    
    return {
        "model": "gpt-4",
        "messages": messages,
        "temperature": 0.0
    }

# --- The Test Suite ---

# 1. Fixtures for reusable test data
@pytest.fixture
def default_sys_prompt():
    return "You are a helpful AI."

@pytest.fixture
def mock_history():
    return [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}]

# 2. Happy Path Test
def test_build_payload_success(default_sys_prompt, mock_history):
    query = "What is the weather?"
    
    result = build_llm_payload(query, mock_history, default_sys_prompt)
    
    assert result["model"] == "gpt-4"
    assert len(result["messages"]) == 4 # 1 sys + 2 history + 1 new query
    assert result["messages"][-1]["content"] == "What is the weather?"

# 3. Edge Case: Empty History
def test_build_payload_no_history(default_sys_prompt):
    result = build_llm_payload("Ping", [], default_sys_prompt)
    assert len(result["messages"]) == 2

# 4. Exception Testing
def test_build_payload_empty_query_raises_error(default_sys_prompt):
    # Pytest context manager to assert an exception is raised
    with pytest.raises(PayloadError) as excinfo:
        build_llm_payload("   ", [], default_sys_prompt)
        
    assert "cannot be empty" in str(excinfo.value)

# Run this file in terminal: `pytest test_payload_builder.py -v`
```
