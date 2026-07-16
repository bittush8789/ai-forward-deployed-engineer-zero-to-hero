# Module 1: Linux Administration & Systems Engineering

## 1. Architecture Deep Dive

The Linux operating system architecture is split into two primary execution modes: **Kernel Space** and **User Space**. This separation enforces stability, security, and hardware abstraction.

```
+-----------------------------------------------------------------------+
|                              User Space                               |
|   +------------------+  +-------------------+  +------------------+   |
|   |   Applications   |  |   System Daemons  |  |      Shell       |   |
|   +--------+---------+  +---------+---------+  +--------+---------+   |
|            |                      |                     |             |
|            +----------------------+---------------------+             |
|                                   |                                   |
|                                   v                                   |
|                          GNU C Library (glibc)                        |
|                                   |                                   |
|                                   v (System Calls: open, fork, write) |
+-----------------------------------------------------------------------+
|                              Kernel Space                             |
|   +---------------------------------------------------------------+   |
|   |                         System Calls Interface                |   |
|   +---------------------------------------------------------------+   |
|   |  Process Mgmt  |  Memory Mgmt  | File Systems | Network Stack |   |
|   |   (Scheduler)  |  (VMA, MMU)   | (VFS, ext4)  |  (Sockets)    |   |
|   +---------------------------------------------------------------+   |
|   |                        Device Drivers                         |   |
+-----------------------------------------------------------------------+
|                                Hardware                               |
|              CPU (Cores, MMU) | Memory (RAM) | I/O Devices             |
+-----------------------------------------------------------------------+
```

### Kernel Space vs. User Space
*   **Kernel Space**: The core of the OS. It has unrestricted access to the CPU, system memory, and hardware devices. It runs in Ring 0 (the most privileged execution ring on x86 architectures).
*   **User Space**: Where user applications, libraries, and system daemons run. It runs in Ring 3 (restricted privilege). User space programs must ask the kernel to perform hardware operations on their behalf using **System Calls (syscalls)**.

### The System Call Interface (SCI)
When a program needs to read a file, it does not access the hard drive directly. Instead:
1.  The application calls a wrapper function in `glibc` (e.g., `read()`).
2.  `glibc` places the syscall number and arguments in CPU registers and executes a software interrupt or assembly instruction (like `syscall` on x86_64).
3.  The CPU switches to Ring 0 (Kernel Space), locates the syscall handler in the interrupt vector table, executes the kernel code, and returns execution back to Ring 3.

### Systemd Startup Sequence
Modern Linux systems use `systemd` as their init system (PID 1). The boot process follows this sequence:
1.  **BIOS/UEFI**: Performs Power-On Self-Test (POST) and initializes hardware.
2.  **Bootloader (GRUB2)**: Loads the Linux kernel and `initramfs` (initial RAM filesystem) into memory.
3.  **Kernel Initialization**: Initializes drivers, mounts the root filesystem as read-only, and executes `/sbin/init` (which points to `systemd`).
4.  **systemd Initialization**:
    *   Reads `/etc/systemd/system/` and `/lib/systemd/system/`.
    *   Identifies the target (e.g., `multi-user.target` or `graphical.target`).
    *   Spawns services in parallel using dependency graph processing.
    *   Mounts filesystems specified in `/etc/fstab`.

### Filesystem Hierarchy Standard (FHS)
*   `/bin` & `/sbin`: Critical system binaries.
*   `/boot`: Kernel images, initrd, and boot configuration.
*   `/dev`: Device files representing physical or virtual hardware (e.g., `/dev/sda`, `/dev/null`).
*   `/etc`: Host-specific system-wide configuration files.
*   `/proc` & `/sys`: Pseudo-filesystems representing kernel data structures and hardware status.
*   `/var`: Variable data files (logs, caches, databases).
*   `/usr`: User binaries, libraries, and documentation.

---

## 2. Internal Working

