# Module 11: Enterprise Cloud Infrastructure on Azure

## 1. Architecture Deep Dive

Microsoft Azure organizes resources into a hierarchical structure: **Management Groups**, **Subscriptions**, **Resource Groups**, and **Resources**.

```
+---------------------------------------------------------------------------------------------------+
|                                           Azure Resource Hierarchy                                |
|   +-------------------------------------------------------------------------------------------+   |
|   |   Management Group                                                                        |   |
|   |   - Governs compliance and policies across multiple subscriptions                        |   |
|   |   +-----------------------------------------------------------------------------------+   |   |
|   |   |   Subscription (e.g., Enterprise Billing Account)                                 |   |   |
|   |   |   - Logic billing and access boundary                                             |   |   |
|   |   |   +---------------------------------------------------------------------------+   |   |   |
|   |   |   |   Resource Group (e.g., prod-rg)                                          |   |   |   |
|   |   |   |   - Lifecycle container grouping related resources                        |   |   |   |
|   |   |   |   +------------------------+  +------------------------+                  |   |   |   |
|   |   |   |   |   AKS Cluster          |  |   Azure SQL Database   |                  |   |   |   |
|   |   |   |   +------------------------+  +------------------------+                  |   |   |   |
|   |   |   +---------------------------------------------------------------------------+   |   |   |
|   |   +-----------------------------------------------------------------------------------+   |   |
|   +-------------------------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------------------------+
```

### Microsoft Entra ID (formerly Azure Active Directory)
Entra ID manages identity and access control within Azure.
*   **Users/Service Principals**: Identities representing human users or automated applications.
*   **Managed Identities**: Automatic identity assignments for Azure resources, removing the need to store credentials in code.
*   **Role-Based Access Control (RBAC)**: Assigns permissions to identities at specific scopes (e.g., Subscription, Resource Group).

### Virtual Network (VNet) Architecture
*   **Subnets**: Private IP ranges within a VNet.
*   **Network Security Groups (NSGs)**: Stateful packet filters applied to subnets or network interfaces.
*   **Azure NAT Gateway**: Provides outbound internet access for private subnets.
*   **Private Endpoints**: Map private IP addresses from a VNet to Azure services (like Key Vault or Blob Storage), keeping traffic off the public internet.

---

## 2. Internal Working

### Entra ID Authentication Flow
1.  A resource (such as a VM) requests an access token from the local Azure Instance Metadata Service (IMDS) endpoint (`http://169.254.169.254/metadata/identity/oauth2/token`).
2.  Azure IMDS forwards the request to Entra ID.
3.  Entra ID validates the resource identity and returns an OAuth 2.0 access token.
4.  The resource presents this token to Azure services to authenticate requests.

### Azure Kubernetes Service (AKS) CNI Networking
AKS supports two primary networking plugins:
*   **Kubenet**: Pods receive IP addresses from a separate virtual network range. Traffic routing between nodes requires NAT translations, which can introduce latency at scale.
*   **Azure CNI**: Pods receive physical IP addresses directly from the VNet subnet range. This allows pods to communicate with other VNet resources with minimal latency, but requires pre-allocating large IP ranges.

---

## 3. Production Use Cases

### High-Availability Web Clusters
Deploying web APIs across multiple availability zones using **Azure Virtual Machine Scale Sets (VMSS)** behind an **Azure Application Gateway** to ensure high availability and load-balancing.

### Secure Key & Secret Management
Storing database connection strings and cryptographic keys in **Azure Key Vault**, allowing application servers to retrieve them securely at runtime using Managed Identities.

---

## 4. Security Best Practices

### Implementing Conditional Access Policies
Enforce Multi-Factor Authentication (MFA) and restrict access to the Azure Portal based on user location or device compliance.

### Hardening Network Security Groups (NSGs)
Apply the principle of least privilege. Block all inbound traffic by default, and allow access only from designated IP addresses or subnets.
```json
// NSG inbound rule allowing SSH access only from a specific admin subnet
{
  "name": "AllowAdminSSH",
  "properties": {
    "protocol": "Tcp",
    "sourcePortRange": "*",
    "destinationPortRange": "22",
    "sourceAddressPrefix": "10.0.1.0/24",
    "destinationAddressPrefix": "*",
    "access": "Allow",
    "priority": 100,
    "direction": "Inbound"
  }
}
```

---

## 5. Scalability Patterns

### Application Gateway + VMSS
Configure Virtual Machine Scale Sets to scale instance counts dynamically based on CPU utilization or request count metrics, using Application Gateway to distribute traffic.

### AKS Pod Autoscaling
Use **KEDA (Kubernetes Event-driven Autoscaling)** to scale pod replicas based on external event sources (such as Azure Service Bus queues or Kafka topics).

---

## 6. Reliability Patterns

### Azure SQL Geo-Replication
Configure Azure SQL databases to replicate data asynchronously to secondary databases in different regions, enabling failover with minimal data loss if a regional outage occurs.

### Azure Backup and Site Recovery
Automate daily backups of virtual machines and storage accounts, and configure Azure Site Recovery to orchestrate disaster recovery workflows across regions.

