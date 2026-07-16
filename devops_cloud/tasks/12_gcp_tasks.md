# Practice Tasks: Module 12 - GCP Infrastructure

This document outlines step-by-step tasks to practice Google Cloud VPC configuration, instance provisioning, and IAM policy bindings using the gcloud CLI.

---

## Task 1: Building a Custom Mode VPC Network
*   **Goal**: Create a Custom mode VPC network with regional subnets and Cloud NAT.
*   **Step-by-Step Instructions**:
    1. Create a custom VPC network:
       ```bash
       gcloud compute networks create lab-vpc --subnet-mode=custom
       ```
    2. Create a subnet inside the VPC:
       ```bash
       gcloud compute networks subnets create lab-subnet \
         --network=lab-vpc \
         --region=us-central1 \
         --range=10.10.1.0/24
       ```
    3. Create a Cloud Router:
       ```bash
       gcloud compute routers create lab-router \
         --network=lab-vpc \
         --region=us-central1
       ```
    4. Create a Cloud NAT configuration on the router to enable outbound internet access:
       ```bash
       gcloud compute routers nats create lab-nat \
         --router=lab-router \
         --region=us-central1 \
         --auto-allocate-nat-external-ips \
         --nat-custom-subnet-ip-ranges=lab-subnet
       ```
*   **Verification**:
    Verify the NAT gateway status:
    ```bash
    gcloud compute routers nats describe lab-nat --router=lab-router --region=us-central1
    ```

---

## Task 2: Compute Engine VM Deployment
*   **Goal**: Deploy a Compute Engine virtual machine inside a private subnet.
*   **Step-by-Step Instructions**:
    1. Provision the virtual machine:
       ```bash
       gcloud compute instances create lab-vm \
         --zone=us-central1-a \
         --subnet=lab-subnet \
         --no-address \
         --image-family=ubuntu-2204-lts \
         --image-project=ubuntu-os-cloud
       ```
    2. Create a firewall rule to allow internal VPC traffic:
       ```bash
       gcloud compute firewall-rules create allow-internal-traffic \
         --network=lab-vpc \
         --allow=tcp,udp,icmp \
         --source-ranges=10.10.1.0/24
       ```
*   **Verification**:
    Verify the instance details:
    ```bash
    gcloud compute instances describe lab-vm --zone=us-central1-a
    ```
    Clean up resources:
    ```bash
    gcloud compute instances delete lab-vm --zone=us-central1-a --quiet
    gcloud compute networks subnets delete lab-subnet --region=us-central1 --quiet
    gcloud compute networks delete lab-vpc --quiet
    ```
