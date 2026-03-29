---
name: china-ai-chip-skill
description: 国产AI芯片 Agent Skills 统一入口 Skill，提供硬件自动识别、Skill 路由和跨平台运维能力。支持沐曦(Metax)、昇腾(Ascend)等国产GPU/NPU 芯片的设备管理、算力测试、通信库配置、推理部署等场景，自动识别当前硬件环境并调用对应的专业 Skills。
keywords:
  - 国产芯片
  - AI芯片
  - GPU
  - NPU
  - 沐曦
  - 昇腾
  - Metax
  - Ascend
  - Skill路由
  - 硬件识别
---

# 国产AI芯片 Agent Skills

## 功能描述

本仓库提供统一的国产 AI 芯片 Agent Skills 框架，自动识别服务器硬件环境并路由到对应的专业 Skills。

## 核心能力

### 1. 硬件自动识别

自动检测当前服务器上的国产 AI 芯片类型。

```bash
# 自动识别硬件
detect-hardware

# 手动指定硬件类型
set-hardware muxi    # 沐曦
set-hardware ascend  # 昇腾
```

**支持的硬件：**
| 硬件 | 目录 | 主要工具 |
|------|------|----------|
| 沐曦 (Metax) | MUXI/ | mx-smi, mxvs, MCCL |
| 昇腾 (Ascend) | ASCEND/ | npu-smi, npu info |

### 2. 硬件路由

根据识别的硬件类型，自动跳转到对应的 Skills 目录。

```
当前硬件: 沐曦 (Metax) C500X
         ↓
路由到:   MUXI/skills/
         ├── mx-smi      (GPU设备管理)
         ├── mx-vs           (算力测试)
         ├── mx-mccl         (通信库)
         ├── mx-cu-bridge    (CUDA兼容层)
         ├── mx-cluster-inspector (集群巡检)
         └── mx-pd-deploy    (PD分离部署)
```

### 3. 统一运维入口

无论什么硬件，都通过统一的命令接口访问。

```bash
# 查看设备状态（自动路由到对应工具）
# 沐曦 -> mx-smi
# 昇腾 -> npu-smi

show-status

# 运行算力测试
# 沐曦 -> mxvs
# 昇腾 -> npu-perf

run-benchmark

# 集群巡检
# 沐曦 -> mx-cci
# 昇腾 -> ascend-inspector

cluster-inspect
```

## 支持的硬件平台

### 沐曦 (Metax)

- **产品系列**: C500X, C500, C550, C588
- **官方工具**: mx-smi, mxvs, MCCL
- **SDK**: MACA SDK
- **Skills 目录**: [MUXI/skills/](MUXI/skills/)

| Skill | 功能说明 |
|-------|----------|
| [mx-smi](MUXI/skills/mx-smi/) | GPU设备管理，实时监控 |
| [mx-vs](MUXI/skills/mx-vs/) | 算力测试，压力测试 |
| [mx-mccl](MUXI/skills/mx-mccl/) | MCCL通信库配置与测试 |
| [mx-cu-bridge](MUXI/skills/mx-cu-bridge/) | CUDA兼容层安装配置 |
| [mx-cluster-inspector](MUXI/skills/mx-cluster-inspector/) | 集群自动化巡检 |
| [mx-pd-deploy](MUXI/skills/mx-pd-deploy/) | PD分离推理部署 |

### 昇腾 (Ascend)

- **产品系列**: 910A, 910B, 310P
- **官方工具**: npu-smi, npu info
- **SDK**: CANN
- **Skills 目录**: [ASCEND/skills/](ASCEND/skills/) *(规划中)*

## 项目结构

```
china-ai-chip-skill/
├── SKILL.md                    # 本文件 - 仓库级入口
├── package.json
├── .github/workflows/validate.yml
├── scripts/
│   └── validate_skills.py     # Skill 校验脚本
├── template/
│   └── SKILL.md               # Skill 模板
├── MUXI/                      # 沐曦 Skills
│   ├── MUXI.md
│   └── skills/
│       ├── mx-smi/
│       ├── mx-vs/
│       ├── mx-mccl/
│       ├── mx-cu-bridge/
│       ├── mx-cluster-inspector/
│       └── mx-pd-deploy/
└── ASCEND/                    # 昇腾 Skills *(规划中)*
    ├── ASCEND.md
    └── skills/
```

## 快速开始

### 1. 安装依赖

```bash
npm install
# 或
pip install pyyaml
```

### 2. 验证 Skills

```bash
# 校验所有 Skills
python scripts/validate_skills.py

# 或
npm run validate
```

### 3. 使用 Skills

根据你的硬件选择对应的 Skill：

**沐曦用户：**
- [GPU设备管理](MUXI/skills/mx-smi/) - mx-smi 使用指南
- [算力测试](MUXI/skills/mx-vs/) - mxvs 性能测试
- [通信库配置](MUXI/skills/mx-mccl/) - MCCL 分布式训练
- [开发环境搭建](MUXI/skills/mx-cu-bridge/) - cu-bridge 安装
- [集群巡检](MUXI/skills/mx-cluster-inspector/) - mx-cci 工具
- [推理部署](MUXI/skills/mx-pd-deploy/) - PD分离部署

## 规范

- 所有 Skill 必须放在 `skills/` 目录下
- 目录采用 kebab-case 扁平化命名
- 每个 Skill 目录内**只能有** SKILL.md 和可选的 references/ 子目录
- **禁止**在 Skill 目录内放置 README.md
- SKILL.md 开头必须是 YAML frontmatter（name、description ≥40字、keywords 数组）

## 相关链接

- [昇腾官方 Skills](https://gitcode.com/Ascend/agent-skills)
- [awesome-ascend-skills](https://github.com/ascend-ai-coding/awesome-ascend-skills)
- [沐曦官网](https://www.metax-tech.com/)
- [昇腾官网](https://www.huawei.com/cn/ascend/)