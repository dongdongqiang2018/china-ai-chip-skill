---
name: biren-suvs
description: BIREN suVS (SUPA Validation Suite) GPU 验证测试套件参考指南。用于 GPU 设备信息检查、软件版本验证、PCIe 带宽测试、P2P 带宽测试、HBM 内存测试、内存带宽测试、视频编解码性能测试、功耗压力测试、SPC 算力测试等。
keywords:
  - suvs
  - biren
  - GPU测试
  - 验证
  - 性能测试
  - 内存测试
  - 带宽测试
  - 壁仞
---

# suVS Command Reference

suVS 是 GPU 验证和测试工具套件，采用插件化架构。

## Quick Start

```bash
suvs -c gpuinfo.conf                      # GPU 信息检查
suvs -c quick.conf -d 5 -l test.log       # 快速测试
suvs -t                                   # 列出所有可用测试
```

## Plugin List

| Plugin | Function | Command Example |
|--------|----------|-----------------|
| GPU INFO | 获取 GPU 设备基本信息 | `suvs -c gpuinfo.conf` |
| SOFTWARE | 检查运行时库版本 | `suvs -c software.conf` |
| PCIE BANDWIDTH | CPU-GPU 传输带宽测试 | `suvs -c pcie_1.conf` |
| P2P BANDWIDTH | GPU 间 P2P 带宽测试 | `suvs -c p2p_1.conf` |
| HBM MEMORY TEST | GPU 内存稳定性测试 | `suvs -c hbm.conf -test 0` |
| MEMORY BANDWIDTH | GPU 内存带宽测试 | `suvs -c membw.conf` |
| VIDEO PERFORMANCE | 视频编解码性能测试 | `suvs -c video.conf` |
| POWER STRESS | 特定功耗下稳定性测试 | `suvs -c power.conf` |
| SPC STRESS | SPC 算力压力测试 | `suvs -c spcstress.conf` |
| SPC PERFORMANCE | SPC 算力测试 | `suvs -c spcperf.conf` |
| GPU MONITOR | 测试过程中监测 | 配合其他插件 |

## Command Parameters

| Parameter | Description |
|-----------|-------------|
| `-c / --config` | 指定配置文件 |
| `-g / --listGpus` | 列出可用 GPU |
| `-i / --indexes` | 指定 GPU 列表 |
| `-t / --listTests` | 列出可用插件 |
| `-d / --debugLevel` | 日志级别 (0-5) |
| `-l / --debugLogFile` | 日志文件 |
| `-v / --verbose` | 详细输出 |

## HBM Memory Test Modes

| Test | Name | Description |
|------|------|-------------|
| 0 | Walking 1 bit | 地址位翻转测试 |
| 1 | Own address test | 地址自身值测试 |
| 2 | Moving inversions, ones&zeros | 全 0/全 1 写入验证 |
| 3 | Moving inversions, 8 bit pat | 8 位重复 pattern |
| 4 | Moving inversions, random pattern | 随机 pattern |
| 5 | Block move, 64 moves | 64 字节块移动 |
| 6 | Moving inversions, 32 bit pat | 32 位移位 pattern |
| 7 | Random number sequence | 随机数序列 |
| 8 | Modulo 20, random pattern | 模 20 随机 pattern |
| 9 | Bit fade test | 90 分钟位衰减测试 |
| 10 | Memory stress test | SPC kernel 方式压测 HBM |

## Configuration File Format (YAML)

```yaml
actions:
- name: action_1
  gpu_id: all
  plugin: p2p
  peers: all
  duration: 5
```

## Test Examples

### Quick Test

```bash
suvs -c quick.conf -d 5 -l test.log
```

### HBM Memory Test

```bash
suvs -c hbm.conf -test 0           # Walking 1 bit
suvs -c hbm.conf -test 10          # Memory stress test
suvs -c hbm.conf -test 4 -i 0       # 指定 GPU
```

### PCIe Bandwidth Test

```bash
suvs -c pcie_1.conf
suvs -c pcie_1.conf -i 0           # 指定 GPU
```

### P2P Bandwidth Test

```bash
suvs -c p2p_1.conf                  # 测试所有 P2P 对
suvs -c p2p_1.conf -i 0,1          # 指定 GPU 对
```

### Memory Bandwidth Test

```bash
suvs -c membw.conf
```

### Video Performance Test

```bash
suvs -c video.conf
```

### Power Stress Test

```bash
suvs -c power.conf
```

### SPC Stress Test

```bash
suvs -c spcstress.conf
```

### SPC Performance Test

```bash
suvs -c spcperf.conf
```

### GPU INFO

```bash
suvs -c gpuinfo.conf
```

### Software Version Check

```bash
suvs -c software.conf
```

## List Available GPUs

```bash
suvs -g
```

## List Available Tests

```bash
suvs -t
```

## Common Options

### Specify GPU

```bash
suvs -c test.conf -i 0              # GPU 0
suvs -c test.conf -i 0,1,2,3         # GPU 0,1,2,3
suvs -c test.conf -i all             # 所有 GPU
```

### Debug Level

```bash
suvs -c test.conf -d 0               # 静默
suvs -c test.conf -d 3               # 信息
suvs -c test.conf -d 5              # 详细
suvs -c test.conf -v                 # 同 -d 5
```

## Output

### Success Output

```
[INFO] Test completed successfully
```

### Failure Output

```
[ERROR] Test failed: <error_message>
```

## Notes

- 大多数测试需要 root 权限
- HBM 内存测试可能需要较长时间
- 部分测试会占用大量 GPU 资源
- 测试前确保没有其他 GPU 程序运行
- P2P 测试需要多块 GPU

## Related Tools

- **BRsmi**: GPU 管理工具
- **suDCGM**: 数据中心 GPU 管理器
- **BRML**: C 语言管理库