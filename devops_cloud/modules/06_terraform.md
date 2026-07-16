# Module 6: Enterprise Infrastructure as Code with Terraform

## 1. Architecture Deep Dive

Terraform is a declarative Infrastructure as Code (IaC) tool that allows developers to define both cloud and on-premises resources in human-readable configuration files.

```
+---------------------------------------------------------------------------------------------------+
|                                          Terraform Core                                           |
|   - Reads configuration files (.tf)                                                               |
|   - Builds the Resource Dependency Graph (Directed Acyclic Graph - DAG)                          |
|   - Reconciles state differences between State File and Real Infrastructure                       |
+------------------------------------+--------------------------------------------------------------+
                                     |
                                     v (RPC Interface)
+------------------------------------+--------------------------------------------------------------+
|                                         Providers                                                 |
|   - Cloud Providers (AWS, Azure, GCP)                                                             |
|   - Platform Providers (Kubernetes, Helm, Docker)                                                 |
|   - Translates Terraform resource calls into target vendor API requests                           |
+------------------------------------+--------------------------------------------------------------+
                                     |
                                     v (Vendor REST APIs)
+------------------------------------+--------------------------------------------------------------+
|                                    Target Infrastructure                                          |
|                AWS APIs | Google Cloud APIs | Azure Resource Manager APIs                         |
+---------------------------------------------------------------------------------------------------+
```

### Directed Acyclic Graph (DAG)
Terraform Core reads configuration files and constructs a Directed Acyclic Graph (DAG) to map dependencies.
*   **Dependency Resolution**: If resource B references resource A (`vpc_id = aws_vpc.main.id`), Terraform schedules resource A to be created first.
*   **Parallel Execution**: Resources without dependencies are created or updated concurrently to optimize execution time.

### State File Purpose
Terraform maintains a JSON file (`terraform.tfstate`) that maps configuration files to real-world resources. The state file tracks metadata (such as IP addresses, resource IDs, and dependencies) to determine changes during execution.

---

## 2. Internal Working

### Execution Lifecycle
1.  **`terraform init`**: Initializes the working directory, downloads provider plugins, and sets up the remote backend.
2.  **`terraform plan`**: Performs a read-only dry run. It queries target APIs to fetch the current state of existing resources, compares it against the configuration files, and outlines the actions (create, update, destroy) needed to reach the desired state.
3.  **`terraform apply`**: Executes the planned actions by calling provider APIs. Upon completion, it writes the updated metadata back to the state file.
4.  **`terraform destroy`**: Reverses the resource graph to delete all resources managed by the current workspace configuration.

### State Locking Mechanics
To prevent concurrent runs from corrupting the state file (e.g., two developers running `apply` at the same time), Terraform locks the state file during mutations. For example, when using an AWS S3 backend, Terraform uses a **DynamoDB table** to acquire and release an exclusive lock ID.

---

## 3. Production Use Cases

### Multi-Account Cloud Architecture
Provisioning isolated VPC networks, security groups, database instances, and IAM roles across development, staging, and production environments.

### Hybrid Cloud Platform Provisioning
Managing physical servers, DNS configurations, Cloudflare routing rules, and Kubernetes workloads through a single, unified codebase.

---

## 4. Security Best Practices

### State File Security
The state file can contain sensitive information in plaintext (such as database passwords or SSH private keys).
*   **Encryption**: Store state files in a remote backend (like AWS S3) with default encryption-at-rest enabled.
*   **Access Control**: Limit IAM permissions to the state bucket.

### Static Analysis Security Scanning
Integrate tools like `tfsec` or `checkov` into CI/CD pipelines to scan configurations for security risks (such as open security groups or unencrypted S3 buckets) before running `apply`.

---

## 5. Scalability Patterns

### Reusable Modules
Avoid duplicating code. Package infrastructure patterns (e.g., standard VPC configurations) into reusable modules:
```hcl
module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
}
```

### Minimizing Blast Radius
Instead of managing all company infrastructure in a single monolithic directory, split configurations into smaller directories (e.g., network, databases, application clusters). This reduces the blast radius of errors and speeds up plans.

---

## 6. Reliability Patterns

