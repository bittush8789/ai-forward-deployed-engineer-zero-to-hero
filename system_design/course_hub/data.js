const courseData = {
  title: "System Design for Enterprise AI Platforms",
  subtitle: "Enterprise Production Grade Curriculum",
  modules: [
    {
      id: "01",
      title: "Distributed Systems Design",
      file: "../modules/01_distributed_systems.md",
      taskFile: "../tasks/01_distributed_systems_tasks.md",
      labFile: "../labs/microservices_check.py",
      description: "REST/gRPC microservices, sharding, replication, CAP theorem, and Saga/CQRS design patterns.",
      skills: ["REST/gRPC", "CAP Theorem", "Saga Pattern", "CQRS"]
    },
    {
      id: "02",
      title: "System Scalability",
      file: "../modules/02_scalability.md",
      taskFile: "../tasks/02_scalability_tasks.md",
      description: "Horizontal/vertical scaling, reverse proxies (NGINX), memory caching (Redis), sharding, and queue-based scaling.",
      skills: ["Load Balancing", "Redis Cache", "Database Sharding", "Kafka"]
    },
    {
      id: "03",
      title: "High Availability",
      file: "../modules/03_high_availability.md",
      taskFile: "../tasks/03_high_availability_tasks.md",
      labFile: "../labs/ha_failover_test.sh",
      description: "Active-Active/Active-Passive setups, primary-secondary database replication, and Multi-AZ layouts.",
      skills: ["Redundancy", "Database replication", "Multi-AZ", "Failovers"]
    },
    {
      id: "04",
      title: "Disaster Recovery",
      file: "../modules/04_disaster_recovery.md",
      taskFile: "../tasks/04_disaster_recovery_tasks.md",
      labFile: "../labs/dr_backup_velero.sh",
      description: "RTO/RPO objectives, Velero backups, cross-region replication, and recovery checks.",
      skills: ["RTO/RPO", "Velero Backups", "Cross-Region Replication", "Disaster Recovery"]
    },
    {
      id: "05",
      title: "Event-Driven Systems",
      file: "../modules/05_event_driven.md",
      taskFile: "../tasks/05_event_driven_tasks.md",
      labFile: "../labs/kafka_event_stream.py",
      description: "Pub/Sub communication, Kafka event streams, consumer decoupling, and event processing.",
      skills: ["Kafka", "Event Streaming", "Decoupling", "Asynchronous"]
    },
    {
      id: "06",
      title: "Enterprise Architecture",
      file: "../modules/06_enterprise_architecture.md",
      taskFile: "../tasks/06_enterprise_architecture_tasks.md",
      description: "Microservices architectures, Domain-Driven Design (DDD), and hexagonal interfaces.",
      skills: ["Clean Architecture", "Hexagonal Design", "Microservices", "DDD"]
    },
    {
      id: "07",
      title: "AI System Design",
      file: "../modules/07_ai_system_design.md",
      taskFile: "../tasks/07_ai_system_design_tasks.md",
      description: "Data, training, serving, and monitoring layers in production AI platforms.",
      skills: ["RAG Design", "AI Agents", "vLLM serving", "Triton Pipelines"]
    },
    {
      id: "08",
      title: "Multi-Tenant Architecture",
      file: "../modules/08_multi_tenant.md",
      taskFile: "../tasks/08_multi_tenant_tasks.md",
      labFile: "../labs/multitenant_routing.py",
      description: "Shared DB vs separate schemas, computing bounds, Keycloak authentication, and usage metering.",
      skills: ["Multi-Tenancy", "SSO/Keycloak", "Billing Metering", "Namespace Isolation"]
    },
    {
      id: "09",
      title: "Capstone System Projects",
      file: "../modules/09_capstone_projects.md",
      description: "Five capstone systems design projects covering RAG platforms, multi-agent routing, Triton inference, MLOps, and SaaS portals.",
      skills: ["RAG Ingestion", "Agent Routing", "Inference Platforms", "MLOps Architectures"]
    },
    {
      id: "10",
      title: "System Design Interview Prep",
      file: "../modules/10_interview_prep.md",
      description: "Technical interview preparation questions and answers across all system design categories.",
      skills: ["Interview Prep", "Architecture Mappings", "Subsystem Mappings", "Diagnostics"]
    }
  ]
};