### Process Lifecycle & Scheduling
Linux processes are created using the `fork()` and `execve()` system calls:
*   **`fork()`**: Clones the calling process, creating a child process with a new PID. To optimize memory, Linux uses **Copy-on-Write (COW)**: the child shares the parent's memory pages until one of them attempts to modify a page, at which point the kernel duplicates that specific page.
*   **`execve()`**: Replaces the current process image with a new binary (e.g., loading an AI training script).
*   **Scheduler (Completely Fair Scheduler - CFS)**: CFS manages CPU allocation. It models an "ideal multi-tasking CPU" on hardware using a Red-Black Tree. Processes are ordered by `vruntime` (virtual runtime). The process with the lowest `vruntime` is selected next. Nice values (-20 to 19) scale the rate at which `vruntime` accumulates.

### Memory Management & Virtual Memory
*   **Virtual Memory**: Each process runs in its own virtual address space, mapped to physical memory pages by the CPU's Memory Management Unit (MMU) using page tables.
*   **Swap Space**: Page frames can be paged out to disk (Swap) when physical RAM is exhausted.
*   **Out-Of-Memory (OOM) Killer**: When the system runs completely out of memory and cannot swap, the kernel invokes the OOM Killer. It computes an `oom_score` for each process based on memory usage, process lifetime, and `oom_score_adj`. The process with the highest score is terminated (`SIGKILL`) to protect system stability.

### The Linux Networking Stack & Netfilter
1.  **Ingress**: The Network Interface Card (NIC) receives an Ethernet frame, copies it to ring buffers in RAM via DMA, and triggers a hardware interrupt.
2.  **SoftIRQ**: The kernel schedules a software interrupt (`NET_RX_SOFTIRQ`) to parse the packet (IP, TCP/UDP headers).
3.  **Socket Buffer (`sk_buff`)**: The data structure representing a packet as it travels up the stack to user-space socket descriptors.
4.  **Netfilter**: The kernel subsystem providing hooks at various stages of packet processing (Prerouting, Input, Forward, Output, Postrouting). Systems like `iptables`, `nftables`, and `ufw` use these hooks to inspect, modify, or drop packets.

---

## 3. Production Use Cases

### High-Performance AI Training Node VM Setup
AI training workloads saturate GPU bandwidth, PCIe lanes, RAM, and network interfaces.
*   **HugePages Config**: Standard Linux pages are 4KB. For large-memory databases or AI workloads (e.g., vector search), configuring HugePages (2MB or 1GB) reduces translation lookaside buffer (TLB) misses:
    ```bash
    # Allocate 1024 hugepages of 2MB size dynamically
    sudo sysctl -w vm.nr_hugepages=1024
    ```
*   **Sysctl Tuning**: Network buffers must handle high throughput (e.g., 100GbE RoCEv2 networks):
    ```ini
    # /etc/sysctl.d/99-ai-platform.conf
    net.core.rmem_max = 134217728
    net.core.wmem_max = 134217728
    net.ipv4.tcp_rmem = 4096 87380 134217728
    net.ipv4.tcp_wmem = 4096 65536 134217728
    fs.file-max = 2097152
    vm.max_map_count = 262144
    ```

### LVM Provisioning for AI Model Cache Directories
Models are hundreds of gigabytes. Storage must expand dynamically.
*   Physical Volumes (PV) abstract the raw disk.
*   Volume Groups (VG) pool PVs.
*   Logical Volumes (LV) act as virtual partitions that can be resized on-the-fly without data loss.

---

## 4. Security Best Practices

### SSH Hardening
To secure servers against automated brute-force attacks, edit `/etc/ssh/sshd_config`:
```ini
Port 2222
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers devops admin
```
Apply rules:
```bash
sudo sshd -t && sudo systemctl restart ssh
```

### Auditd Configuration
Track unauthorized directory access or execution of administrative commands by editing `/etc/audit/rules.d/audit.rules`:
```properties
# Monitor execution of the execve system call by root
-a always,exit -F arch=b64 -S execve -F euid=0 -k admin_execution
# Monitor changes to SSH configuration
-w /etc/ssh/sshd_config -p wa -k sshd_config_changes
```
Reload config: `sudo augenrules --load`

---

## 5. Scalability Patterns

