---
name: mcpytorch
description: 沐曦PyTorch后端，为PyTorch提供曦云GPU支持。支持CUDA API兼容接口，PyTorch代码无需修改即可运行在沐曦GPU上。
keywords:
  - 沐曦
  - PyTorch
  - mcpytorch
  - 深度学习
  - GPU后端
  - AI训练
---

# mcPyTorch 用户指南

mcPyTorch为PyTorch提供曦云GPU后端支持，兼容CUDA API，PyTorch代码无需修改即可运行。

## 快速开始

### 安装

```bash
# 通过pip安装
pip install mcpytorch

# 或使用预编译wheel
pip install /opt/maca/wheel/mcpytorch-*.whl
```

### 验证安装

```python
import torch
print(torch.cuda.is_available())  # 检查是否识别
print(torch.cuda.device_count())  # GPU数量
print(torch.cuda.get_device_name(0))  # 设备名称
```

### 基本使用

```python
import torch

# 检查GPU可用
if torch.cuda.is_available():
    # 设置设备
    device = torch.device('cuda')
    
    # 创建张量
    x = torch.randn(1000, 1000).to(device)
    y = torch.randn(1000, 1000).to(device)
    
    # 计算
    z = torch.matmul(x, y)
    
    print("计算完成")
```

## 设备管理

```python
# 设置默认设备
torch.cuda.set_device(0)

# 获取当前设备
current = torch.cuda.current_device()

# 设备属性
props = torch.cuda.get_device_properties(0)
print(props.name, props.total_memory)
```

## 内存管理

```python
# 缓存清理
torch.cuda.empty_cache()

# 显存统计
print(torch.cuda.memory_allocated())
print(torch.cuda.memory_reserved())

# 显存管理
with torch.cuda.memory.accumulate_memory():
    # 执行操作
    pass
```

## 数据并行

```python
import torch.nn as nn

model = nn.Linear(100, 10).cuda()
model = nn.DataParallel(model)

# 或
model = nn.parallel.DistributedDataParallel(model)
```

## AMP混合精度

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in dataloader:
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## 常用环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| CUDA_VISIBLE_DEVICES | GPU设备ID | 0 |
| PYTORCH_DEFAULT_NCHW | 默认NCHW布局 | 1 |

## 已支持功能

- torch.Tensor (所有基本操作)
- torch.nn (常见层)
- torch.autograd
- torch.cuda (设备管理)
- torch.backends.cudnn
- torch.distributed
- torch.amp (混合精度)
- torch.optim

## 官方参考

- 《曦云系列通用GPU mcPyTorch用户指南》
- MXMACA SDK