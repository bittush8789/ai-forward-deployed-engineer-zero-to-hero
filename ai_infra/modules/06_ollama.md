# Module 6: Local LLM Infrastructure & Modelfile Configurations with Ollama

## 1. Theory (40%)
Ollama is a lightweight, open-source tool designed for running and managing LLMs locally. It simplifies model deployment in private, air-gapped environments by compiling engine runtimes and model checkpoints into a single service.

```
+-------------------------------------------------------------------------------------------------+
|                                           Ollama Service                                        |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                         Modelfile                                       |   |
|   |   - Declares base model parameters, temperature settings, and system prompts            |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Run Model)                                         |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                      Local Engine                                       |   |
|   |   - Quantized inference runs on CPU or local GPU (Metal, CUDA)                          |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Quantization**: Compressing model weights from high precision (like FP16) to lower precision (like INT4 or INT8) to reduce memory usage, allowing large models to run on standard consumer hardware.
*   **Modelfile**: A configuration file used to define base models, model parameters, and custom system instructions.
*   **Offline Serving**: Running LLM inference locally without external cloud dependencies, ensuring data privacy and compliance.

---

## 2. Architecture Deep Dive

Ollama uses a client-server architecture:
*   **Ollama Daemon**: A background service that manages model downloads, loads models into memory, and exposes a REST API endpoint (`localhost:11434`).
*   **Ollama CLI**: A command-line tool that allows users to pull, run, and manage models.
*   **Llama.cpp Backend**: An optimized C++ engine that handles hardware-accelerated tensor math across CPU and GPU cores.

---

## 3. Internal Working

### Model Ingestion & Generation
1.  **Parse Modelfile**: Ollama reads the configuration file to identify the base model and parameters.
2.  **Load Checkpoint**: The daemon loads model weights into memory (VRAM or RAM).
3.  **Execute Inference**: When an API query is received, the C++ engine runs the prompt through the model layers, returning responses.

---

## 4. Tool Comparison

| Feature | Ollama | vLLM | Hugging Face TGI |
|---|---|---|---|
| **Primary Focus** | Local and offline serving | High-throughput cloud serving | Production-grade LLM hosting |
| **Model Format** | GGUF (Quantized) | Safetensors / AWQ | Safetensors / AWQ |
| **Hardware Target** | CPU, GPU, Apple Silicon | Dedicated GPUs | Dedicated GPUs |

---

## 5. Installation Guide
Install Ollama on Ubuntu:
```bash
# Install using the official script
curl -fsSL https://ollama.com/install.sh | sh || echo "Ollama installation failed or already active"
```

---

## 6. Setup Guide
Verify the service is active and listening on port 11434:
```bash
curl -I http://localhost:11434 || echo "Ollama service offline"
```

---

## 7. Commands
```bash
# Download a model version (simulated command)
# ollama pull llama3

# Run a model in interactive terminal mode (simulated command)
# ollama run llama3

# List downloaded models
ollama list || echo "Could not fetch models"

# Display active models running in memory
ollama ps || echo "Ollama service offline"
```

---

## 8. Hands-On Labs
Write a Modelfile configuration `Modelfile` in `/tmp/`:
```properties
# Modelfile configuration
FROM llama3
PARAMETER temperature 0.2
SYSTEM """
You are a secure platform assistant. Return precise, concise technical answers.
"""
```
Write this configuration to disk:
```bash
mkdir -p /tmp/ollama-lab
tee /tmp/ollama-lab/Modelfile << 'EOF'
FROM llama3
PARAMETER temperature 0.2
SYSTEM "You are a secure platform assistant. Return precise answers."
EOF
```
Verify the config is formatted correctly:
```bash
cat /tmp/ollama-lab/Modelfile | grep -i "from"
```

---

## 9. Production Operations

### Designing Private LLM Workloads
For offline applications, download required models in advance and commit custom Modelfiles to Git to version prompt configurations.

---

## 10. Monitoring
Monitor Ollama memory usage:
```bash
ollama ps
```
This shows which models are loaded in memory (VRAM vs CPU RAM) and their memory footprints.

---

## 11. Security
Secure Ollama REST APIs by binding the host address to `127.0.0.1` to block external network access.

---

## 12. Cost Optimization
Use quantized GGUF models (such as Q4_K_M) to reduce VRAM requirements, allowing models to run on cheaper hardware.

---

## 13. Troubleshooting

### Task 13.1: Model Load Slowdowns
*   **Symptom**: Query response times increase on the first request.
*   **Root Cause**: The model is not loaded in memory and must be fetched from disk, or VRAM is exhausted, causing the model to load into slower CPU RAM.
*   **Resolution Strategy**:
    *   Inspect memory allocation:
        ```bash
        ollama ps
        ```
    *   Free up VRAM by closing active applications.

---

## 14. Enterprise Case Studies

### Private AI Assistants at Goldman Sachs
Goldman Sachs deploys Ollama on local developer workstations. By running quantized models locally and blocking external API calls, they provide coding assistants while enforcing data privacy policies.

---

## 15. Interview Questions

### Q1: What is quantization, and why is it critical for local LLM deployments?
*   **Answer**: Quantization compresses model weights to lower precision (like INT4), reducing memory usage and allowing large models to run on standard consumer hardware.

### Q2: Explain the purpose of the Modelfile in Ollama.
*   **Answer**: The Modelfile defines the base model, parameters (like temperature), and custom system instructions for local model deployments.

---

## 16. AI FDE Perspective

### Deploying Local LLMs in Air-Gapped Networks
As an AI Forward Deployed Engineer (FDE), you often deploy local model instances:
*   **Export Models**: Download GGUF checkpoints in advance, copy them to the target system, and build models locally:
    ```bash
    # Build a model from a local GGUF file
    # ollama create my-model -f /tmp/ollama-lab/Modelfile
    ```
This allows deploying custom model versions without needing external network connections.
