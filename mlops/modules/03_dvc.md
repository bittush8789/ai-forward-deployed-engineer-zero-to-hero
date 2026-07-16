# Module 3: Data Version Control (DVC) & Dataset Reproducibility

## 1. Architecture Deep Dive

Data Version Control (DVC) is an open-source tool designed to version datasets, machine learning models, and data pipelines. It extends Git to handle large files that cannot be tracked in code repositories due to size constraints.

```
+-------------------------------------------------------------------------------------------------+
|                                           Git Repository                                        |
|    - Contains Code (.py, .ipynb)                                                                |
|    - Tracks lightweight DVC pointer files (.dvc, dvc.lock, dvc.yaml) containing metadata        |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (Maps to actual binaries using file hashes)
+-----------------------------------------------+-------------------------------------------------+
|                                           DVC Cache                                             |
|    - Located in .dvc/cache/ (Local Storage) or Shared Cache on high-performance SAN             |
|    - Stores data blocks named by their MD5 checksums (de-duplicated storage pool)              |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (DVC Push / Pull commands)
+-----------------------------------------------+-------------------------------------------------+
|                                        Remote Storage Backend                                   |
|               AWS S3 | Azure Blob Storage | Google Cloud Storage | Local MinIO                  |
+-------------------------------------------------------------------------------------------------+
```

### DVC File Pointers
Instead of committing a 10GB dataset to Git, DVC creates a small, human-readable pointer file (e.g., `dataset.csv.dvc`) containing metadata and the file's MD5 checksum. Git tracks this pointer file, while the actual dataset is stored in a remote storage bucket.

---

## 2. Internal Working

### Checksum Calculations & Cache Mappings
1.  **MD5 Evaluation**: When a developer runs `dvc add dataset.csv`, DVC calculates the MD5 hash of the file.
2.  **Move to Cache**: The file is copied or linked to the local cache directory (`.dvc/cache/`). The directory structure uses the first two characters of the MD5 hash as the folder name, and the remaining characters as the filename (e.g., `.dvc/cache/files/md5/3c/a2b73c4e5f6g7h8i9j`).
3.  **Generate Pointer**: DVC creates a `dataset.csv.dvc` pointer file linking to this hash.
4.  **Replace Original**: The original file in the workspace is replaced with a link (symlink, hard link, or reflink) to the cache file.

---

## 3. Production Use Cases

### Reproducible Data Pipelines
Defining data preprocessing and model training steps in a `dvc.yaml` pipeline file. This allows data science teams to reproduce training runs using `dvc repro`, which runs steps only if their dependencies (code or input data) have changed.

### Auditable Model Training
Commit the `.dvc` dataset pointer file alongside the training code commit in Git. This ensures that every model release is tracked to the exact version of the raw dataset used to train it.

---

## 4. Governance Considerations

### Data Lineage & Audit Audits
By tracking data modifications through Git commits, DVC provides a clear audit trail for dataset changes (such as modifications, additions, or deletions), which is critical for meeting data compliance regulations.

---

## 5. Security Best Practices

### Storage IAM Access Controls
*   Enforce read-only IAM access permissions on remote storage buckets for training instances.
*   Limit write permissions to designated data engineers and CI/CD pipelines to prevent unauthorized data modifications.

---

## 6. Scalability Patterns

### Optimization via Link Types
Copying multi-gigabyte datasets during DVC operations can slow down runs and exhaust disk space.
*   Configure DVC to use **hard links**, **symlinks**, or **reflinks** (supported on filesystems like Btrfs or XFS) to link files from the cache directory to the workspace without duplicating data.
*   Configure a shared cache directory on a local network drive to allow multiple developers to access cached files without downloading them.

---

## 7. Reliability Patterns

### Remote Storage Backups
Enable versioning and replication on remote storage buckets to prevent data loss. Use `dvc status -c` to verify that all tracked files are backed up to remote storage.

---

## 8. Cost Optimization

### Garbage Collection (`dvc gc`)
Clean up old, unused dataset versions from the local cache directory to free up disk space:
```bash
# Delete all cached files except those referenced in current Git commits
dvc gc -w -f
```

---

## 9. Hands-On Labs

### Lab 9.1: Setting up DVC with Local Storage on Ubuntu
Run these commands on your Ubuntu system to configure DVC and track a dummy dataset.
```bash
# 1. Install DVC using pip
pip install dvc

# 2. Initialize Git and DVC in a new directory
mkdir -p /tmp/dvc-lab && cd /tmp/tf-lab || cd /tmp/dvc-lab
git init
dvc init

# 3. Create a dummy dataset
echo "id,label,value" > dataset.csv
echo "1,positive,10.5" >> dataset.csv

# 4. Add the dataset to DVC tracking
dvc add dataset.csv

# 5. Commit changes to Git
git add dataset.csv.dvc .gitignore
git commit -m "Initialize dataset tracking"

# 6. Configure a local folder as remote storage
mkdir -p /tmp/dvc-remote
dvc remote add -d myremote /tmp/dvc-remote

# 7. Push the dataset to remote storage
dvc push
```

