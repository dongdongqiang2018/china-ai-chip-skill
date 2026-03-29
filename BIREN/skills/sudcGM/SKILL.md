---
name: sudcGM
description: 壁仞（BIREN）suDCGM 数据中心 GPU 管理器 Skill，提供 GPU 数量查询、功耗/温度/时钟频率/吞吐率等监控能力。suDCGM（Data Center Graphic Monitor）是壁仞官方的数据中心级 GPU 监控工具，用于大规模 GPU 集群的集中管理和监控。
keywords:
  - biren
  - 壁仞
  - suDCGM
  - DCGM
  - 监控
  - 数据中心
---

# suDCGM 壁仞数据中心GPU监控

## 功能描述

suDCGM（Data Center Graphic Monitor）是壁仞官方提供的数据中心级 GPU 监控工具，可用于查询服务器端的 GPU 数量和 GPU 信息，包括功耗、温度、时钟频率、PCIe 吞吐率等。适用于大规模 GPU 集群的集中监控和管理。

## 核心能力

### 1. 基础查询

```bash
# 查看版本
sudcGM --version

# 查询 GPU 列表
sudcGM --query-gpulist

# 查询所有 GPU 信息
sudcGM --query-gpu

# 查询指定 GPU 信息
sudcGM --query-gpu -i 0
```

### 2. 监控指标

```bash
# 查询功耗
sudcGM --query-gpu -i 0 --metrics power.usage

# 查询温度
sudcGM --query-gpu -i 0 --metrics temperature.gpu

# 查询利用率
sudcGM --query-gpu -i 0 --metrics utilization.gpu

# 查询显存
sudcGM --query-gpu -i 0 --metrics memory.used

# 查询时钟频率
sudcGM --query-gpu -i 0 --metrics clock.sm

# 查询 PCIe 吞吐
sudcGM --query-gpu -i 0 --metrics pcie.txthroughput
```

### 3. 实时监控模式

```bash
# 启用监控
sudcGM --loop

# 设置刷新间隔
sudcGM --loop 1000  # 1000ms

# 导出为文件
sudcGM --loop > gpu_monitor.log
```

### 4. 配置管理

```bash
# 导出配置
sudcGM --export-config config.txt

# 导入配置
sudcGM --import-config config.txt
```

### 5. 告警配置

```bash
# 设置告警阈值
sudcGM --set-threshold temperature.gpu=85
sudcGM --set-threshold power.usage=350
sudcGM --set-threshold memory.used=90
```

## 与 brsmi 的区别

| 特性 | suDCGM | brsmi |
|------|--------|-------|
| 用途 | 数据中心级监控 | 单机设备管理 |
| 功能 | 指标收集、告警 | 设备控制、配置 |
| 适用场景 | 集群监控 | 本地调试 |
| API | 远程调用 | 本地命令行 |

## 常见场景

### 场景1：集群状态监控

```bash
# 定期查询集群状态
sudcGM --query-gpu --format csv

# 监控所有 GPU
sudcGM --loop -d 5000  # 每5秒刷新
```

### 场景2：性能基线收集

```bash
# 持续收集指标
sudcGM --loop > baseline_$(date +%Y%m%d).log

# 分析历史数据
python analyze.py baseline_20240101.log
```

### 场景3：告警通知

```bash
# 设置告警
sudcGM --set-threshold temperature.gpu=80

# 启用告警输出
sudcGM --loop --alert

# 配置外部告警
sudcGM --set-alert-webhook http://monitoring:9090/alerts
```

## 故障排查

### 问题1：无法连接

**症状：** suDCGM 连接失败

**排查步骤：**
```bash
# 1. 检查 GPU 状态
brsmi

# 2. 检查服务
systemctl status sudcGM

# 3. 重启服务
sudo systemctl restart sudcGM
```

## 相关文档

- [壁仞_01安装（环境搭建）](../../china-ai-chip-docs/BIREN/壁仞_01安装（环境搭建）.md)
- [壁仞_07GPU管理与测试](../../china-ai-chip-docs/BIREN/壁仞_07GPU管理与测试.md)
- [brsmi](./brsmi/) - GPU 设备管理