#!/usr/bin/env python3
"""
Lab 1: Pinecone namespace query and metadata filtering mock validator.
Simulates a production Pinecone serverless workflow without API keys.
"""
import sys
import time
import hashlib
import numpy as np


def make_embedding(text: str, dims: int = 8) -> list:
    """Deterministic mock embedding from text hash."""
    h = int(hashlib.md5(text.encode()).hexdigest(), 16)
    np.random.seed(h % 2**31)
    return np.random.rand(dims).tolist()


def cosine_sim(a: list, b: list) -> float:
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))


class MockPineconeIndex:
    """Simulates Pinecone index with namespace isolation and metadata filtering."""

    def __init__(self, name: str, dims: int = 8):
        self.name = name
        self.dims = dims
        self.namespaces: dict = {}

    def upsert(self, vectors: list, namespace: str = "default"):
        if namespace not in self.namespaces:
            self.namespaces[namespace] = []
        self.namespaces[namespace].extend(vectors)
        print(f"[Pinecone] Upserted {len(vectors)} vectors -> namespace='{namespace}'")

    def query(self, vector: list, namespace: str = "default",
              filter: dict = None, top_k: int = 3) -> list:
        start = time.time()
        candidates = self.namespaces.get(namespace, [])

        # Apply metadata pre-filter
        if filter:
            filtered = []
            for item in candidates:
                meta = item.get("metadata", {})
                match = all(meta.get(k) == v for k, v in filter.items())
                if match:
                    filtered.append(item)
        else:
            filtered = candidates

        # Score by cosine similarity
        scored = [(cosine_sim(vector, item["values"]), item) for item in filtered]
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item for _, item in scored[:top_k]]
        elapsed = (time.time() - start) * 1000
        print(f"[Pinecone] Query complete | namespace='{namespace}' | "
              f"filter={filter} | results={len(results)} | latency={elapsed:.1f}ms")
        return results


def main():
    print("=" * 55)
    print(" Pinecone RAG Mock Lab")
    print("=" * 55)

    # Initialize index
    index = MockPineconeIndex("enterprise-knowledge", dims=8)

    # --- STEP 1: Upsert documents ---
    docs = [
        {"id": "doc_1", "text": "Claims threshold is $5000 for automatic approval.",
         "dept": "claims"},
        {"id": "doc_2", "text": "Underwriting risk score above 70 requires escalation.",
         "dept": "underwriting"},
        {"id": "doc_3", "text": "Claims flagged for fraud must be reviewed by compliance.",
         "dept": "claims"},
        {"id": "doc_4", "text": "Policy premium rates are reviewed annually.",
         "dept": "underwriting"},
    ]

    vectors = [
        {
            "id": d["id"],
            "values": make_embedding(d["text"]),
            "metadata": {"dept": d["dept"], "source": "policy_v4.pdf"}
        }
        for d in docs
    ]

    index.upsert(vectors, namespace="tenant-bank-a")

    # --- STEP 2: Query with metadata filter ---
    print()
    query_text = "What is the claims approval limit?"
    query_vec = make_embedding(query_text)

    results = index.query(
        vector=query_vec,
        namespace="tenant-bank-a",
        filter={"dept": "claims"},
        top_k=2
    )

    print("\n=== Top Results ===")
    for i, r in enumerate(results, 1):
        original = next(d["text"] for d in docs if d["id"] == r["id"])
        print(f"[{i}] ID: {r['id']} | Dept: {r['metadata']['dept']}")
        print(f"     Text: {original}")

    print("\nPinecone RAG mock lab completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
