#!/usr/bin/env python3
"""
Project 1: Enterprise Knowledge Assistant (Embeddings & RAG)
Skills Focus: Document Chunking, Embedding Similarity, Vector Queries.

This script demonstrates how an FDE builds a vector similarity search engine 
from scratch using math representations. It reads policy documents, chunks them, 
generates dense vector representations, indexes them in a local catalog, 
and retrieves the most relevant chunks using Cosine Similarity.
"""

import math

# Sample document corpus
DOCUMENTS = [
    {
        "id": "Doc-1",
        "title": "Corporate WFH Guideline 2026",
        "content": "All full-time staff can work remotely up to 2 days per week. Managers must approve schedules in the HR hub."
    },
    {
        "id": "Doc-2",
        "title": "Travel Expense Policy",
        "content": "Travel meals are capped at $75 per day. Receipt images must be uploaded within 30 days of returning."
    },
    {
        "id": "Doc-3",
        "title": "IT Equipment Standard",
        "content": "Standard allocation is a laptop, a keyboard, and a 27-inch monitor. Upgrades require director justification."
    }
]

# Vocabulary dictionary for vector representations
VOCABULARY = ["remote", "work", "wfh", "travel", "expense", "meal", "laptop", "monitor", "equipment"]

def get_word_frequencies(text):
    """Calculates term frequency mapping for the text."""
    words = text.lower().replace(".", "").replace(",", "").split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def generate_text_embedding(text, vocab):
    """
    Generates a dense vector representation (embedding) by mapping term 
    frequencies to the vocabulary dimension index.
    """
    freqs = get_word_frequencies(text)
    vector = []
    for word in vocab:
        # Simple count-based embedding mapping
        vector.append(float(freqs.get(word, 0)))
    
    # Normalize vector to unit length
    magnitude = math.sqrt(sum(x**2 for x in vector))
    if magnitude == 0:
        return [0.0] * len(vocab)
    return [x / magnitude for x in vector]

def cosine_similarity(v1, v2):
    """Calculates cosine similarity dot product between two normalized vectors."""
    return sum(a * b for a, b in zip(v1, v2))

class LocalVectorDatabase:
    def __init__(self, vocabulary):
        self.vocab = vocabulary
        self.index = []

    def index_document(self, doc_id, doc_title, text):
        embedding = generate_text_embedding(text, self.vocab)
        self.index.append({
            "id": doc_id,
            "title": doc_title,
            "content": text,
            "embedding": embedding
        })

    def query(self, query_text, top_k=2):
        query_vector = generate_text_embedding(query_text, self.vocab)
        results = []
        
        for item in self.index:
            score = cosine_similarity(query_vector, item["embedding"])
            results.append({
                "id": item["id"],
                "title": item["title"],
                "content": item["content"],
                "score": score
            })
            
        # Sort results by similarity score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

def main():
    print("Project 1: Enterprise Knowledge Assistant (Vector DB Ingest)")
    print("="*60)
    
    db = LocalVectorDatabase(VOCABULARY)
    
    # 1. Ingest corpus
    print("Ingesting and embedding documents...")
    for doc in DOCUMENTS:
        db.index_document(doc["id"], doc["title"], doc["content"])
        print(f" - Indexed: {doc['title']}")
        
    print("\nVector Database Ingestion Complete.")
    print("="*60)
    
    # 2. Run query checks
    queries = [
        "What are the guidelines for remote work or WFH?",
        "How do I submit meal expenses?"
    ]
    
    for query in queries:
        print(f"\nUser Query: '{query}'")
        matches = db.query(query, top_k=1)
        for idx, match in enumerate(matches):
            print(f"Match {idx+1} [Score: {match['score']:.4f}]:")
            print(f" - Title: {match['title']}")
            print(f" - Content: {match['content']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
