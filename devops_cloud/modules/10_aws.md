# Module 10: Enterprise Cloud Infrastructure on AWS

## 1. Architecture Deep Dive

Amazon Web Services (AWS) provides cloud services organized into a hierarchical structure: **Regions**, **Availability Zones (AZs)**, and **Edge Locations**.

```
+---------------------------------------------------------------------------------------------------+
|                                            AWS Global Infrastructure                              |
|   +-------------------------------------------------------------------------------------------+   |
|   |   AWS Region (e.g., us-east-1)                                                            |   |
|   |   - Low-latency geographic area containing isolated AZs                                   |   |
|   |   +--------------------------+  +--------------------------+  +--------------------------+ |   |
|   |   |   Availability Zone 1    |  |   Availability Zone 2    |  |   Availability Zone 3    | |   |
|   |   |   - Isolated data center |  |   - Isolated data center |  |   - Isolated data center | |   |
|   |   |   - Independent power/net|  |   - Independent power/net|  |   - Independent power/net| |   |
|   |   +--------------------------+  +--------------------------+  +--------------------------+ |   |
|   +-------------------------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------------------------+
```

### AWS IAM (Identity and Access Management)
IAM manages authentication and authorization within AWS.
*   **Users**: Physical operators or applications requiring long-lived access credentials.
*   **Groups**: Collections of users sharing common access permissions.
*   **Roles**: Identities assigned permissions for short-lived sessions (e.g., EC2 instances accessing S3 buckets).
*   **Policies**: JSON documents defining allowed or denied actions against resources.

### VPC (Virtual Private Cloud) Network Architecture
A VPC is an isolated network partition inside AWS.
*   **Subnets**: IP ranges within a VPC.
    *   *Public Subnets*: Connect directly to the internet via an **Internet Gateway (IGW)**.
    *   *Private Subnets*: Isolated from direct inbound internet traffic. Outbound traffic is routed through a **NAT Gateway** running in a public subnet.
*   **Route Tables**: Define routing targets for subnet traffic.
*   **VPC Endpoints (PrivateLink)**: Allow private subnets to communicate with AWS services (like S3 or DynamoDB) using AWS internal networks, bypassing the public internet.

---

## 2. Internal Working

### IAM Policy Evaluation Logic
When an identity requests access to a resource, AWS evaluates policy rules using a specific logic:
1.  By default, all requests are **Denied**.
2.  AWS evaluates all applicable policies (Identity-based, Resource-based, SCPs).
3.  If an **Explicit Deny** is found, the evaluation immediately exits, returning **Denied**.
4.  If an **Explicit Allow** is found (and no explicit deny matches), the evaluation returns **Allowed**.
5.  If no explicit allow is found, the request returns **Denied** (Implicit Deny).

### EC2 Nitro System Virtualization
AWS Nitro replaces traditional hypervisors (like Xen) with dedicated hardware cards for network, storage, and security virtualization. This offloads system virtualization tasks from host CPUs, allowing EC2 instances to achieve near-bare-metal performance.

### Amazon EKS & AWS VPC CNI Networking
Unlike standard CNI plugins that use virtual networks, the **Amazon VPC CNI** allocates physical IP addresses from the VPC subnet's IP range directly to Kubernetes pods. This allows pods to communicate with other VPC resources without routing through a NAT translation layer.

---

## 3. Production Use Cases

### Multi-AZ Microservice Infrastructure
Deploying containerized microservices across multiple availability zones behind an **Application Load Balancer (ALB)** to ensure high availability and prevent downtime if a single data center fails.

### Secure Database Hosting
Hosting relational databases (like Amazon RDS) in private subnets, allowing access only from application servers running in designated private subnets.

---

## 4. Security Best Practices

### Hardening IAM Policies
Apply the principle of least privilege. Do not use permanent access keys for deployment pipelines. Instead, use IAM roles and OpenID Connect (OIDC) federation.

