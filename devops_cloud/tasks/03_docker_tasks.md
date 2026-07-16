# Practice Tasks: Module 3 - Docker & Containerization

This document outlines step-by-step tasks to practice Docker image building, multi-stage optimization, and security vulnerability scanning.

---

## Task 1: Multi-Stage Image Optimization
*   **Goal**: Optimize a Python Flask Dockerfile to reduce image size and run as a non-root user.
*   **Step-by-Step Instructions**:
    1. Create a dummy Python application file:
       ```python
       # /tmp/app.py
       from flask import Flask
       app = Flask(__name__)
       @app.route('/')
       def hello(): return "Hello from Docker!"
       if __name__ == '__main__': app.run(host='0.0.0.0', port=8080)
       ```
       Write this file to disk:
       ```bash
       mkdir -p /tmp/docker-lab
       tee /tmp/docker-lab/app.py << 'EOF'
       from flask import Flask
       app = Flask(__name__)
       @app.route('/')
       def hello(): return "Hello from Docker!"
       if __name__ == '__main__': app.run(host='0.0.0.0', port=8080)
       EOF
       ```
    2. Create a requirements lock file:
       ```bash
       echo "Flask==3.0.0" > /tmp/docker-lab/requirements.txt
       ```
    3. Create the multi-stage Dockerfile:
       ```dockerfile
       # /tmp/docker-lab/Dockerfile
       # Stage 1: Build dependencies
       FROM python:3.11-slim AS builder
       WORKDIR /build
       COPY requirements.txt .
       RUN pip install --user --no-cache-dir -r requirements.txt

       # Stage 2: Minimal runtime image
       FROM gcr.io/distroless/python3-debian12:nonroot
       WORKDIR /app
       COPY --from=builder /root/.local /home/nonroot/.local
       COPY app.py .
       ENV PATH=/home/nonroot/.local/bin:$PATH
       EXPOSE 8080
       ENTRYPOINT ["python", "app.py"]
       ```
       Write the Dockerfile to disk:
       ```bash
       tee /tmp/docker-lab/Dockerfile << 'EOF'
       FROM python:3.11-slim AS builder
       WORKDIR /build
       COPY requirements.txt .
       RUN pip install --user --no-cache-dir -r requirements.txt

       FROM gcr.io/distroless/python3-debian12:nonroot
       WORKDIR /app
       COPY --from=builder /root/.local /home/nonroot/.local
       COPY app.py .
       ENV PATH=/home/nonroot/.local/bin:$PATH
       EXPOSE 8080
       ENTRYPOINT ["python", "app.py"]
       EOF
       ```
    4. Build the Docker image:
       ```bash
       cd /tmp/docker-lab
       docker build -t my-flask-app:optimized .
       ```
*   **Verification**:
    Verify the image layer count and total size:
    ```bash
    docker images my-flask-app:optimized
    docker history my-flask-app:optimized
    ```

---

## Task 2: Multi-Container Stack Deployment
*   **Goal**: Deploy a multi-container stack containing a web application and a Redis caching server using Docker Compose.
*   **Step-by-Step Instructions**:
    1. Create a `docker-compose.yml` file in your directory:
       ```yaml
       # /tmp/docker-lab/docker-compose.yml
       version: '3.8'

       services:
         web:
           image: python:3.11-slim
           command: python -m http.server 8080
           ports:
             - "8080:8080"
           networks:
             - app-net
           deploy:
             resources:
               limits:
                 cpus: '0.5'
                 memory: 256M

         cache:
           image: redis:7.0-alpine
           ports:
             - "6379:6379"
           networks:
             - app-net

       networks:
         app-net:
           driver: bridge
       ```
       Write this file to disk:
       ```bash
       tee /tmp/docker-lab/docker-compose.yml << 'EOF'
       version: '3.8'

       services:
         web:
           image: python:3.11-slim
           command: python -m http.server 8080
           ports:
             - "8080:8080"
           networks:
             - app-net
           deploy:
             resources:
               limits:
                 cpus: '0.5'
                 memory: 256M

         cache:
           image: redis:7.0-alpine
           ports:
             - "6379:6379"
           networks:
             - app-net

       networks:
         app-net:
           driver: bridge
       EOF
       ```
    2. Deploy the stack:
       ```bash
       cd /tmp/docker-lab
       docker compose up -d
       ```
*   **Verification**:
    Verify the status of the running containers:
    ```bash
    docker compose ps
    docker compose logs web
    ```
    Clean up the containers:
    ```bash
    docker compose down
    ```

---

## Task 3: Vulnerability Scanning with Trivy
*   **Goal**: Install Trivy and scan your optimized Docker image for CVE security vulnerabilities.
*   **Step-by-Step Instructions**:
    1. Install Trivy:
       ```bash
       sudo apt-get install -y wget apt-transport-https gnupg lsb-release
       wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
       echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
       sudo apt-get update && sudo apt-get install -y trivy
       ```
    2. Scan your optimized image:
       ```bash
       trivy image my-flask-app:optimized
       ```
    3. Scan the image and output only critical and high severity vulnerabilities:
       ```bash
       trivy image --severity HIGH,CRITICAL my-flask-app:optimized
       ```
*   **Verification**:
    Confirm the vulnerability scan runs successfully and outputs a summary table.