---

## 7. Cost Optimization

### Azure Reservations & Spot VMs
*   Use **Azure Reservations** (committing to 1- or 3-year plans) to save up to 72% on virtual machines and SQL databases.
*   Use **Spot VMs** for fault-tolerant, non-critical workloads to run compute instances at a significant discount.

---

## 8. Hands-On Labs

### Lab 8.1: Creating a Custom VNet via Azure CLI
```bash
# 1. Create a Resource Group
az group create --name prod-rg --location eastus

# 2. Create the VNet and a public subnet
az network vnet create \
  --name prod-vnet \
  --resource-group prod-rg \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name public-subnet \
  --subnet-prefixes 10.0.1.0/24

# 3. Create a private subnet
az network vnet subnet create \
  --vnet-name prod-vnet \
  --resource-group prod-rg \
  --name private-subnet \
  --address-prefixes 10.0.2.0/24
```

### Lab 8.2: Deploying a VM with Azure Bastion Access
```bash
# 1. Create the Bastion subnet (must be named AzureBastionSubnet)
az network vnet subnet create \
  --vnet-name prod-vnet \
  --resource-group prod-rg \
  --name AzureBastionSubnet \
  --address-prefixes 10.0.3.0/27

# 2. Create public IP for Bastion host
az network public-ip create \
  --resource-group prod-rg \
  --name bastion-ip \
  --sku Standard

# 3. Provision the Bastion Host
az network bastion create \
  --name prod-bastion \
  --resource-group prod-rg \
  --vnet-name prod-vnet \
  --public-ip-address bastion-ip

# 4. Create a virtual machine in the private subnet
az vm create \
  --resource-group prod-rg \
  --name private-vm \
  --vnet-name prod-vnet \
  --subnet private-subnet \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys
```

### Lab 8.3: Role Assignment Configuration
```bash
# Assign the Reader role to a Service Principal at the Resource Group scope
az role assignment create \
  --assignee "http://my-service-principal" \
  --role "Reader" \
  --resource-group prod-rg
```

### Lab 8.4: Provisioning an AKS Cluster with Azure CNI
```bash
# Provision AKS cluster with Azure CNI networking
az aks create \
  --resource-group prod-rg \
  --name prod-aks-cluster \
  --node-count 3 \
  --network-plugin azure \
  --generate-ssh-keys
```

### Lab 8.5: Configuring Azure Monitor alerts
```bash
# Create an alert rule when VM CPU utilization exceeds 85%
az monitor metrics alert create \
  --name "VM-High-CPU" \
  --resource-group prod-rg \
  --scopes "/subscriptions/1234-5678/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/private-vm" \
  --condition "avg CPU Percentage > 85" \
  --description "Alert when CPU is high"
```

