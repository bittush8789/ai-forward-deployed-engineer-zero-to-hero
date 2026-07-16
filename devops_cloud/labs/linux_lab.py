#!/usr/bin/env python3
"""
Linux Administration System Verification Lab Script.
Demonstrates process monitoring, user verification, and disk statistics extraction.
"""

import os
import sys
import subprocess
import shutil

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\nError: {e.stderr}", file=sys.stderr)
        return None

def check_system_metrics():
    print("=== System Metrics Summary ===")
    
    # 1. Load Average
    load = run_command("uptime")
    print(f"Load Average: {load}")
    
    # 2. Disk Space
    total, used, free = shutil.disk_usage("/")
    print(f"Disk Space: Total: {total // (2**30)} GiB, Used: {used // (2**30)} GiB, Free: {free // (2**30)} GiB")
    
    # 3. CPU Core Count
    cores = os.cpu_count()
    print(f"Available CPU Cores: {cores}")
    
    # 4. Kernel version
    kernel = run_command("uname -r")
    print(f"Kernel Version: {kernel}")
    print("==============================\n")

def check_user_access():
    print("=== User & Access Verification ===")
    # Check if run as root
    is_root = os.getuid() == 0
    print(f"Running as administrative user (root): {is_root}")
    
    # Print current user ID and group ID mappings
    uid = os.getuid()
    gid = os.getgid()
    print(f"User ID (UID): {uid}, Group ID (GID): {gid}")
    
    # List active users logged in
    users = run_command("who")
    print(f"Currently logged-in users:\n{users if users else 'None'}")
    print("==================================\n")

def main():
    print("Initializing Linux Administration Verification Lab...")
    check_system_metrics()
    check_user_access()
    print("Linux lab script execution complete.")

if __name__ == "__main__":
    main()
