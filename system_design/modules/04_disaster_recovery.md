# Module 4: Disaster Recovery, RTO/RPO Metrics & Multi-Region Strategies

## 1. Theory (60%)

### What is Disaster Recovery?
Disaster Recovery (DR) is the set of policies, tools, and procedures configured to restore system operations and access to applications following a catastrophic event (such as a facility outage, natural disaster, or cyberattack).

```
+-------------------------------------------------------------------------------------------------+
|                                     Disaster Recovery Metrics                                   |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |   Disaster Event Occurs                                                                 |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|   <-------------------+ (Data Loss window)                              +---------------------> |
|                       |                                                 | (System offline)      |
|              Recovery Point Objective                          Recovery Time Objective          |
|                       (RPO)                                             (RTO)                   |
+-------------------------------------------------------------------------------------------------+
```

### Critical DR Metrics
*   **Recovery Point Objective (RPO)**: The maximum allowable data loss window, measured in time (e.g., losing at most 5 minutes of transaction data). This determines backup and replication frequencies.
*   **Recovery Time Objective (RTO)**: The target duration to restore system operations after an outage (e.g., recovering system access within 30 minutes).

### Disaster Recovery Strategies
*   **Backup & Restore**: Daily or hourly backups are written to object storage. Slowest recovery time (high RTO) but lowest cost.
*   **Pilot Light**: Core data is replicated to a secondary region, while compute resources remain inactive. During a disaster, the standby region is scaled up to handle traffic.
*   **Warm Standby**: A scaled-down version of the system runs concurrently in a secondary region. During a disaster, traffic is redirected and resources are scaled up.
*   **Multi-Site (Active-Active)**: Complete system deployments run in parallel across multiple regions, sharing load. Near-zero recovery time (low RTO) but high infrastructure cost.

---

## 2. Practical (40%)

### Build: Developing a Multi-Region DR Platform
We will design a disaster recovery strategy using Velero and object storage:
1.  **Kubernetes Resource Backups**: Using **Velero** to backup cluster states, namespaces, and volumes to an external bucket.
2.  **Cross-Region Replication**: Configuring asynchronous bucket replication to copy backup files to an isolated standby region.
3.  **PostgreSQL Backup Schedules**: Running scheduled database dumps stored in encrypted object storage.

```
+-------------------------------------------------------------------------------------------------+
|                                        DR Architecture                                          |
|                                                                                                 |
|   +--------------------------------------------+                                                |
|   |             Primary Region (US-East)       |                                                |
|   |   +------------------------------------+   |                                                |
|   |   |    Kubernetes Cluster (Velero)     |   |                                                |
|   |   +------------------+-----------------+   |                                                |
|   |                      |                     |                                                |
|   |                      v                     |                                                |
|   |   +------------------------------------+   |                                                |
|   |   |       S3 Storage (Backup Bucket)   |   |                                                |
|   |   +------------------+-----------------+   |                                                |
|   +----------------------|---------------------+                                                |
|                          |                                                                      |
|                          v (Asynchronous Cross-Region Replication)                              |
|   +----------------------|---------------------+                                                |
|   |                      v                     |                                                |
|   |   +------------------------------------+   |                                                |
|   |   |     Standby S3 (Replication Bucket) |   |                                                |
|   |   +------------------+-----------------+   |                                                |
|   |                      |                     |                                                |
|   |                      v                     |                                                |
|   |   +------------------------------------+   |                                                |
|   |   |        Standby Region (EU-West)    |   |                                                |
|   |   |   - Restores cluster via Velero    |   |                                                |
|   |   +------------------------------------+   |                                                |
|   +--------------------------------------------+                                                |
+-------------------------------------------------------------------------------------------------+
```

### Hands-On Task: Backup Verification Script
Write a script to automate database backups and simulate cross-region replication:
```bash
# /tmp/dr_backup.sh
#!/usr/bin/env bash
# Simulates database backup generation and replication

set -euo pipefail

BACKUP_DIR="/tmp/dr-backups"
REPLICATED_DIR="/tmp/dr-replicated"
mkdir -p "$BACKUP_DIR" "$REPLICATED_DIR"

echo "=== Starting Database Backup Process ==="

# 1. Simulate database dump
echo "Action: Generating database dump file..."
echo "id,data" > "$BACKUP_DIR/db_dump.sql"
echo "1,user_records" >> "$BACKUP_DIR/db_dump.sql"

# 2. Simulate replication copy to secondary region directory
echo "Action: Replicating backup file to standby region..."
cp "$BACKUP_DIR/db_dump.sql" "$REPLICATED_DIR/db_dump_replicated.sql"

# 3. Verify replication integrity
if [ -f "$REPLICATED_DIR/db_dump_replicated.sql" ]; then
    echo "Success: Database backup replicated to standby region (RPO verified)."
else
    echo "Error: Replication failed."
    exit 1
fi
exit 0
```
Run the backup script:
```bash
chmod +x /tmp/dr_backup.sh
/tmp/dr_backup.sh
```

### Case Study: Cloudflare's Route 53 Failover
During a major cloud provider network outage, Cloudflare redirected routing traffic to healthy standby regions using automated Route 53 DNS records. This design kept application gateways accessible, highlighting the importance of multi-region routing.
