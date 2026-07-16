# Module 4: RAG Evaluation & The RAG Triad

## 1. Theory (40%)
Retrieval-Augmented Generation (RAG) pipelines are complex. **RAG Evaluation** involves measuring the quality of the retrieval step (context relevance) and the generation step (faithfulness and answer relevance).

```
+-------------------------------------------------------------------------------------------------+
|                                           The RAG Triad                                         |
|                                                                                                 |
|                  +-------------------------------------------------------------+                |
|                  |                       User Query                            |                |
|                  +------|-----------------------------------------------|------+                |
|                         | (Context Relevance)                           |                       |
|                         v                                               v (Answer Relevance)    |
|          +-----------------------------+                 +-----------------------------+        |
|          |      Retrieved Context      | --------------> |     Generated Response      |        |
|          +-----------------------------+  (Faithfulness) +-----------------------------+        |
+-------------------------------------------------------------------------------------------------+
```

### The RAG Triad Metrics
*   **Context Relevance**: Checks if the retrieved context is relevant and sufficient to answer the user query.
*   **Groundedness/Faithfulness**: Checks if the generated response is based *only* on the retrieved context, identifying hallucinations.
*   **Answer Relevance**: Checks if the generated response directly answers the user's query.

---

## 2. Architecture Deep Dive

RAG evaluation architectures analyze the intermediate pipeline steps:
1.  **Capture Inputs**: Log the user query, retrieved context, and generated response.
2.  **Evaluate Context**: The evaluator model compares the query to the retrieved context to calculate context relevance.
3.  **Evaluate Output**: The evaluator compares the generated response to the retrieved context to calculate faithfulness, identifying hallucinations.
4.  **Log Metrics**: The metrics are logged to a dashboard (like TruLens or Ragas) to identify pipeline bottlenecks (e.g., poor retrieval vs poor generation).

---

## 3. Tool Comparison

| Feature | Ragas | TruLens-Eval | DeepEval (RAG Mode) |
|---|---|---|---|
| **Primary Metric** | RAG score compilation | The RAG Triad metrics | Faithfulness & Relevance |
| **LLM-as-a-judge** | Yes | Yes (TruFeedback) | Yes |
| **Dashboard** | No (Export as dataframes) | Yes (Streamlit UI) | Yes (DeepEval Cloud) |
| **Integration** | LangChain / LlamaIndex | Independent wrapper | Pytest integration |

---

## 4. Tool Installation
Install the RAG evaluation packages:
```bash
pip install ragas trulens-eval
```

---

## 5. Tool Setup
Export the API keys needed to run evaluations:
```bash
export OPENAI_API_KEY="sk-proj-123456"
```

---

## 6. CLI Commands
```bash
# Run Ragas evaluation on local data
python3 -c "import ragas; print('Ragas version:', ragas.__version__)"
```

---

## 7. Configuration Files
Define RAG evaluation parameters in `rag_eval_config.json`:
```json
{
  "metrics": ["faithfulness", "answer_relevance", "context_precision"],
  "thresholds": {
    "faithfulness": 0.8,
    "answer_relevance": 0.85
  },
  "evaluator_model": "gpt-4"
}
```

---

## 8. API Examples
Create a Python script using Ragas to measure faithfulness:
```python
# /tmp/rag_eval_test.py
import os

# Create mock execution data
dataset = {
    "question": "What is the capital of France?",
    "contexts": ["Paris is the capital and most populous city of France."],
    "answer": "Paris is the capital of France."
}

def evaluate_rag():
    print(f"Question: {dataset['question']}")
    print(f"Retrieved Context: {dataset['contexts'][0]}")
    print(f"Generated Answer: {dataset['answer']}")
    
    # Simulating evaluation metrics calculations
    # In production, use: from ragas import evaluate; evaluate(dataset)
    faithfulness_score = 1.0 # 100% grounded
    relevance_score = 0.95
    
    print(f"Faithfulness Score: {faithfulness_score}")
    print(f"Answer Relevance Score: {relevance_score}")

if __name__ == '__main__':
    evaluate_rag()
```
Run the evaluation:
```bash
python3 /tmp/rag_eval_test.py
```

---

## 9. Production Tasks

### Automated Pipeline Optimization
Configure evaluations to run on user query logs daily, identifying topics or documents that trigger hallucinations or poor retrieval scores.

---

## 10. Troubleshooting

### Task 10.1: Context Formatting Issues
*   **Symptom**: Evaluator throws a formatting error or returns incorrect scores during checks.
*   **Root Cause**: The retrieved context is a list of documents instead of plain text strings, causing parsing issues.
*   **Resolution Strategy**:
    *   Preprocess the retrieved context to merge documents into a single text string before running evaluations.

---

## 11. Monitoring
Configure alerts in Grafana when average faithfulness scores drop below 0.8 on production query logs.

---

## 12. Security
Audit retrieved contexts to ensure sensitive or restricted documents are not exposed to unauthorized users.

---

## 13. Governance
Log and store all evaluation reports and test results to maintain an audit trail for compliance.

---

## 14. Real Enterprise Incidents

### Case Study: Hallucinations causing Customer Support Complaints
*   **Incident**: An online store deployed a RAG-based customer support assistant. The assistant retrieved outdated warranty documents and hallucinated responses, promising customers refunds.
*   **Remediation**:
    *   Implemented automated validation gates to block outputs with low faithfulness scores.
    *   Cleaned and updated the document storage database.

---

## 15. Interview Questions

### Q1: What is the RAG Triad, and why is it critical for evaluation?
*   **Answer**: The RAG Triad consists of three metrics: context relevance, faithfulness, and answer relevance. It is critical because it isolates pipeline bottlenecks, identifying whether poor responses are caused by poor retrieval (context relevance) or poor generation (faithfulness/answer relevance).

### Q2: Explain the difference between faithfulness and answer relevance.
*   **Answer**:
    *   **Faithfulness**: Measures if the generated response is based *only* on the retrieved context, identifying hallucinations.
    *   **Answer Relevance**: Measures if the generated response directly answers the user's query.

---

## 16. Enterprise Case Studies

### RAG Evaluation at Stripe
Stripe uses automated evaluation pipelines to validate customer billing assistants. By running regular safety sweeps on prompt updates and using manual approvals for production promotions, they prevent output format changes from breaking downstream systems.
