# Module 2: Enterprise Shell Scripting & Automation

## 1. Architecture Deep Dive

The Bash (Bourne Again Shell) shell acts as both a command language interpreter and a scripting programming language. Understanding the shell execution sequence is critical for writing robust, error-free code.

```
+-------------------------------------------------------------------+
|                           Bash Script Input                       |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 1. Lexical Analysis (Splits input into tokens, identifies words)  |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 2. Expansion Phase                                                |
|    - Brace Expansion {a,b}                                        |
|    - Parameter/Variable Expansion $VAR                            |
|    - Command Substitution $(cmd)                                  |
|    - Arithmetic Expansion $((1+1))                                |
|    - Word Splitting (Uses IFS)                                    |
|    - Pathname/Glob Expansion *.log                                |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 3. Redirection Handling (Sets up stdin/stdout/stderr file desc.)   |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 4. Execution Phase                                                |
|    - Checks for built-ins (cd, echo, read)                        |
|    - Searches PATH for external binaries (grep, awk)              |
|    - Fork/Execs child processes for external binaries            |
+-------------------------------------------------------------------+
```

### Shebang Execution Mechanics
When a script starts with `#!/usr/bin/env bash`:
1.  The kernel execution handler reads the first line.
2.  It parses `/usr/bin/env` as the target interpreter and passes `bash` and the script's path as arguments.
3.  This approach is preferred over `#!/bin/bash` because it searches the user's current environment `PATH` to locate the shell binary, increasing portability across various Linux distributions (e.g., NixOS, BSD, Ubuntu).

### Subshells vs. Parent Environment
*   **Parent Shell**: Holds current variables, functions, and exported environment variables.
*   **Subshell `(commands)`**: A separate instance of the shell spawned via `fork()`. It inherits variables from the parent but cannot modify the parent's environment. Variables modified inside a subshell are lost when the subshell exits.
*   **Process Substitution `<(commands)` / `>(commands)`**: Spawns a subshell connected to a named pipe (FIFO) in `/dev/fd/`. This allows treating command output as a physical file descriptor.

---

## 2. Internal Working

### File Descriptors & Pipeline Execution
Every process has at least three default File Descriptors (FD):
*   `0`: Standard Input (`stdin`)
*   `1`: Standard Output (`stdout`)
*   `2`: Standard Error (`stderr`)

When executing a pipeline like `cat file.txt | grep "pattern" | wc -l`:
1.  The shell calls `pipe()` to create two file descriptor pairs.
2.  It calls `fork()` to spawn three child processes.
3.  Using `dup2()`, it maps the `stdout` (FD 1) of `cat` to the write end of pipe 1, the `stdin` (FD 0) of `grep` to the read end of pipe 1, and so on.
4.  All processes execute concurrently.

### Word Splitting & Internal Field Separator (IFS)
Bash uses the `IFS` variable to determine word boundaries during expansion. By default, `IFS=$' \t\n'` (space, tab, newline). Failing to control `IFS` when reading files line-by-line can lead to unexpected tokenization.

---

## 3. Production Use Cases

### High-Availability Automated Sync Scripts
Orchestrating model checkpoint replication from local NVMe cache disks to centralized cloud storage (like S3) using `rsync` wrapped in error-handling shell logic.

### Log Auditing & Aggregation
Processing hundreds of megabytes of daily application log output, scrubbing PII (Personally Identifiable Information), extracting performance metrics, and routing them to localized metrics servers.

---

## 4. Security Best Practices

### Avoiding Command Injection
Always double-quote variables in command executions to prevent word splitting and globbing attacks:
```bash
# VULNERABLE to command injection if input contains space or ";"
rm -rf $USER_INPUT

# SECURE
rm -rf "$USER_INPUT"
```

### Static Analysis with ShellCheck
Use `shellcheck` in CI/CD pipelines to catch bugs and syntax anomalies.
```bash
# Install and run ShellCheck
sudo apt-get install -y shellcheck
shellcheck my_script.sh
```