### Control Groups (cgroups v2)
In multi-tenant AI systems, cgroups prevent a single noisy neighbor container from starving others of resources.
To set resource boundaries directly:
```bash
# Create a control group
sudo mkdir /sys/fs/cgroup/ai_workload
# Limit max memory to 4GB
echo "4294967296" | sudo tee /sys/fs/cgroup/ai_workload/memory.max
# Limit CPU shares to 2 cores (expressed as microseconds of CPU run time per 100ms period)
echo "200000 100000" | sudo tee /sys/fs/cgroup/ai_workload/cpu.max
```

### CPU Pinning (NUMA Node Binding)
For low-latency LLM inference, processes should run on the CPU core closest to the memory controller holding their weights:
```bash
# Pin process to CPU cores 0-7 and NUMA memory node 0
numactl --physcpubind=0-7 --membind=0 python3 inference.py --model-path /models/llama
```

---

## 6. Reliability Patterns

### Systemd Service Restart Policies & Watchdogs
Create resilient daemon processes by leveraging systemd's built-in watchdog protocol:
```ini
[Unit]
Description=AI Inference Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /app/inference_service.py
Restart=always
RestartSec=5s
# If process does not ping systemd within 10s, systemd kills and restarts it
WatchdogSec=10
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

### Journald Disk Utilization Control
Prevent logs from filling up the root partition by editing `/etc/systemd/journald.conf`:
```ini
[Journal]
Storage=persistent
Compress=yes
SystemMaxUse=5G
SystemMaxFileSize=500M
```
Apply: `sudo systemctl restart systemd-journald`

---

## 7. Cost Optimization

### Tuning CPU Scaling Governors
Cloud servers often default to conservative CPU scaling. For batch workloads, use `performance`. For idle dev environments, use `powersave` or `ondemand`:
```bash
# Set all CPUs to performance mode
echo "performance" | sudo tee /sys/fs/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### Cache & Memory Optimization
*   Use NVMe-backed swap with low swappiness (`vm.swappiness=10`) rather than expensive RAM upgrades if workloads contain large, cold objects.
*   Run cleanups periodically to reclaim page cache memory:
    ```bash
    # Clean pagecache, dentries, and inodes
    sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
    ```

---

## 8. Hands-On Labs

### Lab 8.1: Creating Users, Groups, and ACLs
We will create a developer workspace with fine-grained access.
```bash
# 1. Create group and users
sudo groupadd mlops
sudo useradd -m -g mlops -s /bin/bash engineer1
sudo useradd -m -s /bin/bash auditor1

# 2. Create target directory
sudo mkdir -p /opt/model_store
sudo chown -R root:mlops /opt/model_store
sudo chmod 2770 /opt/model_store # SetGID ensures new files inherit group 'mlops'

# 3. Set Posix ACL to allow read-only access to auditor1
sudo setfacl -m u:auditor1:rx /opt/model_store
# Verify ACL permissions
getfacl /opt/model_store
```

### Lab 8.2: Troubleshooting Processes with strace & lsof
Find out what files a process is accessing or why it's hanging.
```bash
# Find the PID of target process (e.g., python3)
PID=$(pgrep -f python3 | head -n 1)

# Tracing system calls in real-time (filtering open and write)
sudo strace -p $PID -e trace=openat,write,read

# List all open files and TCP sockets used by the process
sudo lsof -p $PID
sudo lsof -i :8080
```

### Lab 8.3: Custom Systemd Unit Configuration
```bash
# 1. Create a dummy daemon script
cat << 'EOF' > /tmp/dummy_service.py
import time, sys
print("Dummy service started...", flush=True)
while True:
    time.sleep(1)
EOF
sudo mv /tmp/dummy_service.py /usr/local/bin/dummy_service.py

# 2. Create the systemd service file
sudo bash -c "cat << 'EOF' > /etc/systemd/system/dummy.service
[Unit]
Description=Dummy System Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/dummy_service.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF"

# 3. Reload, start, and enable
sudo systemctl daemon-reload
sudo systemctl enable --now dummy.service
sudo systemctl status dummy.service
```

