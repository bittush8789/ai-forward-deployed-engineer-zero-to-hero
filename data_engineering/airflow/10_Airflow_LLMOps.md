# Module 3.10: Airflow for LLMOps

Welcome to **Airflow for LLMOps**. This module bridges traditional data orchestration with LLM systems. In modern enterprise settings, building a RAG (Retrieval-Augmented Generation) system or managing autonomous AI Agents is more than just running a Jupyter notebook. It requires running scheduled, robust, multi-stage pipelines to process unstructured text, generate embeddings, and load vector databases.

---

## 1. Detailed Theory

### The Document Ingestion Pipeline
Ingesting raw data for LLMs is fundamentally different than structured ETL. A typical pipeline consists of:
1. **Document Loading**: Extracting raw text from PDFs, HTML, Word files, or Slack messages.
2. **Text Chunking**: Splitting files into optimal sizes (e.g., 500-character chunks with 50-character overlap) to fit LLM context windows.
3. **Embedding Generation**: Converting text chunks into mathematical vectors (e.g., using OpenAI's `text-embedding-3-small`).
4. **Vector Database Loading**: Indexing vectors and metadata into Pinecone, Weaviate, or ChromaDB.

### Agent Workflow Automation
AI Agents (using frameworks like LangGraph or AutoGen) often perform long-running tasks. Airflow acts as the supervisor that triggers these agents, monitors their execution, captures memory states, and schedules batch evaluation runs.

---

## 2. Architecture Diagram: LLMOps Ingestion Pipeline

```mermaid
flowchart TD
    subgraph "Airflow RAG Ingestion DAG"
        Load[S3FileSensor\nDetect new PDFs] --> Extract[PythonOperator\nExtract Text via PyPDF]
        Extract --> Chunk[PythonOperator\nChunk Text via LangChain]
        
        Chunk --> Map{Dynamic Task Mapping\n.expand()}
        
        Map --> Embed1[OpenAI API\nGenerate Embeddings]
        Map --> Embed2[OpenAI API\nGenerate Embeddings]
        Map --> Embed3[OpenAI API\nGenerate Embeddings]
        
        Embed1 --> LoadDB[PineconeOperator\nUpsert Vectors]
        Embed2 --> LoadDB
        Embed3 --> LoadDB
    end
```

---

## 3. Production Use Cases

1. **Enterprise Knowledge Base Syncing**: Airflow runs every 30 minutes to check if any technical documentation has changed. If so, it processes only the modified files, updates the vectors in Pinecone, and deletes the old vectors.
2. **Batch Evaluation of LLM Outputs**: Once a day, an Airflow DAG runs a test dataset through the current LLM prompt, computes metrics (using Ragas or TruLens) like faithfulness and answer relevance, and alerts the engineering team if the score falls below a threshold.

---

## 4. Real Company Examples

- **Pinecone / Weaviate**: Maintain direct integration guides for Apache Airflow, explaining how to bulk-load enterprise vector data safely using Airflow tasks to avoid HTTP timeouts.
- **LangChain / LangGraph**: Used within Airflow Python operators to build structured agent pipelines that require scheduled batch execution.

---

## 5. Coding Examples

### Airflow RAG Ingestion DAG

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
import openai

def chunk_document(**kwargs):
    raw_text = "Enterprise AI Forward Deployed Engineers build systems that solve real business problems..."
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def embed_and_load(**kwargs):
    ti = kwargs['ti']
    chunks = ti.xcom_pull(task_ids='chunk_text')
    
    pc = Pinecone(api_key="your-pinecone-key")
    index = pc.Index("enterprise-rag")
    
    # Batch embeddings to avoid rate limits
    for i, chunk in enumerate(chunks):
        response = openai.Embedding.create(
            input=chunk,
            model="text-embedding-3-small"
        )
        vector = response['data'][0]['embedding']
        
        index.upsert(vectors=[(f"chunk_{i}", vector, {"text": chunk})])

with DAG('llmops_rag_ingestion', start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    chunk_task = PythonOperator(
        task_id='chunk_text',
        python_callable=chunk_document
    )

    embed_task = PythonOperator(
        task_id='embed_and_load_vectors',
        python_callable=embed_and_load
    )

    chunk_task >> embed_task
```

---

## 6. Hands-on Labs

**Lab: Custom Metadata Design**
**Objective**: Design metadata for document vectors.
**Instructions**:
A company has documents categorized by `department` and `confidentiality_level`. Write the payload dictionary metadata design you would attach to each vector embedding to allow the LLM query system to filter by department AND restrict access to executive-level users only.

---

## 7. Assignments

**Assignment: PDF Processing Bottleneck**
You are processing 10,000 PDF user manuals. Generating embeddings for all files takes 3 hours and frequently runs into OpenAI rate limits (HTTP 429).
Write a short design proposal showing how to structure your Airflow tasks to handle pagination, exponential backoff retries, and dynamic task mapping to handle this workload efficiently.

---

## 8. Interview Questions

1. **Why do we need Airflow for RAG systems if we can just ingest files inside a FastAPI server on-demand?**
   *Answer Hint: API servers are designed for fast, synchronous request-response. Ingesting large manuals involves heavy text extraction, chunking, and calling external model APIs, which can take minutes or hours. Airflow handles these asynchronous pipelines reliably with retry safety and logging, preventing API servers from hanging or timing out.*
2. **What is the risk of using basic text splitters without chunk overlap?**
   *Answer Hint: Semantic context can get cut off in the middle of a sentence at the boundary of a chunk, leading to loss of context. Chunk overlap ensures that contiguous information is preserved across chunks, yielding better vector search results.*

---

## 9. Best Practices (FDE Standards)

- **Vector Metadata Pre-filtering**: Always include tenancy and authorization tags in vector metadata so you can perform fast pre-filtering on the database level, preventing tenant cross-talk.
- **Store Source Mappings**: Always store the mapping between a `vector_id` and the source `document_id` and `page_number` to allow downstream applications to reference sources in chat outputs.

---

## 10. Common Mistakes

- **Hard-indexing Massive Documents**: Uploading complete, raw documents into the Vector database metadata payload, consuming excessive memory and exceeding payload size limits.
- **Ignoring Model Version Upgrades**: Upgrading the embedding model (e.g., from `ada-002` to `text-embedding-3`) without re-embedding the entire historical dataset. You cannot query a database containing mixed-dimension vectors.
