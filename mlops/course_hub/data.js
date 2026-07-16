const courseData = {
  title: "MLOps for Enterprise AI Platforms",
  subtitle: "Enterprise Production Grade Curriculum",
  modules: [
    {
      id: "01",
      title: "MLflow Experiment Tracking",
      file: "../modules/01_mlflow.md",
      taskFile: "../tasks/01_mlflow_tasks.md",
      labFile: "../labs/mlflow_tracker.py",
      description: "Setup MLflow tracking servers, log metrics, register models, and manage lifecycle versioning.",
      skills: ["MLflow", "Model Registry", "MinIO Storage", "SQL DBs"]
    },
    {
      id: "02",
      title: "Kubeflow Orchestration",
      file: "../modules/02_kubeflow.md",
      taskFile: "../tasks/02_kubeflow_tasks.md",
      labFile: "../labs/k8s_ml_pipeline.yaml",
      description: "Build automated pipeline DAGs, schedule training operators, configure Katib tuning, and manage multi-tenant workspaces.",
      skills: ["Kubeflow", "Pipelines", "Katib Tuning", "Training Ops"]
    },
    {
      id: "03",
      title: "Data Version Control (DVC)",
      file: "../modules/03_dvc.md",
      taskFile: "../tasks/03_dvc_tasks.md",
      labFile: "../labs/dvc_pipeline_demo.sh",
      description: "Version datasets, cache configurations, track pointer metadata, and run reproducible pipelines.",
      skills: ["DVC", "Data tracking", "Checksums", "Storage Backends"]
    },
    {
      id: "04",
      title: "LakeFS Data Governance",
      file: "../modules/04_lakefs.md",
      taskFile: "../tasks/04_lakefs_tasks.md",
      description: "Git-like data lake versioning, zero-copy cloning, branching, merging, and pre-merge data checks.",
      skills: ["LakeFS", "Data Lakes", "Branching/Merging", "Audit Trails"]
    },
    {
      id: "05",
      title: "Enterprise Feature Stores",
      file: "../modules/05_feature_store.md",
      taskFile: "../tasks/05_feature_store_tasks.md",
      labFile: "../labs/feast_feature_pipeline.py",
      description: "Offline/Online stores configurations, Feast schemas definition, feature materialization, and low-latency feature serving.",
      skills: ["Feast Store", "Redis Caching", "Materialization", "Feature Catalog"]
    },
    {
      id: "06",
      title: "Model Registry Governance",
      file: "../modules/06_model_registry.md",
      taskFile: "../tasks/06_model_registry_tasks.md",
      description: "Track model versions, manage staging/production approvals, configure audit trails, and cryptographically sign models.",
      skills: ["Model Registry", "Lifecycle Stages", "Approvals", "Audit Logs"]
    },
    {
      id: "07",
      title: "Model Monitoring & Drift",
      file: "../modules/07_model_monitoring.md",
      taskFile: "../tasks/07_model_monitoring_tasks.md",
      labFile: "../labs/evidently_monitoring.py",
      description: "Monitor predictions, run statistical drift tests (KS-test, PSI), configure dashboards, and trigger performance alerts.",
      skills: ["Evidently AI", "Prometheus", "Grafana", "Data Drift"]
    },
    {
      id: "08",
      title: "Continuous Training & CI/CD",
      file: "../modules/08_ml_cicd.md",
      taskFile: "../tasks/08_ml_cicd_tasks.md",
      description: "Build continuous training loops, automate validation check gates, and configure GitOps model updates.",
      skills: ["ML CI/CD", "Continuous Training", "Validation Gates", "GitOps"]
    },
    {
      id: "09",
      title: "MLOps Platform Architecture",
      file: "../modules/09_mlops_architecture.md",
      taskFile: "../tasks/09_mlops_architecture_tasks.md",
      description: "Design end-to-end production AI platforms, mapping database connection routing and storage backends.",
      skills: ["MLOps Topology", "Subsystems", "Network Isolation", "Cloud Platforms"]
    },
    {
      id: "10",
      title: "Responsible AI Governance",
      file: "../modules/10_mlops_governance.md",
      taskFile: "../tasks/10_mlops_governance_tasks.md",
      description: "Audit compliance trails, enforce fairness metrics checks, and document standardized model cards.",
      skills: ["AI Regulations", "Model Cards", "Lineage Checking", "Compliance"]
    },
    {
      id: "11",
      title: "Unified AI Platform Blueprint",
      file: "../modules/11_mlops_ai_platforms.md",
      taskFile: "../tasks/11_mlops_ai_platforms_tasks.md",
      description: "Unified MLOps platform integration blueprint, verifying connection status across all database and storage tools.",
      skills: ["Platform Integrations", "Verification Suite", "Troubleshooting"]
    },
    {
      id: "12",
      title: "Enterprise Capstone Projects",
      file: "../modules/12_capstone_projects.md",
      description: "Seven comprehensive real-world capstone projects combining all MLOps, data engineering, and automation skills.",
      skills: ["MLflow Registry", "Kubeflow Pipelines", "DVC Data Governance", "Drift Monitoring"]
    },
    {
      id: "13",
      title: "MLOps Interview Preparation",
      file: "../modules/13_interview_prep.md",
      description: "Standard technical interview questions and model answers spanning MLOps architecture, tools, and platforms.",
      skills: ["Interview Prep", "Architecture Mappings", "Subsystem Mappings", "Diagnostics"]
    }
  ]
};
