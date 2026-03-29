---
name: succl
description: 壁仞（BIREN）suCCL 通信库配置与测试 Skill，提供单机多卡、多机分布式训练的通信库配置、环境变量优化、性能测试和问题诊断能力。suCCL 兼容 NCCL 接口，是壁仞 GPU 集群进行 AI 训练的核心通信库，支持 AllReduce、AllGather、AllToAll 等集合通信操作。
keywords:
  - biren
  - 壁仞
  - succl
  - NCCL
  - 通信库
  - 分布式训练
---

# succl 壁仞suCCL通信库

## 功能描述

suCCL（SUPA Collective Communication Library）是壁仞官方的 GPU 通信库，兼容 NVIDIA NCCL 接口，为壁仞 BIRENSUPA 系列 GPU 提供高效的集合通信支持。suCCL 支持 P2P 直连、IB/RoCE 网络通信，是分布式 AI 训练的核心组件。

## 核心能力

### 1. 基础环境配置

```bash
# suCCL 测试脚本路径
ls /usr/local/birensupa/succl/tests/

# 常用测试命令
./p2p_test          # P2P 测试
./allreduce_test    # AllReduce 测试
./allgather_test    # AllGather 测试
```

### 2. 关键环境变量

```bash
# 基本配置
export SUCCL_IB_HCA="mlx5_0,mlx5_1"      # 指定计算网卡
export SUCCL_IB_GID_INDEX=3               # RoCE GID 索引
export SUCCL_SOCKET_IFNAME=eth0           # Socket 通信网卡

# P2P 通信层级
export SUCCL_P2P_LEVEL=LOC               # 本地 P2P
export SUCCL_P2P_LEVEL=PIX               # 同 PCIe Switch
export SUCCL_P2P_LEVEL=PXB                # 跨 PCIe Switch
export SUCCL_P2P_LEVEL=SYS                # 跨 NUMA 节点

# GPU Direct RDMA
export SUCCL_NET_GDR_LEVEL=LOC
export SUCCL_NET_GDR_LEVEL=PHB

# 高级配置
export SUCCL_BUFF_SIZE=16                 # 通信缓冲区大小 (MB)
export SUCCL_NTHREADS=2                   # 通信线程数
export SUCCL_DEBUG=INFO                   # 调试信息
```

### 3. 性能测试

```bash
# P2P 带宽测试
cd /usr/local/birensupa/succl/tests
./p2p_test

# AllReduce 测试
./allreduce_test

# AllGather 测试
./allgather_test

# 多节点测试
mpirun -n 8 ./allreduce_test
```

### 4. 使用 suCCL 进行分布式训练

```bash
# 设置环境变量
export SUCCL_IB_HCA="mlx5_0,mlx5_1"
export SUCCL_IB_GID_INDEX=3

# 启动分布式训练
torchrun --nnodes=4 --nproc_per_node=8 train.py
```

## 常见场景

### 场景1：单机 8 卡训练配置

```bash
# 环境变量配置
export SUCCL_IB_HCA="mlx5_0,mlx5_1"
export SUCCL_IB_GID_INDEX=3

# 验证 P2P 连通性
brsmi topo --p2p

# 运行 suCCL 测试
cd /usr/local/birensupa/succl/tests
./allreduce_test

# 启动训练
torchrun --nproc_per_node=8 train.py
```

### 场景2：多机分布式训练配置

```bash
# 主节点配置
export SUCCL_IB_HCA="mlx5_0,mlx5_1"
export SUCCL_IB_GID_INDEX=3
export SUCCL_P2P_LEVEL=SYS

# 创建 hostfile
# node1 slots=8
# node2 slots=8

# 运行多机测试
mpirun -hostfile hostfile -n 16 ./allreduce_test

# 启动分布式训练
torchrun --nnodes=2 --nproc_per_node=8 train.py
```

## 故障排查

### 问题1：通信超时

**症状：** 分布式训练卡在 AllReduce

**排查步骤：**
```bash
# 1. 检查网络连通性
ping <node_ip>

# 2. 检查 IB 网卡
ibstat

# 3. 启用调试
export SUCCL_DEBUG=INFO
python train.py 2>&1 | tee succl_debug.log

# 4. 简化测试
mpirun -n 2 ./allreduce_test
```

### 问题2：通信性能差

**症状：** 训练速度明显低于预期

**排查步骤：**
```bash
# 1. 检查 P2P 拓扑
brsmi topo --p2p

# 2. 测试 P2P 带宽
./p2p_test

# 3. 测试 IB 带宽
ib_write_bw -d mlx5_0

# 4. 优化参数
export SUCCL_BUFF_SIZE=32
export SUCCL_NTHREADS=4
```

## 相关文档

- [壁仞_07GPU管理与测试](../../china-ai-chip-docs/BIREN/壁仞_07GPU管理与测试.md)
- [壁仞_11分布式通信](../../china-ai-chip-docs/BIREN/壁仞_11分布式通信.md)
- [brsmi](./brsmi/) - GPU 设备管理