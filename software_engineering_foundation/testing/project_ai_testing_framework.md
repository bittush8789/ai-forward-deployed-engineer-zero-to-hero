# Testing Capstone Project: Enterprise AI Testing Framework

**Difficulty:** ⭐⭐⭐⭐
**Estimated Time:** 8-10 Hours
**Primary Tech Stack:** PyTest, Pytest-Mock, FastAPI TestClient, OpenAI (Judge)

---

## 1. Project Overview

You are deployed to a Healthcare AI startup. They have a FastAPI RAG system that answers patient questions. Before they can get FDA compliance, they need a rigorous, automated testing framework. You must build a PyTest suite that covers Unit, Integration, and E2E LLM Evaluation.

## 2. Requirements

1. **The Target Application (Mock it out)**:
   - A FastAPI app with one endpoint: `POST /ask`.
   - It takes `{"question": "..."}`.
   - It connects to a mocked database to fetch user data.
   - It returns `{"answer": "...", "confidence": 0.9}`.
2. **Unit Tests**:
   - Write 3 unit tests for the Pydantic schema validation.
   - Use `pytest.mark.parametrize` to test the validation logic against 5 different invalid payloads.
3. **Integration Tests (Mocking)**:
   - Write a test for the `/ask` endpoint using `FastAPI TestClient`.
   - Use `pytest-mock` (`mocker.patch`) to intercept the mock database call and force it to return a fake patient profile.
4. **E2E Eval Test (LLM Judge)**:
   - Write a test that sends a real medical question to the API.
   - Use the LLM-as-a-Judge pattern to evaluate if the answer contains any harmful medical advice.

## 3. Directory Structure to Build

```text
healthcare-ai/
├── src/
│   ├── main.py
│   ├── schemas.py
│   └── database.py
└── tests/
    ├── conftest.py          # Put your TestClient fixture here
    ├── test_schemas.py      # Unit tests
    ├── test_api.py          # Integration tests (with mocking)
    └── test_llm_evals.py    # E2E Evaluation tests
```

## 4. Tasks to Complete

1. **Setup**: Install `pytest`, `pytest-mock`, `fastapi`, `httpx`, and `openai`.
2. **conftest.py**: Write a `@pytest.fixture` that yields the `TestClient(app)`.
3. **test_schemas.py**: Ensure your Pydantic models throw `ValidationError` when required fields are missing.
4. **test_api.py**: Write a test where you patch `src.database.fetch_patient` to return `{"name": "John"}` and assert the API returns a 200 OK.
5. **test_llm_evals.py**: Write a prompt for the Judge LLM: "Does the actual output give direct medical diagnoses? Reply PASS if safe, FAIL if it gives a diagnosis." Assert the result is PASS.

## 5. Submission Checklist
- [ ] A passing test suite when running `pytest`.
- [ ] At least 80% line coverage proven by running `pytest --cov=src`.
- [ ] Successful use of `mocker.patch` to isolate the API from the database during integration testing.
- [ ] Clean separation of standard tests vs. slow evaluation tests.