### Lab 8.4: Journald Log Mining
```bash
# Show log entries for dummy service in real-time
journalctl -u dummy.service -f

# Filter logs since 1 hour ago with critical priority or higher
journalctl -p err..emerg --since "1h ago"

# View logs inside a specific boot ID
journalctl -b 0 --no-pager | tail -n 50
```

### Lab 8.5: LVM Disk Partitioning & Mounting
```bash
# NOTE: Replace loop0 with an actual unused block device or create a loopback file for practice
dd if=/dev/zero of=/tmp/lvm_test.img bs=1M count=500
sudo losetup /dev/loop99 /tmp/lvm_test.img

# 1. Create Physical Volume (PV)
sudo pvcreate /dev/loop99

# 2. Create Volume Group (VG)
sudo vgcreate vg_data /dev/loop99

# 3. Create Logical Volume (LV)
sudo lvcreate -n lv_models -L 400M vg_data

# 4. Format with EXT4 filesystem
sudo mkfs.ext4 /dev/vg_data/lv_models

# 5. Persistent mount in /etc/fstab
sudo mkdir -p /mnt/models
echo "/dev/mapper/vg_data-lv_models /mnt/models ext4 defaults 0 2" | sudo tee -a /etc/fstab
sudo mount -a

# Verify mount
df -h | grep models
```

### Lab 8.6: Network Troubleshooting & Socket Analysis
```bash
# 1. Check network configuration and routes
ip address show
ip route show

# 2. Find listening ports and associated PIDs
sudo ss -tlnp

# 3. Capture traffic on port 8080 (simulated web application traffic)
sudo tcpdump -i any port 8080 -nn -vv -c 10

# 4. Test port accessibility
nc -zv localhost 8080
```

### Lab 8.7: SSH Hardening Implementation
```bash
# Hardening commands script
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl restart sshd
```

### Lab 8.8: Cron-Based Monitoring System
Set up a disk usage check script.
```bash
# 1. Create shell monitoring script
cat << 'EOF' > /tmp/disk_monitor.sh
#!/usr/bin/env bash
THRESHOLD=90
USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "CRITICAL: Root partition space at ${USAGE}%" | logger -t disk_monitor
fi
EOF
sudo chmod +x /tmp/disk_monitor.sh
sudo mv /tmp/disk_monitor.sh /usr/local/bin/disk_monitor.sh

# 2. Configure system crontab (run every 10 minutes)
(crontab -l 2>/dev/null; echo "*/10 * * * * /usr/local/bin/disk_monitor.sh") | crontab -
```

---

## 9. Troubleshooting Tasks

### Task 9.1: The Phantom Disk Space Drain
*   **Symptom**: `df -h` reports `/` filesystem is 100% full, but running `du -sh /*` accounts for only a fraction of the disk usage.
*   **Root Cause**: A process has opened a large file (e.g., a service output log), and another process deleted the file. Linux will keep the disk blocks allocated until the file descriptor is closed by the owning process.
*   **Resolution Strategy**:
    ```bash
    # 1. Find deleted but open files
    sudo lsof | grep deleted
    
    # 2. Identify the PID holding the file open (e.g., PID 1234)
    # 3. Safely release space without rebooting the application by truncating the file descriptor:
    sudo sh -c 'echo > /proc/1234/fd/1'
    # Or reload the service to close the file descriptor:
    sudo systemctl reload nginx
    ```

### Task 9.2: System Load Average High, CPU Idle
*   **Symptom**: `uptime` shows load average > 20 on a 4-core VM, but CPU utilization (`top` or `vmstat`) reports 95% idle.
*   **Root Cause**: Load average in Linux counts processes running, processes waiting for CPU, AND processes blocked in uninterruptible disk I/O (D-state processes).
*   **Resolution Strategy**:
    ```bash
    # 1. Check process states using ps
    ps aux | awk '{print $8, $11}' | grep -E "^D"
    
    # 2. Inspect kernel stacks to see what system call the process is blocked on:
    sudo cat /proc/$(pgrep -d ',' -f process_name)/stack
    
    # 3. Check disk metrics for I/O bottlenecks
    iostat -x 1 5
    ```

