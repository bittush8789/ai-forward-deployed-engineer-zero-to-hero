#!/usr/bin/env python3
"""
Docker Container Integration Verification Lab.
"""

import subprocess
import sys

def check_docker_daemon():
    print("=== Checking Docker Daemon Status ===")
    try:
        # Check if docker command is available
        version = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        print(f"Docker CLI version: {version.stdout.strip()}")
        
        # Check if daemon is responsive
        info = subprocess.run(["docker", "info"], capture_output=True, text=True, check=True)
        print("Docker Daemon is running and responsive.")
        
        # List running containers
        containers = subprocess.run(["docker", "ps"], capture_output=True, text=True, check=True)
        print(f"\nActive containers:\n{containers.stdout.strip()}")
        
    except FileNotFoundError:
        print("Error: Docker command line utility not found. Please install Docker first.", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: Docker daemon is not running or responsive.\nMessage: {e.stderr}", file=sys.stderr)

def main():
    check_docker_daemon()

if __name__ == "__main__":
    main()
