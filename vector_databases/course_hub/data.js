const courseData = {
  title: "Vector Databases for Enterprise AI",
  subtitle: "Phase 7 — Production Retrieval Systems Academy",
  modules: [
    {
      id: "01",
      title: "Pinecone",
      file: "../modules/01_pinecone.md",
      taskFile: "../tasks/01_pinecone_tasks.md",
      labFile: "../labs/pinecone_rag_mock.py",
      description: "Managed serverless vector database with namespace isolation and metadata filtering.",
      skills: ["Serverless Architecture", "Namespaces", "Metadata Filtering", "RAG Integration"],
      category: "Managed DB"
    },
    {
      id: "02",
      title: "ChromaDB",
      file: "../modules/02_chromadb.md",
      taskFile: "../tasks/02_chromadb_tasks.md",
      labFile: "../labs/chroma_local_rag.py",
      description: "Open-source persistent vector store for local and containerized RAG deployments.",
      skills: ["Collections", "Persistence", "Local Deployment", "Embedding Functions"],
      category: "Open Source"
    },
    {
      id: "03",
      title: "Weaviate",
      file: "../modules/03_weaviate.md",
      taskFile: "../tasks/03_weaviate_tasks.md",
      labFile: "../labs/weaviate_hybrid.py",
      description: "GraphQL-based vector DB with native hybrid search (BM25 + vector) and multi-tenancy.",
      skills: ["Schema Design", "Hybrid Search", "RRF Fusion", "Multi-Tenancy"],
      category: "Open Source"
    },
    {
      id: "04",
      title: "Milvus",
      file: "../modules/04_milvus.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      labFile: "../labs/milvus_cluster_check.py",
      description: "Distributed vector database for billion-scale similarity search with decoupled compute and storage.",
      skills: ["Query Node", "Data Node", "Index Node", "Horizontal Scaling"],
      category: "Distributed"
    },
    {
      id: "05",
      title: "FAISS",
      file: "../modules/05_faiss.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      labFile: "../labs/faiss_offline_search.py",
      description: "Facebook AI Similarity Search for high-performance local/offline vector indexing.",
      skills: ["Flat Index", "IVF", "HNSW", "Product Quantization"],
      category: "Local / Offline"
    },
    {
      id: "06",
      title: "Hybrid Search",
      file: "../modules/06_hybrid_search.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      description: "Combining BM25 keyword search and dense vector retrieval using Reciprocal Rank Fusion.",
      skills: ["BM25", "Dense Retrieval", "RRF Scoring", "Cohere Rerank"],
      category: "Search"
    },
    {
      id: "07",
      title: "Semantic Search",
      file: "../modules/07_semantic_search.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      description: "Context-aware intent matching using vector embeddings and cosine similarity.",
      skills: ["Cosine Similarity", "Query Expansion", "NDCG", "MRR"],
      category: "Search"
    },
    {
      id: "08",
      title: "Embedding Models",
      file: "../modules/08_embedding_models.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      description: "Benchmarking OpenAI, Hugging Face, and Cohere embedding models on cost, latency, and quality.",
      skills: ["text-embedding-3", "BGE-M3", "E5-large", "MTEB Benchmark"],
      category: "Models"
    },
    {
      id: "09",
      title: "Retrieval Architecture",
      file: "../modules/09_retrieval_architecture.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      description: "End-to-end RAG pipeline: chunking, embedding, indexing, retrieval, reranking, and generation.",
      skills: ["Chunking Strategies", "Metadata RBAC", "Reranking", "Context Injection"],
      category: "Architecture"
    },
    {
      id: "10",
      title: "Production Operations",
      file: "../modules/10_production_operations.md",
      taskFile: "../tasks/04_to_10_tasks.md",
      description: "Scaling, replication, backups, disaster recovery, security, and monitoring for vector DBs.",
      skills: ["Horizontal Scaling", "DR Testing", "RBAC", "Prometheus Metrics"],
      category: "Operations"
    },
    {
      id: "11",
      title: "Enterprise Projects",
      file: "../modules/11_enterprise_projects.md",
      description: "Five portfolio-level blueprints: Knowledge Assistant, Search Platform, Insurance Copilot, Agent Memory, and Large-Scale RAG.",
      skills: ["Pinecone RAG", "Weaviate Search", "ChromaDB", "FAISS Memory", "Milvus at Scale"],
      category: "Projects"
    },
    {
      id: "12",
      title: "Interview Prep",
      file: "../modules/12_interview_prep.md",
      description: "15 detailed Q&A covering Pinecone, ChromaDB, Weaviate, Milvus, FAISS, and system design interviews.",
      skills: ["Pinecone Q&A", "Retrieval Design", "System Design", "RAG Architecture"],
      category: "Interview"
    }
  ]
};
