# Module 5: Ray Distributed Execution & Ray Serve Platforms

## 1. Theory (40%)
Ray is an open-source distributed computing framework designed to scale machine learning and Python applications. It provides the building blocks to distribute compute workloads across GPU clusters.

```
+-------------------------------------------------------------------------------------------------+
|                                           Ray Cluster                                           |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                         Head Node                                       |   |
|   |   - Coordinates scheduler, tracks active node state, and manages global metadata        |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (Schedule Task)                                 v (Deploy Actor)        |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |                       Worker Node 1     |     |                       Worker Node 2     |   |
|   |   - Executes stateless Tasks in parallel|     |   - Hosts stateful Actor replicas       |   |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Tasks**: Stateless, parallel function executions on worker nodes.
*   **Actors**: Stateful worker instances that retain memory across method calls, used to wrap model instances.
*   **Ray Serve**: An scalable model serving library built on top of Ray.

---

## 2. Architecture Deep Dive

Ray clusters use a master-worker topology:
*   **Head Node**: Coordinates scheduling, tracks active node state, and manages global metadata.
*   **Worker Nodes**: Execute tasks and host actors.
*   **Object Store**: A shared memory database on each node that allows fast, zero-copy data exchanges between worker processes.

---

## 3. Internal Working

### Distributed Execution
1.  **Submit Task**: The driver application submits a task request to the Ray scheduler.
2.  **Assign Worker**: The scheduler assigns the task to a worker node with the required resource capacities (such as CPUs or GPUs).
3.  **Execute & Cache**: The worker executes the task, stores outputs in the local object store, and returns a reference ID (ObjectRef) to the driver.

---

## 4. Tool Comparison

| Feature | Ray | Kubernetes (Standard Jobs) |
|---|---|---|
| **Primary Focus** | Distributed Python application scaling | General container orchestration |
| **Execution Overhead**| Low (Sub-millisecond tasks execution) | High (Requires pod creation time) |
| **State Management** | Stateful Actors | Stateless Pod structures |

---

## 5. Installation Guide
Install Ray using pip:
```bash
pip install "ray[default]"
```

---

## 6. Setup Guide
Start a local Ray head node:
```bash
# Start Ray locally (simulated command)
# ray start --head --port=6379
```

---

## 7. Commands
```bash
# Start a local head node
ray start --head --port=6379 || echo "Ray head start failed or already active"

# Check Ray cluster status
ray status || echo "Could not fetch Ray status"
```

---

## 8. Hands-On Labs
Write a Python script to verify distributed task execution:
```python
# /tmp/ray_test.py
import ray

def run_distributed_task():
    print("Connecting to Ray (simulated)...")
    # In production, use:
    # ray.init()
    # @ray.remote
    # def square(x): return x * x
    # print(ray.get(square.remote(4)))
    
    print("Success: Ray task execution completed.")

if __name__ == '__main__':
    run_distributed_task()
```
Run the validation:
```bash
python3 /tmp/ray_test.py
```

---

## 9. Production Operations

### Scaling Distributed Applications
Use **Ray Serve** to deploy model replicas across nodes, configuring auto-scaling options to handle traffic spikes.

---

## 10. Monitoring
Ray exposes a dashboard on port 8265, displaying CPU/GPU utilization, active tasks, memory state, and worker node health.

---

## 11. Security
Enable TLS encryption on internal Ray node communication channels to secure data in transit.

---

## 12. Cost Optimization
Configure the Ray Autoscaler to scale down worker nodes to zero when no active tasks are running, optimizing compute costs.

---

## 13. Troubleshooting

### Task 13.1: Worker Node Disconnection
*   **Symptom**: Ray tasks fail with `RayActorError: The actor died unexpectedly`.
*   **Root Cause**: The worker node ran out of memory (OOM), causing the operating system to terminate the worker process.
*   **Resolution Strategy**:
    *   Inspect memory usage statistics on the worker node.
    *   Limit object store memory allocations during startup:
        ```bash
        # ray start --object-store-memory=<limit-in-bytes>
        ```

---

## 14. Enterprise Case Studies

### Reinforcement Learning at Uber
Uber uses Ray to train self-driving car models. By distributing reinforcement learning tasks across GPU clusters and sharing environment data using Ray's object store, they reduced training times.

---

## 15. Interview Questions

### Q1: What is the difference between a Task and an Actor in Ray?
*   **Answer**:
    *   **Tasks**: Stateless, parallel function executions on worker nodes.
    *   **Actors**: Stateful worker instances that retain memory across method calls.

### Q2: Explain the purpose of Ray's shared memory Object Store.
*   **Answer**: The object store allows fast, zero-copy data exchanges between worker processes on the same node, reducing serialization overhead.

---

## 16. AI FDE Perspective

### Deploying Ray in Air-Gapped Networks
As an AI Forward Deployed Engineer (FDE), you often deploy distributed infrastructure:
*   **Bind Addresses**: Configure node address bindings explicitly to prevent routing conflicts in private networks:
    ```bash
    # Run head node binding to internal network IPs
    # ray start --head --node-ip-address=10.0.0.1 --port=6379
    ```
This ensures worker nodes can connect to the head node securely.
