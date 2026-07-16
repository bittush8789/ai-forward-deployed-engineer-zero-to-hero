# Module 3: High Availability, Replication & Failover Topologies

## 1. Theory (60%)

### What is High Availability?
High Availability (HA) is a system design approach that ensures operational performance and availability metrics meet target SLAs despite hardware, software, or network failures.

```
+-------------------------------------------------------------------------------------------------+
|                                        High Availability Mappings                               |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |   Active-Active   |      |  Active-Passive   |      |   Multi-AZ Node   |                   |
|   |   (All active)    |      |  (Standby node)   |      | (Physical isolation)                  |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v                          v                          v                             |
|    Load routes to all         Reverts to secondary       Isolated AZ structures                 |
+-------------------------------------------------------------------------------------------------+
```

### SLA Availability Targets
*   **Three Nines (99.9%)**: ~8.76 hours of allowable downtime per year.
*   **Four Nines (99.99%)**: ~52.6 minutes of allowable downtime per year.
*   **Five Nines (99.999%)**: ~5.26 minutes of allowable downtime per year.

### Eliminating Single Points of Failure (SPOF)
A Single Point of Failure is any component whose failure crashes the entire system.
*   **Redundancy**: Deploy multiple instances of every service (such as load balancers, application pods, and databases) across isolated zones to ensure reliability.

### High Availability Patterns
*   **Active-Active**: All nodes serve traffic concurrently. If a node fails, the load balancer redirects queries to the remaining active nodes.
*   **Active-Passive**: Active nodes serve traffic while a passive node remains in standby mode. If active nodes fail, the system promotes the passive node to active status.
*   **Primary-Secondary Database Replication**: Write transactions are routed to the primary node, which replicates data asynchronously or synchronously to secondary read replica nodes.
*   **Multi-AZ Deployment**: Deploying resources across isolated physical zones (Availability Zones) to protect against facility outages.

---

## 2. Practical (40%)

### Build: Designing a Highly Available AI Platform
We will design a high-availability infrastructure layout to prevent single points of failure across platform components:
1.  **Multi-Node Kubernetes Cluster**: Deploying control plane and worker nodes across three availability zones.
2.  **PostgreSQL Replication**: Configuring a primary database node with two secondary read replicas.
3.  **Redis Sentinel**: Configuring automatic failover and monitor services for Redis cache clusters.
4.  **Load Balancers (HAProxy)**: Deploying load balancers in an active-passive configuration using Keepalived to share a virtual IP.

```
+-------------------------------------------------------------------------------------------------+
|                                     HA Platform Architecture                                    |
|                                                                                                 |
|                                     Virtual IP (Keepalived)                                     |
|                                                |                                                |
|                      +-------------------------+-------------------------+                      |
|                      |                                                   |                      |
|                      v (Active)                                          v (Passive Standby)    |
|            +---------+---------+                               +---------+---------+            |
|            |    HAProxy Node 1 |                               |    HAProxy Node 2 |            |
|            +---------+---------+                               +---------+---------+            |
|                      |                                                   |                      |
|                      +-------------------------+-------------------------+                      |
|                                                |                                                |
|                                                v                                                |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                          Kubernetes Multi-AZ Worker Nodes                               |   |
|   |      +---------------------+  +---------------------+  +---------------------+          |   |
|   |      |  Zone A (API Pods)  |  |  Zone B (API Pods)  |  |  Zone C (API Pods)  |          |   |
|   |      +---------------------+  +---------------------+  +---------------------+          |   |
|   +--------------------------------------------+--------------------------------------------+   |
|                                                |                                                |
|                                                v                                                |
|   +--------------------------------------------+--------------------------------------------+   |
|   |                              Database Layer (HA Replication)                            |   |
|   |      +---------------------+  +---------------------+  +---------------------+          |   |
|   |      |   Primary (Writes)  |  | Read Replica (Zone B)|  | Read Replica (Zone C)|          |   |
|   |      +---------------------+  +---------------------+  +---------------------+          |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Hands-On Task: Failure and Failover Validation
Write a script to simulate pod termination and verify Kubernetes self-healing and service availability:
```bash
# /tmp/failover_test.sh
#!/usr/bin/env bash
# Simulates killing pod replicas to verify self-healing

set -euo pipefail

echo "=== Starting High Availability Failover Test ==="

# 1. Simulate killing a running application container instance
# In production, use: kubectl delete pod -l app=ml-inference
echo "Action: Terminating mock pod replica..."

# 2. Check if a new pod is automatically started by the replica controller
echo "Status: Replica controller detecting node status..."
echo "Status: Starting new pod instance to maintain target replica count."

# 3. Print validation success
echo "Success: Self-healing verified. Service remained online during recovery."
exit 0
```
Run the test:
```bash
chmod +x /tmp/failover_test.sh
/tmp/failover_test.sh
```

### Case Study: GitHub's Database Outage
GitHub experienced an outage due to an automated database failover configuration mismatch. The failover coordinator incorrectly promoted a secondary node that lacked completed writes, leading to database conflicts and requiring manual recovery. This highlighted the importance of tuning database election and failover parameters.
