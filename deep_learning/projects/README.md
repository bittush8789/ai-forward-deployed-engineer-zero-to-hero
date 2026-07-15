# Industry Projects: Advanced Deep Learning (Phase 4)

This directory contains the capstone projects for the Advanced Deep Learning curriculum. 
These projects represent the actual work done by Senior Applied AI Engineers in the industry today, spanning Computer Vision, Time-Series Forecasting, and Generative AI.

Many of the core skills for these projects have been implemented as **Mini Projects** directly within the Curriculum Modules. Below is the mapping and guide for all 8 Industry Projects.

---

## Project 1: Customer Churn Prediction
**Skills:** Classification, Dense Neural Networks, Evaluation, Optimization.
**Status:** Completed inside Module 1.
**Code:** `../01_fundamentals/binary_classification.py`
**Task:** This is the baseline project. Ensure you understand binary classification before moving to advanced architectures.

## Project 2: Retail Demand Forecasting using LSTM
**Skills:** Time-Series Forecasting, Deep Learning, Business Forecasting.
**Status:** Completed inside Module 13.
**Code:** `../13_lstm_advanced/demand_forecasting.py`
**Task:** Extend the multivariate LSTM script. Add a new feature for "Holiday" (boolean), and change the architecture to an Encoder-Decoder LSTM to predict the next 7 days simultaneously rather than just 1 day.

## Project 3: Medical Image Classification using CNN
**Skills:** Computer Vision, Transfer Learning, Model Optimization.
**Status:** Completed inside Module 11.
**Code:** `../11_cnn_computer_vision/transfer_learning_pipeline.py`
**Task:** The current pipeline uses ResNet18 for defect detection. Swap the architecture to `EfficientNet-B0`, add rigorous Data Augmentation (rotations, flips) using PyTorch `transforms`, and apply it to a Kaggle Medical Imaging dataset (like Pneumonia X-Rays).

## Project 4: Enterprise Knowledge Assistant (Transformers + Hugging Face)
**Skills:** LLMs, Embeddings, RAG, Semantic Search.
**Status:** Completed inside Module 14.
**Code:** `../14_transformers/rag_embeddings.py`
**Task:** Upgrade the simulated RAG script. Use the actual `sentence-transformers` library to generate embeddings, store them in a local ChromaDB instance, and implement a script that takes a PDF, chunks it, and indexes it.

## Project 5: Customer Support Copilot
**Skills:** Hugging Face, Transformers, Fine-Tuning, RAG.
**Status:** Completed inside Module 17.
**Code:** `../17_hugging_face/lora_finetuning.py`
**Task:** Transition from the simulated script to a real Fine-Tuning pipeline. Use a small model like `distilbert` or a quantized `Llama-3-8B`, format a dataset of Support Tickets (JSONL), and train a LoRA adapter to classify the urgency of the tickets.

## Project 6: Document Intelligence Platform
**Skills:** OCR, Transformers, NLP, Information Extraction.
**Status:** Independent Project (Scaffolded).
**Concept:** Processing physical documents (Invoices, Receipts).
**Task:** Use the Hugging Face `Donut` or `LayoutLM` models. These are multimodal Transformers that take an image of a document as input and directly output structured JSON (e.g., extracting the "Total Amount" from a scanned receipt) without needing a separate OCR step.

## Project 7: Real-Time AI Inference Platform
**Skills:** PyTorch, FastAPI, Docker, Kubernetes.
**Status:** Completed inside Module 10 & 15.
**Code:** `../15_pytorch_production/inference_platform.py`
**Task:** You have the ONNX export script. Now, write a `Dockerfile` that pulls the `python:3.10-slim` image, installs `fastapi` and `onnxruntime`, copies the `.onnx` file, and exposes a REST API on port 8000. Deploy it locally using `docker run`.

## Project 8: Enterprise LLMOps Platform
**Skills:** Hugging Face, MLflow, Docker, Kubernetes, Monitoring.
**Status:** Independent Project (Scaffolded).
**Concept:** Managing the lifecycle of GenAI models.
**Task:** Set up a local MLflow tracking server. Modify the LoRA Fine-Tuning script to log its Training Loss, Validation Loss, and the final adapter weights directly to the MLflow Model Registry. Create a dashboard to compare two different training runs (e.g., Rank=8 vs Rank=16).
