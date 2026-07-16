# Module 7: AI Observability, Tracing & Tracing Infrastructures

## 1. Theory (40%)
AI Observability involves tracking the performance, reliability, and cost of LLM systems. It requires logging model inputs, outputs, and intermediate pipeline steps (such as database queries or agent tool calls) to enable tracing and debugging.

```
+-------------------------------------------------------------------------------------------------+
|                                     Observability Pipeline                                      |
|                                                                                                 |
|   +--------------------+      +--------------------+      +--------------------+                |
|   |   1. User Query    | ---> |  2. RAG Retrieval  | ---> |   3. Model Call    |                |
|   |   (Trace Start)    |      |  (Retrieve docs)   |      |   (Generate text)  |                |
|   +---------+----------+      +---------+----------+      +---------+----------+                |
|             |                           |                           |                           |
|             v (Log Span)                v (Log Span)                v (Log Span)                |
|   +---------+---------------------------+---------------------------+-----------------------+   |
|   |                              4. Tracing Service (LangFuse)                              |   |
|   |   - Compiles spans into a single execution trace                                        |   |
|   |   - Logs latency, token usage, and cost metrics                                         |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Observability Metrics
*   **Latency**: The time taken to return responses.
*   **Token Usage**: The number of input and output tokens consumed.
*   **Cost**: Calculated based on model token rates.
*   **User Feedback**: User satisfaction ratings (e.g., thumbs up/down).

---

## 2. Architecture Deep Dive

Production-grade observability systems run as middleware:
1.  **Trace Context**: The application generates a unique `trace_id` for every request.
2.  **Log Spans**: Each step in the pipeline (retrieval, model call) logs a `span` containing its start/end times and metadata.
3.  **Compile Trace**: The tracing service combines spans into a single execution trace.
4.  **Visualize**: Metrics are displayed in a dashboard (like LangFuse or Arize Phoenix) to identify latency bottlenecks or errors.

---

## 3. Tool Comparison

| Feature | LangFuse | Arize Phoenix | OpenTelemetry |
|---|---|---|---|
| **Primary Focus** | LLM tracing and analytics | ML observability and evaluations | Standard application observability |
| **Self-Hosting** | Moderate complexity | Low complexity | Independent collector setup |
| **Data Format** | Custom JSON format | OTLP / custom formats | OTLP (OpenTelemetry Protocol) |

---

## 4. Tool Installation
Install the observability packages:
```bash
pip install langfuse arize-phoenix opentelemetry-sdk
```

---

## 5. Tool Setup
Configure local credentials for LangFuse:
```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-123456"
export LANGFUSE_SECRET_KEY="sk-lf-123456"
export LANGFUSE_HOST="https://cloud.langfuse.com"
```

---

## 6. CLI Commands
```bash
# Verify OpenTelemetry SDK version
python3 -c "import opentelemetry; print('OpenTelemetry available')"
```

---

## 7. Configuration Files
Define tracing options in `telemetry_config.yaml`:
```yaml
telemetry:
  enabled: true
  provider: langfuse
  sampling_rate: 1.0
  log_inputs: true
```

---

## 8. API Examples
Create a Python script using LangFuse to trace execution steps:
```python
# /tmp/observability_test.py
from langfuse import Langfuse

# 1. Initialize client
langfuse = Langfuse()

def run_traced_pipeline():
    # Start a new trace
    trace = langfuse.trace(name="chat_pipeline")
    
    # 1. Simulate retrieval step (Span)
    span = trace.span(name="document_retrieval")
    # Simulated search logic
    span.end(metadata={"doc_count": 2})
    
    # 2. Simulate model generation (Generation)
    generation = trace.generation(
        name="llm_generation",
        model="gpt-4",
        model_parameters={"temperature": 0.7},
        input="What is LLMOps?",
        output="LLMOps is the practice of running LLMs in production."
    )
    generation.end()
    
    print(f"Logged Trace ID: {trace.id}")

if __name__ == '__main__':
    run_traced_pipeline()
```
Run the trace:
```bash
python3 /tmp/observability_test.py
```

---

## 9. Production Tasks

### Configuring OpenTelemetry Collectors
Deploy OpenTelemetry collectors as sidecars next to your applications to aggregate and route traces to monitoring services.

---

## 10. Troubleshooting

### Task 10.1: Missing Traces in Dashboard
*   **Symptom**: Trace data is not showing up in the LangFuse or Phoenix dashboard.
*   **Root Cause**: Network request drops or incorrect API credentials.
*   **Resolution Strategy**:
    *   Verify credentials and server connection settings:
        ```bash
        curl -I https://cloud.langfuse.com
        ```
    *   Enable debug logging in the SDK client to verify payload transmissions.

---

## 11. Monitoring
Configure alerts in Grafana when average latency exceeds 2 seconds, indicating potential database or model response bottlenecks.

---

## 12. Security
Scrub sensitive user data (like PII) or credentials from traces before logging them to remote dashboards.

---

## 13. Governance
Log and store all execution traces to maintain an audit trail for compliance.

---

## 14. Real Enterprise Incidents

### Case Study: API Keys Leaked in Trace Logs
*   **Incident**: A developer enabled trace logging for debugging. The application logged all API request parameters, including the API key, exposing credentials in the dashboard history.
*   **Remediation**:
    *   Revoked the compromised credentials.
    *   Implemented automated log scrubbing to block sensitive headers.

---

## 15. Interview Questions

### Q1: What is the difference between a Trace and a Span?
*   **Answer**:
    *   **Trace**: The entire execution path of a single request (e.g., user search transaction).
    *   **Span**: A single step within the trace (e.g., database query or model call).

### Q2: Why is OpenTelemetry preferred for enterprise observability?
*   **Answer**: OpenTelemetry is an open standard that decouples metrics collection from specific vendor platforms, allowing teams to route telemetry data to different backends (like Prometheus or Datadog) without rewriting code.

---

## 16. Enterprise Case Studies

### Observability at Bloomberg
Bloomberg uses centralized tracing services to monitor recommender engines. By tracking latency and token usage across runs, they detect execution bottlenecks, optimizing query speeds.