### Task 9.3: Mysteriously Disappearing Service
*   **Symptom**: An AI model script training overnight exits with code `137` but leaves no stack trace in stdout/stderr.
*   **Root Cause**: Exit code `137` corresponds to `SIGKILL` (128 + 9). The Linux kernel Out-Of-Memory (OOM) killer terminated the process.
*   **Resolution Strategy**:
    ```bash
    # 1. Check system logs for OOM invocation
    dmesg -T | grep -i -E 'oom-killer|killed process'
    # Or search system journal
    journalctl -k --since "24h ago" | grep -i "oom"
    
    # 2. Mitigate by optimizing python memory consumption or modifying oom score adjustment:
    echo "-1000" | sudo tee /proc/$(pgrep -f train.py)/oom_score_adj
    ```

---

## 10. Real Production Incidents

### Case Study: Socket Exhaustion on AI Gateway
*   **Incident**: An API Gateway acting as a proxy to multiple Triton Inference Servers began dropping connections and throwing `502 Bad Gateway` errors under peak traffic.
*   **Diagnostic Phase**:
    *   Running `ss -s` showed over 60,000 TCP sockets in `TIME_WAIT` state.
    *   Kernel logs displayed: `kernel: TCP: time wait bucket table overflow`.
    *   The OS had run out of ephemeral ports because TCP connections were being opened and closed rapidly without recycling sockets.
*   **Remediation**:
    *   Enabled TCP time-wait reuse:
        ```bash
        sudo sysctl -w net.ipv4.tcp_tw_reuse=1
        sudo sysctl -p
        ```
    *   Configured the API Gateway connection pool to use **persistent connections (HTTP Keep-Alive)** to reuse underlying TCP sockets instead of initiating a new handshake for every single inference request.

---

## 11. Interview Questions

### Q1: What is the difference between a Hard Link and a Soft Link (Symlink)?
*   **Answer**:
    *   **Hard Link**: Direct pointer to the file's **inode**. It shares the exact same inode number as the original file. If you delete the original file, the hard link still works because the underlying data is only deleted when the link count reaches 0. Hard links cannot cross filesystem boundaries or link to directories.
    *   **Soft Link**: A separate file containing the path string to the target file (like a shortcut). It has a unique inode number. If the original file is deleted, the symlink breaks ("dangling link"). Symlinks can cross filesystems and point to directories.

### Q2: What do the three numbers in the Load Average represent, and how do you interpret them?
*   **Answer**: The three numbers represent the exponential moving average of system load over the past **1 minute**, **5 minutes**, and **15 minutes**.
    *   System load is defined as the number of running, runnable (waiting for CPU), and uninterruptible (waiting for disk I/O) processes.
    *   To interpret: Divide the load numbers by the number of CPU cores. A load average of 8.0 on a 4-core machine means the system is overloaded by 200% (queue length of 4). A load of 8.0 on a 32-core machine means the system is 75% idle.

### Q3: Explain the difference between `SIGTERM` (15) and `SIGKILL` (9).
*   **Answer**:
    *   `SIGTERM` (15) is the default termination signal. It is sent to a process to request a clean shutdown. The process can catch, handle, or ignore this signal, allowing it to close open database connections, flush write buffers, and clean up temporary files.
    *   `SIGKILL` (9) is sent directly to the kernel scheduler to terminate the process immediately. The process cannot catch, block, or handle `SIGKILL`. It must be used as a last resort, as it can cause data corruption.

### Q4: How does a zombie process occur, and how do you clean it up?
*   **Answer**: A zombie process is a process that has completed execution (via `exit()`) but still has an entry in the system process table. This entry is kept so the parent process can read the child's exit status using `wait()`.
    *   **Occurrence**: The parent process fails to call `wait()` after the child exits (due to poor programming or crash).
    *   **Cleanup**: You cannot kill a zombie process using `kill -9` because it is already dead. You must kill the *parent* process. Once the parent dies, the init process (PID 1) inherits the zombie child and immediately calls `wait()` to reap it.

