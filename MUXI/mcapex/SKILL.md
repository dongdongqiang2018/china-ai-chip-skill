---
name: mcapex
description: 沐曦分布式工具，提供多GPU节点通信和协作功能，支持分布式训练的数据同步和参数聚合。
keywords:
  - 沐曦
  - mcapex
  - 分布式
  - 数据同步
  - 参数聚合
---

# mcApex 用户指南

mcApex提供分布式训练工具。

## 快速开始

### 安装

```bash
pip install mcapex
```

### 基本使用

```python
import torch
from mcapex import DistributedOptimizer, DistributedModel

# 分布式模型
model = DistributedModel(model)

# 分布式优化器
optimizer = DistributedOptimizer(optimizer)
```

## 功能

### 梯度同步

```python
# 自动梯度同步
loss.backward()
optimizer.step()
```

### 混合精度

```python
from mcapex import AMP

with AMP(loss_scaler):
    output = model(input)
    loss.backward()
```

### 通信优化

```python
# 梯度压缩
optimizer = DistributedOptimizer(optimizer, compression='powerSGD')
```

## 官方参考

- 《曦云系列通用GPU mcApex用户指南》