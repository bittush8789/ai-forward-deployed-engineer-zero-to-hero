# 08 Streamlit

## Industry Explanation
Streamlit has become the go‑to framework for data scientists and AI engineers to rapidly prototype interactive web apps. Enterprises use it to build internal analytics dashboards, model observability tools, and LLM demo interfaces without heavy front‑end overhead.

## Enterprise Architecture
- Streamlit apps run as Python processes behind a reverse proxy (NGINX, Traefik) and are containerized (Docker) for scaling.
- State is managed via session state (`st.session_state`) and can be persisted to Redis or a database for multi‑user scenarios.
- Deployments often use Kubernetes with `helm` charts or serverless platforms (AWS Lambda via `aws-serverless-express`).

## Business Use Cases
- Real‑time model performance dashboards for monitoring LLM latency and token usage.
- Interactive prompt‑engineering tools where users tweak prompts and see immediate outputs.
- Internal AI knowledge bases that allow employees to query embeddings and view results.

## Production Design
- Use `st.set_page_config` for SEO‑friendly titles and layout.
- Cache expensive computations with `@st.cache_data` or `@st.cache_resource`.
- Secure endpoints by disabling public access and authenticating via OAuth2/JWT.

## Common Failure Modes
- Uncontrolled recomputation causing high CPU load.
- Memory leaks from storing large model objects in session state.
- Lack of authentication exposing internal models.

## Optimization Strategies
- Leverage Streamlit’s built‑in caching and memoization.
- Deploy behind a CDN and enable gzip compression.
- Use async I/O (`asyncio`, `httpx`) for external API calls.

## Security Considerations
- Never expose raw model weights; serve only inference endpoints.
- Enforce CSP headers via reverse proxy.
- Sanitize any user‑provided markdown/HTML displayed with `st.markdown(..., unsafe_allow_html=False)`.

## Accessibility Considerations
- Provide keyboard‑accessible widgets (use `st.button` with proper `key`).
- Ensure color contrast in custom themes.
- Add `aria-label` attributes via `st.markdown` when inserting custom HTML.

## Best Practices
- Keep UI logic separate from model inference; use a service layer.
- Write unit tests for data processing functions with `pytest`.
- Use `streamlit-authenticator` or custom auth for user management.

## AI FDE Perspective
Front‑end engineers bridge AI services and business users by exposing streamlined Streamlit components that hide model complexity while delivering realtime insights.

### Code Example: Streamlit AI Chat Dashboard
```python
import streamlit as st
import httpx

st.set_page_config(page_title="AI Chat Dashboard", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 AI Assistant")

for msg in st.session_state.messages:
    role = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(f"**{role}:** {msg["content"]}")

user_input = st.chat_input("Ask a question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        resp = httpx.post(
            "https://api.example.com/v1/chat",
            json={"messages": st.session_state.messages},
            timeout=30,
        )
        if resp.status_code == 200:
            answer = resp.json()["choices"][0]["message"]["content"]
        else:
            answer = "Error contacting AI service."
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.experimental_rerun()
```
