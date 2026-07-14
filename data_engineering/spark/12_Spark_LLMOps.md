# Module 4.12: Spark for LLMOps

Welcome to **Spark for LLMOps**. While standard data engineering processes records and floats, LLMOps processes unstructured text at scale. To build an enterprise-level RAG (Retrieval-Augmented Generation) system, you must ingest thousands of multi-page PDFs, clean unstructured HTML, chunk text, generate high-dimensional embeddings, and upsert them to a Vector Database. Doing this on a single machine is slow; Spark allows you to parallelize the entire RAG ingestion pipeline.

---

## 1. Detailed Theory

### Unstructured Data Processing at Scale
- **Extraction**: Extracting text from binary files (PDFs, DOCX) using distributed libraries (like PyMuPDF or Tika) wrapped in Spark UDFs.
- **Cleaning**: Removing boilerplate text (headers, footers, HTML tags, script scripts) using regex operations across partitions.

### Distributed Text Chunking
To feed text into an LLM context window, it must be split into chunks:
- A Spark DataFrame contains a column of raw document text.
- A Spark UDF maps over the rows, utilizing chunking libraries (like LangChain's `RecursiveCharacterTextSplitter`) to split the text, returning a list of chunks.
- The DataFrame is then exploded (`F.explode()`) so that each chunk becomes a separate row in the dataset.

### Distributed Embeddings & Loading
- **Embedding Generation**: Calling API endpoints (like OpenAI or Cohere) or running local models (like HuggingFace SentenceTransformers) in parallel on Spark executors to convert text chunks into high-dimensional vectors (e.g., 1536-dimension arrays).
- **Parallel Loading**: Executing parallel writes to a Vector Database (Pinecone, Qdrant, ChromaDB) by establishing database connections locally on each worker.

---

## 2. Architecture Diagram: Distributed RAG Ingestion Flow

```mermaid
flowchart TD
    Raw[(Raw PDFs in S3)] -->|Read Binary Files| Spark[Spark Session]
    Spark -->|UDF: PyMuPDF| Text[DataFrame with Raw Text]
    Text -->|UDF: LangChain Chunking| Chunks[DataFrame with Chunk List]
    Chunks -->|F.explode()| Rows[DataFrame: One Chunk per Row]
    
    subgraph "Parallel Worker Execution"
        Rows -->|Executor 1 API Call| OpenAI1[OpenAI Embeddings]
        Rows -->|Executor 2 API Call| OpenAI2[OpenAI Embeddings]
    end
    
    OpenAI1 -->|Upsert to Pinecone| VectorDB[(Pinecone Vector DB)]
    OpenAI2 -->|Upsert to Pinecone| VectorDB
```

---

## 3. Production Use Cases

1. **Enterprise PDF Ingestion Pipeline**: A bank has 100,000 scanned PDFs of financial statements on S3. A Spark job extracts the text, cleans the characters, chunks the pages, calls the Azure OpenAI API in parallel to generate embeddings, and upserts them to Pinecone.
2. **Dynamic AI Knowledge Base**: Continuously consuming user documentation updates, computing new vector representations, and refreshing the vector database.

---

## 4. Real Company Examples

- **Scale AI**: Processes millions of unstructured documents, images, and sensor data daily, relying on Spark to parallelize formatting and data prep pipelines before feeding them to deep learning models.
- **Palantir**: Uses Spark as the core computing engine to process massive quantities of unstructured client files, building semantic ontologies and linking them to LLM agents.

---

## 5. Coding Examples

### Distributed RAG Ingestion Pipeline in PySpark

```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import ArrayType, StringType
from langchain_text_splitters import RecursiveCharacterTextSplitter
import openai

spark = SparkSession.builder.appName("LLMOpsIngestion").getOrCreate()

# 1. Read binary files (PDFs) from cloud storage
binary_df = spark.read.format("binaryFile").load("s3://enterprise-kb/manuals/*.pdf")

# 2. Extract raw text from binary (using dummy PyMuPDF code for illustration)
def extract_pdf_text(content):
    # Wrap PDF library logic
    import fitz # PyMuPDF
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

extract_text_udf = F.udf(extract_pdf_text, StringType())
text_df = binary_df.withColumn("raw_text", extract_text_udf(F.col("content")))

# 3. Chunk text using LangChain splitter inside a UDF
def chunk_text(text):
    if text is None: return []
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

chunk_udf = F.udf(chunk_text, ArrayType(StringType()))
chunks_df = text_df.withColumn("chunks", chunk_udf(F.col("raw_text")))

# 4. Explode list of chunks into individual rows
exploded_df = chunks_df.select(
    F.col("path").alias("document_path"),
    F.explode(F.col("chunks")).alias("chunk_text")
)

# 5. Generate embeddings and load (executed in parallel on workers)
def generate_embeddings_and_upsert(partition_iterator):
    # Initialize APIs once per partition/worker connection
    from pinecone import Pinecone
    pc = Pinecone(api_key="your-pinecone-key")
    index = pc.Index("rag-index")
    
    batch = []
    for i, row in enumerate(partition_iterator):
        response = openai.Embedding.create(
            input=row.chunk_text,
            model="text-embedding-3-small"
        )
        vector = response['data'][0]['embedding']
        
        batch.append((f"id_{i}", vector, {"text": row.chunk_text, "source": row.document_path}))
        
        # Batch upload to Pinecone
        if len(batch) >= 100:
            index.upsert(vectors=batch)
            batch = []
            
    if len(batch) > 0:
        index.upsert(vectors=batch)

# Trigger execution using mapPartitions
exploded_df.rdd.mapPartitions(generate_embeddings_and_upsert).collect()
```

---

## 6. Hands-on Labs

**Lab: Chunking Exploration**
**Objective**: Build a chunking operator.
**Instructions**:
Write a Python function for a Spark UDF that splits text into chunks. Add metadata to each chunk in the return value (e.g., returning a struct containing `chunk_id`, `chunk_index`, and `character_length`).

---

## 7. Assignments

**Assignment: API Rate Limit Management**
You are calling the OpenAI embedding API from 100 parallel Spark executor tasks. You immediately run into `RateLimitError: 429 Too Many Requests`.
Explain how you would handle this issue in your executor code (e.g., implementing exponential backoff) and how you would configure your Spark session partition size to control concurrency.

---

## 8. Interview Questions

1. **Why do we use `mapPartitions` instead of `map` when calling external APIs or databases in Spark?**
   *Answer Hint: `map` runs row-by-row, meaning Spark would open a connection to the API/database for every single row. `mapPartitions` runs partition-by-partition, allowing you to open one connection per worker partition and reuse it to process thousands of rows, dramatically reducing connection overhead.*
2. **How does `F.explode()` work in PySpark?**
   *Answer Hint: `F.explode()` takes a column containing an array or a list and turns each element of the array into a separate row, repeating the rest of the column values for each new row. This is critical for converting a single document row into multiple chunk rows.*

---

## 9. Best Practices (FDE Standards)

- **Use mapPartitions for API/DB Writes**: Always initialize external API clients (OpenAI, Pinecone) inside a `mapPartitions` block to avoid creating connections for every row.
- **Save Embeddings Offline**: Do not just write embeddings to Pinecone; write them to an offline Delta table on S3. If you need to migrate vector databases later, you can read from S3 instead of re-paying for OpenAI embedding API calls.

---

## 10. Common Mistakes

- **Swallowing HTTP Errors**: Forgetting to catch API timeouts in the executor script, causing a single failed request to crash a 10-hour Spark job.
- **Vector Mismatch**: Changing the embedding model (e.g., from `ada-002` to `text-embedding-3-small`) without updating the vector database schema configuration, resulting in insert errors.
