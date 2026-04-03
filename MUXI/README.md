# MUXI Skills 技能集合

沐曦（MetaX）曦云系列GPU的FAE辅助Skills集合，基于沐曦官方技术文档生成。

## 概述

本目录包含33个技能，覆盖沐曦GPU的运维工具、API库、开发框架、部署运维、通信分布式和应用层场景。

## 技能分类

### 1. 运维工具 (3个)

| 技能 | 说明 |
|------|------|
| [mx-smi](./mx-smi) | GPU设备管理工具，查询状态、功耗、温度等 |
| [mx-diagease](./mx-diagease) | 一键诊断工具，PCIe/内存/压测诊断 |
| [mx-exporter](./mx-exporter) | Prometheus监控指标导出 |
| [mcprofiler](./mcprofiler) | 可视化性能分析工具 |

### 2. API库 (7个)

| 技能 | 说明 |
|------|------|
| [mcblas](./mcblas) | BLAS线性代数库，矩阵运算核心 |
| [mcdnn](./mcdnn) | 深度神经网络库，卷积/池化/激活函数 |
| [mcfft](./mcfft) | 快速傅里叶变换库 |
| [mcrand](./mcrand) | 随机数生成库 |
| [mcsolver](./mcsolver) | 直接求解器，LU/QR/Cholesky/SVD |
| [mcsparse](./mcsparse) | 稀疏矩阵库 |
| [mcsolverit](./mcsolverit) | 迭代求解器，CG/GMRES/AMG |

### 3. 开发框架 (7个)

| 技能 | 说明 |
|------|------|
| [mxcc](./mxcc) | C/C++编译器，GPU程序编译 |
| [mxmaca](./mxmaca) | 软件栈核心，驱动/编译器/工具链 |
| [mxmaca-clangd](./mxmaca-clangd) | C语言服务，代码补全/跳转 |
| [mxmaca-api](./mxmaca-api) | 运行时API，设备/内存/流管理 |
| [mcpy](./mcpy) | Python绑定库 |
| [mcpytorch](./mcpytorch) | PyTorch后端，深度学习框架 |
| [mctriton](./mctriton) | Triton后端，JIT内核编译 |

### 4. 部署运维 (4个)

| 技能 | 说明 |
|------|------|
| [mxdriver](./mxdriver) | 驱动安装和固件更新 |
| [mxk8s](./mxk8s) | Kubernetes GPU调度部署 |
| [mxcloudnative](./mxcloudnative) | 云原生容器化部署 |
| [mxoob](./mxoob) | 带外管理，BMC/IPMI远程控制 |

### 5. 通信分布式 (5个)

| 技能 | 说明 |
|------|------|
| [mccl](./mccl) | 集合通信库，多GPU通信原语 |
| [mccl-test](./mccl-test) | 集合通信测试工具 |
| [mcapex](./mcapex) | 分布式训练工具 |
| [warmreset](./warmreset) | GPU热复位 |
| [dlrover](./dlrover) | 弹性训练，故障恢复 |
| [mceid](./mceid) | 设备标识管理 |

### 6. 应用层 (5个)

| 技能 | 说明 |
|------|------|
| [mxffmpeg](./mxffmpeg) | GPU视频编解码 |
| [mxaiforscience](./mxaiforscience) | 科学计算应用支持 |
| [mxtraining](./mxtraining) | AI训练流程指南 |
| [mxinference](./mxinference) | AI推理部署指南 |
| [mxquickstart](./mxquickstart) | 快速上手入门 |

### 7. 测试工具 (1个)

| 技能 | 说明 |
|------|------|
| [mxvs](./mxvs) | 测试工具套件 |

## 使用说明

### 技能结构

每个技能目录包含：
- `SKILL.md` - 核心内容文档
- `references/` - 详细参考文档（可选）
- `scripts/` - 脚本文件（可选）

### 技能格式

遵循 Claude Code Skill 规范：
- Frontmatter包含 name、description、keywords
- 渐进式披露：核心内容放SKILL.md，详细内容放references/
- 代码块指定语言

## 相关资源

- [fae-skill-generator](../fae-skill-generator) - 技能生成指南
- [全量沐曦文档](../china-ai-chip-docs/MUXI/全量沐曦文档.md) - 原始PDF文档集合
- [Ascend Skills](../Ascend) - 昇腾Skills对比参考

## 更新日志

- 2026-04-03: 初始版本，包含33个技能

---

Generated from 沐曦官方技术文档