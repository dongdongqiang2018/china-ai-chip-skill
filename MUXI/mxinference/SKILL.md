---
name: mxinference
description: 沐曦AI推理用户指南，涵盖模型部署、推理优化、Triton Server、vLLM等推理服务部署。
keywords:
  - 沐曦
  - AI推理
  - mxinference
  - 模型部署
  - 推理服务
  - Triton
---

# AI推理用户指南

曦云GPU AI推理部署完整流程。

## 快速开始

### 模型加载

```python
import torch

# 加载模型
model = torch.jit.load('model.pt')
model.eval()

# 移动到GPU
model = model.cuda()

# 推理
with torch.no_grad():
    output = model(input_data)
```

## 推理服务

### Triton Server

```bash
# 启动Triton
tritonserver --model-repository=/models --backend-directory=/backends
```

### vLLM

```bash
# 启动vLLM
vllm serve meta-llama/Llama-2-7b-hf
```

## 优化

### 动态批处理

```python
# 使用 Triton Dynamic Batching
```

### 模型优化

```python
# TorchScript
model = torch.jit.trace(model, example_input)
model = torch.jit.script(model)

# ONNX
torch.onnx.export(model, input, "model.onnx")
```

## 官方参考

- 《曦云系列通用GPU AI推理用户手册》