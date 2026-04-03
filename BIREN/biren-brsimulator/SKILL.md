---
name: biren-brsimulator
description: BIREN brSimulator 仿真器参考指南。用于在没有壁仞硬件设备的条件下运行 BIRENSUPA 应用程序或壁仞汇编程序，支持 BR100/104/106 系列架构，提供异常检测和警告输出。
keywords:
  - brsimulator
  - biren
  - 仿真器
  - simulator
  - 模拟器
  - 调试
  - 壁仞
---

# brSimulator Command Reference

brSimulator 工具可以模拟壁仞硬件的指令集行为，在没有壁仞硬件设备的条件下运行 BIRENSUPA 应用程序。

## Quick Start

```bash
# 配置驱动环境变量
export BR_UMD_BACKEND=simulator

# 运行 BIREN 可执行程序
./test
```

## Installation

安装路径：`/usr/local/birensupa/sdk/latest/brcc/lib/libBirenSim.so`

确保 `LD_LIBRARY_PATH` 环境变量已包含上述路径。

## Features

- 简化硬件细节，高效运行
- 与 BRCC 工具链协同验证
- 专注软件开发领域用户，软件调试友好
- 功能灵活，扩展性强
- 为 suDebugger、suSanitizer 等提供仿真支持

## Environment Variables

### Target Hardware

```bash
export BR_UMD_SIM_DEVICE_ID=0xb100
```

| Device ID | Architecture |
|-----------|--------------|
| `0xb100` | 100 系列架构 |
| `0xb104` | 104 系列架构 |
| `0xb106` | 106 系列架构 |

### Warning Control

```bash
# 忽略所有警告
export BIREN_SIM_WARNING_FOR=ignore

# 将所有警告当作错误处理
export BIREN_SIM_WARNING_FOR=error
```

### Hang Timeout

```bash
# 设置延时为 10 秒（默认 5 秒，设为 0 关闭）
export BIREN_SIM_HANG_TIMEOUT=10
```

### Device Memory Size

```bash
# 修改预分配内存容量（默认 4096 MB）
export BR_UMD_SIM_DEVICE_MEM_SIZE=8192
```

## Usage

```bash
# 配置环境变量
export BR_UMD_BACKEND=simulator

# 运行程序
./your_biren_program
```

## Exception Types

| Type | Prefix | Description |
|------|--------|-------------|
| 输入错误 | `error` | 可通过调整输入解决 |
| 故障 | `fatal` | brSimulator 内部问题 |
| 未支持 | `unsupported` | 已知未支持的功能 |
| 警告 | `warning` | 不会终止仿真 |

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `no device` | 未成功使能 brSimulator | 检查 `BR_UMD_BACKEND=simulator` |
| `memory allocation failed` | device memory 超出预分配容量 | 使用 `BR_UMD_SIM_DEVICE_MEM_SIZE` |

## Unsupported Features

- 多 Device 特性（多卡协同、数据共享、卡间同步等）
- Non-UVA 访存
- 多 Kernel 数据传递
- 指令 latency
- 指令 pipeline
- 缓存行为
- 硬件未定义行为
- 内存初始化（未初始化内存初始化为 0）
- Sync Channel
- 特殊数据类型（int4、float8）
- 纹理数据和内存
- 硬件 errata
- L2Pad 内存

## Use Cases

### Development Without Hardware

在没有物理 GPU 的情况下开发和测试代码。

### Debugging

使用仿真器进行调试，比实际硬件更易发现问题。

### CI/CD

在 CI/CD 流程中运行测试，无需真实 GPU。

## Performance

- 比实际硬件慢
- 适合功能验证
- 不适合性能测试

## Notes

- brSimulator 会将未初始化内存初始化为 0
- 结果应与实际硬件对比验证
- 某些行为可能与实际硬件不同

## Related Tools

- **suDebugger**: 基于仿真器的调试器
- **suSanitizer**: 基于仿真器的检查工具
- **BRCC**: 编译器