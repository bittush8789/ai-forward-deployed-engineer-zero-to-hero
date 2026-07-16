# Practice Tasks: Module 11 - Azure Infrastructure

This document outlines step-by-step tasks to practice Azure networking, virtual machine provisioning, and IAM role assignment using the Azure CLI.

---

## Task 1: Building a Custom VNet
*   **Goal**: Create an Azure Virtual Network with public and private subnets, and configure Network Security Group rules.
*   **Step-by-Step Instructions**:
    1. Create a Resource Group:
       ```bash
       az group create --name lab-rg --location eastus
       ```
    2. Create a Virtual Network (VNet) with a default public subnet:
       ```bash
       az network vnet create \
         --name lab-vnet \
         --resource-group lab-rg \
         --address-prefixes 192.168.0.0/16 \
         --subnet-name public-subnet \
         --subnet-prefixes 192.168.1.0/24
       ```
    3. Create a private subnet:
       ```bash
       az network vnet subnet create \
         --vnet-name lab-vnet \
         --resource-group lab-rg \
         --name private-subnet \
         --address-prefixes 192.168.2.0/24
       ```
    4. Create a Network Security Group (NSG):
       ```bash
       az network nsg create \
         --name lab-nsg \
         --resource-group lab-rg
       ```
    5. Add a rule to allow inbound SSH (port 22) only from a specific IP range:
       ```bash
       az network nsg rule create \
         --resource-group lab-rg \
         --nsg-name lab-nsg \
         --name AllowAdminSSH \
         --priority 100 \
         --destination-port-ranges 22 \
         --access Allow \
         --protocol Tcp
       ```
*   **Verification**:
    Verify the NSG rules configuration:
    ```bash
    az network nsg rule list --resource-group lab-rg --nsg-name lab-nsg
    ```

---

## Task 2: VM Provisioning with SSH Key Auth
*   **Goal**: Deploy a Linux virtual machine inside a subnet using SSH key authentication.
*   **Step-by-Step Instructions**:
    1. Provision the virtual machine:
       ```bash
       az vm create \
         --resource-group lab-rg \
         --name lab-vm \
         --vnet-name lab-vnet \
         --subnet public-subnet \
         --image Ubuntu2204 \
         --admin-username azureuser \
         --generate-ssh-keys
       ```
    2. Retrieve the public IP of the VM:
       ```bash
       az vm list-ip-addresses --resource-group lab-rg --name lab-vm
       ```
*   **Verification**:
    Verify the VM status is running:
    ```bash
    az vm get-instance-view --name lab-vm --resource-group lab-rg --query "instanceView.statuses[1].displayStatus"
    ```
    Clean up resources:
    ```bash
    az group delete --name lab-rg --y --no-wait
    ```
