const courseData = {
  title: "LLMOps for Enterprise AI Platforms",
  subtitle: "Enterprise Production Grade Curriculum",
  modules: [
    {
      id: "01",
      title: "Prompt Management",
      file: "../modules/01_prompt_management.md",
      taskFile: "../tasks/01_prompt_management_tasks.md",
      description: "Manage prompt lifecycles, configure dynamic templates, and integrate registries.",
      skills: ["LangSmith", "PromptLayer", "LangFuse", "Templating"]
    },
    {
      id: "02",
      title: "Prompt Versioning",
      file: "../modules/02_prompt_versioning.md",
      taskFile: "../tasks/02_prompt_versioning_tasks.md",
      description: "Track prompt revisions, configure Git-integrated registries, and design rollback actions.",
      skills: ["Git Integration", "SemVer", "Prompt Registry", "Rollbacks"]
    },
    {
      id: "03",
      title: "LLM Evaluation",
      file: "../modules/03_llm_evaluation.md",
      taskFile: "../tasks/03_llm_evaluation_tasks.md",
      labFile: "../labs/eval_pipeline.py",
      description: "Measure accuracy, toxicity, safety, and configure benchmarking datasets.",
      skills: ["Ragas", "DeepEval", "TruLens", "LLM-as-a-judge"]
    },
    {
      id: "04",
      title: "RAG Evaluation",
      file: "../modules/04_rag_evaluation.md",
      taskFile: "../tasks/04_rag_evaluation_tasks.md",
      description: "Evaluate context relevance, groundedness, and faithfulness in RAG pipelines.",
      skills: ["RAG Triad", "Context Relevance", "Faithfulness", "Hallucinations"]
    },
    {
      id: "05",
      title: "Safety Guardrails",
      file: "../modules/05_guardrails.md",
      taskFile: "../tasks/05_guardrails_tasks.md",
      labFile: "../labs/guardrails_demo.py",
      description: "Configure safety guardrails, block prompt injections, and scrub PII from outputs.",
      skills: ["Guardrails AI", "NeMo Guardrails", "PII Scrubbing", "Input Validation"]
    },
    {
      id: "06",
      title: "Hallucination Detection",
      file: "../modules/06_hallucination_detection.md",
      taskFile: "../tasks/06_hallucination_detection_tasks.md",
      description: "Extract claims, verify facts against context, and calculate groundedness scores.",
      skills: ["Natural Language Inference", "Groundedness", "Claims Extraction"]
    },
    {
      id: "07",
      title: "AI Observability",
      file: "../modules/07_observability.md",
      taskFile: "../tasks/07_observability_tasks.md",
      labFile: "../labs/observability_tracing.py",
      description: "Log spans and traces, measure latency, and monitor user feedback metrics.",
      skills: ["LangFuse", "Arize Phoenix", "OpenTelemetry", "Tracing"]
    },
    {
      id: "08",
      title: "Cost Optimization",
      file: "../modules/08_cost_optimization.md",
      taskFile: "../tasks/08_cost_optimization_tasks.md",
      labFile: "../labs/cost_optimization_routing.py",
      description: "Configure semantic caching, route queries dynamically, and monitor budgets.",
      skills: ["LiteLLM", "Helicone", "Semantic Cache", "Model Routing"]
    },
    {
      id: "09",
      title: "Enterprise LLMOps Architecture",
      file: "../modules/09_llmops_architecture.md",
      taskFile: "../tasks/09_llmops_architecture_tasks.md",
      description: "Design production blueprints mapping prompt stores, routing proxies, and databases.",
      skills: ["Gateway Proxy", "System Layout", "Network Isolation", "Caching"]
    },
    {
      id: "10",
      title: "LLMOps Governance & Compliance",
      file: "../modules/10_llmops_governance.md",
      taskFile: "../tasks/10_llmops_governance_tasks.md",
      description: "Audit compliance trails, verify model cards, and configure risk controls.",
      skills: ["AI Regulations", "Model Cards", "Audit Logs", "Compliance"]
    },
    {
      id: "11",
      title: "Enterprise Capstone Projects",
      file: "../modules/11_capstone_projects.md",
      description: "Six comprehensive capstone projects combining prompt management, safety, observability, and cost control.",
      skills: ["RAG Evaluation", "Observability Setup", "Guardrails Config", "Cost Control"]
    },
    {
      id: "12",
      title: "LLMOps Interview Preparation",
      file: "../modules/12_interview_prep.md",
      description: "Standard technical interview questions and answers across all LLMOps subsystems.",
      skills: ["Interview Prep", "Architecture Mappings", "Subsystem Mappings", "Diagnostics"]
    }
  ]
};
