---
name: mx-cluster-inspector
description: 沐曦（Metax）集群自动化巡检工具 Skill，提供 GPU 状态检查、PCIe 拓扑验证、网卡配置检查、性能基准测试等自动化巡检能力。mx-cci 是沐曦官方集群检查工具，支持交互式生成配置文件，可快速发现 GPU 掉卡、P2P 异常、网卡故障等集群问题，是大规模部署和日常运维的必备工具。
keywords:
  - muxi
  - metax
  - cluster
  - inspector
  - mx-cci
  - 集群巡检
  - 自动化运维
---

# mx-cluster-inspector 集群自动化巡检工具

## 功能描述

muxi-cluster-inspector（mx-cci）是沐曦官方提供的集群自动化巡检工具，用于大规模 GPU 集群的自动化健康检查和性能验证。mx-cci 支持 GPU 状态检查、PCIe ACS 验证、网卡配置检查、P2P 带宽测试、MCCL 性能测试等，是集群部署验收和日常运维的必备工具。

## 核心能力

### 1. 工具位置与结构

```bash
# 工具路径
ls /opt/maca/tools/mccl/inspector/mx-cci

# 目录结构
# .
# ├── bin/                 # 可执行文件
# ├── conf/                # 配置文件模板
# ├── lib/                 # 依赖库
# └── scripts/             # 测试脚本
```

### 2. 基础巡检功能

```bash
# 进入工具目录
cd /opt/maca/tools/mccl/inspector/mx-cci

# 交互式生成配置文件（首次使用）
./bin/mx-cci --config generate

# 或使用模板配置
cp conf/template.ini my_cluster.ini
# 编辑配置文件
vim my_cluster.ini

# 运行完整巡检
./bin/mx-cci -c my_cluster.ini

# 只运行基础测试
./bin/mx-cci -c my_cluster.ini --basic

# 只运行性能测试
./bin/mx-cci -c my_cluster.ini --perf
```

### 3. 巡检项目

#### 3.1 GPU 基础检查

```bash
# 检查 GPU 在位情况
# 自动检查：
# - GPU 数量是否正确
# - GPU 状态是否 Available
# - 显存使用情况
# - GPU 利用率
```

#### 3.2 PCIe ACS 检查

```bash
# 检查 PCIe ACS 状态
# - ACS 必须关闭以支持 P2P
# - 影响 P2P 性能可达 90%
# - X86: 关闭 BIOS IOMMU + grub 屏蔽
# - ARM: 关闭 BIOS SMMU
```

**ACS 关闭检查：**
```bash
# 检查 ACS 状态
cat /sys/bus/pci/devices/*/acs_enabled

# 正常输出（ACS 关闭）：空或 0
# 异常输出（ACS 开启）：非零值
```

#### 3.3 网卡配置检查

```bash
# 检查网卡状态
# - 网卡 Link 状态
# - 网卡速率 (200G/400G)
# - MTU 设置 (应为 9000)
# - RoCE 配置
```

**手动检查命令：**
```bash
# 查看网卡状态
ethtool mlx5_0

# 查看 IB 设备
ibstat

# 检查 RoCE 配置
rdma link show
```

#### 3.4 驱动版本检查

```bash
# 检查驱动版本一致性
# - 所有节点驱动版本必须一致
# - 驱动与固件版本匹配
```

### 4. 性能测试

#### 4.1 P2P 带宽测试

```bash
# P2P 带宽测试
# 测试项目：
# - CPU→GPU 带宽 (≥22GB/s)
# - GPU→CPU 带宽 (≥18GB/s)
# - GPU→GPU P2P 带宽 (≥44GB/s)
```

**手动测试：**
```bash
cd /opt/maca/tools/mccl/test
bash p2p.sh
```

#### 4.2 IB 网卡带宽测试

```bash
# IB 网卡带宽测试
# - 单向带宽 (≥380Gbps for 400G)
# - 双向带宽
# - 延迟测试
```

**手动测试：**
```bash
# 带宽测试
ib_write_bw -d mlx5_0

# 延迟测试
ib_write_lat -d mlx5_0
```

#### 4.3 MCCL 通信测试

```bash
# MCCL 通信性能测试
# - 单机多卡 AllReduce
# - 多机通信测试
```

**手动测试：**
```bash
# 单机 8 卡
bash /opt/maca/tools/mccl/test/mccl.sh 8

# 多机测试
bash /opt/maca/tools/mccl/test/cluster.sh
```

### 5. 配置文件格式

```ini
[cluster]
name = my_cluster
nodes = node1,node2,node3,node8

[node1]
host = 192.168.1.1
gpu_count = 8
nic = mlx5_0,mlx5_1

[node2]
host = 192.168.1.2
gpu_count = 8
nic = mlx5_0,mlx5_1

[basic_test]
gpu_check = true
pcie_acs_check = true
nic_check = true
driver_check = true

[perf_test]
p2p_test = true
ib_test = true
mccl_test = true

[thresholds]
gpu_util_min = 0
gpu_util_max = 95
mem_util_max = 90
temp_max = 85
p2p_bw_min = 40
ib_bw_min = 380
```

