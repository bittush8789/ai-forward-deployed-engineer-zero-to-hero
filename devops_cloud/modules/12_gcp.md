# Module 12: Enterprise Cloud Infrastructure on GCP

## 1. Architecture Deep Dive

Google Cloud Platform (GCP) organizes resources into a hierarchical structure: **Organization**, **Folders**, **Projects**, and **Resources**.

```
+---------------------------------------------------------------------------------------------------+
|                                            GCP Resource Hierarchy                                 |
|   +-------------------------------------------------------------------------------------------+   |
|   |   Organization (e.g., enterprise.com)                                                     |   |
|   |   - Governs compliance and security policies across the company                           |   |
|   |   +-----------------------------------------------------------------------------------+   |   |
|   |   |   Folder (e.g., Engineering)                                                      |   |   |
|   |   |   - Groups related projects (e.g., Development, Production)                           |   |   |
|   |   |   +---------------------------------------------------------------------------+   |   |   |
|   |   |   |   Project (e.g., prod-data-project)                                       |   |   |   |
|   |   |   |   - Logical billing, resource, and access boundary                            |   |   |   |
|   |   |   |   +------------------------+  +------------------------+                  |   |   |   |
|   |   |   |   |   GKE Cluster          |  |   Cloud Storage Bucket |                  |   |   |   |
|   |   |   |   +------------------------+  +------------------------+                  |   |   |   |
|   |   |   +---------------------------------------------------------------------------+   |   |   |
|   |   +-----------------------------------------------------------------------------------+   |   |
|   +-------------------------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------------------------+
```

### GCP IAM (Identity and Access Management)
IAM manages access control within GCP by defining **who** (members) has **what** (roles) access to **which** resources.
*   **Service Accounts**: Special accounts representing non-human identities (like VMs or automated scripts).
*   **Roles**: Collections of permissions. GCP supports Primitive roles (Owner, Editor, Viewer), Predefined roles, and Custom roles.

### VPC (Virtual Private Cloud) Network Architecture
*   **Custom Mode VPC**: Allows manually creating subnets with custom IP ranges in specific regions (preferred in production over Auto Mode VPCs, which create default subnets in every region).
*   **Firewall Rules**: Stateful packet filters applied to VPC resources using network tags.
*   **Cloud NAT**: Provides outbound internet access for private subnets.
*   **Private Service Connect**: Allows private subnets to connect to Google APIs or external service endpoints using private IP addresses.

---

## 2. Internal Working

### Service Account Token Generation
1.  A resource (such as a Compute Engine VM) requests an access token from the local metadata server (`http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`).
2.  The metadata server validates the VM identity and requests an OAuth 2.0 access token from GCP Resource Manager.
3.  GCP Resource Manager returns the access token to the VM, allowing it to authenticate API requests to other GCP services.

### GKE (Google Kubernetes Engine) VPC-Native Networking
In VPC-Native clusters, pod IP addresses are allocated directly from alias IP ranges defined in the VPC subnet. Traffic between pods on different nodes is routed natively using the VPC network routing infrastructure, eliminating the need for NAT translations or routing tables.

---

## 3. Production Use Cases

### High-Availability GKE Workloads
Deploying web services across multiple zones within a region using GKE managed node pools, horizontal pod autoscaling, and global load-balancing.

### Secure Database Access
Hosting relational databases (like Cloud SQL) with private IP addresses, allowing access only from application servers running in the same VPC network.

---

## 4. Security Best Practices

### Hardening Service Account Permissions
Apply the principle of least privilege. Disable default compute service account permissions and use **GKE Workload Identity** to assign Google Cloud service accounts to Kubernetes ServiceAccounts, avoiding the need for static credentials.

### Enforcing Uniform Bucket-Level Access
Disable fine-grained Access Control Lists (ACLs) on Cloud Storage buckets and enforce IAM policies at the bucket level to simplify access control and audit compliance.

---

## 5. Scalability Patterns

### HTTP(S) Load Balancing + Managed Instance Groups (MIGs)
Configure Managed Instance Groups to scale VM instances dynamically based on CPU utilization or HTTP load balancer traffic metrics.
*   **HTTP(S) Load Balancer**: Anycast IP address routing that directs incoming traffic to the nearest healthy MIG instance.

### GKE Autoscaling Profiles
Configure GKE cluster autoscaler profiles (like `optimize-utilization` or `balanced`) to scale nodes dynamically based on pending pod requirements.

---

## 6. Reliability Patterns

### Cloud Spanner Multi-Region Deployments
Use Cloud Spanner to replicate database workloads across multiple regions with strong consistency, enabling automatic failover and high availability.

### Cloud DNS Failover Routing
Configure Cloud DNS routing policies to failover user traffic to backup endpoints if the primary servers fail health checks.

---

## 7. Cost Optimization

