# Diffusers 环境安装详细指南

本文档提供详细的安装步骤，是 [../SKILL.md](../SKILL.md) 的参考文档。

## 1. CANN 环境验证

### 检测 CANN 版本

CANN 8.5 及之后版本采用新的目录结构。使用以下逻辑自动检测：

```bash
# CANN 8.5+
if [ -d "/usr/local/Ascend/cann" ]; then
    source /usr/local/Ascend/cann/set_env.sh
    echo "CANN 8.5+ detected"
# CANN 8.5 之前
elif [ -d "/usr/local/Ascend/ascend-toolkit" ]; then
    source /usr/local/Ascend/ascend-toolkit/set_env.sh
    echo "CANN (before 8.5) detected"
else
    echo "Error: CANN not found"
fi
```

### 验证 CANN 环境变量

激活环境后，检查以下变量是否设置：

```bash
echo $ASCEND_HOME_PATH
echo $ASCEND_TOOLKIT_HOME
echo $ASCEND_OPP_PATH
echo $ASCEND_AICPU_PATH
```

正常输出应显示具体路径，而非空值。

### Python 验证

```python
import os

# 检查关键环境变量
required_vars = ["ASCEND_HOME_PATH", "ASCEND_TOOLKIT_HOME", "ASCEND_OPP_PATH"]
for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"✓ {var} = {value}")
    else:
        print(f"✗ {var} not set")
```

**注意**：假设 CANN 已预先安装。如需安装 CANN，请参考[官方文档](https://www.hiascend.com/document)。

## 2. PyTorch + torch_npu 安装

### 安装策略

1. **推荐方式**：先安装 PyTorch，再安装同版本的 torch_npu
2. **如遇版本问题**：参考 [torch_npu README](https://gitcode.com/Ascend/pytorch/README.md) 查看完整配套表

### 安装步骤

**1. 安装前置依赖**

```bash
# numpy 必须 < 2.0（关键要求）
pip install "numpy<2.0"
pip install pyyaml setuptools
```

**2. 安装 PyTorch**

```bash
# x86 架构
pip install torch --index-url https://download.pytorch.org/whl/cpu

# aarch64 架构
pip install torch
```

**3. 安装 torch_npu（版本自动匹配）**

```bash
# 自动安装与当前 PyTorch 版本匹配的 torch_npu
pip install torch-npu
```

如果上述命令失败（版本不匹配），请：

1. 检查 PyTorch 版本：`python -c "import torch; print(torch.__version__)"`
2. 访问 [torch_npu README](https://gitcode.com/Ascend/pytorch/README.md) 查看配套表
3. 安装指定版本：`pip install torch-npu=={version}`

### 版本配套参考

完整配套表请参考 [torch_npu README](https://gitcode.com/Ascend/pytorch/README.md)。以下是 **CANN 8.3.RC1** 的配套：

| PyTorch | torch_npu | Python |
|---------|-----------|--------|
| 2.8.0 | 2.8.0 | 3.9 - 3.11 |
| 2.7.1 | 2.7.1 | 3.9 - 3.11 |
| 2.6.0 | 2.6.0.post3 | 3.9 - 3.11 |
| 2.1.0 | 2.1.0.post17 | 3.8 - 3.11 |

> **注意**：不同 CANN 版本支持的 PyTorch/torch_npu 版本不同，请以官方文档为准。

### 快速验证

```python
import torch
import torch_npu

# 检查 NPU 可用性
print(f"PyTorch version: {torch.__version__}")
print(f"NPU available: {torch.npu.is_available()}")
print(f"NPU count: {torch.npu.device_count()}")

# 简单张量测试
if torch.npu.is_available():
    x = torch.tensor([1.0, 2.0, 3.0]).npu()
    print(f"Tensor on NPU: {x}")
```

## 3. Diffusers 安装

### 标准安装

根据[官方安装指南](https://huggingface.co/docs/diffusers/en/installation)：

```bash
# 基础安装（仅 PyTorch 后端）
pip install diffusers["torch"]

# 完整安装（推荐用于开发）
pip install diffusers["torch"] transformers accelerate

# 带可选依赖的完整安装
pip install diffusers["torch"] transformers accelerate safetensors
```

### 开发版安装

如需使用最新特性或修复：

```bash
# 从源码安装
git clone https://github.com/huggingface/diffusers.git
cd diffusers
pip install -e ".[torch]"
```

### 版本兼容性说明

| Diffusers 版本 | 推荐 PyTorch | 推荐 transformers | 说明 |
|----------------|--------------|-------------------|------|
| 0.30.0+        | 2.0+         | 4.40.0+           | 支持 SD3、Flux |
| 0.28.0+        | 2.0+         | 4.30.0+           | 支持 SDXL |
| 0.21.0+        | 1.13+        | 4.25.0+           | 支持 ControlNet |

### 模型缓存配置

Diffusers 默认将模型下载到用户目录的缓存中。可配置缓存位置：

```bash
# 设置环境变量
export HF_HOME="/path/to/your/cache"
export HF_HUB_CACHE="/path/to/your/hub/cache"
```

或在代码中指定：

```python
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    cache_dir="/path/to/cache"
)
```

### 禁用遥测

Diffusers 会收集使用统计信息。如需禁用：

```bash
export HF_HUB_DISABLE_TELEMETRY=1
```

## 4. 手动环境验证

```python
# 完整环境验证
import sys

def check_environment():
    results = []
    
    # 1. 检查 CANN 环境
    import os
    cann_path = os.environ.get("ASCEND_HOME_PATH")
    results.append(("CANN Path", cann_path or "Not set"))
    
    # 2. 检查 PyTorch
    try:
        import torch
        results.append(("PyTorch", torch.__version__))
    except ImportError:
        results.append(("PyTorch", "Not installed"))
        return results
    
    # 3. 检查 torch_npu
    try:
        import torch_npu
        results.append(("torch_npu", torch_npu.__version__))
    except ImportError:
        results.append(("torch_npu", "Not installed"))
    
    # 4. 检查 NPU
    if torch.npu.is_available():
        results.append(("NPU Available", f"Yes ({torch.npu.device_count()} devices)"))
    else:
        results.append(("NPU Available", "No"))
    
    # 5. 检查 Diffusers
    try:
        import diffusers
        results.append(("Diffusers", diffusers.__version__))
    except ImportError:
        results.append(("Diffusers", "Not installed"))
    
    # 6. 检查 numpy
    import numpy as np
    np_version = np.__version__
    results.append(("NumPy", f"{np_version} {'✓' if int(np_version.split('.')[0]) < 2 else '✗ (need < 2.0)'}"))
    
    return results

# 输出结果
for name, value in check_environment():
    print(f"{name:20s}: {value}")
```
