# AI Infrastructure Engineering for Enterprise AI Platforms (Phase 14)

Welcome to the **AI Infrastructure Engineering for Enterprise AI Platforms** curriculum. This curriculum focuses on GPU architectures, CUDA programming tools, vLLM performance tuning, Triton Inference Server, distributed computing with Ray, local model hosting with Ollama, serverless inference via KServe, optimization frameworks, and multi-tenant AI systems.

## Table of Contents
- [Modules](#modules)
- [Practice Tasks](#practice-tasks)
- [Labs](#labs)
- [Dashboard](#dashboard)

### Modules
| # | Module | Description |
|---|--------|-------------|
| 01 | [NVIDIA GPU](./modules/01_nvidia_gpu.md) | Tensor Cores, VRAM hierarchy, MIG slicing, and DCGM exporter setup. |
| 02 | [CUDA](./modules/02_cuda.md) | Kernels, NCCL collectives, grid configurations, and compilers execution. |
| 03 | [vLLM](./modules/03_vllm.md) | PagedAttention KV cache mechanics, parallel context execution, and OpenAI compatible API setups. |
| 04 | [Triton Inference Server](./modules/04_triton.md) | Dynamic batching pipelines, model repository layouts, multi-model execution, and metrics export. |
| 05 | [Ray](./modules/05_ray.md) | Actors/tasks distribution, Ray Serve model deployments, cluster auto-scalers, and data ingestion. |
| 06 | [Ollama](./modules/06_ollama.md) | Modelfiles configuration, GGUF/AWQ quantized model serving, offline private assistant layouts. |
| 07 | [KServe](./modules/07_kserve.md) | Knative serverless serving, Istio ingress configurations, canary traffic split, and inference services. |
| 08 | [Model Serving](./modules/08_model_serving.md) | Real-time vs batch APIs, FastAPI scaling patterns, ASGI routers under load. |
| 09 | [Inference Optimization](./modules/09_inference_optimization.md) | ONNX profiling, TensorRT engine compilation (trtexec), pipeline vs tensor parallelism. |
| 10 | [Multi-Tenant AI Platforms](./modules/10_multi_tenant.md) | Namespace isolation, GPU resource slices allocation (MIG), Keycloak auth, Istio VirtualServices rules. |
| 11 | [Capstone Projects](./modules/11_capstone_projects.md) | Seven comprehensive capstone projects covering LLM serving platforms, inference platforms, Ray clusters, local servers, and unified portals. |
| 12 | [Interview Prep](./modules/12_interview_prep.md) | Interview preparation questions and answers. |

### Practice Tasks
Tasks are located under [ai_infra/tasks/](./tasks/).

### Dashboard
A premium glass-morphic learning portal dashboard is available under [ai_infra/course_hub/](./course_hub/).
