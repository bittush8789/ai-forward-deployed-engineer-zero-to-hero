# 07 Design & Data Modeling

## Theory & Architecture (Ubuntu Setup)
- **Installation**: No additional services are required for pure data modeling; however, installing **SQLAlchemy** and **PyMongo** helps illustrate ORM/ODM patterns.
  ```bash
  sudo apt-get update && sudo apt-get install -y python3-pip
  pip3 install sqlalchemy psycopg2-binary pymongo
  ```
- **Concepts**: 
  - **Entity‑Relationship (ER) modeling** for relational databases.
  - **Document schema design** for MongoDB (flexible, optional fields).
  - **Graph schema design** for Neo4j (node/relationship types).
  - **Hybrid modeling** – combining relational, document, and graph stores in a single AI platform.

## Production Internals
- **SQLAlchemy** generates DDL from Python classes, enabling version‑controlled schema migrations (via Alembic).
- **MongoDB ODM** (e.g., **MongoEngine**) provides model‑level validation.
- **Neo4j OGM** (e.g., **Neomodel**) maps Python classes to graph structures.

## Business Use Cases
- Multi‑tenant SaaS platforms where each tenant has its own schema namespace.
- Storing LLM experiment metadata (relational) alongside chat logs (document) and knowledge graph relationships (graph).

## Schema Design Example (SQLAlchemy)
```python
#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid, datetime

Base = declarative_base()

class Model(Base):
    __tablename__ = "ai_models"
    model_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    metrics = relationship("Metric", back_populates="model")

class Metric(Base):
    __tablename__ = "model_metrics"
    metric_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_id = Column(String, ForeignKey('ai_models.model_id'))
    metric_key = Column(String, nullable=False)
    value = Column(Integer)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    model = relationship("Model", back_populates="metrics")

# Create SQLite for demo (replace with PostgreSQL URL in production)
engine = create_engine('sqlite:///demo.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert a sample model and metric
new_model = Model(name='gpt-x', version='v1.0')
new_metric = Metric(metric_key='accuracy', value=95, model=new_model)
session.add(new_model)
session.commit()
print('Inserted model and metric via SQLAlchemy.')
```
Save as `design_demo.py` in `databases/projects/` and run `python3 design_demo.py`.

## Practical Code (MongoDB ODM via PyMongo)
```python
#!/usr/bin/env python3
from pymongo import MongoClient
import uuid, datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['ai_platform']
models = db['models']
metrics = db['metrics']

model_doc = {
    "_id": str(uuid.uuid4()),
    "name": "gpt-x",
    "version": "v1.0",
    "created_at": datetime.datetime.utcnow()
}
model_id = models.insert_one(model_doc).inserted_id

metric_doc = {
    "_id": str(uuid.uuid4()),
    "model_id": model_id,
    "metric_key": "accuracy",
    "value": 0.96,
    "ts": datetime.datetime.utcnow()
}
metrics.insert_one(metric_doc)
print('Inserted model and metric into MongoDB.')
```
Save as `mongodb_demo_design.py` and run it similarly.

## Interview Questions
- How do you decide between **normalized** relational schema vs. **denormalized** document schema?
- What are the trade‑offs of using an **OGM** (Object Graph Mapper) versus raw Cypher?
- Explain how **multi‑tenant** data isolation can be achieved in PostgreSQL.

## AI FDE Perspective
Front‑end services often rely on a **single API gateway** that abstracts away the underlying storage choice. Consistent data contracts (OpenAPI) ensure UI stability regardless of whether the data lives in PostgreSQL, MongoDB, or Neo4j.
