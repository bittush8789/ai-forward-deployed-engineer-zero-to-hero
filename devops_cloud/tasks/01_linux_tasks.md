# Practice Tasks: Module 1 - Linux Administration

This document outlines step-by-step tasks to practice Linux system administration, security hardening, and process troubleshooting.

---

## Task 1: User Privilege Management
*   **Goal**: Create a secure user group named `mlops` and assign access permissions to a directory.
*   **Step-by-Step Instructions**:
    1. Open a terminal on your Ubuntu system.
    2. Create the group:
       ```bash
       sudo groupadd mlops
       ```
    3. Create a new user named `developer` and assign them to the `mlops` group:
       ```bash
       sudo useradd -m -g mlops -s /bin/bash developer
       ```
    4. Create a target directory for shared resources:
       ```bash
       sudo mkdir -p /var/data/models
       ```
    5. Change ownership of the directory to root and the `mlops` group:
       ```bash
       sudo chown -R root:mlops /var/data/models
       ```
    6. Set directory permissions to allow read, write, and execute for owners and group members, and block others:
       ```bash
       sudo chmod 770 /var/data/models
       ```
    7. Enable POSIX Access Control Lists (ACLs) to grant read-only access to user `nobody`:
       ```bash
       sudo setfacl -m u:nobody:rx /var/data/models
       ```
*   **Verification**:
    Verify the directory permissions and ACL rules:
    ```bash
    getfacl /var/data/models
    ```

---

## Task 2: Process Inspection and Resource Tuning
*   **Goal**: Run a background process, inspect its resource consumption, and modify its scheduling priority.
*   **Step-by-Step Instructions**:
    1. Start a dummy CPU-intensive command in the background:
       ```bash
       dd if=/dev/zero of=/dev/null &
       ```
    2. Find the PID of the running command:
       ```bash
       PID=$(pgrep -f "dd if=/dev/zero")
       echo "Running process PID: $PID"
       ```
    3. Monitor the process resource usage in real-time:
       ```bash
       top -p $PID -b -n 1
       ```
    4. Change the process priority (nice value) to 10:
       ```bash
       sudo renice 10 -p $PID
       ```
    5. Monitor system metrics (such as I/O wait and CPU idle percentage) using `vmstat`:
       ```bash
       vmstat 1 5
       ```
    6. Terminate the background task:
       ```bash
       kill -9 $PID
       ```
*   **Verification**:
    Verify the background task has been terminated successfully:
    ```bash
    pgrep -f "dd if=/dev/zero" || echo "Task terminated"
    ```

---

## Task 3: SSH Configuration Hardening
*   **Goal**: Restrict SSH root logins and disable password-based authentication.
*   **Step-by-Step Instructions**:
    1. Create a backup of the existing SSH configuration file:
       ```bash
       sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
       ```
    2. Edit the configuration file:
       ```bash
       sudo nano /etc/ssh/sshd_config
       ```
    3. Update the following lines (uncomment if necessary):
       ```ini
       PermitRootLogin no
       PasswordAuthentication no
       PubkeyAuthentication yes
       ```
    4. Validate the configuration file syntax:
       ```bash
       sudo sshd -t
       ```
    5. Restart the SSH service to apply changes:
       ```bash
       sudo systemctl restart sshd
       ```
*   **Verification**:
    Attempt to connect to the server via SSH without using a private key. The server should reject the password connection request.

---

## Task 4: Custom Systemd Service Automation
*   **Goal**: Create and deploy a custom systemd service with automated recovery policies.
*   **Step-by-Step Instructions**:
    1. Create a simple Python worker script:
       ```python
       # /usr/local/bin/worker.py
       import time, sys
       print("Worker daemon initialized.", flush=True)
       while True:
           time.sleep(5)
       ```
       Write this file to disk:
       ```bash
       sudo tee /usr/local/bin/worker.py << 'EOF'
       import time, sys
       print("Worker daemon initialized.", flush=True)
       while True:
           time.sleep(5)
       EOF
       ```
    2. Make the script executable:
       ```bash
       sudo chmod +x /usr/local/bin/worker.py
       ```
    3. Create a custom systemd service file:
       ```bash
       sudo tee /etc/systemd/system/worker.service << 'EOF'
       [Unit]
       Description=Custom Worker Service
       After=network.target

       [Service]
       ExecStart=/usr/bin/python3 /usr/local/bin/worker.py
       Restart=always
       RestartSec=3s
       StandardOutput=journal
       StandardError=journal

       [Install]
       WantedBy=multi-user.target
       EOF
       ```
    4. Reload systemd, start the service, and enable it on boot:
       ```bash
       sudo systemctl daemon-reload
       sudo systemctl enable --now worker.service
       ```
*   **Verification**:
    Check the status and log output of the service:
    ```bash
    sudo systemctl status worker.service
    journalctl -u worker.service --since "5 minutes ago"
    ```
