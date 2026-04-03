---
name: mxaiforscience
description: 沐曦AI for Science应用指南，支持科学计算应用（如分子动力学、物理仿真）的GPU加速。包括PhysicsNeMo、DeepXDE、Warp等。
keywords:
  - 沐曦
  - AI for Science
  - mxaiforscience
  - 科学计算
  - 分子动力学
  - 物理仿真
---

# AI for Science 应用指南

沐曦GPU在科学计算领域的应用支持。

## 支持的框架

### 分子动力学

| 框架 | 说明 |
|------|------|
| OpenMM | 分子动力学模拟 |
| DeepMD | 深度学习分子动力学 |
| LAMMPS | 大规模原子/分子模拟 |

### 物理仿真

| 框架 | 说明 |
|------|------|
| DeepXDE | 深度学习PDE求解 |
| Simnet | 物理信息神经网络 |
| Warp | 粒子仿真 |

### 图神经网络

| 框架 | 说明 |
|------|------|
| DGL | 图神经网络 |
| PyG | PyTorch Geometric |

## 快速开始

### 安装

```bash
# 安装支持包
pip install mx-aiforscience

# 或使用Docker
docker run -it metax/aiforscience:latest
```

### 运行环境

```bash
# 设置环境
source /opt/maca/env.sh
```

## 官方参考

- 《曦云系列通用GPU AI for Science应用用户手册》