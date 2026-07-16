# Practice Tasks: Module 2 - Shell Scripting

This document outlines step-by-step tasks to practice Bash scripting, variable handling, and process pipeline automation.

---

## Task 1: Log Scraping and CSV Processing
*   **Goal**: Write a script to parse log files, extract slow requests, and output them to a CSV file.
*   **Step-by-Step Instructions**:
    1. Create a dummy log file:
       ```bash
       cat << 'EOF' > /tmp/api_access.log
       2026-07-16 06:12:01 INFO path=/index latency=12ms
       2026-07-16 06:12:05 WARN path=/predict latency=450ms
       2026-07-16 06:12:12 INFO path=/health latency=5ms
       2026-07-16 06:12:18 ERROR path=/predict latency=1200ms
       EOF
       ```
    2. Create a script named `process_logs.sh`:
       ```bash
       touch /tmp/process_logs.sh
       chmod +x /tmp/process_logs.sh
       ```
    3. Add the following content to the script:
       ```bash
       #!/usr/bin/env bash
       set -euo pipefail

       LOG_FILE="/tmp/api_access.log"
       OUTPUT_CSV="/tmp/slow_requests.csv"
       THRESHOLD_MS=400

       echo "timestamp,level,path,latency_ms" > "$OUTPUT_CSV"

       # Parse logs using awk and output slow requests to CSV
       awk -v limit="$THRESHOLD_MS" '
       {
           # Extract latency value using match or split
           split($6, lat, "=");
           gsub("ms", "", lat[2]);
           latency = lat[2] + 0;
           
           if (latency >= limit) {
               split($4, p, "=");
               print $1" "$2"," $3"," p[2]"," latency;
           }
       }' "$LOG_FILE" >> "$OUTPUT_CSV"

       echo "Log processing complete. Slow requests saved to $OUTPUT_CSV"
       ```
    4. Run the script:
       ```bash
       /tmp/process_logs.sh
       ```
*   **Verification**:
    Verify the output file contains the correct CSV rows:
    ```bash
    cat /tmp/slow_requests.csv
    ```

---

## Task 2: Service Health Checks with Notifications
*   **Goal**: Create an automated health check script that verifies HTTP responses and logs alerts to syslog if failures occur.
*   **Step-by-Step Instructions**:
    1. Create the health check script:
       ```bash
       sudo tee /usr/local/bin/health_check.sh << 'EOF'
       #!/usr/bin/env bash
       set -euo pipefail

       URL="http://localhost:8080/health"
       EXPECTED="UP"
       TIMEOUT_SECS=3

       # Fetch health endpoint status with timeout limits
       if ! RESPONSE=$(curl -s --max-time "$TIMEOUT_SECS" "$URL"); then
           logger -t health_check -p user.err "CRITICAL: Connection to $URL failed or timed out."
           exit 1
       fi

       # Validate response content matches the expected string
       if echo "$RESPONSE" | grep -q "$EXPECTED"; then
           echo "OK: Service is running healthy."
           exit 0
       else
           logger -t health_check -p user.warn "WARNING: Health endpoint returned unexpected response: '$RESPONSE'"
           exit 2
       fi
       EOF
       ```
    2. Make the script executable:
       ```bash
       sudo chmod +x /usr/local/bin/health_check.sh
       ```
*   **Verification**:
    Verify the script behavior by running it against a dummy server:
    ```bash
    # Run a simple HTTP listener on port 8080 returning "UP"
    python3 -c 'from http.server import BaseHTTPRequestHandler, HTTPServer;
class H(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"UP")
HTTPServer(("localhost", 8080), H).serve_forever()' &
    HTTP_PID=$!
    
    # Run healthcheck
    /usr/local/bin/health_check.sh
    
    # Clean up HTTP listener
    kill "$HTTP_PID"
    ```

---

## Task 3: Automatic Directory Backups
*   **Goal**: Write a script to package configuration directories and upload them to cloud storage with retry logic.
*   **Step-by-Step Instructions**:
    1. Create the backup script:
       ```bash
       sudo tee /usr/local/bin/backup_logs.sh << 'EOF'
       #!/usr/bin/env bash
       set -euo pipefail

       SOURCE_DIR="/var/log/nginx"
       BACKUP_DEST="/tmp/backups"
       TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
       ARCHIVE="${BACKUP_DEST}/nginx_logs_${TIMESTAMP}.tar.gz"

       mkdir -p "$BACKUP_DEST"

       if [ ! -d "$SOURCE_DIR" ]; then
           echo "Error: Source directory $SOURCE_DIR not found. Exiting." >&2
           exit 1
       fi

       echo "Compressing logs from $SOURCE_DIR..."
       tar -czf "$ARCHIVE" -C "$SOURCE_DIR" .

       # Simulate upload to cloud storage with retry limits
       MAX_RETRIES=3
       COUNT=0
       SUCCESS=false

       until [ "$COUNT" -ge "$MAX_RETRIES" ]; do
           echo "Uploading $ARCHIVE to backup store... (Attempt $((COUNT + 1)))"
           # Simulated upload logic (e.g. aws s3 cp "$ARCHIVE" s3://backup-bucket/)
           if true; then
               SUCCESS=true
               break
           fi
           COUNT=$((COUNT + 1))
           sleep 2
       done

       if [ "$SUCCESS" = true ]; then
           echo "Backup uploaded successfully."
           rm -f "$ARCHIVE" # Clean up local archive file
       else
           echo "Error: Backup upload failed after $MAX_RETRIES attempts." >&2
           exit 2
       fi
       EOF
       ```
    2. Make the script executable:
       ```bash
       sudo chmod +x /usr/local/bin/backup_logs.sh
       ```
*   **Verification**:
    Run the script and verify the log output messages:
    ```bash
    # Create dummy source directory for simulation
    sudo mkdir -p /var/log/nginx
    sudo touch /var/log/nginx/access.log
    
    # Run backup script
    sudo /usr/local/bin/backup_logs.sh
    ```
