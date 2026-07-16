# Module 3: Docker & Containerization Technology

## 1. Architecture Deep Dive

Docker abstracts operating-system-level virtualization to deliver software in packages called containers. It has transitioned from a monolithic daemon to a modular architecture governed by the Open Container Initiative (OCI) standards.

```
+-----------------------------------------------------------------------+
|                             Docker Client                             |
|          - CLI commands (docker build, docker run, docker push)       |
|          - Interacts with Host via REST API / Unix Socket              |
+-----------------------------------------------------------------------+
                                   |
                                   v (Unix Socket: /var/run/docker.sock)
+-----------------------------------------------------------------------+
|                             Docker Host                               |
|   +---------------------------------------------------------------+   |
|   |                 Docker Daemon (dockerd)                       |   |
|   |    - Manages images, networks, volumes, and authentication    |   |
|   +-------------------------------|-------------------------------+   |
|                                   v (gRPC)                            |
|   +---------------------------------------------------------------+   |
|   |                       containerd                              |   |
|   |    - Manages container lifecycle (start, stop, pause, delete)  |   |
|   +-------------------------------|-------------------------------+   |
|                                   v (spawns container-shim)           |
|   +---------------------------------------------------------------+   |
|   |                       container-shim                          |   |
|   |    - Decouples container execution from containerd             |   |
|   |    - Keeps stdio open if daemon restarts                       |   |
|   +-------------------------------|-------------------------------+   |
|                                   v                                   |
|   +---------------------------------------------------------------+   |
|   |                        runc (OCI Runtime)                     |   |
|   |    - Low-level executor. Interacts with kernel to configure    |   |
|   |      namespaces and cgroups, starts process, then exits       |   |
|   +-------------------------------+-------------------------------+   |
+-----------------------------------|-----------------------------------+
                                    v
                       Container Execution State
```

### Layered Filesystem (OverlayFS)
Docker images are built up as a series of read-only layers. When a container is started, a thin writeable layer ("Container Layer") is added on top. All changes are written here.
*   **Lowerdir**: Read-only image layers containing base OS binaries and application code.
*   **Upperdir**: Writable layer containing files created, modified, or deleted during container execution.
*   **Merged**: The unified view that the container process sees.
*   **Workdir**: Internal directory used for OverlayFS transaction operations.

---

## 2. Internal Working

### Linux Namespaces (Process Isolation)
Docker isolates processes by utilizing Linux Namespaces:
*   **PID**: Isolates process IDs. The main process inside the container becomes PID 1.
*   **NET**: Isolates network interfaces, IP routing tables, and firewall rules.
*   **MNT**: Isolates filesystem mount points.
*   **IPC**: Isolates Inter-Process Communication resources (shared memory, message queues).
*   **UTS**: Isolates hostname and domain name.
*   **User**: Isolates UID and GID mappings, allowing a user to have root access inside the container while being mapped to a non-privileged UID on the host.

### Control Groups (cgroups)
cgroups regulate system resources for containers:
*   **Memory**: Limits RAM usage and triggers OOM actions.
*   **CPU**: Restricts CPU execution time (shares, cores).
*   **Blkio**: Restricts disk I/O read/write rates.

### Seccomp (Secure Computing Mode)
Docker uses seccomp to filter system calls made by container processes. By default, Docker blocks around 44 system calls (like `mount`, `reboot`, and `kexec_load`) out of the hundreds available in the Linux kernel to limit exploit paths.

---

## 3. Production Use Cases

### GPU-Enabled AI Container Stacks
In production, machine learning teams deploy inference models using GPU resources. By configuring `nvidia-container-runtime`, container workloads access physical hardware devices directly.

### Multi-Tier Microservice Architectures
Containers isolate API routes, caching engines, and message brokers on a single host. By defining networks and storage pools, they replicate full target systems with minimal resource overhead.

---

## 4. Security Best Practices

### Rootless Docker Mode
Run the Docker daemon and containers as a non-root user to mitigate host-compromise risks if a container escape vulnerability is exploited.

### Security Hardening Settings
*   **Drop Capabilities**: Drop unused kernel privileges.
    ```bash
    docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE my-app
    ```
*   **Read-Only Root Filesystem**: Prevent files from being modified inside the container.
    ```bash
    docker run --read-only --tmpfs /tmpmy-app
    ```

---

## 5. Scalability Patterns

### Multi-Stage Build Caching
By restructuring Dockerfiles, developers leverage layer caching to speed up CI/CD pipeline builds. Put slow-changing commands (like package installation) near the top, and fast-changing application code near the bottom.

### Image Compression Strategy
Smaller images download faster and reduce network bottlenecks. Use `distroless` or `alpine` base images to keep image sizes minimal.

