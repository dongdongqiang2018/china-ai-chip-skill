---
name: mxvs
description: 沐曦验收测试套件（MetaXValidationSuite）使用指南，用于GPU硬件测试、PCIe/显存/MetaXLink带宽测试、眼图测试、压力测试等。是FAE进行硬件验证和质量检测的核心工具。
keywords:
  - mxvs
  - 验收测试
  - 带宽测试
  - 压力测试
  - 眼图测试
  - PCIe测试
  - P2P测试
  - MetaXLink
  - 硬件验证
---

# mxvs 使用指南

mxvs（MetaXValidationSuite）是沐曦面向服务器合作伙伴以及开发者提供的测试软件集合，便于用户方便快捷地了解曦云®系列GPU的硬件能力，它支持PCIe带宽测试和眼图报告获取、显存带宽测试、算力测试、压力测试等功能。

## 快速开始

### 环境要求
```bash
# 1. 确保已加载GPU驱动
lsmod | grep metax

# 2. 确保有root权限
whoami  # 应为root

# 3. 确保FUSE已安装
dpkg -l | grep fuse
```

### 基本命令
```bash
# 查看设备列表
mxvs devices

# 动态监控GPU状态
mxvs dashboard

# 查看帮助
mxvs --help
```

### 快速测试
```bash
# PCIe带宽测试（单向）
mxvs pcie benchmark unidirection --src-devices 0 --dst-devices 1

# 显存带宽测试
mxvs memory benchmark --devices 0

# MetaXLink带宽测试
mxvs metaxlink benchmark --devices 0

# XCore压力测试
mxvs stress --xcore --xcore-devices 0
```

---

## 设备信息

### 查看设备列表
```bash
mxvs devices
```
显示所有CPU和GPU设备信息。

### 动态监控
```bash
# 默认监控（功耗、温度、使用率）
mxvs dashboard

# 指定设备
mxvs dashboard -d 0,1

# 指定监控面板
# 0:BOARDPOWER, 1:TEMPERATURE, 2:USAGE
# 3:HBMBANDWIDTH, 4:PCIEBANDWIDTH
# 5:METAXLINKBANDWIDTH, 6:PMBUSPOWER, 7:ETHBANDWIDTH
mxvs dashboard -d 0,1 -p 2,3,4
```

---

## PCIe验收测试

### 实时带宽查询
```bash
mxvs pcie bandwidth --devices <DEVICE_ID>

# 持续监控
mxvs pcie bandwidth --devices 0 --continuous
```

### 带宽测试

#### 单向带宽
```bash
# 基本用法
mxvs pcie benchmark unidirection --src-devices 0 --dst-devices 1

# 指定数据大小
mxvs pcie benchmark unidirection --src-devices 0 --dst-devices 1 --data-sizes 1KB,1MB,1GB

# 多设备测试
mxvs pcie benchmark unidirection --src-devices all --dst-devices all

# 详细结果
mxvs pcie benchmark unidirection --src-devices 0 --dst-devices 1 --detail

# JSON输出
mxvs pcie benchmark unidirection --src-devices 0 --dst-devices 1 --json result.json

# 关闭数据校验
mxvs pcie benchmark unidirection --src-devices 0 --dst-devices 1 --no-check
```

**常用参数**：
| 参数 | 说明 |
|------|------|
| `--src-devices` | 源设备ID |
| `--dst-devices` | 目标设备ID |
| `-s, --data-sizes` | 数据大小 |
| `--cpu-affinity` | CPU亲和度 |
| `--json` | JSON输出 |
| `--detail` | 详细结果 |
| `--no-check` | 关闭校验 |

#### 双向带宽
```bash
mxvs pcie benchmark bidirection --devices 0,1

# 指定数据大小
mxvs pcie benchmark bidirection --devices 0,1 --data-sizes 1GB
```

### 眼图测试
```bash
# 基本用法
mxvs eye --devices 0

# 指定物理层和Lane
mxvs eye --devices 0 --phys 0 --lanes 0

# 所有物理层和Lane
mxvs eye --devices 0 --phys 0-3 --lanes 0-3
```

**注意**：
- 眼图测试前确保无其他进程使用GPU
- 测试过程中请勿中断
- 测试结束后建议重启服务器

---

## 显存验收测试

### 实时带宽查询
```bash
mxvs memory bandwidth --devices 0
mxvs memory bandwidth --devices 0 --continuous
```

### 带宽测试
```bash
# 基本用法
mxvs memory benchmark --devices 0

# 读测试（默认）
mxvs memory benchmark --devices 0

# 读写测试
mxvs memory benchmark --devices 0 --kernel-copy

# 指定数据大小
mxvs memory benchmark --devices 0 --data-sizes 10GB

# JSON输出
mxvs memory benchmark --devices 0 --json result.json
```

---

## MetaXLink验收测试