### Lab 9.2: Creating and Running a Pipeline (`dvc.yaml`)
Create a reproducible data processing pipeline step.
```bash
# 1. Create a dummy processing script
tee /tmp/dvc-lab/process.py << 'EOF'
import sys
print("Processing dataset...")
with open("dataset.csv", "r") as f_in:
    lines = f_in.readlines()
with open("clean_data.csv", "w") as f_out:
    f_out.writelines(lines[:2]) # Save header and first row
print("Processing complete.")
EOF

# 2. Define the pipeline step in dvc.yaml
dvc stage add -n preprocess \
  -d dataset.csv -d process.py \
  -o clean_data.csv \
  python3 process.py

# 3. Run the pipeline (this executes process.py and generates dvc.lock)
dvc repro
```
Verify pipeline status:
```bash
# Check pipeline state (it should report no changes)
dvc status
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Checksum Mismatch during `dvc pull`
*   **Symptom**: `dvc pull` fails with `Error: Corrupted cache file: ... Checksum mismatch`.
*   **Root Cause**: A file inside the local cache directory was modified manually, corrupting its hash.
*   **Resolution Strategy**:
    *   Find the corrupted hash file in the cache directory.
    *   Delete the corrupted file:
        ```bash
        rm -f .dvc/cache/files/md5/3c/a2b73c4e5f6g7h8i9j
        ```
    *   Re-pull the dataset from remote storage:
        ```bash
        dvc pull -f
        ```

### Task 10.2: Remote Push Fails due to Missing Credentials
*   **Symptom**: `dvc push` fails with `botocore.exceptions.NoCredentialsError: Unable to locate credentials`.
*   **Root Cause**: AWS CLI credentials are not configured or are missing from the environment variables.
*   **Resolution Strategy**:
    *   Verify AWS credentials are configured correctly:
        ```bash
        aws sts get-caller-identity
        ```
    *   Configure DVC to use specific credentials or AWS profile:
        ```bash
        dvc remote modify myremote profile my-aws-profile
        ```

---

## 11. Real Production Incidents

### Case Study: Git Bloat from Committed Datasets
*   **Incident**: A developer ran `git add dataset.csv` instead of `dvc add dataset.csv`, committing a 5GB dataset directly to Git. The Git repository size increased, slowing down clone and pull speeds across the team.
*   **Remediation**:
    *   Used `git-filter-repo` to remove the large dataset from Git history.
    *   Added the dataset path to the `.gitignore` file.
    *   Added the dataset to DVC tracking:
        ```bash
        dvc add dataset.csv
        git add dataset.csv.dvc
        ```

---

## 12. Interview Questions

### Q1: How does DVC track large files without committing them to Git?
*   **Answer**: DVC calculates the MD5 hash of the file and moves it to the local cache directory (`.dvc/cache/`). It then creates a small, human-readable pointer file (e.g., `dataset.csv.dvc`) containing the hash. Git tracks this pointer file, while the actual dataset is stored in a remote storage bucket.

### Q2: Explain the purpose of the `dvc.lock` file.
*   **Answer**: The `dvc.lock` file stores the exact inputs, outputs, and MD5 hashes of all stages executed in a pipeline. It is committed to Git to ensure that other team members pull the exact same versions of intermediate files during pipeline runs.

### Q3: What is the benefit of configuring DVC link types?
*   **Answer**: Link types (such as hard links, symlinks, or reflinks) allow referencing files from the cache directory to the workspace without duplicating data, saving disk space and reducing file I/O latency for large datasets.

### Q4: How does `dvc gc` optimize storage costs?
*   **Answer**: `dvc gc` deletes all cached files except those referenced in current Git commits, freeing up disk space in the local cache directory.

### Q5: What are the risks of using default local cache directories in multi-tenant environments?
*   **Answer**: Default local cache directories can exhaust disk space on the host machine. Mitigate by configuring a shared cache directory on a network drive and setting up user-level access controls.

---

## 13. Enterprise Case Studies

### Data Versioning at DHL Logistics
DHL Logistics teams use DVC to manage training datasets for delivery optimization models. By storing dataset versions in a centralized S3 bucket and tracking `.dvc` files in Git, they automated pipeline executions, ensuring models are trained on the correct dataset versions and reducing training errors.

---

## 14. AI FDE Perspective

### Managing Large Datasets in Air-Gapped Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Local Remote Configuration**: If cloud storage is blocked, deploy **MinIO** in the local network to serve as a private S3-compatible backend.
*   **Pre-caching**: Download required datasets in advance, copy them to a shared network drive, and configure DVC to use this drive as a shared cache:
    ```bash
    dvc config cache.shared group
    dvc config cache.dir /mnt/shared_dvc_cache
    ```
This allows development teams to access datasets without needing external network connections.
