---
name: biren-placeholder
description: 壁仞科技(Biren) GPU Skills占位目录。用于存放壁仞GPU相关的FAE技能。
keywords:
  - Biren
  - 壁仞
  - BR100
  - BR104
  - GPU
  - 人工智能
---

# 壁仞(Biren) Skills

本目录用于存放壁仞科技GPU的相关Skills。

## 目录结构

```
BIREN/
├── (待添加Skills)
```

## 待添加内容

### 基础管理工具

- `biren-smi` - 设备管理工具
- `biren-toolkit` - 壁仞工具包

### 编程接口

- `biren-runtime` - 运行时API
- `biren-ccl` - 集合通信库

### 开发工具

- `biren-compiler` - 编译工具链
- `biren-profiler` - 性能分析工具

## 快速参考

### 查看设备

```bash
# 列出设备（需要安装对应驱动后）
biren-cli list-devices

# 查看设备状态
biren-smi
```

### 环境配置

```bash
# 设置环境变量
export BIREN_HOME=/opt/biren
export LD_LIBRARY_PATH=$BIREN_HOME/lib:$LD_LIBRARY_PATH
```

## 参考资源

- 壁仞科技官方文档（待补充）
- Biren SDK文档（待补充）

## 备注

本目录用于后续添加壁仞科技相关Skills。当前壁仞科技主要产品包括：
- BR100系列
- BR104系列

如需了解最新信息，请访问壁仞科技官方网站。