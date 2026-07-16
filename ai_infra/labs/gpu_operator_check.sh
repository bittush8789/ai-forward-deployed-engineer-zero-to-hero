#!/usr/bin/env bash
# GPU Operator validation and status checks.
# Verifies container runtime and nvidia-smi status.

set -euo pipefail

echo "=== Verifying GPU Container Runtime ==="

# 1. Check if docker is active
if systemctl is-active --quiet docker; then
    echo "Docker service is ONLINE."
else
    echo "Docker service is OFFLINE."
fi

# 2. Check if nvidia-smi command is present
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA System Management Interface (nvidia-smi) is present."
    nvidia-smi
else
    echo "NVIDIA Driver or GPU SMI tools are missing. Run installation steps."
fi

echo "GPU Operator checks completed successfully."
exit 0
