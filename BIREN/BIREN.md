---
name: birenskills
description: 壁仞（BIREN）国产GPU芯片 Skills 集合，提供 BIRENSUPA SDK、GPU 设备管理、通信库配置、容器工具包和数据中心监控等完整运维能力。
keywords:
  - 壁仞
  - BIREN
  - brsmi
  - suCCL
  - GPU
---

# 壁仞 (BIREN) GPU Skills

壁仞国产 GPU 芯片的专用 Agent Skills 集合，面向 BIRENSUPA 系列 GPU 的运维场景。

## 可用 Skills

| Skill | 功能说明 |
|-------|----------|
| [brsmi](skills/brsmi/) | GPU 设备管理，实时监控 |
| [biren-sdk](skills/biren-sdk/) | BIRENSUPA SDK 安装配置 |
| [succl](skills/succl/) | suCCL 通信库配置与测试 |
| [biren-container](skills/biren-container/) | 容器工具包安装配置 |
| [sudcGM](skills/sudcGM/) | 数据中心 GPU 监控 |

## 快速开始

```bash
# 查看 GPU 状态
brsmi

# 监控 GPU
brsmi gpu dmon

# 查看拓扑
brsmi topo --p2p
```

## 核心工具

| 工具 | 路径 | 用途 |
|------|------|------|
| brsmi | /usr/local/birensupa/bin/brsmi | GPU 设备管理 |
| brsw | /usr/local/birensupa/container-toolkit/bin/brsw | 容器工具 |
| suDCGM | /usr/local/birensupa/bin/sudcGM | 数据中心监控 |
| suCCL | /usr/local/birensupa/succl | 通信库 |

## 相关文档

- [壁仞官方文档](https://www.biren.tech/)
- [芯片文档目录](../../china-ai-chip-docs/BIREN/)
- [返回主入口](../SKILL.md)