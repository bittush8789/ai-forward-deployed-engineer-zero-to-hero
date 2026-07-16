# Phase 5: Enterprise Prompt Engineering Academy

Welcome to the **Enterprise Prompt Engineering Academy**. This phase of the AI Forward Deployed Engineer (FDE) curriculum is designed to teach you Prompt Engineering from beginner to enterprise level. 

Instead of basic ChatGPT hacks and generic tricks, this curriculum is tailored to **production-grade LLM applications**, enterprise copilots, Retrieval-Augmented Generation (RAG) systems, autonomous AI agents, security hardening, and performance optimization.

---

## 🗺️ Course Syllabus

The academy is divided into **12 theoretical modules (90%)** and **5 practical projects (10%)**, alongside an interactive web dashboard for hands-on learning.

### 📚 Theory Modules
1. **[Module 1: Fundamentals](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/01_fundamentals.md)**: Prompt anatomy, components, constraints, and lifecycle management.
2. **[Module 2: LLM Behavior](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/02_llm_behavior.md)**: Context windows, tokenization awareness, instruction adherence, and hallucination mechanics.
3. **[Module 3: Prompt Design Principles](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/03_design_principles.md)**: Role assignment, context injection, and structured instruction constraints.
4. **[Module 4: Prompting Techniques](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/04_prompting_techniques.md)**: Zero-shot, few-shot, Chain-of-Thought (CoT), self-consistency, and output format controls.
5. **[Module 5: System Prompts](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/05_system_prompts.md)**: Behavioral boundaries, safety controls, business rule enforcement, and governance.
6. **[Module 6: Enterprise Frameworks](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/06_enterprise_frameworks.md)**: Prompt templating, dynamic workflows, orchestration layers, and standardization.
7. **[Module 7: RAG Prompting](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/07_prompt_for_rag.md)**: Context injection, document citation, hallucination mitigation, and grounding.
8. **[Module 8: Prompting for AI Agents](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/08_prompt_for_agents.md)**: ReAct framing, tool description engineering, state memory formatting, and error handling.
9. **[Module 9: Prompt Evaluation](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/09_prompt_evaluation.md)**: LLM-as-a-judge, automated metrics, assertions, and semantic evaluation.
10. **[Module 10: Prompt Optimization](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/10_prompt_optimization.md)**: Cost optimization, latency reduction, prompt pruning, and semantic caching.
11. **[Module 11: Prompt Security](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/11_prompt_security.md)**: Prompt injection, jailbreak defenses, leakage prevention, and input sanitization.
12. **[Module 12: Prompt Engineering for AI FDE](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/modules/12_fde_perspective.md)**: Discovery workshops, business-to-prompt translation, and ROI metrics.

---

## 🛠️ Practical Projects (10%)

Each project folder includes a complete mockable implementation showing variable interpolation, schema parsing, and evaluation.

1. **[Project 1: Enterprise Knowledge Assistant](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/projects/project1_knowledge_assistant/run_project.py)**
   * **Skills**: RAG prompting, context injection, hallucination reduction, citations.
2. **[Project 2: Customer Support Copilot](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/projects/project2_support_copilot/run_project.py)**
   * **Skills**: System prompt boundaries, safety controls, multi-state dialog handling.
3. **[Project 3: Insurance Claims Assistant](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/projects/project3_claims_assistant/run_project.py)**
   * **Skills**: Domain-specific context, structured output formatting (Pydantic / JSON).
4. **[Project 4: Sales Intelligence Copilot](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/projects/project4_sales_intelligence/run_project.py)**
   * **Skills**: Prompt templates, dynamically computed personas, evaluation scorecards.
5. **[Project 5: Enterprise AI Agent](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/projects/project5_enterprise_agent/run_project.py)**
   * **Skills**: Tool definitions, ReAct execution loops, memory logging.

---

## 🎓 Interview Preparation
- **[Interview Preparation Guide](file:///d:/ai-forward-deployed-engineer-zero-to-hero/generative_ai/prompt_engineering/interview_prep.md)**: A complete question bank with system design cases, technical queries, and AI FDE scenario responses.

---

## 🌐 Interactive Web Hub (Course Dashboard)

To explore interactive playgrounds, cost calculators, security simulators, and quiz modules:
1. Locate the directory `generative_ai/prompt_engineering/course_hub/`.
2. Launch a local web server to prevent browser CORS blocks:
   ```bash
   python -m http.server 8000 --directory generative_ai/prompt_engineering/course_hub
   ```
3. Open your browser and navigate to `http://localhost:8000/`.
