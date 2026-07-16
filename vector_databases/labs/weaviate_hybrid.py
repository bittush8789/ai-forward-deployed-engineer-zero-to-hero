#!/usr/bin/env python3
"""
Lab 3: Weaviate schema definition, data ingestion, and hybrid search mock.
Simulates BM25 + Vector fusion without requiring a running Weaviate instance.
"""
import sys
import math
import hashlib
import numpy as np
from collections import defaultdict


def make_embedding(text: str, dims: int = 8) -> list:
    h = int(hashlib.md5(text.encode()).hexdigest(), 16)
    np.random.seed(h % 2**31)
    return np.random.rand(dims).tolist()


def cosine_sim(a: list, b: list) -> float:
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))


class MockWeaviateBM25:
    """Simple BM25 scorer over stored documents."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs: list = []
        self.df: dict = defaultdict(int)
        self.avg_len: float = 0.0

    def index(self, docs: list):
        self.docs = docs
        for doc in docs:
            tokens = set(doc["content"].lower().split())
            for t in tokens:
                self.df[t] += 1
        lengths = [len(d["content"].split()) for d in docs]
        self.avg_len = sum(lengths) / len(lengths) if lengths else 1.0

    def score(self, query: str) -> list:
        N = len(self.docs)
        qterms = query.lower().split()
        scores = []
        for doc in self.docs:
            tf_map = defaultdict(int)
            for token in doc["content"].lower().split():
                tf_map[token] += 1
            doc_len = len(doc["content"].split())
            score = 0.0
            for term in qterms:
                tf = tf_map.get(term, 0)
                df = self.df.get(term, 0)
                if df == 0:
                    continue
                idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
                tf_norm = (tf * (self.k1 + 1)) / (
                    tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_len)
                )
                score += idf * tf_norm
            scores.append((score, doc))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores


def rrf_merge(sparse_ranking: list, dense_ranking: list, k: int = 60) -> list:
    """Reciprocal Rank Fusion combiner."""
    scores = {}
    for rank, (_, doc) in enumerate(sparse_ranking, start=1):
        doc_id = doc["id"]
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    for rank, (_, doc) in enumerate(dense_ranking, start=1):
        doc_id = doc["id"]
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    id_to_doc = {doc["id"]: doc for _, doc in sparse_ranking + dense_ranking}
    sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(scores[i], id_to_doc[i]) for i, _ in sorted_ids]


def main():
    print("=" * 55)
    print(" Weaviate Hybrid Search Mock Lab")
    print("=" * 55)

    # Sample document corpus
    documents = [
        {"id": "d1", "content": "Claims threshold is $5000 for automatic approval.",
         "department": "claims"},
        {"id": "d2", "content": "Underwriting risk score above 70 requires escalation.",
         "department": "underwriting"},
        {"id": "d3", "content": "Claims flagged for fraud must go to compliance.",
         "department": "claims"},
        {"id": "d4", "content": "Annual premium rate tables are updated each January.",
         "department": "underwriting"},
        {"id": "d5", "content": "Automatic approvals apply to claims under policy threshold.",
         "department": "claims"},
    ]

    # --- STEP 1: Index documents ---
    bm25 = MockWeaviateBM25()
    bm25.index(documents)
    print(f"\n[Weaviate] Indexed {len(documents)} documents.\n")

    # --- STEP 2: Hybrid search ---
    query = "What is the claims automatic approval limit?"
    alpha = 0.5  # 0=BM25 only, 1=vector only

    # Sparse (BM25) search
    sparse_ranked = bm25.score(query)
    print(f"[BM25] Top sparse result: '{sparse_ranked[0][1]['content']}'")

    # Dense (vector) search
    qvec = make_embedding(query)
    dense_ranked = sorted(
        [(cosine_sim(qvec, make_embedding(d["content"])), d) for d in documents],
        key=lambda x: x[0], reverse=True
    )
    print(f"[Dense] Top dense result: '{dense_ranked[0][1]['content']}'")

    # RRF fusion
    merged = rrf_merge(sparse_ranked, dense_ranked)
    print(f"\n[Hybrid] alpha={alpha} | RRF merged {len(merged)} results.\n")

    print("=== Hybrid Search Results ===")
    for i, (score, doc) in enumerate(merged[:3], 1):
        print(f"[{i}] Score: {score:.4f} | Dept: {doc['department']}")
        print(f"     {doc['content']}")

    print("\nWeaviate hybrid search mock lab completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
