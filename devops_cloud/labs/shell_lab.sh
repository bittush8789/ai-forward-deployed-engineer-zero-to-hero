#!/usr/bin/env bash
# Shell Scripting Verification Lab Script
# Demonstrates directory creation, log rotation check, and error handling pattern.

set -euo pipefail
IFS=$'\n\t'

echo "=== Starting Shell Scripting Lab ==="

# 1. Setup temp workspace
WORKSPACE="/tmp/shell_lab_workspace"
mkdir -p "$WORKSPACE"
echo "Created workspace: $WORKSPACE"

# 2. Create mock logs file
LOG_FILE="${WORKSPACE}/app_run.log"
echo "$(date +'%Y-%m-%d %H:%M:%S') [INFO] Application execution started." > "$LOG_FILE"
echo "$(date +'%Y-%m-%d %H:%M:%S') [WARN] Ephemeral network socket connection timeout. Retrying." >> "$LOG_FILE"
echo "$(date +'%Y-%m-%d %H:%M:%S') [ERROR] Database write transaction failed." >> "$LOG_FILE"

# 3. Parse logs and audit errors
echo "Auditing log file for errors..."
if grep -q "\[ERROR\]" "$LOG_FILE"; then
    echo "Alert: High severity errors identified in the log file!"
    # Display error lines
    grep "\[ERROR\]" "$LOG_FILE"
fi

# 4. Clean workspace
echo "Cleaning up local workspace files..."
rm -rf "$WORKSPACE"

echo "=== Shell Scripting Lab Completed Successfully ==="
exit 0
