import torch
import numpy as np

# ==========================================
# 1. Reproducibility
# ==========================================
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 2. Industry RAG Concept (Micro Search Engine)
# ==========================================
print("--- Enterprise RAG: Semantic Similarity Engine ---")

# In production, we use Hugging Face:
# from transformers import AutoTokenizer, AutoModel
# tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
# model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# To allow this script to run instantly without downloading 500MB models, 
# we will simulate the output of the Embedding Model.
# An embedding model takes a string and outputs a dense vector (e.g., size 384).

documents = [
    "The termination clause states that Client X requires 30 days notice.",
    "The cafeteria serves pizza on Fridays.",
    "To reset your VPN password, contact IT support at extension 404.",
    "Client Y's contract expires on December 31st and requires a 60 day notice."
]

queries = [
    "How do I fix my internet connection?",
    "What is the cancellation policy for Client X?"
]

# Simulate a 5-dimensional embedding space for simplicity
# In reality, 'sentence-transformers' produces 384-dimensional embeddings
doc_embeddings = np.array([
    [0.1, 0.1, 0.9, 0.0, 0.2], # Contract/Client X concept
    [0.9, 0.2, 0.0, 0.1, 0.0], # Food concept
    [0.0, 0.9, 0.1, 0.8, 0.1], # IT/Tech concept
    [0.1, 0.1, 0.8, 0.0, 0.5]  # Contract/Client Y concept
])

query_embeddings = np.array([
    [0.0, 0.8, 0.0, 0.9, 0.1], # IT/Tech query
    [0.2, 0.0, 0.9, 0.0, 0.1]  # Contract/Client X query
])

# ==========================================
# 3. Vector Search (Cosine Similarity)
# ==========================================
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

for i, query in enumerate(queries):
    print(f"\n[USER QUESTION]: {query}")
    
    q_emb = query_embeddings[i]
    
    # Calculate similarity against all documents in the 'database'
    scores = []
    for j, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(q_emb, doc_emb)
        scores.append((score, documents[j]))
        
    # Sort by highest score
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Retrieve Top 1 Document
    top_score, top_doc = scores[0]
    
    print(f"[RETRIEVED CONTEXT] (Score: {top_score:.2f}): {top_doc}")
    print("[ACTION]: Pass the Question and the Context to ChatGPT/Llama to generate the final answer.")

print("\nSuccess: RAG Vector Search Simulated.")
print("In production, replace NumPy similarity with a Vector Database like FAISS or ChromaDB.")