---

## 6. Reliability Patterns

### Configuring Standard Daemon Log Rotation
Prevent containers from filling the host disk by editing `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  }
}
```
Apply config: `sudo systemctl reload docker`

### Docker Healthcheck Directive
Validate application readiness within the container itself:
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

---

## 7. Cost Optimization

### Reclaiming Dangling Resources
Automate dangling image and stopped container pruning via scheduled cron tasks:
```bash
# Force prune unused resources
docker system prune -a --volumes -f
```
This cleans up cached build layers and unused volumes, keeping cloud storage costs low.

---

## 8. Hands-On Labs

### Lab 8.1: Multi-Stage Python Dockerfile Construction
We will build a secure, optimized container for a Python application.
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

COPY requirements.txt .
RUN pip install --user --no-warn-script-location --no-cache-dir -r requirements.txt

# Stage 2: Runtime image
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/nonroot/.local
COPY app.py .

ENV PATH=/home/nonroot/.local/bin:$PATH
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
```

### Lab 8.2: Dockerfile Layer Optimization
```dockerfile
# BAD: Every command creates a layer and cache is not optimized
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3
COPY ./src /app
RUN pip install -r /app/requirements.txt

# GOOD: Combined RUN statements and proper file copy ordering
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src .
```

### Lab 8.3: Docker Compose Application Stack
Create a multi-container environment with a Web App and a Redis caching server.
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    image: python:3.11-slim
    command: python -m http.server 8080
    ports:
      - "8080:8080"
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  cache:
    image: redis:7.0-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network

volumes:
  redis-data:

networks:
  app-network:
    driver: bridge
```
Execute commands:
```bash
docker compose up -d
docker compose ps
```

### Lab 8.4: Private Container Registry Setup
```bash
# 1. Start a local registry container
docker run -d -p 5001:5000 --restart=always --name local-registry registry:2

# 2. Tag a sample image for the local registry
docker pull alpine:latest
docker tag alpine:latest localhost:5001/my-alpine:1.0

# 3. Push the image
docker push localhost:5001/my-alpine:1.0

# 4. Pull the image to verify
docker pull localhost:5001/my-alpine:1.0
```

### Lab 8.5: Container Lifecycle Troubleshooting
```bash
# 1. View low-level config details
docker inspect local-registry

# 2. View real-time container metrics
docker stats local-registry --no-stream

# 3. View container log output
docker logs local-registry --tail 50
```

### Lab 8.6: Security Scanning with Trivy
```bash
# 1. Install Trivy
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install -y trivy

# 2. Scan an image for vulnerabilities
trivy image --severity HIGH,CRITICAL python:3.11-slim
```

