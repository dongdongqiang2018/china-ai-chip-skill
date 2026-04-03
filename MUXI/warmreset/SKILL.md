---
name: warmreset
description: 沐曦GPU热复位工具，用于在不重启系统的情况下复位GPU。用于故障恢复和驱动刷新场景。
keywords:
  - 沐曦
  - 热复位
  - warmreset
  - GPU复位
  - 故障恢复
---

# Warm Reset 使用指南

Warm Reset允许在不重启系统的情况下复位曦云GPU。

## 快速开始

### 基本用法

```bash
# 查看GPU列表
mx-smi -L

# 热复位单个GPU
sudo mx-smi --id=0 --warm-reset

# 热复位所有GPU
sudo mx-smi --warm-reset
```

### 检查状态

```bash
# 查看GPU状态
mx-smi

# 查看复位状态
mx-smi --id=0 --query-gpu=state
```

## 使用场景

### 驱动异常

```bash
# 驱动无响应时复位
sudo mx-smi --id=0 --warm-reset
```

### 显存泄漏

```bash
# 显存无法释放时复位
sudo mx-smi --id=0 --warm-reset
```

### 性能恢复

```bash
# 性能下降时恢复
sudo mx-smi --id=0 --warm-reset
```

## 注意事项

1. 复位前确保无重要任务运行
2. 复位会终止GPU上所有进程
3. 需要sudo权限

## 官方参考

- 《曦云系列通用GPU Warm Reset使用指南》