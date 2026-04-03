---
name: biren-superfviz
description: BIREN suPerfViz (DRPERFVIZ) 可视化性能分析工具参考指南。基于 Web 的性能指标数据可视化工具，用于查看 GPU kernel 级别的性能分析结果，支持 Home/Configure/Net/Kernel 多视图分析。
keywords:
  - superfviz
  - drperfviz
  - biren
  - 性能可视化
  - profiler
  - GPU分析
  - 壁仞
---

# suPerfViz Command Reference

suPerfViz (DRPERFVIZ) 是一款基于 Web 的性能指标数据可视化工具。

## Quick Start

```bash
# 启动服务
drperfviz_srv -d {path/to/the/drperf/database}

# 指定端口
drperfviz_srv -d llama_enc.db -p 8088

# 浏览器访问
http://<machine IP>:8087
```

## Installation

- 安装路径：`/usr/local/birensupa/sdk/latest/suPerfViz/`
- 环境设置：`source /usr/local/birensupa/sdk/latest/scripts/brsw_set_env.sh`
- 默认端口：8087

## Architecture

```
采集 perf counter → 后处理（dump 解析、数据转换为 db file）→ 可视化（Viz）
```

## Data Source

drperf database 文件由 `doctor_perf` 后处理工具生成（详见 suProfiler 用户指南）。

## Views

### Home View

整网基于 kernel-name 聚合的性能指标：
- Top-K Piechart
- 利用率
- 时间表

### Configure View

设置分析范围：
- Range Slider：选择时间范围
- Dropdown：选择单个 kernel

### Net View

范围分析：
- TopK Pie/Table：Top K 分析
- Perf Warning Bubble：性能告警
- Roofline：Tcore & Vcore roofline

### Kernel View

单 kernel 多维度分析，包含 6 个子视图：

| Sub-View | Content |
|----------|---------|
| Perf Warnings | 性能告警指标 |
| Memory View | 内存访问相关 HW counters |
| Utilization View | HW Unit spent time、GEMM utilization、EU utilization |
| Stall View | 连接间 stalls、计算单元内部 stalls |
| Diagram | SVG 展示 traffic/bandwidth/stalls/utilizations |
| Metric View | 指定 metric 按 SPC ID 展示，支持两个 kernel 对比 |

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-d` | drperf database 路径 | 必需 |
| `-p` | 端口号 | 8087 |
| `-h` | 显示帮助 | - |

## Usage

### Step 1: 数据采集

使用 suProf 采集性能数据：

```bash
suprof --process-filter=python --collect-counter=hbmc \
  python train.py
```

### Step 2: 数据处理

使用 doctor_perf 生成 database：

```bash
doctor_perf -i suprof_spc_counter-XXXX.raw -o output.db
```

### Step 3: 可视化

启动 suPerfViz：

```bash
drperfviz_srv -d output.db
```

### Step 4: 查看结果

浏览器访问：`http://<machine IP>:8087`

## Key Metrics

### Performance Warnings

| Warning | Description |
|---------|-------------|
| Low EU Utilization | EU 利用率低 |
| High Stall Rate | 停顿率高 |
| Low Memory Bandwidth | 内存带宽低 |
| Low L2 Hit Rate | L2 命中率低 |

### Memory Metrics

| Metric | Description |
|--------|-------------|
| L1/L2 Cache Hit Rate | 缓存命中率 |
| Memory Read/Write Bandwidth | 内存读写带宽 |
| Global Memory Access | 全局内存访问 |

### Utilization Metrics

| Metric | Description |
|--------|-------------|
| EU Utilization | EU 利用率 |
| GEMM Utilization | GEMM 利用率 |
| TCore Utilization | TCore 利用率 |

### Stall Metrics

| Metric | Description |
|--------|-------------|
| Instruction Fetch Stall | 指令获取停顿 |
| Execution Dependency Stall | 执行依赖停顿 |
| Memory Dependency Stall | 内存依赖停顿 |

## Browser Interface

### Navigation

- 顶部导航栏：切换视图
- 左侧面板：kernel 列表和过滤器
- 主区域：图表展示
- 底部：详细信息

### Interactions

- Hover：查看详细数值
- Click：选中 kernel
- Drag：框选时间范围
- Scroll：缩放

## Export

支持导出分析报告为 PDF/PNG 格式。

## Integration

与 suProfiler 完整集成：
1. suProf 采集数据
2. doctor_perf 后处理
3. suPerfViz 可视化

## Notes

- 需要有效的 drperf database 文件
- 浏览器需支持 WebGL
- 大数据文件可能加载较慢

## Related Tools

- **suProfiler**: 性能分析工具
- **suPTI**: 性能追踪接口
- **doctor_perf**: 后处理工具