# Module 14: Transformers & Large Language Models

## 1. Industry Explanation
LSTMs revolutionized sequence learning, but they had a fatal flaw: they process data **sequentially**. If a sentence has 1,000 words, the LSTM must wait for word 999 to finish before processing word 1,000. You cannot parallelize it on a GPU.

In 2017, Google published *"Attention Is All You Need"*, introducing the **Transformer**. Transformers process the *entire sequence at once*. They use a mechanism called **Self-Attention** to calculate exactly how much focus every single word should place on every other word in the sentence simultaneously.

**The Split:**
- **Encoders (BERT):** Read the whole text at once to understand deep bidirectional context. Used for Classification, Sentiment, and Embeddings.
- **Decoders (GPT):** Read left-to-right to predict the next word. Used for Generation (ChatGPT, Copilot).
- **Encoder-Decoder (T5, BART):** Used for Translation and Summarization.

---

## 2. Why It Matters (The Business Context)
Before Transformers, training a text model meant gathering 10,000 labeled examples of "Spam" and "Not Spam", and training an LSTM from scratch.
Today, we use **Foundation Models**. OpenAI, Meta (Llama), and Google (Gemini) spent $100M+ training massive GPT models on the entire internet. 

In industry, you rarely train a Transformer from scratch. You either:
1. **Prompt Engineering:** Send the text to an API and ask it to classify it.
2. **Fine-Tuning (LoRA):** Take an open-source model (Llama-3) and train it for 2 hours on your proprietary data.
3. **RAG (Retrieval-Augmented Generation):** Give the model a search engine so it can read your company's private PDFs before answering.

---

## 3. Python Example (Theory / Conceptual)
*The core of a Transformer: Scaled Dot-Product Attention.*

```python
import numpy as np

# Suppose we have 3 words in a sentence, each represented by a 4-dimensional embedding
# Sentence: "Bank of the River" (We want the model to know "Bank" means water, not money)
embeddings = np.array([
    [1.0, 0.0, 0.1, 0.0], # Bank
    [0.0, 1.0, 0.0, 0.0], # of
    [0.0, 0.0, 1.0, 0.9]  # River
])

# In a real Transformer, these are learned weight matrices. We use random for theory.
W_Q = np.random.rand(4, 4) # Query: "What am I looking for?"
W_K = np.random.rand(4, 4) # Key: "What do I contain?"
W_V = np.random.rand(4, 4) # Value: "If you match with me, take this information."

Q = np.dot(embeddings, W_Q)
K = np.dot(embeddings, W_K)
V = np.dot(embeddings, W_V)

# Calculate Attention Scores (Dot product of Queries and Keys)
# High score = High relevance between two words
scores = np.dot(Q, K.T) / np.sqrt(4) # Scale by sqrt(dimension)

# Softmax to get probabilities (weights sum to 1)
attention_weights = np.exp(scores) / np.sum(np.exp(scores), axis=1, keepdims=True)

# The new representation of each word is a weighted sum of all other words' Values!
new_representations = np.dot(attention_weights, V)
```

---

## 4. PyTorch Example (Production Grade)
*Using PyTorch's native `nn.Transformer` for a custom task.*

```python
import torch
import torch.nn as nn

class CustomTransformer(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_layers, num_classes):
        super(CustomTransformer, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        # The core Transformer Encoder (like BERT)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        self.fc = nn.Linear(d_model, num_classes)
        
    def forward(self, src):
        # src shape: [batch_size, sequence_length]
        embedded = self.embedding(src) # [batch_size, sequence_length, d_model]
        
        # Transformer output shape: [batch_size, sequence_length, d_model]
        out = self.transformer_encoder(embedded)
        
        # For classification, we usually take the output of the FIRST token (like BERT's [CLS] token)
        # or average the outputs (Mean Pooling). Here we use Mean Pooling.
        pooled = out.mean(dim=1)
        
        return self.fc(pooled)
```

---

