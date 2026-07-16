# Phase 5: Enterprise Generative AI & LLMs Academy

Welcome to the **Enterprise Generative AI & LLMs Academy**. This phase of the AI Forward Deployed Engineer (FDE) curriculum covers the fundamentals of Large Language Models, embeddings, RAG architectures, model fine-tuning (including parameter-efficient PEFT like LoRA and QLoRA), function calling, schema validation, and autonomous AI agents.

This curriculum focuses on how these components are designed, deployed, optimized, and governed in enterprise-grade applications.

---

## 🗺️ Course Syllabus

The academy consists of **9 theoretical modules (90%)** and **5 practical projects (10%)**, alongside an interactive dashboard for hands-on calculations and evaluations.

### 📚 Theory Modules
1. **[Module 1: LLM Fundamentals](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/01_llm_fundamentals.md)**: Architecture, tokenization, training pipeline (pretraining/alignment), and generation constraints.
2. **[Module 2: Embeddings](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/02_embeddings.md)**: Vector representations, similarity search (cosine, dot product), semantic understanding, and dimensional indexing.
3. **[Module 3: Retrieval-Augmented Generation (RAG)](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/03_rag.md)**: Chunking strategies, vector search integrations, retrieval pipelines, and grounding validations.
4. **[Module 4: Fine-Tuning](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/04_fine_tuning.md)**: Domain adaptation, supervised fine-tuning (SFT), training setups, and model evaluations.
5. **[Module 5: LoRA](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/05_lora.md)**: Low-Rank Adaptation, matrix decomposition, parameter efficiency, and GPU memory math.
6. **[Module 6: QLoRA](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/06_qlora.md)**: Quantization mathematics, 4-bit NormalFloat (NF4), double quantization, and low-cost training pipelines.
7. **[Module 7: Function Calling](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/07_function_calling.md)**: Tool binding schemas, API parsing loops, state synchronization, and error recovery.
8. **[Module 8: Structured Output](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/08_structured_output.md)**: Pydantic schemas, JSON constraints, validation hooks, and reliable pipeline interfaces.
9. **[Module 9: AI Agents](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/modules/09_ai_agents.md)**: Autonomous reasoning (ReAct), system tool integration, memory architectures, and multi-agent setups.

---

## 🛠️ Practical Projects (10%)

Each project folder includes a complete mockable implementation showing real APIs, dynamic data orchestration, and validation checks:

1. **[Project 1: Enterprise Knowledge Assistant](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/projects/project1_knowledge_assistant/run_project.py)**
   * **Skills**: Document chunking, vector storage (ChromaDB), semantic search retrieval.
2. **[Project 2: Insurance Underwriting Copilot](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/projects/project2_underwriting_copilot/run_project.py)**
   * **Skills**: Schema parsing, JSON validation, function-calling API loops.
3. **[Project 3: Customer Support Copilot](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/projects/project3_support_copilot/run_project.py)**
   * **Skills**: LangChain tool-calling agents, conversation checkpoints, state execution.
4. **[Project 4: Legal Document Assistant](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/projects/project4_legal_assistant/run_project.py)**
   * **Skills**: SFT training data preparation, validation splits, downstream parsing.
5. **[Project 5: Enterprise Multi-Agent Platform](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/projects/project5_multi_agent_platform/run_project.py)**
   * **Skills**: LangGraph-style state routing, multi-agent orchestration, state memory.

---

## 🎓 Interview Preparation
- **[Interview Preparation Guide](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/interview_prep.md)**: Technical questions, system designs, and FDE customer discovery protocols for LLMs, RAG, PEFT, and agents.

---

## 🌐 Interactive Web Hub (Course Dashboard)

To explore interactive dashboards, GPU memory calculators, quiz modules, and playgrounds:
1. Locate the directory `generative_ai/prompt_engineering/course_hub/` (for Prompt Engineering) or `generative_ai/course_hub/` (for the Generative AI Academy).
2. Launch a local web server:
   ```bash
   python -m http.server 8000 --directory generative_ai/course_hub
   ```
3. Open your browser and navigate to `http://localhost:8000/`.
