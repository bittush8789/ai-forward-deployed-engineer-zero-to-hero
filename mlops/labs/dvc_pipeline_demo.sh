#!/usr/bin/env bash
# DVC pipeline validation helper script.
# Demonstrates Git initialization, DVC caching configuration, and data staging.

set -euo pipefail

echo "=== Initializing DVC Pipeline Lab ==="

WORKSPACE="/tmp/dvc_pipeline_lab"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

# 1. Initialize Git and DVC
git init
dvc init

# 2. Configure local directory remote
mkdir -p "/tmp/dvc_remote_store"
dvc remote add -d myremote "/tmp/dvc_remote_store"

# 3. Create dummy file
echo "data_index,feature_val" > raw_data.csv
echo "1,22.4" >> raw_data.csv

# 4. Add file and track
dvc add raw_data.csv
git add raw_data.csv.dvc .gitignore
git commit -m "Add tracked dataset"

# 5. Push data to remote store
dvc push

echo "DVC Pipeline initialization completed successfully."
exit 0
