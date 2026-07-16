# Module 8: Enterprise CI/CD with Jenkins

## 1. Architecture Deep Dive

Jenkins is an open-source automation server designed to orchestrate complex continuous integration and continuous delivery (CI/CD) pipelines. It uses a **Controller-Agent (Master-Worker)** architecture to scale builds.

```
+---------------------------------------------------------------------------------------------------+
|                                       Jenkins Controller (Master)                                 |
|   - Hosts the web UI, configuration engine, and scheduling manager                                |
|   - Parses and schedules Jenkinsfile pipelines                                                    |
|   - Manages user authentication, plug-ins, and build history metadata                             |
+------------------------------------+--------------------------------------------------------------+
                                     |
                                     v (Communication: SSH or JNLP protocols)
+------------------------------------+--------------------------------------------------------------+
|                                        Agent Nodes (Workers)                                      |
|   +------------------------------------+-----------------------------------------------------+    |
|   |    Static VM Agent (Linux/Win)     |         Dynamic Kubernetes Pod Agent                |    |
|   |    - Runs java agent.jar           |         - Kubelet provisions agent pods on-demand   |    |
|   |    - Persistent build directories  |         - Ephemeral, cleaned up after execution     |    |
|   +------------------------------------+-----------------------------------------------------+    |
+---------------------------------------------------------------------------------------------------+
```

### Controller vs. Agent Execution Rules
*   **Controller**: The control plane. It should only coordinate jobs, track schedules, and render the UI. It should not execute builds directly, as this exposes the host system to security risks and can cause performance bottlenecks.
*   **Agents**: Dedicated machines (physical VMs or containers) that run a lightweight Java agent (`agent.jar`). They receive execution commands from the controller and run the build steps.

### Agent Connection Protocols
*   **SSH**: The controller initiates the connection to a remote agent using SSH credentials, copies `agent.jar` to the agent, and starts it.
*   **Inbound Agents (JNLP)**: The agent initiates a connection to the controller over TCP. This is ideal for agents behind firewalls or inside private subnets.

---

## 2. Internal Working

### Declarative vs. Scripted Pipelines
*   **Declarative Pipelines**: Modern, structured format. Defined within a `pipeline {}` block. Enforces a strict schema with clear sections (`stages`, `stage`, `steps`, `post`), making it easier to read and maintain.
*   **Scripted Pipelines**: Traditional, imperatively executed Groovy code. Defined within a `node {}` block. Highly flexible but harder to debug and prone to complex, unreadable code.

### Pipeline Execution & Groovy Sandbox
Jenkins runs pipeline Groovy code inside a restricted sandbox to prevent scripts from executing malicious system calls on the controller host. Unsafe calls (like reading local host files or modifying system configurations) require admin approval in the Jenkins console.

---

## 3. Production Use Cases

### Multi-Stage Software Assembly
Orchestrating long-running builds that compile code, run security tests, and deploy packages across multiple cloud environments.

### Parallel Integration Test Execution
Splitting integration test suites into parallel execution paths running across different agent nodes, reducing total build time.

---

## 4. Security Best Practices

### Disabling Executions on the Controller
Set the controller executor count to **0** to ensure all builds run on remote agents. This protects the controller configuration directory (`JENKINS_HOME`) from access by build scripts.

### Hardening Configuration Settings
*   Enable **CSRF Protection** (default in modern versions).
*   Disable the Jenkins CLI port if not used.
*   Configure the **Role-Based Authorization Strategy** plugin to restrict access to projects using folder-level permissions.

---

## 5. Scalability Patterns

### Dynamic Agent Provisioning on Kubernetes
Instead of maintaining a static pool of idle VMs, configure the Kubernetes plugin to spin up agent pods on-demand. The agent pod runs the build steps and terminates once the job completes, saving infrastructure costs.

### Jenkins Shared Libraries
Avoid duplication by packaging common pipeline helper functions (like sending Slack alerts or building Docker images) into a Git repository. Import and reuse them across all company Jenkinsfiles:
```groovy
@Library('my-shared-library') _
stage('Notify') {
    slackNotifier.send("Build Succeeded")
}
```

---

## 6. Reliability Patterns

### Disaster Recovery
The entire state of a Jenkins server is stored in flat XML files within `$JENKINS_HOME`.
*   **Backups**: Automate backups of XML files (excluding workspaces and build history) using the `thinBackup` plugin.
*   **Git-Managed Configurations**: Store configuration templates in Git, allowing you to recreate the server environment if it crashes.

---

## 7. Cost Optimization