## 5. Business Use Case
**Enterprise RAG Assistant (Retrieval-Augmented Generation)**
A law firm wants an AI that can answer questions about their 50,000 internal legal contracts. 
They cannot use ChatGPT directly because ChatGPT hasn't read their private contracts, and if it guesses, it might hallucinate laws that don't exist.

The MLE team builds a **RAG Pipeline**:
1. They use an **Embedding Model** (a Transformer Encoder) to convert all 50,000 PDFs into dense vectors and store them in a Vector Database (ChromaDB / FAISS).
2. When a lawyer asks, *"What is the termination clause for Client X?"*, the question is embedded.
3. The database performs a semantic Similarity Search and retrieves the exact 3 paragraphs from the database that match the question.
4. The system sends those 3 paragraphs AND the lawyer's question to a **Generative LLM** (a Transformer Decoder), prompting it: *"Based strictly on the provided text, answer the question."*
5. The firm gets perfectly accurate, cited answers without spending $1M fine-tuning an LLM.

---

## 6. Mini Project: RAG Embeddings Scaffold
Run the accompanying script `rag_embeddings.py`.
In industry, we rarely write PyTorch `nn.Transformer` from scratch anymore. We use the **Hugging Face** library.
This script demonstrates the core of modern Enterprise AI: generating semantic embeddings and performing cosine similarity to build a micro-search engine.

**To run:**
```bash
# Requires: pip install transformers torch scikit-learn
python rag_embeddings.py
```

---

## 7. Production Considerations
- **Context Window Limits**: A Transformer has a strict maximum sequence length (e.g., 4,096 or 128k tokens). If you pass a document longer than the limit, the model truncates it or crashes. In production RAG, you must use a Text Splitter (like LangChain's `RecursiveCharacterTextSplitter`) to chunk massive PDFs into 500-word blocks with 50-word overlaps.
- **Vector Databases**: Don't use `numpy` or `scikit-learn` cosine similarity in production. When you have 10 million embeddings, a linear scan takes too long. You must deploy a specialized Vector Database like **Pinecone**, **Milvus**, or **ChromaDB** which uses Hierarchical Navigable Small Worlds (HNSW) to search millions of vectors in milliseconds.

---

## 8. Common Failures
1. **The "Lost in the Middle" Phenomenon**: Even if a modern LLM has a 128k context window, studies show that if you pack the prompt with 50 pages of retrieved documents, the Transformer pays heavy attention to the first page and the last page, but completely ignores the information hidden in the middle pages. RAG systems must retrieve and rank only the top 3-5 most relevant chunks.
2. **Hallucinations**: Generative Transformers are designed to predict the most likely next word, not to state facts. If they don't know the answer, they will confidently lie. RAG mitigates this, but you must actively prompt the model: *"If the answer is not in the context, reply 'I do not know'."*

---

## 9. Interview Questions

**Q1: What is the primary architectural difference between BERT and GPT?**
*Answer*: "BERT is an Encoder-only Transformer. It reads the entire sequence simultaneously in both directions (bidirectional) and is typically used for classification or extracting embeddings. GPT is a Decoder-only Transformer. It reads sequences autoregressively (left-to-right) and uses masked attention to ensure it cannot 'look ahead' at future words, making it perfect for generating text."

**Q2: Explain how the Attention Mechanism allows Transformers to process sequences faster than LSTMs.**
*Answer*: "LSTMs process sequences one token at a time, updating a hidden state sequentially, which prevents GPU parallelization. The Attention Mechanism in Transformers calculates the relevance score between all pairs of words in the sequence simultaneously using massive matrix multiplications. This allows the entire sequence to be processed in parallel across GPU cores."

**Q3: What is RAG, and why is it preferred over Fine-Tuning for injecting private company knowledge into an LLM?**
*Answer*: "RAG (Retrieval-Augmented Generation) stores private documents in a vector database. When a user asks a question, it retrieves the relevant documents and passes them to the LLM as context. It is preferred over fine-tuning because: 1) It prevents hallucinations by grounding the model in retrieved facts. 2) You can easily trace and cite the source document. 3) Updating knowledge is as easy as adding a document to the database, whereas fine-tuning requires retraining the network."