### Defensive Script Header
Always start production scripts with:
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```
*   `-e`: Exit immediately if any command exits with a non-zero status.
*   `-u`: Treat unset variables as an error.
*   `-o pipefail`: Return the exit status of the first command in the pipeline that failed, rather than the final command.

---

## 5. Scalability Patterns

### Concurrent Execution using xargs -P
For bulk actions (like downloading a list of 100 model files), processing them sequentially is inefficient. Run them in parallel instead:
```bash
# Download 8 files concurrently using xargs
cat download_urls.txt | xargs -P 8 -n 1 curl -O -s
```

### Using Subshell Backgrounding & wait
```bash
# Run multiple background checks and wait for all to complete
check_gpu_temp &
check_disk_space &
check_network_latency &

wait # Blocks execution until all background jobs exit
echo "All sanity checks complete."
```

---

## 6. Reliability Patterns

### Using flock for Mutual Exclusion
Prevent multiple instances of the same cron script from running simultaneously and causing race conditions:
```bash
# Acquire an exclusive lock on fd 200 (bound to /var/lock/backup.lock)
exec 200>/var/lock/backup.lock
flock -n 200 || { echo "Script is already running!"; exit 1; }

# Critical section
echo "Performing backup operations..."
```

---

## 7. Cost Optimization

### S3 Multi-Part Upload Checking
Before transferring large database snapshots, check the size of the target file using standard HTTP HEAD requests via `curl` to skip unnecessary uploads:
```bash
SIZE_LOCAL=$(stat -c%s "/data/snapshot.tar.gz")
SIZE_REMOTE=$(curl -sI "https://my-bucket.s3.amazonaws.com/snapshot.tar.gz" | grep -i Content-Length | awk '{print $2}' | tr -d '\r')

if [ "$SIZE_LOCAL" -eq "$SIZE_REMOTE" ]; then
    echo "Files match. Skipping upload."
    exit 0
fi
```

---

## 8. Hands-On Labs

### Lab 8.1: User Automation Script (`add_user.sh`)
This script automates user creation, group mapping, and password enforcement with auditing.
```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <group>" >&2
    exit 1
fi

USERNAME="$1"
GROUP="$2"

# Check if group exists, if not create it
if ! getent group "$GROUP" >/dev/null; then
    echo "Group '$GROUP' not found. Creating it..."
    sudo groupadd "$GROUP"
fi

# Check if user exists
if getent passwd "$USERNAME" >/dev/null; then
    echo "Error: User '$USERNAME' already exists." >&2
    exit 2
fi

# Generate strong random password
PASSWORD=$(openssl rand -base64 12)

# Create user
sudo useradd -m -g "$GROUP" -s /bin/bash "$USERNAME"
echo "$USERNAME:$PASSWORD" | sudo chpasswd

# Force password change on first login
sudo chage -d 0 "$USERNAME"

# Log event
logger -t add_user "Created user $USERNAME in group $GROUP"

# Display credentials safely to stdout
echo "=========================================="
echo "User '$USERNAME' created successfully."
echo "Temporary Password: $PASSWORD"
echo "=========================================="
```

### Lab 8.2: S3 Backup Automation Script (`backup_s3.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/var/log"
DEST_BUCKET="s3://my-enterprise-backups-bucket/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE="/tmp/backup_${TIMESTAMP}.tar.gz"

echo "Creating compressed tarball..."
tar -czf "$ARCHIVE" -C "$BACKUP_DIR" .

# Calculate MD5 hash for integrity checking
MD5_HASH=$(md5sum "$ARCHIVE" | awk '{print $1}')
echo "Backup MD5: $MD5_HASH"

# Upload to S3 (Simulating AWS S3 call - replace with real s3 cp in production)
echo "Uploading to $DEST_BUCKET..."
# aws s3 cp "$ARCHIVE" "${DEST_BUCKET}/backup_${TIMESTAMP}.tar.gz" --metadata md5chk="$MD5_HASH"
echo "Upload complete (simulated)."

# Cleanup local archive
rm -f "$ARCHIVE"
```

### Lab 8.3: Custom Log Rotation Script (`custom_rotate.sh`)
Rotates log files if they exceed a target size threshold.
```bash
#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="/var/log/my_app.log"
MAX_SIZE_BYTES=10485760 # 10MB
BACKUP_COUNT=5

