---
name: mx-mccl
description: 沐曦（Metax）MCCL 通信库配置与测试 Skill，提供单机多卡、多机分布式训练的通信库配置、环境变量优化、性能测试和问题诊断能力。MCCL 兼容 NCCL 接口，是沐曦 GPU 集群进行 AI 训练的核心通信库，支持 P2P、AllReduce、AllToAll 等集合通信操作。
keywords:
  - muxi
  - metax
  - mccl
  - NCCL
  - 通信库
  - 分布式训练
  - AllReduce
---

# mx-mccl 沐曦MCCL通信库

## 功能描述

MCCL（Metax Collective Communication Library）是沐曦官方的 GPU 通信库，兼容 NVIDIA NCCL 接口，为沐曦 C500 系列 GPU 提供高效的集合通信支持。MCCL 支持 P2P 直连、IB/RoCE 网络通信，是分布式 AI 训练的核心组件。本 Skill 提供完整的配置指南、性能测试和问题诊断能力。

## 核心能力

### 1. 基础环境配置

沐曦 GPU 集群的 MCCL 基础环境配置。

```bash
# MCCL 测试脚本路径
ls /opt/maca/tools/mccl/test/

# 常用测试脚本
bash /opt/maca/tools/mccl/test/p2p.sh        # 单机 P2P 测试
bash /opt/maca/tools/mccl/test/mccl.sh      # 单机多卡测试
bash /opt/maca/tools/mccl/test/mccl.sh 8     # 8卡测试
bash /opt/maca/tools/mccl/test/cluster.sh   # 多机测试
```

### 2. 关键环境变量配置

```bash
# 基本配置
export MCCL_IB_HCA="mlx5_0,mlx5_1"           # 指定计算网卡
export MCCL_IB_GID_INDEX=3                    # RoCE GID 索引 (3=IPv4, 1=IPv6)
export MCCL_SOCKET_IFNAME=eth0                # Socket 通信网卡

# P2P 通信层级（重要！）
export MCCL_P2P_LEVEL=LOC                    # 同 GPU：本地 P2P
export MCCL_P2P_LEVEL=MetaxLink               # MXLK 互联
export MCCL_P2P_LEVEL=PIX                      # 同 PCIe Switch
export MCCL_P2P_LEVEL=PXB                      # 跨 PCIe Switch
export MCCL_P2P_LEVEL=PHB                      # 跨 PCIe 主桥
export MCCL_P2P_LEVEL=SYS                      # 跨 NUMA 节点

# GPU Direct RDMA
export MCCL_NET_GDR_LEVEL=LOC                  # GPU-网卡 P2P
export MCCL_NET_GDR_LEVEL=PHB                 # 跨 PCIe 主桥

# 高级配置
export MCCL_CROSS_NIC=0                        # 跨网卡流量控制 (0/1/2)
export MCCL_PCIE_BUFFER_MODE=0                 # PCIe 缓冲模式
export MCCL_DMABUF_ENABLE=1                     # 启用 dmabuf（内核≥5.15）
export MCCL_BUFF_SIZE=16                       # 通信缓冲区大小 (MB)
export MCCL_NTHREADS=2                         # 通信线程数
```

### 3. 性能测试

MCCL 通信库性能基准测试。

```bash
# 1. P2P 单机测试
bash /opt/maca/tools/mccl/test/p2p.sh

# 预期：MX 连接带宽 ≥ 50 GB/s

# 2. 单机 4 卡测试
bash /opt/maca/tools/mccl/test/mccl.sh

# 3. 单机 8 卡测试
bash /opt/maca/tools/mccl/test/mccl.sh 8

# 4. 多机测试
# 在主节点执行
bash /opt/maca/tools/mccl/test/cluster.sh

# 或指定节点文件
bash /opt/maca/tools/mccl/test/cluster.sh -f hostfile
```

**性能基准参考：**
| 测试场景 | 总带宽基准 |
|----------|-----------|
| 单机 8 卡（光互连） | ≥200 GB/s |
| 兄弟机 16 卡（光互连） | ≥175 GB/s |
| 跨超节点双机 16 卡 | ≥38 GB/s |
| 完整超节点 64 卡 | ≥160 GB/s |

### 4. 网卡带宽测试

```bash
# IB 网卡带宽测试
ib_write_bw -d mlx5_0

# 带 RDMA 的带宽测试
ib_write_bw -d mlx5_0 -R

# 双向带宽测试
ib_write_bw -d mlx5_0 --bidirectional

# 预期：400G 网卡 ≥ 380 Gbps
```

### 5. 异构混训配置

沐曦与其他厂商 GPU 混训配置。

```bash
# 沐曦 + NVIDIA 混训
export MCCL_EXT_CCL_ENABLE=1
export MCCL_HC_PLUGIN=/path/to/libmxccl_21403plugin.so
# 插件版本需与 NCCL 版本匹配
```

## 常见场景

### 场景1：单机 8 卡训练配置

