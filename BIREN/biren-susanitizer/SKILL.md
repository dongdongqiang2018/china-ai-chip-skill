---
name: biren-susanitizer
description: BIREN suSanitizer 检查工具参考指南。提供 Memcheck、Synccheck、Racecheck 三种检查工具，用于检测 BIRENSUPA 代码中的内存访问错误、同步操作错误、数据竞争问题，帮助发现潜在的编程错误。
keywords:
  - susanitizer
  - biren
  - 检查工具
  - sanitizer
  - 内存检查
  - 同步检查
  - 壁仞
---

# suSanitizer Command Reference

suSanitizer 工具用于检查 BIRENSUPA 代码中可能出现的功能异常操作。

## Quick Start

```bash
# 调用所有工具进行检查
supa-sanitizer test

# 调用 memcheck 工具
supa-sanitizer --tool=memcheck test

# 调用 synccheck 工具
supa-sanitizer --tool=synccheck test

# 调用 racecheck 工具
supa-sanitizer --tool=racecheck test
```

## Installation

默认安装路径：`/usr/local/birensupa/sdk/latest/supa-sanitizer/bin`

验证安装：
```bash
$ supa-sanitizer --version
Biren Technology, Inc.
  supa-sanitizer version: 0.5.1
```

## Tools

### Memcheck

对设备内存的细粒度管理来捕获内存访问行为，可检测：
- 程序访问 TLM（Thread Local Memory）内存溢出
- 程序访问 GSM（Group Shared Memory）内存溢出
- 程序访问 GLM（Global Memory）内存溢出
- 程序访问 TLM 及 GSM 内存非对齐地址
- 程序访问 TLM、GSM、GLM 内存非法地址

### Synccheck

识别应用程序是否使用了正确的同步操作，可检测：
- 程序运行时由于 hang 被挂起的行为
- sync thread/warp 操作非法行为
- T-Core GSC（GEMM Sync Channel）非法状态转移
- T-Core GSC 运行结束时状态未恢复

### Racecheck

检查代码中是否出现数据竞争问题，可检测：
- GSM 内存访问数据竞争的行为

## Command Options

| Option | Description |
|--------|-------------|
| `--version` | 打印软件版本信息 |
| `--tool=<memcheck\|synccheck\|racecheck\|allcheck>` | 指定需要使能的工具 |
| `--execution-file=<filename-path>` | 指定包含 BIREN device code 的文件路径 |
| `--device=<device-id>` | 指定程序运行的 BIREN 硬件版本 |
| `--help` | 查看帮助信息 |

### Device Options

| Device ID | Description |
|-----------|-------------|
| `br106` | 默认值 |
| `br166` | BR166 |
| `br106` | BR106 |

## Usage

### Basic Usage

```bash
# 完整检查
supa-sanitizer test_program

# 指定工具
supa-sanitizer --tool=memcheck test_program
supa-sanitizer --tool=synccheck test_program
supa-sanitizer --tool=racecheck test_program

# 指定设备
supa-sanitizer --device=br106 test_program
```

### Compilation

目标程序准备：建议使用 `-G` 选项编译，以提供准确的源程序位置信息。

```bash
# 编译测试程序
brcc -G test.su -o test
```

## Memcheck Errors

| Error Message | Description |
|---------------|-------------|
| `Thread local memory (TLM) access overflow` | 访问 TLM 内存溢出 |
| `Group shared memory (GSM) access overflow` | 访问 GSM 内存溢出 |
| `Global memory (GLM) access overflow` | 访问 GLM 内存溢出 |
| `Unaligned address` | 访问内存的地址未对齐 |
| `Invalid USharp alignment` | 使用 U# 访问内存的数据未对齐 |
| `Invalid address` | 访问非法地址 |

## Synccheck Errors

| Error Message | Description |
|---------------|-------------|
| `Program hang detected` | 程序运行时由于 hang 被挂起 |
| `Illegal sync operation` | sync thread/warp 操作非法 |
| `Illegal GSC state transition` | T-Core GSC 非法状态转移 |
| `GSC state not restored` | T-Core GSC 运行结束时状态未恢复 |

## Racecheck Errors

| Error Message | Description |
|---------------|-------------|
| `GSM data race detected` | GSM 内存访问数据竞争 |

## Example

```bash
# 编译
brcc -G vector_add.su -o vector_add

# 运行检查
supa-sanitizer --tool=memcheck ./vector_add

# 输出示例
== RUNNING Test ==
== Memcheck: TLM access overflow at kernel:vectorAdd ==
== TLM access overflow at address 0x7f8c00000000 ==
```

## Notes

- 需要使用 `-G` 选项编译以提供准确的源程序位置信息
- 基于 brSimulator 实现
- 检查会影响性能，建议在开发阶段使用
- 某些检测可能产生误报

## Related Tools

- **brSimulator**: 仿真器
- **suDebugger**: 调试器
- **BRCC**: 编译器