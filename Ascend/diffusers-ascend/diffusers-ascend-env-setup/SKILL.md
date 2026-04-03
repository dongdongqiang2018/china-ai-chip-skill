---
name: diffusers-ascend-env-setup
description: HuggingFace Diffusers 环境配置指南，用于华为昇腾 NPU。覆盖 CANN 版本检测、PyTorch + torch_npu 安装、Diffusers 库安装及环境验证。当用户需要在昇腾 NPU 上配置 Diffusers 环境时使用。
keywords:
    - diffusers
    - pytorch
    - torch_npu
    - cann
    - npu
---

# Diffusers 昇腾 NPU 环境配置

本 Skill 指导用户在华为昇腾 NPU 上配置 HuggingFace Diffusers 开发环境。

## 快速开始

4 步完成环境搭建：

```bash
# 1. 激活 CANN 环境（自动检测版本）
if [ -d "/usr/local/Ascend/cann" ]; then
    source /usr/local/Ascend/cann/set_env.sh
else
    source /usr/local/Ascend/ascend-toolkit/set_env.sh
fi

# 2. 安装 PyTorch + torch_npu（版本自动匹配）
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install torch-npu  # 自动匹配已安装的 PyTorch 版本

# 3. 安装 Diffusers
pip install diffusers["torch"] transformers

# 4. 验证环境
python scripts/validate_environment.py
```

## 安装概览

| 步骤 | 详细指南 |
|------|----------|
| CANN 验证 | [references/cann-versions.md](references/cann-versions.md) |
| PyTorch + torch_npu | [references/installation.md](references/installation.md) |
| Diffusers 安装 | [references/installation.md](references/installation.md) |

## 版本兼容性

| 组件 | 版本 | 说明 |
|------|------|------|
| CANN | 8.0.RC1+ | NPU 支持必需 |
| PyTorch | 2.1.0 - 2.8.0 | 含 torch_npu 扩展 |
| Diffusers | 0.28.0+ | 支持 SDXL、SD3、Flux |

**torch_npu 版本匹配**：
- 默认安装与 PyTorch 版本相同的 torch_npu：`pip install torch-npu`
- 如安装失败，请参考 [torch_npu Release](https://gitcode.com/Ascend/pytorch/README.md) 查看完整版本配套表

**示例**（CANN 8.3.RC1）：

| PyTorch | torch_npu | Python |
|---------|-----------|--------|
| 2.8.0 | 2.8.0 | 3.9 - 3.11 |
| 2.7.1 | 2.7.1 | 3.9 - 3.11 |
| 2.6.0 | 2.6.0.post3 | 3.9 - 3.11 |

## 环境验证

运行验证脚本：

```bash
python scripts/validate_environment.py
```

检查项：

| 检查项 | 说明 |
|--------|------|
| CANN 安装 | 目录存在且环境变量已设置 |
| PyTorch | import 成功，版本匹配 |
| torch_npu | import 成功，NPU 可见 |
| Diffusers | import 成功 |
| numpy | 版本 < 2.0 |

## 参考资源

- [详细安装指南](references/installation.md) - 完整的安装步骤和命令
- [CANN 版本说明](references/cann-versions.md) - 版本检测和差异说明
- [故障排查](references/troubleshooting.md) - 常见问题和解决方案
- [Diffusers 官方文档](https://huggingface.co/docs/diffusers)
- [昇腾 PyTorch 扩展](https://www.hiascend.com/document/detail/zh/Pytorch/720/apiref/torchnpuCustomsapi/context/概述.md)
- [torch_npu Release](https://gitcode.com/Ascend/pytorch/releases)
