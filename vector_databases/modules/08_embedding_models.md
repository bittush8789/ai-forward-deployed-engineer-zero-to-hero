# Module 8: Embedding Models - Selection, Benchmarking and Cost Analysis

## 1. Theory (50%)

### What Are Embedding Models?
Embedding models convert raw text into dense numerical vectors that capture semantic meaning. The quality of these vectors directly impacts retrieval accuracy in RAG and search systems.

### Embedding Model Landscape

| Provider | Model | Dimensions | Type |
|---|---|---|---|
| OpenAI | text-embedding-3-small | 1536 | API-based |
| OpenAI | text-embedding-3-large | 3072 | API-based |
| Hugging Face | BAAI/bge-m3 | 1024 | Open-source |
| Hugging Face | intfloat/e5-large-v2 | 1024 | Open-source |
| Hugging Face | all-MiniLM-L6-v2 | 384 | Open-source |
| Cohere | embed-v3 | 1024 | API-based |

### OpenAI Embeddings Cost Reference

| Model | Dimensions | Cost per 1M tokens | Best For |
|---|---|---|---|
| text-embedding-3-small | 1536 | $0.020 | Cost-optimized production |
| text-embedding-3-large | 3072 | $0.130 | Maximum quality retrieval |
| ada-002 (legacy) | 1536 | $0.100 | Legacy compatibility |

### Hugging Face Models Reference

| Model | Dimensions | Best For |
|---|---|---|
| BAAI/bge-m3 | 1024 | Multi-lingual, zero-shot retrieval |
| intfloat/e5-large-v2 | 1024 | Instruction-following retrieval |
| hkunlp/instructor-xl | 768 | Task-specific embedding generation |
| all-MiniLM-L6-v2 | 384 | Low-latency, local, lightweight |

### Enterprise Selection Framework
1. **Cost**: API-based models (OpenAI) charge per token. Open-source models run free locally but require GPU infrastructure.
2. **Latency**: Local models like all-MiniLM-L6-v2 run in under 5ms. API calls to OpenAI average 100-300ms.
3. **Quality**: Measured by MTEB benchmark scores for retrieval tasks.
4. **Scalability**: For high throughput, self-host BGE on GPU pods behind a load balancer.

### Architecture Best Practice
- **Development**: Use text-embedding-3-small (cheap, fast, good quality).
- **Production RAG**: Use text-embedding-3-large or BGE-M3 for maximum recall.
- **Edge or Air-Gapped**: Use all-MiniLM-L6-v2 (no network dependency).

---

## 2. Practical (50%)

### Setup
```bash
pip install sentence-transformers openai
```

### Embedding Generation and Benchmark Script
```python
# /tmp/embedding_benchmark.py
import sys
import time
import numpy as np

class MockEmbeddingModel:
    """Simulates different embedding models with dimension and latency profiles."""

    PROFILES = {
        "text-embedding-3-small": {"dims": 1536, "latency_ms": 120},
        "text-embedding-3-large": {"dims": 3072, "latency_ms": 250},
        "bge-m3":                 {"dims": 1024, "latency_ms": 15},
        "all-MiniLM-L6-v2":      {"dims": 384,  "latency_ms": 5},
    }

    def __init__(self, model_name: str):
        if model_name not in self.PROFILES:
            raise ValueError(f"Unknown model: {model_name}")
        self.model_name = model_name
        self.profile = self.PROFILES[model_name]

    def embed(self, text: str):
        """Generate a mock embedding vector."""
        np.random.seed(hash(text) % 2**31)
        time.sleep(self.profile["latency_ms"] / 1000.0)
        return np.random.rand(self.profile["dims"]).astype("float32")


def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def benchmark(model_name: str, texts: list):
    print(f"\n--- Benchmarking: {model_name} ---")
    model = MockEmbeddingModel(model_name)

    start = time.time()
    embeddings = [model.embed(t) for t in texts]
    elapsed_ms = (time.time() - start) * 1000

    # Compute avg pairwise similarity
    sims = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sims.append(cosine_similarity(embeddings[i], embeddings[j]))

    print(f"  Dimensions : {model.profile['dims']}")
    print(f"  Total Time : {elapsed_ms:.1f}ms for {len(texts)} texts")
    print(f"  Avg Pairwise Cosine Similarity: {np.mean(sims):.4f}")


if __name__ == "__main__":
    sample_texts = [
        "The claims threshold is $5000 for auto repairs.",
        "Policy limit for automobile damage claims.",
        "Employee health insurance annual cap is $10,000."
    ]

    for model in ["text-embedding-3-small", "bge-m3", "all-MiniLM-L6-v2"]:
        benchmark(model, sample_texts)

    print("\nBenchmark complete.")
    sys.exit(0)
```

Run the benchmark:
```bash
python3 /tmp/embedding_benchmark.py
```

### Project: Embedding Benchmark Platform
Build a benchmarking platform that evaluates multiple embedding models on your own document corpus and reports accuracy (NDCG@10), latency, and cost per 1M tokens.