if [ ! -f "$LOG_FILE" ]; then
    echo "Log file $LOG_FILE does not exist. Exiting."
    exit 0
fi

FILE_SIZE=$(stat -c%s "$LOG_FILE")

if [ "$FILE_SIZE" -gt "$MAX_SIZE_BYTES" ]; then
    echo "Log file size ($FILE_SIZE bytes) exceeds limit ($MAX_SIZE_BYTES bytes). Rotating..."
    
    # Shift old archives
    for i in $(seq $((BACKUP_COUNT - 1)) -1 1); do
        if [ -f "${LOG_FILE}.${i}.gz" ]; then
            mv "${LOG_FILE}.${i}.gz" "${LOG_FILE}.$((i + 1)).gz"
        fi
    done
    
    # Compress current file and recreate it empty
    mv "$LOG_FILE" "${LOG_FILE}.1"
    touch "$LOG_FILE"
    chmod 640 "$LOG_FILE"
    gzip "${LOG_FILE}.1"
    
    echo "Log rotation completed."
fi
```

### Lab 8.4: HTTP Service Health Check (`http_health.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

URL="http://localhost:8080/health"
EXPECTED_STRING="UP"
TIMEOUT_SECS=5

RESPONSE=$(curl -s --max-time "$TIMEOUT_SECS" "$URL") || {
    echo "CRITICAL: Connection to $URL failed or timed out." >&2
    exit 2
}

if echo "$RESPONSE" | grep -q "$EXPECTED_STRING"; then
    echo "OK: Service is healthy."
    exit 0
else
    echo "CRITICAL: Health endpoint did not return '$EXPECTED_STRING'. Response: $RESPONSE" >&2
    exit 1
fi
```

### Lab 8.5: Container Deployment Orchestrator (`deploy_service.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="ml-inference"
IMAGE_TAG="localhost:5000/ml-inference:latest"
PORT_MAPPING="8080:8080"

echo "Pulling latest image: $IMAGE_TAG"
# docker pull "$IMAGE_TAG" (simulated)

if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
fi

echo "Starting new container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT_MAPPING" \
    --restart unless-stopped \
    "$IMAGE_TAG"

# Wait for container initialization and perform curl validation
echo "Verifying deployment..."
for i in {1..5}; do
    if curl -s http://localhost:8080/health | grep -q "UP"; then
        echo "Deployment successful."
        exit 0
    fi
    echo "Waiting for healthcheck... trial $i"
    sleep 3
done

echo "Error: Deployment verification failed. Checking logs..."
docker logs "$CONTAINER_NAME" | tail -n 20
exit 1
```

### Lab 8.6: System Performance Monitor Alerting (`perf_alert.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

THRESHOLD_CPU=85
THRESHOLD_MEM=90

# Calculate CPU Usage (idle percentage from mpstat or top)
CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk '{print $8}')
CPU_USAGE=$(echo "100 - $CPU_IDLE" | bc)

# Calculate Memory Usage
MEM_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')

echo "Metrics: CPU Usage = ${CPU_USAGE}%, RAM Usage = ${MEM_USAGE}%"

if (( $(echo "$CPU_USAGE > $THRESHOLD_CPU" | bc -l) )); then
    logger -t perf_alert "WARNING: High CPU utilization detected: ${CPU_USAGE}%"
fi

if (( $(echo "$MEM_USAGE > $THRESHOLD_MEM" | bc -l) )); then
    logger -t perf_alert "CRITICAL: High Memory utilization detected: ${MEM_USAGE}%"
fi
```

### Lab 8.7: Log File CSV Processor (`process_data.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT_CSV="/tmp/application_metrics.csv"
OUTPUT_SQL="/tmp/insert_metrics.sql"

# Generate mock CSV for processing
cat << 'EOF' > "$INPUT_CSV"
timestamp,metric_name,value
1718928300,inference_latency_ms,230.4
1718928360,inference_latency_ms,245.1
1718928420,inference_latency_ms,602.8
EOF