```bash
# 环境变量配置
export MCCL_IB_HCA="mlx5_0,mlx5_1"
export MCCL_P2P_LEVEL=MetaxLink

# 验证 P2P 连通性
mx-smi topo --matrix

# 运行 MCCL 测试
bash /opt/maca/tools/mccl/test/mccl.sh 8

# 启动训练
python train.py --tensor_model_parallel_size=8
```

### 场景2：多机分布式训练配置

```bash
# 主节点配置
export MCCL_IB_HCA="mlx5_0,mlx5_1"
export MCCL_IB_GID_INDEX=3
export MCCL_P2P_LEVEL=SYS
export MCCL_NET_GDR_LEVEL=PHB

# 创建 hostfile 文件
# cat hostfile
# node1 slots=8
# node2 slots=8
# node3 slots=8
# node4 slots=8

# 运行多机测试
bash /opt/maca/tools/mccl/test/cluster.sh -f hostfile

# 启动分布式训练
torchrun --nnodes=4 --nproc_per_node=8 train.py
```

### 场景3：超节点架构训练

沐曦超节点（8 台服务器 + 4 台 PCIe 交换机）配置。

```bash
# 超节点配置
export MCCL_P2P_LEVEL=MetaxLink
export MCCL_IB_HCA="mlx5_0,mlx5_1,mlx5_2,mlx5_3"

# 检查 MXLK 拓扑
mx-smi topo --show-mxlk

# 验证 GPU 互联
mx-smi topo --matrix

# 64 卡训练配置
# TP=8, PP=1, DP=8
torchrun --nnodes=8 --nproc_per_node=8 train.py
```

### 场景4：RDMA 网络配置

```bash
# 检查网卡状态
ibstat
# 输出示例：
# mlx5_0: Active
# Port 1: LinkUp

# 检查 RoCE 配置
rdma link show

# 设置 RoCEv2 模式
rdma link set mlx5_0/1 roce_mode ribf

# 验证 GID
ibgids mlx5_0

# 配置 ECN
# 在交换机上配置 ECN 标记
# DSCP 值对应 ToS=160 (queue 5)
```

## 故障排查

### 问题1：通信超时

**症状：** 分布式训练卡在 AllReduce/AllToAll

**排查步骤：**
```bash
# 1. 检查网络连通性
ping <node_ip>
ib_ping <node_ip>

# 2. 检查网卡状态
ibstat
ethtool mlx5_0

# 3. 检查防火墙
systemctl status firewalld
sudo firewall-cmd --list-all

# 4. 检查 NCCL 调试输出
export NCCL_DEBUG=INFO
python train.py 2>&1 | tee nccl_debug.log

# 5. 简化测试
bash /opt/maca/tools/mccl/test/cluster.sh
```

### 问题2：通信性能差

**症状：** 训练速度明显低于预期

**排查步骤：**
```bash
# 1. 检查 P2P 拓扑
mx-smi topo --matrix

# 2. 检查 MXLK 状态
mx-smi topo --show-mxlk

# 3. 运行性能基准测试
bash /opt/maca/tools/mccl/test/p2p.sh
bash /opt/maca/tools/mccl/test/mccl.sh 8

# 4. 检查环境变量
echo $MCCL_P2P_LEVEL
echo $MCCL_IB_HCA

# 5. 优化通信配置
export MCCL_BUFF_SIZE=32
export MCCL_NTHREADS=4
```

### 问题3：GPU 通信失败

**症状：** P2P 通信报错

**排查步骤：**
```bash
# 1. 检查 GPU 是否支持 P2P
mx-smi topo --matrix
# 查看 N/A 表示不支持 P2P

# 2. 检查 PCIe ACS 状态
# 物理机必须关闭 ACS
cat /sys/bus/pci/devices/*/acs_enabled

# 3. 调整 P2P 层级
export MCCL_P2P_LEVEL=PIX  # 降级到同 Switch
```

### 问题4：IB 网卡不可用

**症状：** ibstat 显示 no PM

**排查步骤：**
```bash
# 1. 检查驱动加载
lsmod | grep mlx

# 2. 重置网卡
rdma link reset mlx5_0

# 3. 检查固件版本
flint -d mlx5_0 q

# 4. 检查 PCIe 状态
lspci | grep -i mellox
```

## 常用命令速查

```bash
# 查看 MCCL 版本
ls /opt/maca/tools/mccl/

# 运行所有测试
bash /opt/maca/tools/mccl/test/all.sh

# 查看测试日志
cat ~/mccl_test.log

# NCCL 调试
NCCL_DEBUG=INFO NCCL_DEBUG_SUBSYS=ALL python train.py
```

## 相关文档

- [曦云系列GPU用户指南](../china-ai-chip-docs/MUXI/972_曦云系列通用GPU用户指南.md)
- [曦云系列GPU驱动安装指南](../china-ai-chip-docs/MUXI/971_曦云系列通用GPU驱动安装指南.md)
- [muxi-npu-smi](./muxi-npu-smi/) - GPU 设备管理
- [muxi-vs](./muxi-vs/) - 算力测试工具