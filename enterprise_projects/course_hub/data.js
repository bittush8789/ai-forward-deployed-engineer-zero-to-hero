const courseData = {
  title: "Build Production-Level Enterprise AI Projects",
  subtitle: "Enterprise Production Grade Curriculum",
  modules: [
    {
      id: "01",
      title: "Enterprise RAG Platform",
      file: "../modules/01_enterprise_rag.md",
      taskFile: "../tasks/01_rag_tasks.md",
      labFile: "../labs/rag_gateway_mock.py",
      description: "Chunking, hybrid search, Qdrant vectors, PostgreSQL logs, and ArgoCD deployment.",
      skills: ["Hybrid Search", "Vector DB", "Groundedness", "ArgoCD"]
    },
    {
      id: "02",
      title: "AI Copilot Platform",
      file: "../modules/02_ai_copilot.md",
      taskFile: "../tasks/02_copilot_tasks.md",
      labFile: "../labs/copilot_tool_mock.py",
      description: "React chat, FastAPI agents, PostgreSQL tool logs, and Kubernetes autoscaling.",
      skills: ["FastAPI agents", "React chat", "Tool calls", "Autoscaling"]
    },
    {
      id: "03",
      title: "Multi-Agent AI System",
      file: "../modules/03_multi_agent.md",
      taskFile: "../tasks/03_agent_tasks.md",
      labFile: "../labs/agent_router_mock.py",
      description: "CrewAI/LangGraph planner, analyst, and reviewer registries, Redis state storage.",
      skills: ["LangGraph", "CrewAI", "Redis memory", "Agent registries"]
    },
    {
      id: "04",
      title: "AI Underwriting Copilot",
      file: "../modules/04_underwriting_copilot.md",
      taskFile: "../tasks/04_underwriting_tasks.md",
      description: "Risk audits, structured Pydantic outputs, and compliance workflows.",
      skills: ["Pydantic schemas", "Risk scoring", "Structured output", "Compliance audit"]
    },
    {
      id: "05",
      title: "AI Claims Assistant",
      file: "../modules/05_claims_assistant.md",
      taskFile: "../tasks/05_claims_tasks.md",
      description: "OCR parsers, image ingestion, fraud flags, and claims database updates.",
      skills: ["OCR parsing", "Visual parsing", "Claims database", "Auto-approval"]
    },
    {
      id: "06",
      title: "AI Fraud Detection Platform",
      file: "../modules/06_fraud_detection.md",
      taskFile: "../tasks/06_fraud_tasks.md",
      labFile: "../labs/fraud_scorer_mock.py",
      description: "XGBoost predictors, Feast features, Kafka events, and Grafana alert limits.",
      skills: ["XGBoost models", "Kafka streams", "Feast feature store", "Grafana alerts"]
    },
    {
      id: "07",
      title: "Enterprise LLMOps Platform",
      file: "../modules/07_llmops_platform.md",
      taskFile: "../tasks/07_llmops_tasks.md",
      labFile: "../labs/observability_exporter.py",
      description: "Prompt versioning tables, LangFuse trackers, evaluation scores (Ragas).",
      skills: ["LangFuse", "Ragas evaluation", "Prompt registry", "Token telemetry"]
    },
    {
      id: "08",
      title: "Multi-Tenant AI Platform",
      file: "../modules/08_multi_tenant_eks.md",
      taskFile: "../tasks/08_multitenant_tasks.md",
      description: "Terraform EKS node pools, Istio virtual namespaces, Keycloak auth, Stripe usage metering.",
      skills: ["AWS EKS", "Istio namespaces", "Keycloak SSO", "Stripe billing"]
    },
    {
      id: "09",
      title: "AI Customer Support Agent",
      file: "../modules/09_customer_support.md",
      description: "Zendesk/Jira connector logic, sentiment analysis, and escalation protocols.",
      skills: ["Jira integration", "Zendesk sync", "Sentiment check", "Escalation paths"]
    },
    {
      id: "10",
      title: "AI Platform Engineering",
      file: "../modules/10_platform_engineering.md",
      description: "Kubeflow training runs, Triton dynamic batch models, vLLM cache tuning.",
      skills: ["Kubeflow", "Triton models", "vLLM serving", "MIG GPU Slicing"]
    }
  ]
};
