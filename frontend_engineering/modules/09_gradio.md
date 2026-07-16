# 09 Gradio

## Industry Explanation
Gradio is a Python library that lets developers quickly turn machine‑learning models into interactive web UIs. It is widely adopted for showcasing LLM demos, vision models, and data‑science prototypes, allowing rapid feedback loops without a dedicated front‑end team.

## Enterprise Architecture
- Gradio apps run as lightweight Flask servers, often containerized with Docker.
- For production, they are placed behind reverse proxies (NGINX) and managed with Kubernetes deployments.
- Authentication is added via middleware or API gateways, and static assets are served through a CDN.

## Business Use Cases
- Model demo portals for customers to test LLM capabilities.
- Internal tools for data scientists to experiment with prompts and view results.
- Rapid prototyping of AI‑powered widgets that later get re‑implemented in React/Next.js.

## Production Design
- Define a clear `interface` for inputs/outputs (e.g., `gr.Textbox`, `gr.Label`).
- Use `gr.Blocks` for composable layouts and theming.
- Deploy with `uvicorn` and configure `workers` for concurrency.
- Enable logging and telemetry (Prometheus) for usage monitoring.

## Common Failure Modes
- Memory exhaustion when loading large models in the same process.
- Unhandled exceptions causing the UI to freeze.
- Lack of rate limiting leading to abuse of the demo endpoint.

## Optimization Strategies
- Load models lazily or in a separate worker process.
- Cache inference results with `functools.lru_cache` or external caches (Redis).
- Use `gradio.AsyncIO` for non‑blocking I/O.

## Security Considerations
- Never expose raw model weights; keep them server‑side.
- Enforce authentication at the reverse‑proxy level.
- Sanitize any user‑provided text before passing to the model to avoid injection attacks.

## Accessibility Considerations
- Provide descriptive `label` attributes for Gradio components.
- Ensure keyboard navigation works (tab order, focus). 
- Use high‑contrast themes and test with screen readers.

## Best Practices
- Separate model loading from UI definition.
- Write unit tests for preprocessing functions.
- Keep the UI stateless; rely on Gradio’s session state only when needed.

## AI FDE Perspective
Gradio serves as the rapid‑iteration layer for AI engineers. Production teams later replace Gradio prototypes with robust front‑ends, but the initial UI must still follow security, logging, and compliance standards.

### Code Example: Simple LLM Chat Demo with Gradio
```python
import gradio as gr
import httpx

def query_llm(message: str) -> str:
    resp = httpx.post(
        "https://api.example.com/v1/chat",
        json={"messages": [{"role": "user", "content": message}]},
        timeout=30,
    )
    if resp.status_code != 200:
        return "Error contacting LLM service"
    data = resp.json()
    return data["choices"][0]["message"]["content"]

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AI Chat Demo")
    chatbot = gr.Chatbot()
    txt = gr.Textbox(label="Your message", placeholder="Ask something...")
    btn = gr.Button("Send")

    def respond(message, history):
        reply = query_llm(message)
        history = history + [(message, reply)]
        return history, ""

    btn.click(respond, inputs=[txt, chatbot], outputs=[chatbot, txt])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
```
