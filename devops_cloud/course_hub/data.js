const courseData = {
  title: "DevOps & Cloud Engineering Academy",
  subtitle: "Enterprise Production Grade Curriculum",
  modules: [
    {
      id: "01",
      title: "Linux Administration",
      file: "../modules/01_linux.md",
      taskFile: "../tasks/01_linux_tasks.md",
      labFile: "../labs/linux_lab.py",
      description: "Linux architecture, systemd service management, processes, namespaces, resource limits, disk partitioning, and kernel auditing policies.",
      skills: ["Linux Kernels", "Systemd", "cgroups", "Namespaces", "Sysctl", "LVM"]
    },
    {
      id: "02",
      title: "Enterprise Shell Scripting",
      file: "../modules/02_shell_scripting.md",
      taskFile: "../tasks/02_shell_tasks.md",
      labFile: "../labs/shell_lab.sh",
      description: "Writing production shell automations, signal trapping, pipeline redirection, process locking, and custom deployment validation scripts.",
      skills: ["Bash Core", "Process Pipelines", "Signal Handling", "flock", "Automation"]
    },
    {
      id: "03",
      title: "Docker & Containerization",
      file: "../modules/03_docker.md",
      taskFile: "../tasks/03_docker_tasks.md",
      labFile: "../labs/docker_lab.py",
      description: "High-performance containers, multi-stage builds, daemon logging optimization, seccomp filters, and security vulnerability scanning.",
      skills: ["Docker Core", "OverlayFS", "Multi-stage Build", "Trivy Scan", "Docker Compose"]
    },
    {
      id: "04",
      title: "Production Kubernetes",
      file: "../modules/04_kubernetes.md",
      taskFile: "../tasks/04_kubernetes_tasks.md",
      labFile: "../labs/k8s_lab.yaml",
      description: "Multi-replica cluster orchestration, ingress traffic management, config state mapping, rolling updates, and node pressure troubleshooting.",
      skills: ["Kubernetes", "Pod Lifecycles", "Ingress Routes", "Autoscaling", "Troubleshooting"]
    },
    {
      id: "05",
      title: "Helm Package Management",
      file: "../modules/05_helm.md",
      taskFile: "../tasks/05_helm_tasks.md",
      description: "Standardizing application packaging, template rendering engine, multi-environment overrides, and secure secrets management.",
      skills: ["Helm v3", "Go Templates", "Secrets Encryption", "Rollbacks", "Chart Registries"]
    },
    {
      id: "06",
      title: "Infrastructure as Code: Terraform",
      file: "../modules/06_terraform.md",
      taskFile: "../tasks/06_terraform_tasks.md",
      description: "Declarative infrastructure state tracking, remote backends with DynamoDB locking, reusable module engineering, and drift detection.",
      skills: ["Terraform Core", "DAG Graph", "State Locking", "Drift Analysis", "Modules"]
    },
    {
      id: "07",
      title: "GitHub Actions CI/CD",
      file: "../modules/07_github_actions.md",
      taskFile: "../tasks/07_github_actions_tasks.md",
      description: "Event-driven workflows, matrix testing configurations, OpenID Connect federation, and automated vulnerability scanning.",
      skills: ["GitHub Actions", "OIDC Federation", "CI/CD Pipelines", "Dependency Caching", "Security Scans"]
    },
    {
      id: "08",
      title: "Jenkins Pipelines",
      file: "../modules/08_jenkins.md",
      taskFile: "../tasks/08_jenkins_tasks.md",
      description: "Controller-agent architecture, declarative Groovy pipelines, dynamic Kubernetes agents, and shared code libraries.",
      skills: ["Jenkins Core", "Declarative DSL", "Kubernetes Pod Agents", "Shared Libraries"]
    },
    {
      id: "09",
      title: "ArgoCD GitOps Delivery",
      file: "../modules/09_argocd.md",
      taskFile: "../tasks/09_argocd_tasks.md",
      description: "GitOps architecture, three-way diff reconciliations, self-healing deployments, and App-of-Apps pipeline hierarchies.",
      skills: ["ArgoCD", "GitOps", "Three-way Diff", "App-of-Apps", "ApplicationSets"]
    },
    {
      id: "10",
      title: "Amazon Web Services (AWS)",
      file: "../modules/10_aws.md",
      taskFile: "../tasks/10_aws_tasks.md",
      description: "AWS multi-account networking, IAM privilege mapping, EKS cluster provisioning, CloudWatch logs, and cost lifecycle optimization.",
      skills: ["AWS Cloud", "IAM hardening", "Transit Gateway", "Amazon EKS", "CloudWatch"]
    },
    {
      id: "11",
      title: "Microsoft Azure Cloud",
      file: "../modules/11_azure.md",
      taskFile: "../tasks/11_azure_tasks.md",
      description: "VNet hub-and-spoke networking, Microsoft Entra ID integration, AKS cluster deployment, Key Vault secrets, and Geo-Replication.",
      skills: ["Azure Cloud", "Entra ID Role Mapping", "Azure AKS", "Key Vault", "VNet Transit"]
    },
    {
      id: "12",
      title: "Google Cloud Platform (GCP)",
      file: "../modules/12_gcp.md",
      taskFile: "../tasks/12_gcp_tasks.md",
      description: "Custom mode subnets, GKE Workload Identity, Shared VPC networking, cloud monitoring, and budget control policies.",
      skills: ["Google Cloud", "GKE clusters", "Workload Identity", "Shared VPC", "Cloud NAT"]
    },
    {
      id: "13",
      title: "Enterprise Capstone Projects",
      file: "../modules/13_capstone_projects.md",
      description: "Five comprehensive real-world infrastructure orchestration projects combining all DevOps and cloud engineering skills.",
      skills: ["GitOps Platform", "CI/CD Integration", "Multi-Cloud Networks", "AI Infrastructure"]
    }
  ]
};