### Committed Use Discounts (CUDs)
Commit to a stable amount of resource consumption (1- or 3-year terms) to save up to 70% on Compute Engine VMs, Cloud SQL databases, or GKE nodes.

### Using GCP Spot VMs
Use Spot VMs (preemptible VMs with no 24-hour runtime limit but subject to reclamation with a 30-second warning) for fault-tolerant workloads to reduce compute costs.

---

## 8. Hands-On Labs

### Lab 8.1: Creating a Custom VPC via gcloud CLI
```bash
# 1. Create a custom VPC network
gcloud compute networks create prod-vpc --subnet-mode=custom

# 2. Create a custom subnet in us-central1
gcloud compute networks subnets create public-subnet \
  --network=prod-vpc \
  --region=us-central1 \
  --range=10.0.1.0/24

# 3. Create a private subnet
gcloud compute networks subnets create private-subnet \
  --network=prod-vpc \
  --region=us-central1 \
  --range=10.0.2.0/24
```

### Lab 8.2: Deploying a VM with IAP Access
Deploy a VM without a public IP address and configure Identity-Aware Proxy (IAP) to allow secure SSH access.
```bash
# 1. Create a private VM instance
gcloud compute instances create private-vm \
  --zone=us-central1-a \
  --subnet=private-subnet \
  --no-address \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud

# 2. Create a firewall rule to allow IAP traffic
gcloud compute firewall-rules create allow-ssh-iap \
  --network=prod-vpc \
  --allow=tcp:22 \
  --source-ranges=35.235.240.0/20
```

### Lab 8.3: IAM Configuration
```bash
# Bind the Storage Object Viewer role to a service account at the project scope
gcloud projects add-iam-policy-binding prod-data-project \
  --member="serviceAccount:my-sa@prod-data-project.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

### Lab 8.4: Provisioning a GKE VPC-Native Cluster
```bash
# Provision GKE cluster with VPC-Native alias IP allocation
gcloud container clusters create prod-gke-cluster \
  --region=us-central1 \
  --node-locations=us-central1-a,us-central1-b \
  --num-nodes=1 \
  --enable-ip-alias \
  --network=prod-vpc \
  --subnetwork=private-subnet \
  --workload-pool=prod-data-project.svc.id.goog
```

### Lab 8.5: Configuring Cloud Monitoring Alerts
```bash
# Create a CPU alert policy for VM instances
gcloud alpha monitoring policies create \
  --display-name="High-CPU-Usage" \
  --conditions="resource.type=\"gce_instance\" AND metric.type=\"compute.googleapis.com/instance/cpu/utilization\" AND value > 0.8" \
  --combiner="OR" \
  --enabled
```

### Lab 8.6: Private Service Connect Configuration
```bash
# 1. Allocate a private IP range in the VPC
gcloud compute addresses create google-apis-ip \
  --global \
  --purpose=VPC_PEERING \
  --addresses=10.0.99.0 \
  --prefix-length=24 \
  --network=prod-vpc

# 2. Create a Private Service Connect endpoint mapping
gcloud compute forwarding-rules create psc-google-apis \
  --global \
  --network=prod-vpc \
  --address=google-apis-ip \
  --target-google-apis-bundle=all-apis
```

### Lab 8.7: Hardening Cloud Storage Buckets
```bash
# Create bucket and enforce Uniform Bucket-Level Access
gcloud storage buckets create gs://my-hardened-enterprise-gcs-bucket --location=us-central1
gcloud storage buckets update gs://my-hardened-enterprise-gcs-bucket --uniform-bucket-level-access
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Private VM Connection Outbound Failure
*   **Symptom**: A virtual machine in a private subnet cannot connect to the internet or run updates.
*   **Root Cause**: The subnet lacks a route to outbound internet access, or Cloud NAT is missing or misconfigured.
*   **Resolution Strategy**:
    *   Verify the subnet has a route to a **Cloud NAT Gateway**:
        ```bash
        gcloud compute routers nats list --router=my-router --region=us-central1
        ```
    *   Verify the firewall rules allow outbound traffic to the destination IP ranges.

### Task 9.2: Access Denied to Cloud Storage
*   **Symptom**: An application running on Compute Engine throws `403 Forbidden: Access denied`.
*   **Root Cause**: The VM service account lacks permissions, or the Cloud Storage bucket IAM policy is explicitly denying access.
*   **Resolution Strategy**:
    *   Verify the service account assigned to the VM:
        ```bash
        gcloud compute instances describe private-vm --zone=us-central1-a | grep serviceAccounts
        ```
    *   Verify the service account has the Storage Object Viewer role on the target bucket:
        ```bash
        gcloud storage buckets get-iam-policy gs://my-target-bucket
        ```