### Dynamic Compute Scale-Down
When running dynamic agents on Kubernetes, configure the idle retention time to terminate agent pods immediately after jobs finish, freeing up compute capacity.

---

## 8. Hands-On Labs

### Lab 8.1: Creating a Declarative Pipeline
```groovy
// Jenkinsfile
pipeline {
    agent { label 'linux-agent' }
    
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'python3 -m unittest discover'
            }
        }
    }
    
    post {
        always {
            cleanWs() // Clean workspace after run completes
        }
    }
}
```

### Lab 8.2: Configuring Dynamic Kubernetes Agents
```groovy
// Jenkinsfile.k8s
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: python-builder
    image: python:3.11-slim
    command: ["cat"]
    tty: true
  - name: docker-builder
    image: docker:dind
    securityContext:
      privileged: true
'''
        }
    }
    stages {
        stage('Build inside container') {
            steps {
                container('python-builder') {
                    sh 'python3 --version'
                }
            }
        }
    }
}
```

### Lab 8.3: Docker Integration Pipeline
Build a Docker image and push it to a registry.
```groovy
// Jenkinsfile
pipeline {
    agent any
    environment {
        REGISTRY = "localhost:5001"
        IMAGE_NAME = "my-app"
    }
    stages {
        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'registry-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    docker login -u "$USER" -p "$PASS" $REGISTRY
                    docker build -t $REGISTRY/$IMAGE_NAME:$BUILD_NUMBER .
                    docker push $REGISTRY/$IMAGE_NAME:$BUILD_NUMBER
                    '''
                }
            }
        }
    }
}
```

### Lab 8.4: Parallel Stages Execution
```groovy
stage('Parallel Integration Tests') {
    parallel {
        stage('API Tests') {
            steps {
                sh 'pytest tests/api'
            }
        }
        stage('UI Tests') {
            steps {
                sh 'pytest tests/ui'
            }
        }
    }
}
```

### Lab 8.5: Troubleshooting Pipelines
*   Check the build log console output.
*   Check thread dumps to diagnose hung builds: navigate to `Manage Jenkins` -> `System Information` -> `Thread Dumps`.

### Lab 8.6: Designing Shared Libraries
Create a directory structure in a Git repository named `pipeline-shared-library`:
```
src/
└── org/
    └── enterprise/
        └── Helper.groovy
vars/
└── buildDocker.groovy
```
Content of `vars/buildDocker.groovy`:
```groovy
def call(Map config) {
    sh "docker build -t ${config.imageName} ."
}
```
Import in Jenkinsfile:
```groovy
@Library('pipeline-shared-library@main') _
stage('Build') {
    steps {
        buildDocker(imageName: 'my-app')
    }
}
```

---

## 9. Troubleshooting Tasks

### Task 9.1: Agent Offline
*   **Symptom**: Builds are queued, displaying `is offline` or `waiting for next available executor`.
*   **Root Cause**: The agent daemon process has crashed, Java versions on controller and agent mismatch, or network ports (such as SSH) are blocked.
*   **Resolution Strategy**:
    *   Navigate to `Manage Jenkins` -> `Nodes` -> Select the offline agent -> View the log.
    *   Verify the agent can connect to the controller's TCP port:
        ```bash
        nc -zv <controller-ip> 50000
        ```
    *   Restart the agent process on the worker machine:
        ```bash
        java -jar agent.jar -jnlpUrl http://<controller-ip>:8080/computer/<agent-name>/jenkins-agent.jnlp
        ```

### Task 9.2: Pipeline Hanging in Groovy Sandbox Approvals
*   **Symptom**: Pipeline hangs at a step or fails with `org.jenkinsci.plugins.scriptsecurity.sandbox.RejectedAccessException: Scripts not permitted to use method ...`.
*   **Root Cause**: The script is using a Java/Groovy method that is blocked by Jenkins' security sandbox.
*   **Resolution Strategy**:
    *   Navigate to `Manage Jenkins` -> `In-process Script Approval`.
    *   Review the requested method call and click **Approve**.
    *   *Alternative*: Rewrite the pipeline code to use standard, sandbox-approved Jenkins pipeline DSL steps.

### Task 9.3: Disk Space Full on Controller Node
*   **Symptom**: Jenkins becomes slow, plugins fail to load, or builds fail with `No space left on device`.
*   **Root Cause**: Old build logs and workspace artifacts are filling up `$JENKINS_HOME/jobs/`.
*   **Resolution Strategy**:
    ```bash
    # 1. Check disk utilization of JENKINS_HOME
    df -h /var/jenkins_home
    
    # 2. Find the largest job directories
    du -sh /var/jenkins_home/jobs/* | sort -h
    
    # 3. Fix by configuring Build Discarder in job definitions:
    # Set "Max # of builds to keep" to 10.
    ```