### 实时带宽查询
```bash
mxvs metaxlink bandwidth --devices 0
mxvs metaxlink bandwidth --devices 0 --continuous
```

### 带宽测试
```bash
# 基本用法
mxvs metaxlink benchmark --devices 0

# 指定数据大小
mxvs metaxlink benchmark --devices 0 --data-sizes 1KB,1MB,1GB

# 指定模式
# ingress: 源从目标拷贝
# egress: 源向目标拷贝
mxvs metaxlink benchmark --devices 0 --mode ingress

# JSON输出
mxvs metaxlink benchmark --devices 0 --json result.json
```

### 眼图测试
```bash
mxvs eye --metaxlink --metaxlink-ports 0 --devices 0 --lanes 0
```

---

## P2P验收测试

### P2P带宽测试

P2P（点对点）通信测试用于验证GPU之间的直接通信能力，支持MetaXLink和PCIe两种拓扑。

```bash
# 基本用法
mxvs p2p --src-devices 0 --dst-devices 1

# 多对多测试
mxvs p2p --src-devices 0 --dst-devices 1,2,3
mxvs p2p --src-devices 1,2,3 --dst-devices 0

# 全设备测试（所有GPU两两测试）
mxvs p2p --src-devices all --dst-devices all

# 环形测试
mxvs p2p --src-devices 0,2,1,3 --dst-devices
```

### 输出结果解读

| 字段 | 说明 |
|------|------|
| TOPOLOGY | 通信拓扑（metaxlink 或 pcie） |
| SIZE | 测试数据大小 |
| EFFECTIVE BANDWIDTH | 有效带宽（实际数据传输带宽） |
| RAW BANDWIDTH | 原始带宽（含协议开销） |
| TRANS DELAY | 传输延迟（μs） |

### 带宽预期值

| 拓扑 | 预期带宽 |
|------|----------|
| MetaXLink | ~99 GB/s |
| PCIe | ~78 GB/s |

**注意**：P2P测试主要用于硬件验证，日常集合通信测试请使用 MCCL。详见 [mccl-test技能](../mccl-test/SKILL.md)

---

## 算力测试

```bash
# 基本用法
mxvs ops --devices 0 --models resnet50

# 可用模型
# resnet50, mobilenet, bert, gpt2, etc.
```

---

## 压力测试

### XCore压力测试
```bash
# 基本用法
mxvs stress --xcore --xcore-devices 0

# 指定持续时间
mxvs stress --xcore --xcore-devices 0 --duration 300

# 后台运行
nohup mxvs stress --xcore --xcore-devices 0 --duration 3600 &

# 后台运行日志
nohup mxvs stress --xcore --xcore-devices 0-3 --duration 3600 > stress.log 2>&1 &

# 指定迭代次数
mxvs stress --xcore --xcore-devices 0 --iterations 1000
```

### MetaXLink压力测试
```bash
mxvs stress --metaxlink
mxvs stress --metaxlink --duration 300
nohup mxvs stress --metaxlink --duration 3600 > mxlk_stress.log 2>&1 &
```

### ETH压力测试（仅C600）
```bash
mxvs stress --eth
mxvs stress --eth --duration 300
```

---

## ETH验收测试（仅C600）

### ETH眼图测试
```bash
mxvs eye --eth --devices 0 --lanes 0
```

---

## 光模块测试（仅C500X）

### 单机MetaXLink带宽测试
```bash
mxvs om client --src-devices 0 --dst-devices 1
```

### 跨机MetaXLink带宽测试
```bash
# Server端
mxvs om server

# Client端
mxvs om client --dst-addr <SERVER_IP> --src-devices 0 --dst-devices 1
```

---

## 日志管理

### 默认日志位置
```
/var/log/mxvs/
```

### 自定义日志目录
```bash
export MXVS_REPORT_DIR=/home/user1/mxvs
```

---

## 故障排查

### 测试失败

**检查项**：
1. 驱动是否加载
2. GPU是否可用
3. 权限是否正确

```bash
# 检查驱动
lsmod | grep metax

# 检查GPU
mxvs devices

# 检查权限
whoami  # 需root
```

### 带宽测试结果异常

**问题**：带宽低于预期

**可能原因**：
- NUMA节点跨节点访问
- CPU亲和性不佳

**解决方案**：
```bash
# 清理缓存
echo 3 > /proc/sys/vm/drop_caches

# 指定CPU亲和度
--cpu-affinity 0,1,2,3
```

### 眼图测试失败

**可能原因**：
- GPU被占用
- 测试中断

**解决方案**：
```bash
# 确认无进程
mx-smi --show-all-process

# 测试后重启
```

---

## 官方参考

- [曦云系列通用GPU mxvs测试工具套件使用手册_CN_V20.pdf](../文档/mxvs测试工具套件使用手册_CN_V20.pdf)
- [曦云系列通用GPU mx-smi使用手册_CN_V13.pdf](../文档/mx-smi使用手册_CN_V13.pdf)