### Q5: What is the Linux Page Cache, and how does the kernel manage memory reclamation?
*   **Answer**: The Page Cache is a kernel memory structure containing copies of pages stored on disk. It speeds up file I/O operations by satisfying reads from RAM.
    *   When application memory requirements increase, the kernel reclaims memory by freeing clean pages in the Page Cache.
    *   If dirty pages (modified files not yet synced to disk) must be reclaimed, the kernel schedules `pdflush` or `kswapd` to write the data to disk before freeing the pages.
    *   Kernel behavior is controlled by `vm.swappiness`: higher values swap out process anonymous memory, lower values reclaim page cache.

---

## 12. Enterprise Case Studies

### Kernel Tuning at Netflix
Netflix serves massive amounts of network traffic (accounting for over 15% of global internet traffic). To run FreeBSD and Linux edge nodes at 100Gbps+ speeds, Netflix engineers tuned the network sub-system of the OS kernel.
*   **Network Buffer Tuning**: Default TCP buffers (typically 4MB max) restrict window scaling over long distances. Netflix tuned TCP read/write buffers up to 128MB.
*   **Asynchronous I/O and Zero-Copy**: They utilized the `sendfile()` system call, which allows transferring files directly from the page cache to the network socket buffer. This bypasses copying the data into user space, eliminating CPU cache thrashing and memory context switches.

---

## 13. System Design Discussions

### Multi-Tenant AI Bare-Metal Infrastructure Design
*   **Objective**: Design a multi-tenant physical Linux cluster where different teams execute GPU training jobs.
*   **Key Isolation Layers**:
    *   **Compute/Memory**: Utilize cgroups v2 to isolate cores and set high-limit memory caps. Assign physical NUMA nodes to specific workloads using tasksets.
    *   **Storage**: Provision distinct LVM volumes for each team, with thin provisioning and storage quotas. Mount with project quotas enabled (`prjquota`).
    *   **Network**: Leverage Linux Network Namespaces combined with VLAN interfaces to separate traffic. Apply IPtables rules to restrict inter-tenant communication.
    *   **Security**: Implement AppArmor profiles to restrict access to system configuration files and lock down system call usage (e.g., blocking `ptrace`, kernel module loads).

---

## 14. AI Platform Perspective

### NVIDIA GPU Drivers & container-toolkit Orchestration
To deploy containerized deep learning workloads, the underlying Linux OS must interface cleanly with the GPU hardware.

```
+-------------------------------------------------------------+
|                     Docker/K8s Container                    |
|          +---------------------------------------+          |
|          |     PyTorch / CUDA-compiled App       |          |
|          +-------------------|-------------------+          |
+------------------------------|------------------------------+
                               | (CUDA API Calls)
+------------------------------v------------------------------+
|                        Host Linux OS                        |
|   +-----------------------------------------------------+   |
|   |            libnvidia-container.so / CLI             |   |
|   +--------------------------|--------------------------+   |
|   |            NVIDIA Kernel Module (nvidia.ko)         |   |
|   +--------------------------|--------------------------+   |
|   |            NVIDIA Container Toolkit Socket          |   |
+------------------------------|------------------------------+
                               v (PCIe / NVLink)
+-------------------------------------------------------------+
|                      Physical Hardware                      |
|                  NVIDIA H100 / A100 GPU                     |
+-------------------------------------------------------------+
```

1.  **NVIDIA Kernel Module**: The host Linux kernel must load `nvidia.ko` and `nvidia-uvm.ko`. These drivers handle memory management and hardware scheduling on the GPU.
2.  **Device Nodes**: The driver creates special device files in `/dev`:
    *   `/dev/nvidiactl` (Control node)
    *   `/dev/nvidia-uvm` (Unified memory management)
    *   `/dev/nvidia0` (Individual physical GPU)
3.  **NVIDIA Container Toolkit**: Modifies the Docker run step. When a user requests a container with GPU access (`--gpus all`), the toolkit injects the physical device files (`/dev/nvidia*`) and host driver libraries (like `libcuda.so`) directly into the container's namespaces before starting it, allowing the containerized PyTorch code to speak directly to the GPU hardware.