---

## 10. Real Production Incidents

### Case Study: Controller Crash due to Master Builds Execution
*   **Incident**: An enterprise Jenkins controller crashed during a release. The root cause was that several resource-heavy jobs (compiling large Java applications) were configured to run on the controller node instead of agents. The controller ran out of RAM, triggered a JVM out-of-memory error, and crashed.
*   **Remediation**:
    *   Configured the controller node's executors to **0** to prevent job execution on the master.
    *   Configured memory limits on JVM startup parameters (`-Xmx8g`, `-XX:+UseG1GC`) to ensure stable memory reclamation.
    *   Migrated workloads to dynamic Kubernetes agent pods.

---

## 11. Interview Questions

### Q1: What is the difference between Declarative and Scripted pipelines in Jenkins?
*   **Answer**:
    *   **Declarative Pipelines** are structured and use a predefined syntax schema inside a `pipeline {}` block. They enforce clean separation of stages, support built-in error handling, and are easier to configure.
    *   **Scripted Pipelines** use Groovy code inside a `node {}` block. They are highly flexible and allow you to write complex logic, but are harder to maintain and debug.

### Q2: Why is it bad practice to run build steps on the Jenkins controller node?
*   **Answer**: Running builds on the controller node presents a security risk, as scripts can access the controller's file system (`JENKINS_HOME`), credentials, and private keys. It can also cause performance bottlenecks, slowing down the UI and scheduling engine.

### Q3: Explain what the `thinBackup` plugin does.
*   **Answer**: The `thinBackup` plugin automates backups of Jenkins configuration files (such as XML configurations for jobs, plugins, and credentials). It excludes heavy files like workspace directories and build history artifacts, keeping backup sizes small and recovery times fast.

### Q4: How do JNLP inbound agents differ from SSH agents?
*   **Answer**:
    *   **SSH agents**: The controller initiates a connection to the agent over SSH, copies `agent.jar`, and starts it.
    *   **JNLP inbound agents**: The agent initiates a connection to the controller over TCP. This is ideal for agents behind firewalls or inside private subnets that cannot accept inbound connections.

### Q5: How do Jenkins Shared Libraries work, and where are they stored?
*   **Answer**: Shared Libraries are written in Groovy and stored in a version-controlled Git repository. They define reusable functions and steps that can be imported into Jenkinsfiles using the `@Library` annotation, reducing duplication across pipelines.

---

## 12. Enterprise Case Studies

### Pipeline Modernization at Capital One
Capital One migrated hundreds of legacy Jenkins instances to a centralized cloud-native platform running on AWS EKS. They standardized delivery pipelines by creating common Shared Libraries and enforced compliance checks (such as static analysis and security scanning) in every build. By moving to dynamic containerized agents, they reduced VM infrastructure costs by over 40%.

---

## 13. System Design Discussions

### High-Availability Jenkins Cluster Architecture
*   **Objective**: Design a highly available, cluster-wide Jenkins platform.
*   **Architecture Considerations**:
    *   **Controller Clustering**: Run Jenkins on Kubernetes. Use a multi-master setup (via tools like CloudBees Jenkins Enterprise) or configure automated failover for a single controller instance.
    *   **Storage**: Store `$JENKINS_HOME` on a high-performance network filesystem (like AWS EFS) to ensure data is preserved if the controller pod restarts on another node.
    *   **Agent Provisioning**: Configure the Kubernetes plugin to spin up agent pods dynamically across multiple availability zones.

---

## 14. AI Platform Perspective

### Automating ML Model Promotions with Jenkins Pipelines
```groovy
pipeline {
    agent { label 'ml-agent' }
    environment {
        MODEL_REGISTRY = "s3://my-enterprise-model-store/vgg16"
    }
    stages {
        stage('Evaluate & Promote Model') {
            steps {
                sh '''
                python3 evaluate.py --model-dir ./model
                if [ $(cat evaluation_score.txt) -gt 90 ]; then
                    echo "Model passed quality checks. Uploading to production store..."
                    aws s3 cp ./model $MODEL_REGISTRY/prod/ --recursive
                else
                    echo "Model score was too low. Skipping promotion."
                    exit 1
                fi
                '''
            }
        }
    }
}
```
This integrates machine learning release tasks (such as validation, tagging, and promotion) directly into enterprise CI/CD workflows, ensuring models meet quality standards before deployment.