### Restricting S3 Public Access
Block public access at the S3 bucket level and use Bucket Policies to restrict access to specific IAM roles or VPC Endpoints:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPrivateEndpointAccessOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-secure-bucket",
        "arn:aws:s3:::my-secure-bucket/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:sourceVpce": "vpce-123456"
        }
      }
    }
  ]
}
```

---

## 5. Scalability Patterns

### ALB + Auto Scaling Groups (ASG)
Configure Auto Scaling Groups to scale EC2 instances dynamically based on CPU utilization or request count metrics.
*   **ALB**: Load-balances incoming HTTP/HTTPS traffic across instances in the ASG.
*   **Target Groups**: Keep track of healthy instances within the ASG.

### Amazon EKS Node Scaling
Use **Karpenter** to provision right-sized nodes in seconds based on pending pod requirements, optimizing compute resources and cost.

---

## 6. Reliability Patterns

### Multi-AZ Database Deployments
Use RDS Multi-AZ configurations to replicate data synchronously to a standby instance in a different AZ. If the primary database fails, RDS executes automatic DNS failover to the standby instance, minimizing database downtime.

### Route53 DNS Failover
Configure Route53 health checks to route user traffic away from unhealthy endpoints to backup servers or static S3 hosting buckets.

---

## 7. Cost Optimization

### S3 Lifecycle Rules
Reduce storage costs by configuring lifecycle rules to transition old objects (like backup logs or training datasets) to cold storage classes (like Glacier) after a set period.

### Using AWS Spot Instances
Use Spot Instances for non-critical, fault-tolerant workloads (like development environments or batch processing jobs) to save up to 90% compared to On-Demand pricing.

---

## 8. Hands-On Labs

### Lab 8.1: Creating a Custom VPC via AWS CLI
```bash
# 1. Create the VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
echo "Created VPC: $VPC_ID"

# 2. Enable DNS hostnames
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames '{"Value":true}'

# 3. Create a public subnet
PUBLIC_SUBNET_ID=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
echo "Created Public Subnet: $PUBLIC_SUBNET_ID"

# 4. Create an Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --vpc-id "$VPC_ID" --internet-gateway-id "$IGW_ID"
echo "Attached IGW: $IGW_ID"

# 5. Create a Route Table for the public subnet
ROUTE_TABLE_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id "$ROUTE_TABLE_ID" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID"
aws ec2 associate-route-table --subnet-id "$PUBLIC_SUBNET_ID" --route-table-id "$ROUTE_TABLE_ID"
```

### Lab 8.2: Deploying an EC2 Instance with SSM access
```bash
# 1. Create an IAM Instance Profile with AmazonSSMManagedInstanceCore permissions
# 2. Deploy EC2 instance in the subnet
aws ec2 run-instances \
  --image-id ami-0c7217cdde317cfec \
  --instance-type t3.micro \
  --subnet-id "$PUBLIC_SUBNET_ID" \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ssm-server}]'
```

### Lab 8.3: IAM Credentials Configuration
```bash
# 1. Create a user group for read-only access to S3
aws iam create-group --group-name S3ReadOnlyGroup

# 2. Attach AWS managed ReadOnly policy
aws iam attach-group-policy --group-name S3ReadOnlyGroup --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

### Lab 8.4: Provisioning an EKS Cluster
Deploy an EKS cluster using `eksctl`.
```bash
# Create cluster config yaml
cat << 'EOF' > eks-config.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: prod-eks-cluster
  region: us-east-1
  version: "1.29"

managedNodeGroups:
  - name: general-nodes
    instanceType: t3.medium
    desiredCapacity: 2
    maxSize: 5
    minSize: 1
EOF

# Deploy cluster (this will take 15-20 minutes)
eksctl create cluster -f eks-config.yaml
```

