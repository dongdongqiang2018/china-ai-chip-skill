---
name: muxiskills
description: 沐曦（Metax）国产GPU芯片 Skills 集合，提供 C500 系列 GPU 的设备管理、算力测试、通信库配置、CUDA 兼容层安装、集群巡检和 PD 分离部署等完整运维能力。
keywords:
  - 沐曦
  - Metax
  - C500
  - GPU
  - 算力测试
  - 分布式训练
---

# 沐曦 (Metax) GPU Skills

沐曦国产 GPU 芯片的专用 Agent Skills 集合，面向 C500 系列 GPU 的运维场景。

## 可用 Skills

| Skill | 功能说明 |
|-------|----------|
| [mx-smi](skills/mx-smi/) | GPU 设备管理，实时监控 |
| [mx-vs](skills/mx-vs/) | 算力测试，压力测试 |
| [mx-mccl](skills/mx-mccl/) | MCCL 通信库配置与测试 |
| [mx-cu-bridge](skills/mx-cu-bridge/) | CUDA 兼容层安装配置 |
| [mx-cluster-inspector](skills/mx-cluster-inspector/) | 集群自动化巡检 |
| [mx-pd-deploy](skills/mx-pd-deploy/) | PD 分离推理部署 |

## 快速开始

```bash
# 查看 GPU 状态
mx-smi

# 运行算力测试
mxvs ops -m fp16

# 压力测试
mxvs stress -t 300

# 查看拓扑
mx-smi topo --show-mxlk
```

## 核心工具

| 工具 | 路径 | 用途 |
|------|------|------|
| mx-smi | /usr/local/bin/mx-smi | GPU 设备管理 |
| mxvs | /opt/maca/bin/mxvs | 算力测试 |
| MCCL | /opt/maca/tools/mccl | 通信库 |
| cu-bridge | /opt/maca/tools/cu-bridge | CUDA 兼容层 |
| mx-cci | /opt/maca/tools/mccl/inspector/mx-cci | 集群巡检 |

## 相关文档

- [沐曦官方文档](https://www.metax-tech.com/)
- [芯片文档目录](../../china-ai-chip-docs/MUXI/)
- [返回主入口](../SKILL.md)