## 常见场景

### 场景1：新集群部署验收

新集群上线前的全面验收测试。

```bash
# 1. 生成配置文件
cd /opt/maca/tools/mccl/inspector/mx-cci
./bin/mx-cci --config generate

# 2. 修改配置文件，添加所有节点
vim my_cluster.ini

# 3. 运行完整巡检
./bin/mx-cci -c my_cluster.ini -v

# 4. 查看巡检报告
cat ~/inspector_logs/*.log
```

**验收检查清单：**
- [ ] 所有 GPU 显示 Available
- [ ] PCIe ACS 已关闭
- [ ] 网卡状态 Active
- [ ] P2P 带宽 ≥ 44 GB/s
- [ ] IB 带宽 ≥ 380 Gbps
- [ ] MCCL 通信正常

### 场景2：日常运维巡检

定期巡检发现潜在问题。

```bash
# 定时任务配置
# crontab -e
# 0 2 * * * /opt/maca/tools/mccl/inspector/mx-cci/bin/mx-cci -c /path/to/config.ini

# 手动巡检
./bin/mx-cci -c my_cluster.ini -o daily_report_$(date +%Y%m%d).html

# 邮件通知配置
./bin/mx-cci -c my_cluster.ini --alert-email admin@example.com
```

### 场景3：故障定位

集群异常时的快速诊断。

```bash
# 1. 查看告警日志
cat ~/inspector_logs/alert_*.log

# 2. 运行针对性测试
./bin/mx-cci -c my_cluster.ini --gpu-check     # 只检查 GPU
./bin/mx-cci -c my_cluster.ini --nic-check     # 只检查网卡
./bin/mx-cci -c my_cluster.ini --p2p-check     # 只检查 P2P

# 3. 详细输出模式
./bin/mx-cci -c my_cluster.ini --verbose
```

### 场景4：性能基线建立

建立性能基线用于后续对比。

```bash
# 1. 初始基线测试
./bin/mx-cci -c my_cluster.ini --perf -o baseline.json

# 2. 定期对比
./bin/mx-cci -c my_cluster.ini --perf --compare baseline.json

# 3. 性能趋势分析
# 查看历史报告对比
ls -lt ~/inspector_logs/*.json | head -10
```

## 巡检报告解读

### 报告结构

```
inspector_logs/
├── summary_20240101_120000.html     # HTML 报告
├── summary_20240101_120000.json     # JSON 数据
├── alert_20240101_120000.log        # 告警日志
├── gpu_check_20240101_120000.log   # GPU 检查详情
├── nic_check_20240101_120000.log   # 网卡检查详情
└── perf_test_20240101_120000.log  # 性能测试详情
```

### 告警级别

| 级别 | 颜色 | 说明 | 行动 |
|------|------|------|------|
| CRITICAL | 红色 | 严重故障 | 立即处理 |
| ERROR | 橙色 | 错误 | 24 小时内处理 |
| WARNING | 黄色 | 警告 | 3 天内处理 |
| INFO | 蓝色 | 信息 | 定期关注 |

### 常见告警

```
[CRITICAL] GPU 3 not available - 需检查驱动
[ERROR] PCIe ACS enabled on node2 - 需关闭 ACS
[WARNING] GPU temperature 87°C - 需检查散热
[WARNING] P2P bandwidth 38GB/s < 44GB/s - 需检查拓扑
[ERROR] IB link down on mlx5_2 - 需检查网卡
```

## 故障排查

### 问题1：巡检失败

**症状：** 巡检脚本执行报错

**排查步骤：**
```bash
# 1. 检查日志
cat ~/inspector_logs/error.log

# 2. 检查配置文件语法
./bin/mx-cci -c my_cluster.ini --validate

# 3. 手动运行单个测试
./bin/mx-cci -c my_cluster.ini --basic --verbose
```

### 问题2：节点连接失败

**症状：** SSH 连接超时

**排查步骤：**
```bash
# 1. 检查 SSH 免密
ssh node1 hostname

# 2. 检查节点可达性
ping node1

# 3. 检查防火墙
ssh node1 "systemctl status sshd"
```

### 问题3：性能测试超时

**症状：** MCCL 测试超时

**排查步骤：**
```bash
# 1. 单独测试节点
ssh node1 "bash /opt/maca/tools/mccl/test/mccl.sh 8"

# 2. 检查 NCCL 调试
ssh node1 "NCCL_DEBUG=INFO bash /opt/maca/tools/mccl/test/mccl.sh 8"

# 3. 检查网络
ssh node1 "ibstat"
```

## 相关文档

- [曦云系列GPU用户指南](../china-ai-chip-docs/MUXI/972_曦云系列通用GPU用户指南.md)
- [仪电集群部署指南](../china-ai-chip-docs/MUXI/仪电集群部署指南-V-latest.docx)
- [muxi-npu-smi](./muxi-npu-smi/) - GPU 设备管理
- [muxi-mccl](./muxi-mccl/) - MCCL 通信库
- [muxi-vs](./muxi-vs/) - 算力测试