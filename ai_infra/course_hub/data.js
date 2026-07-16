const courseData = {
  title: "AI Infrastructure Engineering for Enterprise AI Platforms",
  subtitle: "Enterprise Production Grade Curriculum",
  modules: [
    {
      id: "01",
      title: "NVIDIA GPU Architecture",
      file: "../modules/01_nvidia_gpu.md",
      taskFile: "../tasks/01_nvidia_gpu_tasks.md",
      labFile: "../labs/gpu_operator_check.sh",
      description: "Tensor Cores, VRAM hierarchy, MIG slicing, and DCGM exporter setup.",
      skills: ["GPU Architecture", "MIG Slicing", "Interconnects", "DCGM Exporter"]
    },
    {
      id: "02",
      title: "CUDA Programming",
      file: "../modules/02_cuda.md",
      taskFile: "../tasks/02_cuda_tasks.md",
      labFile: "../labs/cuda_verify.cu",
      description: "Kernels, NCCL collectives, grid configurations, and compilers execution.",
      skills: ["CUDA Toolkit", "NCCL Collectives", "Warp Scheduling", "Memory Coalescing"]
    },
    {
      id: "03",
      title: "vLLM Serving Engine",
      file: "../modules/03_vllm.md",
      taskFile: "../tasks/03_vllm_tasks.md",
      labFile: "../labs/vllm_benchmark.py",
      description: "PagedAttention KV cache mechanics, parallel context execution, and OpenAI compatible API setups.",
      skills: ["vLLM Engine", "PagedAttention", "KV Cache", "Throughput Tuning"]
    },
    {
      id: "04",
      title: "Triton Inference Server",
      file: "../modules/04_triton.md",
      taskFile: "../tasks/04_triton_tasks.md",
      labFile: "../labs/triton_perf_client.py",
      description: "Dynamic batching pipelines, model repository layouts, multi-model execution, and metrics export.",
      skills: ["Triton Server", "Dynamic Batching", "Concurrent Models", "Pipelines"]
    },
    {
      id: "05",
      title: "Ray Distributed Platform",
      file: "../modules/05_ray.md",
      taskFile: "../tasks/05_ray_tasks.md",
      labFile: "../labs/ray_cluster_setup.sh",
      description: "Actors/tasks distribution, Ray Serve model deployments, cluster auto-scalers, and data ingestion.",
      skills: ["Ray Core", "Ray Serve", "Stateful Actors", "Object Store"]
    },
    {
      id: "06",
      title: "Ollama Local Hosting",
      file: "../modules/06_ollama.md",
      taskFile: "../tasks/06_ollama_tasks.md",
      description: "Modelfiles configuration, GGUF/AWQ quantized model serving, offline private assistant layouts.",
      skills: ["Ollama", "Quantization", "Modelfiles", "Offline AI"]
    },
    {
      id: "07",
      title: "KServe Serverless Serving",
      file: "../modules/07_kserve.md",
      taskFile: "../tasks/07_kserve_tasks.md",
      description: "Knative serverless serving, Istio ingress configurations, canary traffic split, and inference services.",
      skills: ["KServe", "Knative Serving", "Istio Routing", "Canary split"]
    },
    {
      id: "08",
      title: "Model Serving Gateways",
      file: "../modules/08_model_serving.md",
      taskFile: "../tasks/08_model_serving_tasks.md",
      description: "Real-time vs batch APIs, FastAPI scaling patterns, ASGI routers under load.",
      skills: ["API Gateway", "FastAPI", "ASGI servers", "Gunicorn/Uvicorn"]
    },
    {
      id: "09",
      title: "Inference Optimizations",
      file: "../modules/09_inference_optimization.md",
      taskFile: "../tasks/09_inference_optimization_tasks.md",
      description: "ONNX profiling, TensorRT engine compilation (trtexec), pipeline vs tensor parallelism.",
      skills: ["TensorRT", "ONNX format", "Pruning", "Parallelism"]
    },
    {
      id: "10",
      title: "Multi-Tenant AI Platforms",
      file: "../modules/10_multi_tenant.md",
      taskFile: "../tasks/10_multi_tenant_tasks.md",
      description: "Namespace isolation, GPU resource slices allocation (MIG), Keycloak auth, Istio VirtualServices rules.",
      skills: ["Tenancy isolation", "Resource Quotas", "Keycloak", "GPU Allocation"]
    },
    {
      id: "11",
      title: "Enterprise Capstone Projects",
      file: "../modules/11_capstone_projects.md",
      description: "Seven comprehensive capstone projects covering LLM serving platforms, inference platforms, Ray clusters, local servers, and unified portals.",
      skills: ["vLLM Tuning", "Triton Deployment", "Ray Serve Platforms", "MIG Tenancy"]
    },
    {
      id: "12",
      title: "AI Infrastructure Interview Prep",
      file: "../modules/12_interview_prep.md",
      description: "Technical interview questions and answers across all AI infrastructure subsystems.",
      skills: ["Interview Prep", "Architecture Mappings", "Subsystem Mappings", "Diagnostics"]
    }
  ]
};