### Explicit Dependencies
When Terraform cannot determine dependency ordering automatically (e.g., when a resource relies on an IAM policy role mapping that isn't referenced directly in the resource parameters), use `depends_on`:
```hcl
resource "aws_instance" "app" {
  ami           = "ami-123456"
  instance_type = "t3.micro"
  
  depends_on = [aws_iam_role_policy_attachment.attach]
}
```

### Lifecycle Blocks
Protect critical resources from accidental deletion:
```hcl
lifecycle {
  prevent_destroy = true
}
```

---

## 7. Cost Optimization

### Dynamic Compute Configuration
Configure auto-scaling groups to scale resource footprints down during off-peak hours.

### Cost Estimation Integration
Integrate `infracost` into pull requests to calculate cost changes before running `apply`.

---

## 8. Hands-On Labs

### Lab 8.1: Setting up an AWS VPC Network
Create a virtual network with public and private subnets.
```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "production-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  
  tags = {
    Name = "public-subnet"
  }
}
```

### Lab 8.2: Creating a Custom EC2 Module
Create a reusable module directory `/modules/ec2/`.
```hcl
# modules/ec2/variables.tf
variable "instance_name" {
  type    = string
  default = "web-instance"
}

variable "subnet_id" {
  type = string
}

# modules/ec2/main.tf
resource "aws_instance" "server" {
  ami           = "ami-0c7217cdde317cfec" # Ubuntu x86_64
  instance_type = "t3.micro"
  subnet_id     = var.subnet_id
  
  tags = {
    Name = var.instance_name
  }
}

# modules/ec2/outputs.tf
output "instance_ip" {
  value = aws_instance.server.public_ip
}
```
Using the module in root directory:
```hcl
module "web_server" {
  source        = "./modules/ec2"
  instance_name = "prod-web"
  subnet_id     = aws_subnet.public.id
}
```

### Lab 8.3: Configuring a Remote Backend with State Locking
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-enterprise-tfstate-bucket"
    key            = "state/production.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}
```

### Lab 8.4: Managing Environments with Workspaces
```bash
# 1. Create a workspace for staging
terraform workspace new staging

# 2. Select staging workspace
terraform workspace select staging

# 3. List active workspaces
terraform workspace list
```

### Lab 8.5: Resource Verification CLI flow
```bash
# Initialize working directory
terraform init

# Generate configuration execution plan
terraform plan -out=tfplan.binary

# Apply configuration changes
terraform apply tfplan.binary
```

### Lab 8.6: Importing Infrastructure
Import an existing S3 bucket into Terraform management.
```hcl
# 1. Declare the empty resource shell in main.tf
resource "aws_s3_bucket" "imported_bucket" {}
```
Run command:
```bash
# 2. Import state metadata mapping
terraform import aws_s3_bucket.imported_bucket my-existing-aws-bucket-name
```

### Lab 8.7: Drift Detection
```bash
# Compare real-world resources against state file
terraform plan -detailed-exitcode
# Exit code 0 = No changes, 2 = Drift detected (requires updates)
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Releasing a State Lock
*   **Symptom**: `terraform apply` fails with `Error: Error acquiring the state lock: ... Lock Info: ID: 3ca2b73... info: lock acquired by devops@laptop`.
*   **Root Cause**: A developer ran an execution and force-closed it (e.g., killing the process or terminal window crash). The lock ID was not released.
*   **Resolution Strategy**:
    ```bash
    # 1. Identify the lock ID from the error output (e.g., 3ca2b73)
    # 2. Run force-unlock command (WARNING: verify no one else is currently running apply)
    terraform force-unlock 3ca2b73
    ```

### Task 9.2: Cycle Dependency Errors
*   **Symptom**: `terraform validate` fails with `Error: Cycle: aws_instance.web, aws_security_group.web-sg`.
*   **Root Cause**: Resource A references resource B, and resource B references resource A.
*   **Resolution Strategy**:
    *   Identify the cycle dependency path.
    *   Extract references. For security groups, separate the rules from the group container resource:
        ```hcl
        # Break cycle by using separate security group rule resources
        resource "aws_security_group_rule" "allow_inbound" {
          type              = "ingress"
          security_group_id = aws_security_group.web-sg.id
          # rules...
        }
        ```

### Task 9.3: Missing Required Provider Version Compatibility
*   **Symptom**: `terraform init` fails downloading plugins.
*   **Root Cause**: Declared resource features are incompatible with the downloaded provider version.
*   **Resolution Strategy**:
    *   Inspect `.terraform.lock.hcl` file.
    *   Clear provider caches and update requirements versions:
        ```bash
        rm -rf .terraform/ .terraform.lock.hcl
        terraform init -upgrade
        ```

---

## 10. Real Production Incidents

### Case Study: Accidental Deletion of Database Instances
*   **Incident**: A junior developer renamed a database module reference in the root configuration. Running `terraform apply` interpreted the rename as destroying the old database resource and creating a new one. The database was deleted, causing a 2-hour recovery window.
*   **Remediation**:
    *   Enabled deletion protection (`prevent_destroy = true`) on all production databases.
    *   Integrated mandatory code reviews for Terraform plans in pull requests using automated CI tooling.
    *   Configured automated daily snapshot backups stored in separate accounts.

---

## 11. Interview Questions

### Q1: What is the difference between `count` and `for_each` when creating resources dynamically?
*   **Answer**:
    *   `count` creates resources based on an integer index. If you delete an item from the middle of a list, Terraform will re-create all subsequent resources because their indices shift.
    *   `for_each` accepts maps or sets. Resources are keyed by stable strings instead of numbers. Deleting or modifying a single resource does not affect others.

### Q2: How does Terraform plan determine drift without modifying resources?
*   **Answer**: Terraform fetches state files. During `plan`, it queries cloud provider APIs to fetch the current live attributes of managed resources and compares them to the state file and configuration. If a resource attribute was changed manually in the AWS Console, Terraform highlights it as "Drift" and outlines the steps to revert it back to the config configuration.

### Q3: Explain what `.terraform.lock.hcl` is used for.
*   **Answer**: It is the provider lockfile. It records the exact versions and checksums of the provider plugins downloaded for a project. Committing this file to Git ensures all team members and CI/CD runners use the same provider versions.

### Q4: When would you use a `local-exec` provisioner?
*   **Answer**: To run commands on the local machine executing Terraform (e.g., executing a script to write configuration files or triggering a webhook). Provisioners should be used as a last resort, as they break the declarative model of Terraform.

### Q5: What is the role of `terraform refresh`?
*   **Answer**: `terraform refresh` queries cloud provider APIs to update the state file with any changes made to resources outside of Terraform. It does not modify real infrastructure or configuration files. It is run automatically as part of the `plan` and `apply` lifecycle.

---

## 12. Enterprise Case Studies

### Multi-Cloud Infrastructure Deployment at HashiCorp
HashiCorp uses its own tools to manage hybrid deployments across AWS, GCP, and Azure. By defining infrastructure in a unified repository using Terraform modules, they provision networking interfaces and compute instances across cloud boundaries, maintaining consistency across environments.

---

## 13. System Design Discussions

### GitOps Infrastructure Pipeline Design
*   **Objective**: Design an automated workflow for infrastructure changes.
*   **Architecture Considerations**:
    *   **Automation**: Use tools like Atlantis or GitHub Actions.
    *   **Review Flow**:
        1. A developer creates a Pull Request modifying Terraform files.
        2. The pipeline runs `terraform fmt` and static security scans.
        3. The pipeline runs `terraform plan` and comments the output directly on the PR.
        4. Once approved, a user merges the PR, triggering `terraform apply` to deploy changes.
    *   **State Locking**: Use DynamoDB to lock the state file during runs.

---

## 14. AI Platform Perspective

### Provisioning Compute Infrastructure for AI Training
Provisioning EKS nodes with specialized GPU instances (e.g., G5 or P4 instances on AWS) and configuring node groups:
```hcl
resource "aws_eks_node_group" "gpu_nodes" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "gpu-inference-nodes"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = 2
    max_size     = 10
    min_size     = 1
  }

  instance_types = ["g5.2xlarge"] # GPU instance

  labels = {
    accelerator = "nvidia-a10g"
  }
}
```
This integrates infrastructure provisioning directly into the development lifecycle, allowing AI platform scaling teams to manage GPU allocations alongside standard CPU resources.
