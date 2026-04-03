---
name: biren-brsmi
description: BIREN BRsmi 命令行 GPU 管理工具参考指南。用于查询 GPU 状态（温度、功耗、显存、利用率、ECC）、监控性能（dmon/pmon）、设置 GPU 参数（计算模式、SVI 模式、SPC 频率）、查询拓扑信息、复位 GPU 等操作。
keywords:
  - brsmi
  - biren
  - GPU管理
  - 设备监控
  - 功耗
  - 温度
  - 显存
  - 拓扑
  - 壁仞
---

# BRsmi Command Reference

BRsmi（BIREN System Management Interface）是基于 BRML 的命令行 GPU 管理工具，类似 NVIDIA 的 nvidia-smi。

## Quick Start

```bash
brsmi                                  # GPU 信息总览
brsmi --version                        # 显示版本
brsmi gpu list                         # 列出所有 GPU
brsmi gpu dmon                         # 滚动监控 GPU
brsmi gpu query -i 0 -d temperature    # 查询温度
```

## GPU Information Queries

### Basic Queries

```bash
brsmi                                   # 总览（名称、温度、功耗、显存、利用率、ECC）
brsmi --version                         # 显示各模块版本
brsmi gpu list                          # 列出所有 GPU 设备及 Bus-id
brsmi gpu query                         # 查询 GPU 详细信息
```

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| `-i` | GPU ID |
| `-d` | 查询数据类型 |
| `-f` | 输出格式 (csv, table) |
| `-l` | 输出行数限制 |
| `-x` | XML 格式输出 |

### Query Data Types

```bash
brsmi gpu query -d name                 # 设备名称
brsmi gpu query -d temperature           # 温度
brsmi gpu query -d power                 # 功耗
brsmi gpu query -d memory               # 显存
brsmi gpu query -d utilization          # 利用率
brsmi gpu query -d ecc                  # ECC 错误
brsmi gpu query -d clock                # 时钟信息
brsmi gpu query -d pci                  # PCIe 信息
brsmi gpu query -d uuid                 # UUID
brsmi gpu query -d health               # 健康状态
```

### Custom Query Example

```bash
brsmi gpu --query-gpu=serial,temperature.gpu --format=csv,noheader,nounits -i 0 -l 3
```

## Device Monitoring (DMON)

```bash
brsmi gpu dmon                          # 默认监控（功耗+温度）
brsmi gpu dmon -s p                     # 功耗和温度
brsmi gpu dmon -s u                     # SPC/Memory/Encoder/Decoder 利用率
brsmi gpu dmon -s c                     # 时钟信息（SOC/Core/Memory/Video）
brsmi gpu dmon -s v                     # 功耗和温度违规
brsmi gpu dmon -s m                     # 内存信息
brsmi gpu dmon -s e                     # ECC 和 AER 错误
brsmi gpu dmon -s t                     # PCIe Rx/Tx 吞吐量
brsmi gpu dmon -s b                     # P2P Rx/Tx 吞吐量
brsmi gpu dmon -s d                     # 显存读写带宽
brsmi gpu dmon -i 0                     # 指定 GPU
brsmi gpu dmon -c 10                    # 刷新次数
brsmi gpu dmon -d 1000                  # 刷新间隔（毫秒）
```

## Process Monitoring (PMON)

```bash
brsmi gpu pmon                          # 进程监控
brsmi gpu pmon -i 0                     # 指定 GPU
brsmi gpu pmon -c 10                    # 刷新次数
brsmi gpu pmon -d 1000                  # 刷新间隔
```

## GPU Status

```bash
brsmi gpu stats                         # 显示 GPU 状态
brsmi gpu stats -i 0                    # 指定 GPU
```

## FRU Information

```bash
brsmi gpu fru                           # 显示 FRU 信息
brsmi gpu fru -i 0                      # 指定 GPU
```

## GPU Configuration

### Set Parameters

```bash
brsmi gpu set -c exclusive_process     # 设置计算模式
brsmi gpu set -p 1                       # 设置持久模式
brsmi gpu set -s 2                       # SVI 模式（0=关, 1=二切, 2=四切）
brsmi gpu set --pclk 1000                # 设置 SPC 频率
brsmi gpu set --perf 0                   # 设置性能级别
brsmi gpu set -i 0                       # 指定 GPU
```

### Configuration Parameters

| Parameter | Function | Example |
|-----------|----------|---------|
| `-c <mode>` | 计算模式 | `brsmi gpu set -c exclusive_process` |
| `-p <0/1>` | 持久模式 | `brsmi gpu set -p 1` |
| `-s <0/1/2>` | SVI 模式 | `brsmi gpu set -s 2` |
| `--pclk <freq>` | SPC 频率 | `brsmi gpu set --pclk 1000` |
| `--perf <level>` | 性能级别 | `brsmi gpu set --perf 0` |

### Compute Modes

- `default` - 默认模式
- `exclusive_process` - 独占进程模式
- `prohibited` - 禁止使用

## GPU Topology

```bash
brsmi topo -m                           # 显示 GPU 拓扑互联信息
brsmi topo --p2p                        # 显示 P2P 连接信息
brsmi topo -i 0                         # 指定 GPU
```

## GPU Reset

```bash
brsmi reset -g                          # 复位 GPU
brsmi reset -e                          # 复位 ECC 计数器
brsmi reset -i 0                        # 指定 GPU
```

## BAR Space Configuration

```bash
brsmi gpu conf                          # 显示 BAR 空间配置
```

## Optical Module Information

```bash
brsmi gpu optm                          # 显示光模块信息
```

## Output Format Options

```bash
brsmi gpu query --format=csv            # CSV 格式
brsmi gpu query --format=table          # 表格格式
brsmi gpu query --format=csv,noheader   # 无表头
brsmi gpu query --format=csv,nounits    # 无单位
```

## Common Examples

### Check All GPUs

```bash
brsmi
brsmi gpu list
```

### Monitor GPU in Real-time

```bash
brsmi gpu dmon -s p,u,c -d 2000         # 监控功耗、温度、利用率、时钟
```

### Check GPU Health

```bash
brsmi gpu query -d health -i 0
brsmi gpu query -d ecc -i 0
```

### Check Temperature

```bash
brsmi gpu query -d temperature -i 0
```

### Check Memory

```bash
brsmi gpu query -d memory -i 0
```

### Check Power

```bash
brsmi gpu query -d power -i 0
```

## Error Handling

| Error Code | Description |
|------------|-------------|
| SUCCESS | 操作成功 |
| ERROR_UNINITIALIZED | 未初始化 |
| ERROR_INVALID_ARGUMENT | 无效参数 |
| ERROR_TIMEOUT | 超时 |
| ERROR_UNKNOWN | 未知错误 |

## Notes

- 大多数配置命令需要 **root 权限**
- GPU ID 从 `brsmi gpu list` 获取
- 时钟和功耗设置可能需要管理员权限
- SVI 模式切换需要确保 GPU 没有程序在使用
- 复位操作会中断正在运行的 GPU 任务

## Official Documentation

- BIREN SUPA SDK 文档
- BRML 用户指南（包含 API 详细信息）