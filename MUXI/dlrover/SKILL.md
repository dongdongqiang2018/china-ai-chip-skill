---
name: dlrover
description: 沐曦深度学习训练加速工具，支持弹性训练、自动故障恢复、动态资源调度等企业级分布式训练能力。
keywords:
  - 沐曦
  - DLRover
  - dlrover
  - 分布式训练
  - 弹性训练
  - 故障恢复
---

# DLRover 使用指南

DLRover提供企业级分布式训练能力，包括弹性训练、故障恢复、动态资源调度。

## 快速开始

### 安装

```bash
pip install dlrover
```

### 基本使用

```bash
# 启动elastic训练
dlrover-run --num_nodes=4 --max_node=8 python train.py
```

## 功能

### 弹性训练

```python
from dlrover.trainer import ElasticTrainer

trainer = ElasticTrainer()
trainer.prepare()

# 动态调整
trainer.scale(6)  # 扩展到6节点
trainer.scale(3)  # 收缩到3节点
```

### 故障恢复

```python
# 自动检查点
trainer.enable_auto_checkpoints()

# 故障后恢复
trainer.recover()
```

### 资源调度

```yaml
# dlrover job配置
apiVersion: dlrover.com/v1
kind: ElasticJob
metadata:
  name: training-job
spec:
  replicaSpecs:
    chief:
      replicas: 1
    worker:
      replicas: 4
      minReplicas: 1
      maxReplicas: 8
```

## 官方参考

- 《曦云系列通用GPU DLRover使用手册》