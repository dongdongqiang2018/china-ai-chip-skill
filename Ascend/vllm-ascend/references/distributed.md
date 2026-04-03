# vLLM-Ascend Distributed Inference Guide

This guide covers distributed inference configuration for vLLM-Ascend, including tensor parallelism, pipeline parallelism, and multi-node deployment.

---

## Table of Contents

1. [Tensor Parallelism](#tensor-parallelism)
2. [Pipeline Parallelism](#pipeline-parallelism)
3. [Multi-Node Deployment](#multi-node-deployment)
4. [Network Verification](#network-verification)

---

## Tensor Parallelism

Tensor parallelism (TP) splits individual layers across multiple NPUs. Each NPU processes a portion of the tensor operations, and results are synchronized via collective communication.

### Configuration

Use the `--tensor-parallel-size` (or `-tp`) argument to specify the number of NPUs for tensor parallelism.

```bash
# Single node with 8 NPUs
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --device ascend
```

### Atlas A2 vs A3 Hardware Differences

| Feature | Atlas A2 | Atlas A3 |
|---------|----------|----------|
| NPUs per Node | 8 (device IDs 0-7) | 16 (device IDs 0-15) |
| Max TP Size (Single Node) | 8 | 16 |
| Memory per NPU | 64 GB HBM | 64 GB HBM |
| Recommended TP | 4 or 8 | 8 or 16 |

**Atlas A2 Configuration (8 NPUs):**
```bash
# Use all 8 NPUs for large models
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --device ascend \
    --max-model-len 32768

# Use 4 NPUs for medium models (better throughput)
vllm serve /path/to/model \
    --tensor-parallel-size 4 \
    --device ascend \
    --max-model-len 32768
```

**Atlas A3 Configuration (16 NPUs):**
```bash
# Use all 16 NPUs for very large models
vllm serve /path/to/model \
    --tensor-parallel-size 16 \
    --device ascend \
    --max-model-len 65536

# Use 8 NPUs for balanced performance
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --device ascend \
    --max-model-len 32768
```

### Tensor Parallelism with Ray

For multi-node tensor parallelism, vLLM-Ascend uses Ray for distributed coordination.

**Head Node Setup:**
```bash
# Start Ray head node
ray start --head --port=6379

# Launch vLLM with Ray
vllm serve /path/to/model \
    --tensor-parallel-size 16 \
    --device ascend \
    --distributed-executor-backend ray
```

**Worker Node Setup:**
```bash
# Connect to Ray head
ray start --address="head-node-ip:6379"
```

### Example Commands by Model Size

**Small Models (7B-13B):**
```bash
# Single NPU is usually sufficient
vllm serve /path/to/model \
    --tensor-parallel-size 1 \
    --device ascend

# Use TP=2 for higher batch sizes
vllm serve /path/to/model \
    --tensor-parallel-size 2 \
    --device ascend
```

**Medium Models (30B-70B):**
```bash
# Atlas A2: Use 4-8 NPUs
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --device ascend

# Atlas A3: Use 8 NPUs
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --device ascend
```

**Large Models (100B+):**
```bash
# Requires multi-node setup
vllm serve /path/to/model \
    --tensor-parallel-size 16 \
    --pipeline-parallel-size 2 \
    --device ascend \
    --distributed-executor-backend ray
```

---

## Pipeline Parallelism

Pipeline parallelism (PP) splits model layers across multiple NPUs or nodes. Each NPU processes a subset of layers, and activations are passed between stages.

### Configuration

Use the `--pipeline-parallel-size` (or `-pp`) argument with `--tensor-parallel-size`:

```bash
# 2 pipeline stages, each with 8-way tensor parallelism
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --device ascend
```

### Combined Parallelism Strategy

The total number of NPUs required is `TP * PP`.

| Configuration | TP | PP | Total NPUs | Use Case |
|---------------|----|----|------------|----------|
| Small Model | 4 | 1 | 4 | 7B-13B models |
| Medium Model | 8 | 1 | 8 | 30B-70B models on A2 |
| Large Model | 8 | 2 | 16 | 100B+ models on A2 |
| Very Large | 16 | 2 | 32 | 200B+ models on A3 |

### Example Commands

**Single Node Pipeline Parallelism (Atlas A3):**
```bash
# Split 16 NPUs into 2 pipeline stages of 8 TP each
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --device ascend
```

**Multi-Node Pipeline Parallelism:**
```bash
# 2 nodes, each with 8 NPUs
# Node 1 handles pipeline stage 0
# Node 2 handles pipeline stage 1
vllm serve /path/to/model \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --device ascend \
    --distributed-executor-backend ray
```

**Optimal Configuration for Common Models:**

```bash
# Qwen2.5-72B on Atlas A2 (2 nodes)
vllm serve Qwen/Qwen2.5-72B \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --device ascend \
    --max-model-len 32768

# DeepSeek-V3 on Atlas A3 (2 nodes)
vllm serve deepseek-ai/DeepSeek-V3 \
    --tensor-parallel-size 16 \
    --pipeline-parallel-size 2 \
    --device ascend \
    --max-model-len 65536
```

### Performance Considerations

1. **Communication Overhead**: Pipeline parallelism has higher communication overhead than tensor parallelism. Minimize pipeline stages if possible.

2. **Micro-Batching**: vLLM automatically handles micro-batching to keep all pipeline stages busy.

3. **Memory Usage**: Pipeline parallelism reduces per-NPU memory usage more effectively than tensor parallelism.

---

## Multi-Node Deployment

Multi-node deployment extends inference across multiple physical servers, enabling support for very large models.

### Network Requirements

**Minimum Requirements:**
- RDMA-capable network (RoCE v2 or InfiniBand)
- Minimum 100 Gbps bandwidth between nodes
- Sub-10 microsecond latency

**Recommended Configuration:**
- 200 Gbps or higher bandwidth
- Dual-port NICs for redundancy
- Dedicated network for NPU communication

**Network Topology:**
```
Node 1                    Node 2
┌─────────┐              ┌─────────┐
│ NPU 0-7 │◄────────────►│ NPU 0-7 │
│ (TP=8)  │   RoCE/IB    │ (TP=8)  │
└─────────┘              └─────────┘
   ▲                          ▲
   └──────── Pipeline ─────────┘
```

### Docker Configuration

**Node 1 (Head Node):**
```bash
docker run -d --name vllm-head \
    --network host \
    --privileged \
    --device /dev/davinci0 \
    --device /dev/davinci1 \
    --device /dev/davinci2 \
    --device /dev/davinci3 \
    --device /dev/davinci4 \
    --device /dev/davinci5 \
    --device /dev/davinci6 \
    --device /dev/davinci7 \
    --device /dev/davinci_manager \
    --device /dev/devmm_svm \
    --device /dev/hisi_hdc \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver:ro \
    -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware:ro \
    -v /path/to/model:/model:ro \
    -e ASCEND_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
    -p 6379:6379 \
    -p 8000:8000 \
    vllm-ascend:latest
```

**Node 2 (Worker Node):**
```bash
docker run -d --name vllm-worker \
    --network host \
    --privileged \
    --device /dev/davinci0 \
    --device /dev/davinci1 \
    --device /dev/davinci2 \
    --device /dev/davinci3 \
    --device /dev/davinci4 \
    --device /dev/davinci5 \
    --device /dev/davinci6 \
    --device /dev/davinci7 \
    --device /dev/davinci_manager \
    --device /dev/devmm_svm \
    --device /dev/hisi_hdc \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver:ro \
    -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware:ro \
    -v /path/to/model:/model:ro \
    -e ASCEND_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
    vllm-ascend:latest
```

### Hostfile Setup

Create a hostfile for multi-node coordination:

**~/vllm-hosts.txt:**
```
192.168.1.10 slots=8
192.168.1.11 slots=8
```

Each line specifies:
- IP address of the node
- Number of NPUs (slots) available on that node

### Multi-Node Launch Process

**Step 1: Start Ray on Head Node**
```bash
# Inside head node container
ray start --head --port=6379 --dashboard-host=0.0.0.0
```

**Step 2: Connect Worker Nodes**
```bash
# Inside worker node container
ray start --address="192.168.1.10:6379"
```

**Step 3: Verify Ray Cluster**
```bash
# On head node
ray status

# Expected output:
# Node status
# -------------------------------------------------------------
# 1 node(s) with resources: ...
# 1 node(s) with resources: ...
```

**Step 4: Launch vLLM Service**
```bash
# On head node only
vllm serve /model \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --device ascend \
    --distributed-executor-backend ray \
    --host 0.0.0.0 \
    --port 8000
```

### Environment Variables

Set these environment variables on all nodes:

```bash
# CANN environment
source /usr/local/Ascend/ascend-toolkit/set_env.sh

# HCCL configuration
export HCCL_SOCKET_FAMILY=AF_INET
export HCCL_CONNECT_TIMEOUT=600
export HCCL_EXEC_TIMEOUT=600

# For multi-node RDMA
export HCCL_RDMA_ENABLE=1
export HCCL_RDMA_DEVICE=mlx5_0

# Debug (optional)
export HCCL_DEBUG=INFO
```

---

## Network Verification

Before running distributed inference, verify network connectivity between nodes.

### hccn_tool Commands

The `hccn_tool` utility diagnoses NPU network interfaces.

**Check NPU Network Status:**
```bash
# Show all NPU network interfaces
hccn_tool -i 0 -nethealth
hccn_tool -i 1 -nethealth
hccn_tool -i 2 -nethealth
hccn_tool -i 3 -nethealth
hccn_tool -i 4 -nethealth
hccn_tool -i 5 -nethealth
hccn_tool -i 6 -nethealth
hccn_tool -i 7 -nethealth
```

**Check Link Status:**
```bash
# Check physical link status for all NPUs
for i in {0..7}; do
    echo "=== NPU $i ==="
    hccn_tool -i $i -link
    hccn_tool -i $i -speed
done
```

**Verify IP Configuration:**
```bash
# Check IP addresses assigned to NPU interfaces
hccn_tool -i 0 -ip -g
```

### PING Tests

Test connectivity between nodes using NPU network interfaces.

**Basic Connectivity:**
```bash
# From Node 1: Ping Node 2 NPU IPs
ping 192.168.100.10  # Node 2 NPU 0
ping 192.168.100.11  # Node 2 NPU 1
```

**All-to-All Test Script:**
```bash
#!/bin/bash
# network-test.sh - Run on all nodes

NODE_IPS=("192.168.100.10" "192.168.100.20")
NPU_IPS=("192.168.101.10" "192.168.101.11" "192.168.101.12" "192.168.101.13"
         "192.168.101.14" "192.168.101.15" "192.168.101.16" "192.168.101.17")

echo "Testing NPU network connectivity..."
for ip in "${NPU_IPS[@]}"; do
    if ping -c 3 -W 2 "$ip" > /dev/null 2>&1; then
        echo "✓ $ip reachable"
    else
        echo "✗ $ip unreachable"
    fi
done
```

### HCCL Communication Test

Use the HCCL test utility to verify collective communication.

**Run HCCL Bandwidth Test:**
```bash
# On all nodes, run simultaneously
mpirun --hostfile ~/vllm-hosts.txt \
    -x LD_LIBRARY_PATH \
    -x ASCEND_VISIBLE_DEVICES \
    -x HCCL_SOCKET_FAMILY \
    ./hccl_test -b 8M -e 1G -f 2 -t all_reduce
```

**Expected Bandwidth:**
- Intra-node (same server): 200+ GB/s
- Inter-node (RDMA): 80-100 Gbps
- Inter-node (TCP): 10-25 Gbps

### Troubleshooting Network Issues

**Issue: HCCL timeout errors**
```
# Solution: Increase timeout values
export HCCL_CONNECT_TIMEOUT=1200
export HCCL_EXEC_TIMEOUT=1200
```

**Issue: Low inter-node bandwidth**
```bash
# Check RDMA is enabled
ibstat | grep -A 5 "State"

# Should show: State: Active
# If not, check cable connections and subnet manager
```

**Issue: NPU network interface down**
```bash
# Reset NPU network
hccn_tool -i 0 -reset

# Or restart Ascend driver
/usr/local/Ascend/driver/tools/ascend_toolkit restart
```

**Issue: Firewall blocking communication**
```bash
# Open required ports
sudo firewall-cmd --add-port=6379/tcp   # Ray
sudo firewall-cmd --add-port=8000/tcp   # vLLM API
sudo firewall-cmd --add-port=10001/tcp  # HCCL
sudo firewall-cmd --reload
```

---

## Quick Reference

### Command Summary

| Task | Command |
|------|---------|
| TP only | `vllm serve model --tp 8 --device ascend` |
| TP + PP | `vllm serve model --tp 8 --pp 2 --device ascend` |
| Multi-node | `vllm serve model --tp 8 --pp 2 --device ascend --distributed-executor-backend ray` |
| Check network | `hccn_tool -i 0 -nethealth` |
| Test connectivity | `ping <npu-ip>` |

### Common Configurations

**Atlas A2 Single Node (8 NPUs):**
```bash
vllm serve /model --tensor-parallel-size 8 --device ascend
```

**Atlas A3 Single Node (16 NPUs):**
```bash
vllm serve /model --tensor-parallel-size 16 --device ascend
```

**Atlas A2 Multi-Node (16 NPUs across 2 nodes):**
```bash
vllm serve /model --tensor-parallel-size 8 --pipeline-parallel-size 2 --device ascend --distributed-executor-backend ray
```

---

## Official References

- [vLLM-Ascend Multi-Node Deployment](https://docs.vllm.ai/projects/ascend/en/latest/installation.html#multi-node-deployment)
- [HCCL User Guide](https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/aiopsdevg/acedg/aceug_0001.html)
- [Ascend NPU Network Configuration](https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/envdeployment/instg/instg_0045.html)