### Task 9.3: GKE Pods Fail to Resolve DNS
*   **Symptom**: Pods start but throw connection timeout errors when trying to reach Google APIs or external domains.
*   **Root Cause**: GKE kube-dns is failing or overloaded, or the VPC network lacks DNS routing rules.
*   **Resolution Strategy**:
    *   Check the status of kube-dns pods in the cluster:
        ```bash
        kubectl get pods -n kube-system -l k8s-app=kube-dns
        ```
    *   Verify the VPC subnet has DNS servers configured, or deploy NodeLocal DNSCache in GKE to reduce DNS latency.

---

## 10. Real Production Incidents

### Case Study: Exposed Default Service Account Permissions
*   **Incident**: A GKE cluster was deployed using default compute service account permissions (`editor` role by default). A vulnerability in a public-facing web pod allowed attackers to run shell commands inside the container. Using the container shell, the attackers queried the VM metadata server, retrieved the VM access token, and used its editor permissions to delete critical project resources.
*   **Remediation**:
    *   Disabled default compute service account permissions on all new projects.
    *   Migrated workloads to **GKE Workload Identity**, assigning Google Cloud service accounts with limited permissions to specific Kubernetes ServiceAccounts.

---

## 11. Interview Questions

### Q1: What is GKE Workload Identity, and how does it work?
*   **Answer**: GKE Workload Identity is the recommended way to access Google Cloud APIs from GKE.
    *   It binds a Kubernetes ServiceAccount (KSA) to a Google Cloud Service Account (GSA).
    *   When a pod makes an API request, GKE intercepts the request and exchanges the pod's Kubernetes service account token for a temporary Google Cloud service account token, avoiding the need to store static credentials in Kubernetes secrets.

### Q2: What is the difference between Auto Mode and Custom Mode VPCs in GCP?
*   **Answer**:
    *   **Auto Mode**: Creates default subnets with predefined IP ranges in every region automatically. While simple, it can lead to IP range conflicts when peering networks.
    *   **Custom Mode**: Allows manually creating subnets with custom IP ranges in specific regions, which is preferred in production to prevent IP conflicts and improve network design.

### Q3: Explain how GCP Shared VPC works.
*   **Answer**: Shared VPC allows an organization to connect resources from multiple host and service projects to a common Virtual Private Cloud (VPC) network.
    *   **Host Project**: Hosts the Shared VPC network configurations (subnets, routing, firewalls).
    *   **Service Projects**: Connect their resources (such as Compute Engine VMs or GKE node pools) to subnets in the host project, enabling centralized network administration and isolation.

### Q4: How do Uniform and Fine-Grained access control models differ in Cloud Storage?
*   **Answer**:
    *   **Uniform Access**: Disables Access Control Lists (ACLs) on the bucket. All permissions are managed using IAM policies at the bucket level, simplifying administration.
    *   **Fine-Grained Access**: Allows managing permissions at the individual object level using ACLs, which is useful when files within the same bucket require different access controls.

### Q5: What is the purpose of Cloud NAT in GCP?
*   **Answer**: Cloud NAT provides outbound internet access for virtual machines and GKE pods running in private subnets, without exposing those resources to direct inbound internet traffic.

---

## 12. Enterprise Case Studies

### High-Volume Architecture scaling at Spotify
Spotify operates its infrastructure on GCP. They migrated their music streaming service container workloads to GKE, using Google Cloud Storage to host audio files. By utilizing the global HTTP(S) Load Balancer and Google Cloud CDN, they route client requests to the nearest healthy GKE region, reducing latency for users.

---

## 13. System Design Discussions

### Secure Shared VPC Network Design
*   **Objective**: Design a secure network architecture for an enterprise.
*   **Architecture Considerations**:
    *   **Shared VPC**: Deploy a Shared VPC in a Network Host Project. Connect service projects (such as Development or Production) to specific subnets.
    *   **Firewall Rules**: Enforce firewall rules in the host project using network tags to restrict traffic between service projects.
    *   **External Access**: Route outbound internet traffic through Cloud NAT Gateways in the host project, and restrict inbound access using Cloud Armor protection.

---

## 14. AI Platform Perspective

### Provisioning Compute Infrastructure for AI Training
Running deep learning models requires provisioning GPU-enabled virtual machines (such as A2 or G2 instance families on GCP) and configuring storage buffers.

```hcl
# Terraform definition for GCP GPU VM
resource "google_compute_instance" "gpu_node" {
  name         = "gpu-ml-node"
  machine_type = "a2-highgpu-1g" # NVIDIA A100 GPU
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "deeplearning-platform-release/pytorch-latest-gpu"
    }
  }

  network_interface {
    network    = "prod-vpc"
    subnetwork = "private-subnet"
  }

  guest_accelerator {
    type  = "nvidia-tesla-a100"
    count = 1
  }

  # Allow host GPU drivers to load
  scheduling {
    on_host_maintenance = "TERMINATE"
  }
}
```
This integrates infrastructure provisioning directly into the development lifecycle, allowing MLOps teams to deploy GPU instances alongside GKE node groups and GCS buckets.
