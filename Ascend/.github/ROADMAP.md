# Awesome Ascend Skills Roadmap

> 昇腾 AI Agents 技能仓 - 端到端 Agent Skill 规划

---

## 概述

Awesome Ascend Skills 是面向华为昇腾 NPU 的结构化 AI Agent 知识库，覆盖昇腾端到端开发流程，帮助 Agent 更好地理解昇腾的使用方式。

**当前状态**：
- ✅ 已完成：9 个 Skills
- 📋 待规划：21 个 Skills

---

## 目录

- [1. 基础环境](#1-基础环境)
  - [1.1 基础指令](#11-基础指令)
  - [1.2 环境安装](#12-环境安装)
  - [1.3 基础测试](#13-基础测试)
- [2. 开发](#2-开发)
  - [2.1 通用框架](#21-通用框架)
  - [2.2 推理](#22-推理)
  - [2.3 训练](#23-训练)
  - [2.4 算子](#24-算子)
  - [2.5 Profiling](#25-profiling)

---

## 1. 基础环境

### 1.1 基础指令

#### **npu-smi** ✅ 已规划

NPU 设备管理命令工具，用于查询设备健康状态、监控温度/功耗、管理固件升级和虚拟化配置。

- **文档**: [npu-smi/SKILL.md](../npu-smi/SKILL.md)
- **类型**: 运维
- **官方文档**: https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/envdeployment/instg/instg_0045.html

#### **open-euler 基础指令** 📋 待规划

OpenEuler 操作系统基础指令集，提供操作系统层面的昇腾设备支持、驱动配置和系统优化指南。

- **类型**: 系统配置
- **范围**: 
  - 操作系统安装与配置
  - 驱动安装与验证
  - 系统优化建议

---

### 1.2 环境安装

#### **CANN (8.5 之前与之后)** 📋 待规划

华为昇腾 CANN 开发环境安装指南，覆盖 8.5 之前与之后版本的安装方案。

- **类型**: 开发环境
- **范围**:
  - CANN 8.5 之前版本安装
  - CANN 8.5 及之后版本安装
  - 依赖项检查
  - 环境验证

#### **HDK/Kernels** 📋 待规划

HDK (Hardware Development Kit) 和 Kernels 开发技能。

- **类型**: 底层开发
- **范围**:
  - HDK 环境搭建
  - Kernel 开发指南
  - 自定义算子开发

---

### 1.3 基础测试

#### **hccl-test 打流** ✅ 已规划

HCCL (Huawei Collective Communication Library) 集合通信性能测试工具，提供带宽测试和性能基准测试。

- **文档**: [hccl-test/SKILL.md](../hccl-test/SKILL.md)
- **类型**: 测试
- **官方文档**: https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/parameterconfiguration/paramconfig/paramconfig_0031.html

#### **docker 搭建** ✅ 已规划

昇腾 Docker 容器化开发环境配置技能，提供 NPU 设备映射和开发环境隔离的最佳实践。

- **文档**: [ascend-docker/SKILL.md](../ascend-docker/SKILL.md)
- **类型**: 运维
- **官方文档**: https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/dockerdevelopment/dockerdev/dockerdev_0001.html

#### **Ascend-dmi 压测** 📋 待规划

Ascend DMI (Device Management Interface) 性能压测工具。

- **类型**: 测试
- **范围**:
  - DMI 工具使用
  - 性能压测方法
  - 结果分析

#### **NPU 算子单用例验证** 📋 待规划

NPU 算子单独用例验证方法，确保算子功能正确性。

- **类型**: 测试
- **范围**:
  - 单算子测试框架
  - 用例编写规范
  - 验证流程

---

## 2. 开发

### 2.1 通用框架

#### **torch_npu** ✅ 已规划

华为昇腾 Ascend Extension for PyTorch (torch_npu)，提供 PyTorch 在 NPU 上的运行支持。

- **文档**: [torch_npu/SKILL.md](../torch_npu/SKILL.md)
- **类型**: 通用框架
- **范围**:
  - ✅ PyTorch 算子 API
  - 📋 … (待规划）

#### **OP-Plugin** 📋 待规划

扩展算子插件，提供额外的算子支持。

- **类型**: 通用框架
- **范围**:
  - 📋 算子接入
  - 📋 … （待规划）

---

### 2.2 推理

#### **Diffusers** 📋 待规划

Diffusers 模型库昇腾优化技能，提供 Stable Diffusion、FLUX 等扩散模型的 NPU 推理支持。

- **类型**: 推理
- **范围**:
  - 📋 部署
  - 📋 适配
  - 📋 测试

#### **vllm-ascend** ✅ 已规划

vLLM 推理引擎昇腾优化技能，提供高性能大语言模型推理服务。

- **文档**: [vllm-ascend/SKILL.md](../vllm-ascend/SKILL.md)
- **类型**: 推理
- **范围**:
  - ✅ 部署
  - ✅ 适配
  - ✅ 测试

#### **vllm-omni** 📋 待规划

vLLM 多模态推理引擎昇腾优化技能，支持文本、图像、音频等多模态输入。

- **类型**: 推理
- **范围**:
  - 📋 部署
  - 📋 适配
  - 📋 测试

#### **sglang** 📋 待规划

SGLang 推理框架昇腾优化技能，提供高性能推理服务。

- **类型**: 推理
- **范围**:
  - 📋 部署
  - 📋 适配
  - 📋 测试

#### **vllm-benchmark** 📋 待规划

vLLM 推理性能基准测试工具。

- **类型**: 测试
- **范围**:
  - 性能测试方法
  - 指标采集
  - 结果分析

#### **ais-bench** ✅ 已规划

AI 模型评估工具，支持精度评估和性能评估。

- **文档**: [ais-bench/SKILL.md](../ais-bench/SKILL.md)
- **类型**: 测试
- **范围**:
  - 精度评估（MMLU、GSM8K、MMMU 等）
  - 性能压测

#### **sglang-benchmark** 📋 待规划

SGLang 推理性能基准测试工具。

- **类型**: 测试
- **范围**:
  - 性能测试方法
  - 对比分析

#### **小模型** 📋 待规划

轻量级模型推理技能，支持 ONNX 和 PyTorch 格式。

- **类型**: 推理
- **范围**:
  - 📋 onnx
  - 📋 pt (PyTorch)
- **适用场景**: 边缘部署、快速原型验证

#### **atc-model-converter** ✅ 已规划

ATC (Ascend Tensor Compiler) 模型转换工具，将模型转换为昇腾 .om 格式。

- **文档**: [atc-model-converter/SKILL.md](../atc-model-converter/SKILL.md)
- **类型**: 推理优化
- **范围**:
  - ONNX 转 OM
  - 精度对比
  - YOLO 端到端部署

#### **msmodelslim** ✅ 已规划

模型压缩量化工具，支持 W4A8、W8A8 等量化方案。

- **文档**: [msmodelslim/SKILL.md](../msmodelslim/SKILL.md)
- **类型**: 推理优化
- **范围**:
  - 模型量化
  - 精度调优
  - 部署优化

---

### 2.3 训练

#### **MindSpeed** 📋 待规划

MindSpeed 训练框架昇腾优化技能，提供高性能分布式训练支持。

- **类型**: 训练
- **范围**:
  - 📋 部署
  - 📋 适配
  - 📋 测试

#### **MindSpore** 📋 待规划

华为原生 MindSpore 深度学习框架技能。

- **类型**: 训练
- **范围**:
  - 📋 部署
  - 📋 适配
  - 📋 测试

#### **Verl** 📋 待规划

Verl RLHF 训练框架昇腾优化技能。

- **类型**: 训练
- **范围**:
  - 📋 部署
  - 📋 适配
  - 📋 测试

---

### 2.4 算子

#### **AscendC** ✅ 已规划

AscendC 算子开发技能，提供 Transformer 相关算子的实现指南。

- **文档**: [ascendc/SKILL.md](../ascendc/SKILL.md)
- **类型**: 算子开发
- **范围**:
  - FFN/GMM/MoE 等算子
  - CANN API 示例

#### **Catlass** 📋 待规划

高级算子库开发技能。

- **类型**: 算子开发
- **范围**: 待规划

#### **Triton** 📋 待规划

Triton 跨平台算子开发技能，支持在昇腾 NPU 上开发高性能算子。

- **类型**: 算子开发
- **范围**: 待规划

#### **TileLang-Ascend** 📋 待规划

TileLang 昇腾适配技能，新兴算子开发语言。

- **类型**: 算子开发
- **范围**: 待规划

---

### 2.5 Profiling

#### **推理 Profiling** 📋 待规划

推理场景性能分析技能。

- **类型**: 性能分析
- **范围**:
  - 📋 采集
  - 📋 分析

#### **训练 Profiling** 📋 待规划

训练场景性能分析技能。

- **类型**: 性能分析
- **范围**:
  - 📋 采集
  - 📋 分析

---

## 统计

| 类别 | 已完成 | 待规划 | 总计 |
|------|--------|--------|------|
| 1. 基础环境 | 3 | 5 | 8 |
| 2.1 通用框架 | 1 | 1 | 2 |
| 2.2 推理 | 5 | 8 | 13 |
| 2.3 训练 | 0 | 3 | 3 |
| 2.4 算子 | 1 | 3 | 4 |
| 2.5 Profiling | 0 | 1 | 1 |
| **总计** | **10** | **21** | **31** |

---

## 贡献指南

如果您想为 Awesome Ascend Skills 贡献新的 Skill 或改进现有内容：

1. 查看现有 Skills 的结构和格式
2. 按照 [AGENTS.md](../AGENTS.md) 中的规范创建新 Skill
3. 提交 Pull Request

详细贡献指南请参考 [README.md](../README.md#贡献指南)。

---

## 相关资源

- **华为昇腾官方文档**: https://www.hiascend.com/document
- **GitHub 仓库**: https://github.com/ascend-ai-coding/awesome-ascend-skills
- **Issue 追踪**: https://github.com/ascend-ai-coding/awesome-ascend-skills/issues

---

## 更新日志

- **2026-03-02**: 初始版本，规划 31 个 Skills（10 个已完成 + 21 个待规划）
