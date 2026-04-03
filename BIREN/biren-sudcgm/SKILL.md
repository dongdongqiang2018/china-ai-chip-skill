---
name: biren-sudcgm
description: BIREN suDCGM (Data Center GPU Monitor) 数据中心 GPU 管理器参考指南。用于查询 GPU 列表、监控性能指标、健康状态诊断、GPU 组管理、字段组管理、策略设置、任务统计等 C/S 架构管理操作。
keywords:
  - sudcgm
  - br-dcgm
  - br-dcgmi
  - biren
  - GPU管理
  - 数据中心
  - 监控
  - 壁仞
---

# suDCGM Command Reference

suDCGM 是壁仞数据中心 GPU 管理器，采用 C/S 架构（br-dcgmd 服务端 + br-dcgmi 客户端）。

## Quick Start

```bash
# 启动服务
br-dcgmd -c config.json

# 使用客户端
br-dcgmi discovery -l
br-dcgmi dmon -e 100 -d 2000
```

## Architecture

- **服务端**: br-dcgmd
- **客户端**: br-dcgmi

依赖：BRML、BRsmi、suVS、brmsg

## Service Management

### Start Service

```bash
# 前台运行
br-dcgmd -c config.json

# 后台运行
br-dcgmd --daemon -c config.json

# 使用 systemctl
systemctl start br-dcgmd
```

### Default Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--port` | 8182 | 监听端口 |
| `--log-level` | debug | 日志级别 |
| `--update-interval` | 2000 | 数据更新周期(ms) |

## Client Commands

### Discovery

```bash
br-dcgmi discovery -l                    # 查询 GPU 列表及详细信息
br-dcgmi discovery -l -i 0               # 指定 GPU
```

### Modules

```bash
br-dcgmi modules -l                       # 列出所有模块状态
```

### Group Management

```bash
br-dcgmi group -c test --allgpus          # 创建包含所有 GPU 的组
br-dcgmi group -d test                    # 删除组
br-dcgmi group -g test                    # 查询组信息
```

### Field Group

```bash
br-dcgmi fieldgroup -c name -f 0,1,2      # 创建字段组
br-dcgmi fieldgroup -d name               # 删除字段组
br-dcgmi fieldgroup -g name               # 查询字段组
```

### Configuration

```bash
br-dcgmi config --get -i 0                # 查询配置
br-dcgmi config --set -i 0 -k SviMode -v 2 # 设置配置
```

Configurable options:
- `SviMode` - SVI 模式
- `PowerThreshold` - 功耗阈值

### Device Monitoring

```bash
br-dcgmi dmon -e 100 -d 2000              # 监控字段数据
br-dcgmi dmon -e 100 -d 2000 -i 0         # 指定 GPU
br-dcgmi dmon -g test                     # 监控组
```

### Diagnostics

```bash
br-dcgmi diag -r 1                        # GPU 诊断（调用 suVS）
br-dcgmi diag -r 1 -i 0                   # 指定 GPU
```

### Health Monitoring

```bash
br-dcgmi health -s                        # 查询健康状态
br-dcgmi health --check                   # 检查健康状态
br-dcgmi health -s -i 0                   # 指定 GPU
```

### Policy

```bash
br-dcgmi policy --set <policy>            # 设置策略
br-dcgmi policy --reg <policy>            # 注册策略
```

### Statistics

```bash
br-dcgmi stats --enable                    # 启用统计
br-dcgmi stats --start                    # 开始统计
br-dcgmi stats -i 0                       # 查询统计信息
```

### Topology

```bash
br-dcgmi topo --gpuid 0                   # 查询拓扑信息
```

## Monitored Fields

### Version Information

- Driver Version
- UMD Version
- BRML Version
- SUPA Version
- Firmware versions

### Hardware Information

- Device Name
- UUID
- Serial Number
- PCI Information
- NUMA Node

### Real-time Metrics

- Temperature
- Power
- Clock
- Utilization
- Memory
- PCIe Throughput
- ECC Errors

### Fault Information

- Xid Error Codes

## Installation

```bash
# 安装
sudo ./<sudcgm*.run>

# 配置文件
# config.json
```

## Examples

### List All GPUs

```bash
br-dcgmi discovery -l
```

### Monitor GPU Metrics

```bash
br-dcgmi dmon -e 100,101,102 -d 1000
```

### Check GPU Health

```bash
br-dcgmi health -s -i 0
```

### Run GPU Diagnostics

```bash
br-dcgmi diag -r 1 -i 0
```

### Configure GPU

```bash
br-dcgmi config --set -i 0 -k PowerThreshold -v 300
```

## Error Handling

| Error | Description |
|-------|-------------|
| SUCCESS | 操作成功 |
| ERROR_UNINITIALIZED | 未初始化 |
| ERROR_INVALID_ARGUMENT | 无效参数 |
| ERROR_TIMEOUT | 超时 |
| ERROR_UNKNOWN | 未知错误 |

## Notes

- 需要启动 br-dcgmd 服务端
- 客户端连接默认端口 8182
- 大多数操作需要管理员权限
- 健康检查会调用 suVS 工具

## Related Tools

- **BRML**: C 语言管理库
- **BRsmi**: 命令行管理工具
- **suVS**: GPU 验证测试套件
- **brmsg**: 内核日志解析工具