# Parse CSV and write SQL insert statements using awk
echo "-- Generated SQL Queries" > "$OUTPUT_SQL"
awk -F',' 'NR > 1 {
    print "INSERT INTO inference_metrics (timestamp, metric_name, value) VALUES ("$1", \x27"$2"\x27, "$3");"
}' "$INPUT_CSV" >> "$OUTPUT_SQL"

echo "SQL generation complete. Output saved to $OUTPUT_SQL"
```

### Lab 8.8: Crontab Provisioner (`schedule_cron.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

CRON_JOB="0 0 * * * /usr/local/bin/custom_rotate.sh"

# Read existing crontab, append new job, and reload
(crontab -l 2>/dev/null | grep -v "custom_rotate.sh" ; echo "$CRON_JOB") | crontab -
echo "Cron job scheduled successfully."
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Script Hangs on Network Pipeline
*   **Symptom**: A script running a log-download process hangs indefinitely without throwing errors or exiting.
*   **Root Cause**: The script invokes a network socket command (like `curl` or `nc`) without explicit connect/read timeout parameters.
*   **Resolution Strategy**:
    ```bash
    # 1. Run bash in debug mode to see where it blocks
    bash -x ./run_download.sh
    
    # 2. Identify the process ID and run strace to see what syscall it is stuck on
    sudo strace -p <PID> -e trace=network
    
    # 3. Fix by adding connection timeouts to all cURL commands:
    curl --connect-timeout 5 --max-time 30 -O http://example.com/logs.gz
    ```

### Task 9.2: "Unary Operator Expected" Conditional Failure
*   **Symptom**: Script exits with `line 12: [: unary operator expected`.
*   **Root Cause**: A single-bracket conditional test `[ $VAR -eq 10 ]` is evaluated. If `$VAR` is empty or null, the expression expands to `[ -eq 10 ]`, which is a syntax error.
*   **Resolution Strategy**:
    *   Change single brackets `[` to double brackets `[[`.
    *   Double bracket syntax `[[` handles empty variables gracefully.
    *   Always quote variables: `[[ "$VAR" -eq 10 ]]`.

### Task 9.3: Silent Failures in Mid-Pipeline Commands
*   **Symptom**: The script finishes with success code `0`, but the intermediate step in a command chain failed to run.
*   **Root Cause**: The exit status of a shell pipeline is determined by the exit code of the *last* command in the chain. E.g., `false | true` returns `0`.
*   **Resolution Strategy**:
    *   Set `pipefail` at the start of the script:
        ```bash
        set -o pipefail
        ```

---

## 10. Real Production Incidents

### Case Study: The Runaway Cleanup Script
*   **Incident**: An automated log cleaner cron script ran on a storage cluster. Due to an empty environment variable, it executed `rm -rf /$UNSET_VAR/tmp/log/*`. Since the variable was unset, the command resolved to `rm -rf //tmp/log/*` and started deleting system binaries in `/`.
*   **Remediation**:
    *   Implemented strict environment checking at the top of the script using the `-u` flag (`set -u`), which immediately aborts execution when an unbound variable is encountered.
    *   Modified the deletion pattern to use absolute prefixes and perform sanity checks:
        ```bash
        TARGET_DIR="/var/log/app"
        if [[ -z "${TARGET_DIR:-}" ]] || [[ "$TARGET_DIR" == "/" ]]; then
            echo "Critical: Dangerous target directory evaluation: '$TARGET_DIR'" >&2
            exit 99
        fi
        find "$TARGET_DIR" -type f -mtime +7 -delete
        ```

---

## 11. Interview Questions

### Q1: What is the exact difference between `[[` and `[` (test command) in Bash?
*   **Answer**:
    *   `[` is a POSIX standard utility (built-in or `/usr/bin/[`). It requires double quoting of variables to prevent expansion errors, and handles operators like `-a` (AND) and `-o` (OR) using standard parameter parsing.
    *   `[[` is a Bash keyword (syntax extension). It does not require double quoting variables to prevent word splitting or globbing, allows native pattern matching (using `=~` regex), and handles boolean operators using standard `&&` and `||`.

