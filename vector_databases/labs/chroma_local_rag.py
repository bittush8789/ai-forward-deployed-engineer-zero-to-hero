#!/usr/bin/env python3
"""
Lab 2: ChromaDB persistent collection management mock.
Simulates add, query, and metadata filtering workflows.
"""
import sys
import hashlib
import numpy as np


def make_embedding(text: str, dims: int = 8) -> list:
    h = int(hashlib.md5(text.encode()).hexdigest(), 16)
    np.random.seed(h % 2**31)
    return np.random.rand(dims).tolist()


def cosine_sim(a: list, b: list) -> float:
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))


class MockChromaCollection:
    def __init__(self, name: str):
        self.name = name
        self._store: list = []

    def add(self, ids: list, documents: list, metadatas: list):
        for i in range(len(ids)):
            emb = make_embedding(documents[i])
            self._store.append({
                "id": ids[i],
                "document": documents[i],
                "embedding": emb,
                "metadata": metadatas[i]
            })
        print(f"[ChromaDB] Added {len(ids)} docs to collection '{self.name}'.")

    def query(self, query_texts: list, n_results: int = 3, where: dict = None) -> dict:
        results = {"ids": [], "documents": [], "metadatas": [], "distances": []}
        for query in query_texts:
            qvec = make_embedding(query)
            candidates = self._store
            if where:
                candidates = [
                    item for item in candidates
                    if all(item["metadata"].get(k) == v for k, v in where.items())
                ]
            scored = [(1.0 - cosine_sim(qvec, item["embedding"]), item)
                      for item in candidates]
            scored.sort(key=lambda x: x[0])
            top = scored[:n_results]
            results["ids"].append([t[1]["id"] for t in top])
            results["documents"].append([t[1]["document"] for t in top])
            results["metadatas"].append([t[1]["metadata"] for t in top])
            results["distances"].append([round(t[0], 4) for t in top])
        return results

    def count(self) -> int:
        return len(self._store)


class MockChromaClient:
    def __init__(self, persist_directory: str = ":memory:"):
        self._collections: dict = {}
        self.persist_directory = persist_directory
        print(f"[ChromaDB] PersistentClient initialized | path='{persist_directory}'")

    def get_or_create_collection(self, name: str) -> MockChromaCollection:
        if name not in self._collections:
            self._collections[name] = MockChromaCollection(name)
            print(f"[ChromaDB] Created collection '{name}'.")
        else:
            print(f"[ChromaDB] Loaded existing collection '{name}'.")
        return self._collections[name]


def main():
    print("=" * 55)
    print(" ChromaDB Local RAG Mock Lab")
    print("=" * 55)

    # Initialize persistent client
    client = MockChromaClient(persist_directory="/data/chroma")
    collection = client.get_or_create_collection("policy_docs")

    # --- STEP 1: Add documents ---
    print()
    collection.add(
        ids=["doc_1", "doc_2", "doc_3", "doc_4"],
        documents=[
            "Claims threshold for auto-approval is $5000.",
            "Underwriting risk score above 70 requires senior review.",
            "Fraud claims must be escalated to the compliance department.",
            "Annual premium reviews happen every January 1st."
        ],
        metadatas=[
            {"dept": "claims",        "source": "policy_v4.pdf"},
            {"dept": "underwriting",  "source": "uw_guide_v2.pdf"},
            {"dept": "claims",        "source": "fraud_policy.pdf"},
            {"dept": "underwriting",  "source": "pricing_manual.pdf"}
        ]
    )

    print(f"[ChromaDB] Collection size: {collection.count()} documents\n")

    # --- STEP 2: Semantic query ---
    results = collection.query(
        query_texts=["What is the approval limit for claims?"],
        n_results=2,
        where={"dept": "claims"}
    )

    print("=== Query Results (dept=claims) ===")
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ), 1):
        print(f"[{i}] {doc}")
        print(f"     Source: {meta['source']} | Distance: {dist}")

    print("\nChromaDB local RAG mock lab completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
