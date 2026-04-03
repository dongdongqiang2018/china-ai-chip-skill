---
name: biren-suprof
description: BIREN suProfiler 性能分析工具参考指南。用于采集和分析 GPU 性能数据，支持 System 模式和 Compute 模式，采集 API 调用、Kernel 执行、硬件计数器等数据，配合 suProfiler UI 可视化分析。
keywords:
  - suprof
  - biren
  - 性能分析
  - profiler
  - 性能优化
  - 硬件计数器
  - 壁仞
---

# suProfiler Command Reference

suProfiler 是壁仞跨平台 GPU 性能分析工具。

## Quick Start

```bash
# System 模式 - 整网性能分析
suprof --process-filter=python --collect-counter=hbmc \
  --collect-counter-interval=20 --trace=supa,sutx,sudnn \
  python -u src/train_softmax.py

# Compute 模式 - 单 kernel 分析
suprof --process-filter=python \
  --compute="_7rnel0_fused2_conv_fwd_1:1" \
  python -u src/train_softmax.py
```

## Components

| Component | Description |
|-----------|-------------|
| suProf | Linux 后端采集程序 (suPTI) |
| suProfiler UI | 前端图形展示工具 |

## Supported OS

| OS | Kernel Version | GPU |
|----|----------------|-----|
| Ubuntu 22.04 | 5.15.0-97 | 壁砺™106B/106C |
| Ubuntu 20.04 | 5.15.0-52 | 壁砺™106B/106C |
| openEuler 22.03 | 10.0-60.18.0.50 | 壁砺™106B/106C |
| CGSL 6.06 | 5.10.134-13.1 | 壁砺™106B/106C |
| BCLinux for Euler 21.10 | 4.19.90 | 壁砺™106B/106C |

## suProf Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--process-filter` | - | 目标程序（如 python） |
| `-t, --trace` | supa,sudrv,sutx | 追踪的 API 模块 |
| `--collect-counter` | none | counter 类型 (hbmc/ha/meminfo/none) |
| `--collect-counter-interval` | 1000ms | counter 采样间隔 |
| `-c, --capture-range` | none | 采集范围控制 |
| `-y, --delay` | - | 延迟启动（秒） |
| `-d, --duration` | - | 采集时长（秒） |
| `--api-trace-mode` | none | 抓取模式 (none/host/host-cpts) |
| `--graph-mode` | g | Graph 追踪模式 (g/k/m) |
| `-O, --output-directory` | /run/suprof/ | 输出路径 |
| `--compress` | - | 压缩 .raw 文件 |

### Trace Modules

| Module | Description |
|--------|-------------|
| `supa` | SUPA Runtime API |
| `sudrv` | SUPA Driver API |
| `sutx` | suTX API |
| `sudnn` | suDNN API |
| `sublas` | suBLAS API |
| `succl` | suCCL API |
| `sufft` | suFFT API |
| `surand` | suRand API |

### Capture Range

| Value | Description |
|-------|-------------|
| `none` | 全量采集 |
| `supaProfilerApi` | 使用 suProfiler API 控制 |

## Data Collection

### Output Files

- `suprof_event-xxxx.log` - API 追踪日志
- `suprof_spc_counter-xxxx.raw` - SPC counter 数据

### Parse Raw Data

```bash
python3 parse_ptiraw.py <RawFilePath>/suprof_spc_counter-XXXX.raw
```

### Output CSV Files

- `1_perf_dump_spc0.csv` - SPC counter 数据
- `perf_dump_ha.csv` - PCIE 性能计数

## DR.Perf CLI

```bash
# 基本用法
doctor_perf -i suprof_spc_counter-24239.raw

# 指定输出文件
doctor_perf -o myout.txt -i <spc raw file>
```

### Key Metrics

| Metric | Description |
|--------|-------------|
| `elapsed_cycles_spc.avg/max/min` | SPC 活动 cycles |
| `elapsed_cycles_eu.avg/max` | EU 活动 cycles |
| `elapsed_cycles_gemm.avg/max` | GEMM 活动 cycles |
| `elapsed_cycles_tcore.avg/max` | Tcore 活动 cycles |
| `eu_utilization.avg/max/min` | EU 利用率 |
| `gemm_util_rate.avg` | GEMM 利用率 |
| `ipc.avg` | 每时钟周期执行指令数 |
| `l2_read/write_hit_rate` | L2 缓存命中率 |

## suProfiler UI

### System Mode (Timeline View)

| Area | Description |
|------|-------------|
| 时间轴 | 全局时间轴 + 当前时间轴 |
| 层次化树形列表 | Processes/Devices/CPU |
| 时序视图 | 折线图或柱状图 |
| 统计表面板 | 框选数据详情 |
| 详情面板 | 统计信息、调用栈、拓扑图 |

### Compute Mode (Kernel View)

| View | Content |
|------|---------|
| Compute Analysis | VCore/TCore 指令数、Active Cycles |
| Memory Analysis | 各级缓存读写带宽 |
| Roofline Chart | 计算强度 vs 浮点性能 |

## Range Profiling

### Code-based

```cpp
suProfilerStart();
// ... 需要分析的代码段 ...
suProfilerStop();
```

### Command-based

```bash
suprof -c supaProfilerApi ./a.out
```

## suProfX Interactive

```bash
export ENABLE_COMM=1
suprof --enable_socket_comm ./<yourapplication>
suprofX  # 启动控制台控制采集
```

## Graph Mode

| Mode | Description |
|------|-------------|
| `g` | 只追踪 graph 调度执行 |
| `k` | 追踪 graph 内部每个核函数 |
| `m` | 追踪 graph 和内部核函数 |

## Examples

### Profile Python Training

```bash
suprof --process-filter=python --collect-counter=hbmc \
  --trace=supa,sudnn,sudrv python train.py
```

### Profile Specific Kernel

```bash
suprof --process-filter=python \
  --compute="conv2d_forward_kernel:1" python train.py
```

### API Trace Only

```bash
suprof --api-trace-mode=host ./test_supti
```

## Notes

- 需要 root 权限
- 采集大量数据会影响性能
- 合理设置采集范围和时长

## Related Tools

- **suPTI**: 性能追踪接口
- **suPerfViz**: 可视化分析工具
- **suTX**: 代码标记接口