### Lab 8.7: Disk Space Cleanup
```bash
# Analyze disk usage of docker components
docker system df

# Clean all unused networks, containers, and dangling images
docker system prune -f
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Port Bind Failure
*   **Symptom**: `docker run` exits with `docker: Error response from daemon: driver failed programming external connectivity on endpoint ... bind: address already in use`.
*   **Root Cause**: The host port requested is already bound to another application or container.
*   **Resolution Strategy**:
    ```bash
    # 1. Identify which process is holding the port (e.g., port 8080)
    sudo ss -tlnp | grep 8080
    # Or use lsof
    sudo lsof -i :8080
    
    # 2. Terminate the conflicting host process or map the container to a different host port:
    docker run -d -p 9090:8080 my-app
    ```

### Task 9.2: Volume Bind Mount Permission Denied
*   **Symptom**: Container starts but immediately exits. Inspection of logs reveals `permission denied` when writing to a mounted directory.
*   **Root Cause**: The container process is running as a specific UID/GID that lacks write permissions on the host directory.
*   **Resolution Strategy**:
    ```bash
    # 1. Identify the UID running inside the container
    docker inspect my-container | grep -i User
    
    # 2. Modify host directory permissions to match the container's UID (e.g., UID 1000):
    sudo chown -R 1000:1000 /mnt/host_data
    ```

### Task 9.3: Out-Of-Memory Container Exits
*   **Symptom**: Container dies without warning. Running `docker inspect` shows `"OOMKilled": true` and `"ExitCode": 137`.
*   **Root Cause**: The container exceeded its configured cgroup memory limit, and the kernel terminated it.
*   **Resolution Strategy**:
    *   Verify application memory footprint (e.g., profiling python variables).
    *   Increase container limit allocations:
        ```bash
        docker run -d --memory 1g my-app
        ```

---

## 10. Real Production Incidents

### Case Study: Standard Output Log Explosion
*   **Incident**: An API container service was deployed without log rotation configurations. Over three weeks, the container's standard output filled `/var/lib/docker/containers/` with a 120GB JSON log file, exhausting all host disk space and causing database services to crash.
*   **Remediation**:
    *   Configured the default log driver in `/etc/docker/daemon.json` to cap log files at 50MB and keep only 3 rotation backups.
    *   Implemented a deployment rule to always pass `--log-opt` values to standalone runs.
    *   Ran a cleanup script to truncate existing log files without stopping containers:
        ```bash
        sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*.log'
        ```

---

## 11. Interview Questions

### Q1: What is the difference between `ENTRYPOINT` and `CMD` in a Dockerfile?
*   **Answer**:
    *   `ENTRYPOINT` defines the executable binary that is run when the container starts. It cannot be overridden easily during `docker run` unless the `--entrypoint` flag is passed.
    *   `CMD` defines the default arguments passed to the `ENTRYPOINT`. If no `ENTRYPOINT` is defined, `CMD` acts as the default command. `CMD` can be overridden by passing arguments at the end of the `docker run` command: `docker run my-image /bin/bash`.

### Q2: Explain how OverlayFS mounts layers together to construct a single filesystem directory.
*   **Answer**: OverlayFS combines multiple directories (layers) into a single mount point.
    *   **Lowerdir**: The read-only directories representing lower image layers.
    *   **Upperdir**: The read-write directory representing the active container layer.
    *   **Merged**: The virtual filesystem directory exposed to the container process. If a file exists in both lowerdir and upperdir, the version in upperdir masks the version in lowerdir. Deleting a lowerdir file creates a special character device called a "whiteout" file in upperdir to hide it from the merged view.

### Q3: What is the purpose of the `container-shim` process?
*   **Answer**: The `container-shim` runs between containerd and runc. It sits above the container process and is responsible for:
    *   Maintaining the container's open file descriptors (stdin, stdout, stderr) even if containerd or dockerd crashes or restarts.
    *   Reporting the container's exit status back to containerd.
    *   Preventing the container from becoming a zombie process if the main daemon dies.

### Q4: Why is it bad practice to run apt-get update and apt-get install on separate lines in a Dockerfile?
*   **Answer**: If they are on separate lines, Docker caches the layer created by `RUN apt-get update`. If you modify the install command later (e.g., adding `RUN apt-get install -y curl`), Docker will reuse the cached `apt-get update` layer. This can lead to installing outdated packages or failing to build if the package lists are no longer valid. Combining them into `RUN apt-get update && apt-get install -y curl` ensures they are executed together.

### Q5: How do Docker volume mounts differ from bind mounts?
*   **Answer**:
    *   **Volumes**: Managed by Docker. They are stored in a part of the host filesystem managed by Docker (`/var/lib/docker/volumes/`). Non-Docker processes should not modify this directory. Volumes are portable, support volume drivers (for cloud storage), and are safer to use.
    *   **Bind Mounts**: Mount any file or directory on the host machine into the container. They rely on the host's directory structure. This can introduce security issues, as containers can modify critical host files.

---

## 12. Enterprise Case Studies

### Microservice Containerization at Uber
Uber shifted its legacy monolithic infrastructure to microservices run inside Docker containers. This allowed engineers to specify the exact execution environments (dependencies, libraries, Python versions) for their services. By standardizing on Docker, they reduced boot times, simplified localized development environments, and built a unified deployment pipeline that ran containerized workloads across thousands of physical servers.

---

## 13. System Design Discussions

### Secure Internal Container Registry Architecture
*   **Objective**: Design a secure, high-throughput container registry for an enterprise team.
*   **Architecture Considerations**:
    *   **Access Control**: Integrate the registry with Active Directory or LDAP via OAuth2. Use RBAC to restrict who can write to production repositories.
    *   **Storage Backend**: Store image layers in a high-availability cloud storage bucket (like AWS S3) behind a CDN to speed up image pulls across multiple geographic regions.
    *   **Security Scanning**: Integrate vulnerability scanners (like Trivy or Clair) to scan images on push. Block deployment if critical CVEs are found.
    *   **High Availability**: Deploy registry instances behind a load balancer with auto-scaling enabled.

---

## 14. AI Platform Perspective

### NVIDIA GPU Runtime Integration
```dockerfile
# Dockerfile for GPU-enabled PyTorch execution
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Run application using CUDA hardware
CMD ["python3", "gpu_inference.py"]
```
To run this container with host GPU hardware:
```bash
docker run --gpus all -d -p 8080:8080 my-pytorch-app
```
The `--gpus all` flag instructs the Docker daemon to pass NVIDIA device nodes (`/dev/nvidia*`) and dynamic CUDA libraries to the container, enabling high-performance GPU utilization.