### Lab 8.5: Configuring CloudWatch Alarms
```bash
# Create a CloudWatch CPU alarm for an EC2 instance
aws cloudwatch put-metric-alarm \
  --alarm-name "High-CPU-Utilization" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --evaluation-periods 2
```

### Lab 8.6: Security Group Configuration
```bash
# 1. Create security group
SG_ID=$(aws ec2 create-security-group --group-name web-sg --description "Allow HTTP" --vpc-id "$VPC_ID" --query 'GroupId' --output text)

# 2. Authorize ingress rules (allow HTTP from anywhere)
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80 --cidr 0.0.0.0/0
```

### Lab 8.7: Hardening S3 Buckets
```bash
# Create bucket and block public access configurations
aws s3api create-bucket --bucket my-hardened-enterprise-bucket --region us-east-1
aws s3api put-public-access-block \
  --bucket my-hardened-enterprise-bucket \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Private Instance Outbound Connectivity Failure
*   **Symptom**: An EC2 instance deployed in a private subnet cannot run `apt-get update` or reach the public internet.
*   **Root Cause**: The route table associated with the private subnet is missing a route to a NAT Gateway, or the NAT Gateway itself is failing or misconfigured.
*   **Resolution Strategy**:
    *   Inspect the route table of the private subnet:
        ```bash
        aws ec2 describe-route-tables --route-table-ids rtb-123456
        ```
    *   Verify there is a route: `0.0.0.0/0` -> `nat-123456`.
    *   Verify the NAT Gateway is deployed in a **public subnet** that has a route to the Internet Gateway (`igw-123456`).

### Task 9.2: IAM Access Denied Error
*   **Symptom**: An application running on EC2 throws `An error occurred (AccessDenied) when calling the ListObjectsV2 operation`.
*   **Root Cause**: The IAM role assigned to the instance profile is missing permissions, or the S3 bucket policy is explicitly denying access.
*   **Resolution Strategy**:
    *   Verify the IAM policy attached to the instance role:
        ```bash
        aws iam list-attached-role-policies --role-name my-instance-role
        ```
    *   Check for explicit denies in the target S3 bucket policy:
        ```bash
        aws s3api get-bucket-policy --bucket my-target-bucket
        ```

### Task 9.3: EKS Nodes Fail to Join Cluster
*   **Symptom**: EKS cluster runs, but `kubectl get nodes` returns no worker nodes.
*   **Root Cause**: Worker nodes cannot communicate with the EKS control plane due to missing security group rules, routing issues, or missing tags on subnets.
*   **Resolution Strategy**:
    *   Verify worker node security groups allow traffic to/from the control plane.
    *   Ensure subnets are tagged: `kubernetes.io/cluster/<cluster-name> = shared`.
    *   Inspect `kubelet` log on the worker node to diagnose startup issues:
        ```bash
        journalctl -u kubelet -n 100
        ```

---

## 10. Real Production Incidents

### Case Study: Exposing Access Keys in Git
*   **Incident**: A developer committed a testing script containing AWS access keys (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) to a public GitHub repository. Within minutes, automated scanners detected the keys and used them to spin up hundreds of high-compute GPU instances for cryptocurrency mining, resulting in a large bill before security teams detected the anomaly.
*   **Remediation**:
    *   Revoked the compromised credentials.
    *   Replaced permanent credentials with temporary IAM roles and OpenID Connect (OIDC) federation for CI/CD pipelines.
    *   Deployed automated secret scanning to block commits containing sensitive strings.

---

## 11. Interview Questions

### Q1: What is the difference between Security Groups and Network ACLs (NACLs)?
*   **Answer**:
    *   **Security Groups**: Act as a firewall for EC2 instances. They are **stateful** (if you allow inbound traffic on port 80, the return outbound traffic is automatically allowed). Rules evaluate only allows (no denies).
    *   **Network ACLs**: Act as a firewall for subnets. They are **stateless** (you must configure both inbound and outbound rules explicitly). Rules are evaluated in numerical order, supporting both allow and deny rules.

### Q2: What is the difference between a VPC Peering Connection and an AWS Transit Gateway?
*   **Answer**:
    *   **VPC Peering**: Connects two VPCs directly. It does not support transitive routing (if VPC A peers with B, and B peers with C, A cannot talk to C). Peering becomes complex to manage at scale.
    *   **Transit Gateway**: A hub-and-spoke router that connects multiple VPCs, VPN connections, and AWS accounts, simplifying network architecture and routing at scale.

### Q3: Explain what a VPC Endpoint is and name the two types.
*   **Answer**: A VPC Endpoint allows private subnets to connect to AWS services (like S3 or DynamoDB) using AWS internal networks, bypassing the public internet.
    *   **Gateway Endpoints**: Used for S3 and DynamoDB. They modify route tables to direct traffic to the service and are free.
    *   **Interface Endpoints (PrivateLink)**: Provision elastic network interfaces (ENIs) with private IP addresses in target subnets. They support DNS routing and are charged hourly.

### Q4: How does EKS manage pod identity authentication internally?
*   **Answer**: EKS uses OpenID Connect (OIDC) federation. You associate an IAM role with a Kubernetes ServiceAccount (IRSA). When a pod runs, EKS injects a temporary OIDC token into the pod. The AWS SDK reads this token and exchanges it with AWS STS for temporary IAM credentials, avoiding the need to store static AWS keys in Kubernetes secrets.

### Q5: What is the difference between On-Demand, Spot, and Reserved EC2 instances?
*   **Answer**:
    *   **On-Demand**: Pay for compute capacity by the second. No long-term commitments.
    *   **Spot Instances**: Bid on spare AWS compute capacity. Save up to 90% but AWS can terminate instances with a 2-minute warning if they need the capacity back.
    *   **Reserved Instances/Savings Plans**: Commit to a specific amount of compute usage (1 or 3 years) in exchange for a significant discount.

---

## 12. Enterprise Case Studies

### High-Volume Architecture scaling at Airbnb
Airbnb manages its infrastructure on AWS. They migrated their services from EC2 classic to a unified VPC layout. By utilizing ALBs and Auto Scaling Groups, they scale compute capacity dynamically to handle traffic fluctuations. They use Amazon EMR and S3 to process large datasets, using Spot Instances to reduce data processing costs.

---

## 13. System Design Discussions

### Secure Multi-Account Network Architecture
*   **Objective**: Design a multi-account cloud network for an enterprise.
*   **Architecture Considerations**:
    *   **Account Isolation**: Use AWS Organizations to split workloads into separate accounts (e.g., Development, Production, Security).
    *   **Centralized Routing**: Connect all VPCs to a central Transit Gateway in a Network Account. Route outbound internet traffic through a centralized inspection VPC containing NAT Gateways and firewalls.
    *   **Access Control**: Integrate IAM with okta using Single Sign-On (SSO).

---

## 14. AI Platform Perspective

### Provisioning Multi-GPU Infrastructure for LLM Training
Running deep learning models requires provisioning GPU-enabled EC2 instances (such as P4de or G5 instances) and configuring storage buffers.

```hcl
# Terraform definition for ML compute node
resource "aws_instance" "gpu_worker" {
  ami           = "ami-0c7217cdde317cfec" # Deep Learning AMI
  instance_type = "p4d.24xlarge" # 8x NVIDIA A100 GPUs
  subnet_id     = aws_subnet.private.id

  # Mount high-throughput NVMe instance storage
  ephemeral_block_device {
    device_name  = "/dev/sdb"
    virtual_name = "ephemeral0"
  }

  tags = {
    Workload = "llm-training"
  }
}
```
This integrates infrastructure provisioning directly into the development lifecycle, allowing MLOps teams to deploy GPU instances alongside AWS EKS nodes and ECR registries.
