---
name: mxtraining
description: 沐曦AI训练用户指南，涵盖PyTorch/TensorFlow/PaddlePaddle在曦云GPU上的训练流程、数据加载、优化配置等。
keywords:
  - 沐曦
  - AI训练
  - mxtraining
  - PyTorch
  - 深度学习训练
---

# AI训练用户指南

曦云GPU AI训练完整流程。

## 快速开始

### 环境准备

```bash
# 安装驱动（见mxdriver）
# 安装MXMACA
# 安装PyTorch
pip install mcpytorch
```

### 基础训练

```python
import torch

# 检查GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using {device}")

# 简单训练
model = Model().to(device)
optimizer = torch.optim.Adam(model.parameters())
criterion = torch.nn.CrossEntropyLoss()

for data, target in dataloader:
    data, target = data.to(device), target.to(device)
    optimizer.zero_grad()
    output = model(data)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

## 分布式训练

### 数据并行

```python
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# 初始化
dist.init_process_group(backend='mccl')

# 包装模型
model = DDP(model)
```

### 混合精度训练

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

with autocast():
    output = model(data)
    loss = criterion(output, target)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

## 数据加载

### GPU数据加载

```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=64,
    num_workers=4,
    pin_memory=True
)
```

## 优化技巧

### 显存优化

```python
# 梯度检查点
torch.utils.checkpoint.checkpoint(model, x)

# 混合精度
model = model.half()
```

## 官方参考

- 《曦云系列通用GPU AI训练用户手册》