### Q2: How does command substitution using `$(cmd)` differ from backticks \`cmd\`?
*   **Answer**:
    *   `$(cmd)` is the modern POSIX standard. It allows nesting without complex backslash escaping: `$(cat $(find . -name "*.txt"))`.
    *   Backticks \`cmd\` are deprecated. Nesting requires escaping internal backticks, which makes code hard to read and debug.

### Q3: Explain what `2>&1` means and why the order of redirection matters.
*   **Answer**:
    *   `2>&1` means redirect File Descriptor 2 (`stderr`) to the same location/stream where File Descriptor 1 (`stdout`) is currently pointing.
    *   **Order matters**: `>file.log 2>&1` first points `stdout` to `file.log`, then points `stderr` to `file.log`. Both streams are written to the file.
    *   If you write `2>&1 >file.log`, `stderr` points to where `stdout` is *currently* pointing (the console), and then `stdout` is redirected to the file. This results in `stderr` still printing to the screen.

### Q4: How do you handle system signals (like SIGINT, SIGTERM) inside a running Bash script?
*   **Answer**: Using the `trap` built-in command. You specify a function or command string to run when the shell receives specific signals:
    ```bash
    cleanup() {
        echo "Cleaning up temporary files..."
        rm -f /tmp/lock.tmp
    }
    trap cleanup SIGINT SIGTERM EXIT
    ```

### Q5: What is the difference between `exec` and launching a process in a standard shell wrapper?
*   **Answer**:
    *   Standard launch forks a child process and runs it, while the parent shell process waits for the child to exit before continuing.
    *   `exec` replaces the current shell process image with the target command process. The PID remains the same, but the parent shell is terminated. No code block following `exec` will run unless the target binary fails to load.

---

## 12. Enterprise Case Studies

### Deploying AWS Infrastructure via CLI Scripting
Before adopting Terraform, massive enterprise environments were spun up using shell wrappers that called the AWS CLI (`aws ec2 create-vpc`, etc.). The key to scaling these scripts lay in querying state via `--query` parameters and JSON parsers (`jq`) to create dependency pipelines (e.g., getting the VPC ID to feed into subnet creation). This proved that scripting can model complete declarative patterns if developers write robust input/output parsing logic.

---

## 13. System Design Discussions

### Creating an Enterprise Bootstrap Tool
*   **Scenario**: Design a bootstrapper script to configure local developer environments (install tools, set up ssh keys, clone git repos).
*   **System Considerations**:
    *   **Idempotency**: The script should be runnable multiple times without duplicating entries in `~/.bashrc` or generating errors.
    *   **Modularity**: Divide functions into separate files (e.g., `networking.sh`, `packages.sh`) and load them dynamically using `source`.
    *   **Logging**: Mirror all operations to a local file (`/var/log/bootstrap.log`) and stdout using the `tee` command:
        ```bash
        exec > >(tee -a /var/log/bootstrap.log) 2>&1
        ```

---

## 14. AI Platform Perspective

### Orchestrating Model Weight Synchronization
AI platforms require copying massive weights (gigabytes to terabytes) across physical locations. A robust shell architecture uses `rclone` or `aws s3 sync` in combination with process monitoring to handle intermittent network failures:
```bash
#!/usr/bin/env bash
set -euo pipefail

MODEL_BUCKET="s3://my-enterprise-llm-weights/llama-3-70b"
LOCAL_DIR="/mnt/nvme/models/llama-3-70b"

# Use exponential backoff to handle transient AWS connection errors
max_retries=5
count=0
until aws s3 sync "$MODEL_BUCKET" "$LOCAL_DIR" --quiet; do
    exit_code=$?
    count=$((count + 1))
    if [ "$count" -ge "$max_retries" ]; then
        echo "Critical: Failed to sync model weights after $count attempts. Exit code: $exit_code" >&2
        exit $exit_code
    fi
    sleep_time=$((2 ** count))
    echo "Sync failed. Retrying in $sleep_time seconds..."
    sleep "$sleep_time"
done
echo "Model weight synchronization completed successfully."
```