### Lab 8.6: Private Endpoint Setup
```bash
# 1. Create a storage account
az storage account create \
  --name prodstorageacct99 \
  --resource-group prod-rg \
  --location eastus \
  --sku Standard_LRS

# 2. Disable public access to the storage account
az storage account update \
  --name prodstorageacct99 \
  --resource-group prod-rg \
  --default-action Deny

# 3. Create a private endpoint link
az network private-endpoint create \
  --name storage-pe \
  --resource-group prod-rg \
  --vnet-name prod-vnet \
  --subnet private-subnet \
  --private-connection-resource-id "/subscriptions/1234-5678/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstorageacct99" \
  --group-id blob \
  --connection-name storage-connection
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Private Subnet Connection Outbound Failure
*   **Symptom**: A virtual machine in a private subnet cannot connect to the internet or run updates.
*   **Root Cause**: The subnet lacks a route to outbound internet access, or Network Security Group (NSG) rules block outbound traffic on ports 80/443.
*   **Resolution Strategy**:
    *   Verify the subnet is associated with an **Azure NAT Gateway**:
        ```bash
        az network vnet subnet show --resource-group prod-rg --vnet-name prod-vnet --name private-subnet
        ```
    *   Verify the NSG associated with the subnet allows outbound traffic to the internet:
        ```bash
        az network nsg rule list --resource-group prod-rg --nsg-name private-subnet-nsg
        ```

### Task 9.2: Access Denied to Azure Key Vault
*   **Symptom**: An application running on an Azure VM throws `Forbidden: Access denied to Key Vault`.
*   **Root Cause**: The VM lacks a System-Assigned Managed Identity, or the Key Vault access policies/RBAC permissions do not grant the VM permission to retrieve secrets.
*   **Resolution Strategy**:
    *   Enable Managed Identity on the VM:
        ```bash
        az vm identity assign --name private-vm --resource-group prod-rg
        ```
    *   Grant the VM Key Vault Secrets User permissions:
        ```bash
        az keyvault set-policy --name prod-vault --object-id <vm-identity-principal-id> --secret-permissions get list
        ```

### Task 9.3: AKS Subnet IP Exhaustion
*   **Symptom**: Pods fail to schedule in AKS, displaying `NetworkPlugin cni failed to set up pod ... Network namespace setup failed`.
*   **Root Cause**: Using Azure CNI, every pod receives a real IP address from the subnet. If the subnet's IP range is too small, the cluster runs out of IPs, blocking pod scheduling.
*   **Resolution Strategy**:
    *   Check available IP addresses in the subnet:
        ```bash
        az network vnet subnet show --resource-group prod-rg --vnet-name prod-vnet --name private-subnet
        ```
    *   Mitigate by migrating to a larger subnet, or configuring **Azure CNI with Dynamic IP Allocation** to allocate IPs for pods from a separate VNet.

---

## 10. Real Production Incidents

### Case Study: Traffic Manager Cache Routing Issues
*   **Incident**: During a regional database upgrade, operations teams configured Azure Traffic Manager to route traffic away from the primary region to a backup server. However, users continued to experience errors because their local DNS servers cached the primary region's IP address, bypassing the Traffic Manager configuration changes.
*   **Remediation**:
    *   Reduced the Traffic Manager DNS Time-to-Live (TTL) setting from 300 seconds to 30 seconds.
    *   Migrated regional routing configurations to **Azure Front Door**, which uses Anycast DNS routing and instant backend health probes to failover traffic immediately without relying on client-side DNS caching.

---

## 11. Interview Questions

### Q1: What is the difference between Azure RBAC and Key Vault Access Policies?
*   **Answer**:
    *   **Azure RBAC**: Managed at the subscription or resource group scope. It grants permissions to manage Azure resources (like creating virtual machines or databases).
    *   **Key Vault Access Policies**: Managed at the Key Vault resource level. They grant permissions to read, write, or delete secrets, keys, and certificates stored *inside* the Key Vault. Modern vaults support migrating fully to Azure RBAC roles.

### Q2: Explain the difference between Azure CNI and Kubenet networking in AKS.
*   **Answer**:
    *   **Azure CNI**: Every pod receives a real IP address from the host VNet subnet. This enables direct, low-latency communication with other VNet resources, but requires a large allocation of IP addresses.
    *   **Kubenet**: Pods receive IP addresses from a separate virtual network range. Traffic routing between nodes requires NAT translations, which can introduce latency but requires fewer VNet IP allocations.

### Q3: What is a Resource Lock in Azure, and what are the two types?
*   **Answer**: A Resource Lock prevents accidental deletion or modification of critical Azure resources.
    *   **CanNotDelete**: Users can read and modify the resource, but cannot delete it.
    *   **ReadOnly**: Users can read the resource, but cannot delete or modify it.

### Q4: How do System-Assigned and User-Assigned Managed Identities differ?
*   **Answer**:
    *   **System-Assigned**: Created as part of a specific Azure resource (such as a VM). Its lifecycle is tied to the resource; if you delete the VM, the identity is automatically deleted.
    *   **User-Assigned**: Created as a standalone Azure resource. It can be shared across multiple resources (e.g., assigning the same identity to multiple VMs in a scale set) and has an independent lifecycle.

### Q5: What is VNet Peering transit, and how does it work?
*   **Answer**: VNet Peering connects two virtual networks. VNet Peering transit allows a spoke VNet to route traffic to the internet or on-premises networks through a gateway (VPN or ExpressRoute) deployed in a hub VNet, simplifying network routing configurations.

---

## 12. Enterprise Case Studies

### Cloud Migration at Maersk
Maersk migrated its core logistics application pipelines to Microsoft Azure. They standardized their deployments on AKS clusters, using Azure DevOps to automate CI/CD pipelines. By storing credentials in Azure Key Vault and using Managed Identities, they improved security and met enterprise compliance requirements.

---

## 13. System Design Discussions

### Secure Enterprise Hub-and-Spoke VNet Design
*   **Objective**: Design a secure network architecture for an enterprise.
*   **Architecture Considerations**:
    *   **Hub VNet**: Deploy central network services (such as Azure Firewall, VPN Gateway, and DNS) in a central Hub VNet.
    *   **Spoke VNets**: Connect spoke VNets (hosting workloads like Development or Production) to the Hub VNet using VNet Peering.
    *   **Traffic Routing**: Configure Route Tables in the spoke VNets to route all outbound internet traffic through the Azure Firewall in the Hub VNet for security inspection.

---

## 14. AI Platform Perspective

### Provisioning Azure GPU Clusters for Machine Learning
Running deep learning models requires provisioning GPU-enabled virtual machines (such as NC or ND series VMs) and configuring container registries.

```hcl
# Terraform definition for Azure GPU VM
resource "azurerm_linux_virtual_machine" "gpu_node" {
  name                = "gpu-ml-node"
  resource_group_name = "prod-rg"
  location            = "eastus"
  size                = "Standard_NC6s_v3" # NVIDIA Tesla V100 GPU
  admin_username      = "azureuser"

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "microsoft-dsvm"
    offer     = "ubuntu-hpc"
    sku       = "2204"
    version   = "latest"
  }
}
```
This integrates infrastructure provisioning directly into the development lifecycle, allowing MLOps teams to deploy GPU instances alongside AKS node groups and Azure Container Registry (ACR) repositories.
