---
name: biren-brvllm
description: BIREN brvllm 大模型推理服务参考指南。基于 vLLM 的壁仞大模型推理服务，支持离线推理和在线推理服务部署，提供 Chat API 和 Completions API 接口，用于 LLM 推理部署和量化模型推理。
keywords:
  - brvllm
  - biren
  - 大模型
  - LLM
  - 推理服务
  - vLLM
  - 量化推理
  - 壁仞
---

# brvllm Command Reference

brvllm 依托壁仞自研大模型推理引擎 suinfer-llm，为用户提供大模型推理能力。

## Quick Start

### Offline Inference

```python
from vllm import LLM, SamplingParams

config_path = "configs/qwen2_72b.json"
prompts = ["Hello, my name is", ...]
sampling_params = [SamplingParams(n=1, temperature=0.9, top_p=0.95, max_tokens=512)] * len(prompts)

llm = LLM(config_path=config_path, trust_remote_code=True)
outputs = llm.generate(prompts, sampling_params)
```

### Online Inference

```bash
br_api_server --config qwen2_72b.json --port port_id
```

## Environment Requirements

- OS: Ubuntu 20.04
- Python: 3.8 / 3.10
- BIRENSUPA SDK, suinfer-llm

Python Dependencies:
- psutil, sentencepiece, numpy
- transformers>=4.40.0
- fastapi==0.111.0, uvicorn[standard]
- pydantic==2.7.1, prometheus_client>=0.18.0
- torch==2.3.1, py-cpuinfo
- outlines==0.0.34

## Model Conversion

### Environment

- Ubuntu 20.04
- Python 3.8
- transformers, loguru
- torch==2.0.1
- accelerate==0.33.0
- sentencepiece==0.2.0

### Conversion Steps

1. Download model from HuggingFace
2. Set `use_cache` to false in config.json
3. Convert to .pt format using torch.jit.trace

```python
from transformers import AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained(model_dir, ignore_mismatched_sizes=True)
traced_model = torch.jit.trace(model, torch.randint(1, 10, (1, 10)), strict=False, check_trace=False)
torch.jit.save(traced_model, os.path.join(output_dir, model_name + ".pt"))
```

## Configuration (JSON)

### Key Fields

| Field | Description |
|-------|-------------|
| `model` | HuggingFace 完整模型名称 |
| `cached_dir` | 本地模型缓存路径 |
| `input_name` | pt 模型输入节点名称（统一为 "input_ids.1"） |
| `output_name` | pt 模型输出节点名称 |
| `vocab_size` | 模型词表大小 |
| `model_file` | pt 格式模型文件路径 |
| `serialize_file` | 序列化文件保存路径 |
| `model_precision` | 推理数据类型 |
| `build_seq` | 最大上下文长度 |
| `build_batch` | 最大推理 batchsize |
| `distribute_param` | 分布式策略 [TP, PP, DP] |
| `devices` | GPU 下标序列 |
| `all_models` | 服务地址到模型名的映射 |

### Model Precision

| Value | Description |
|-------|-------------|
| `a_bf16_w_int8_kv_int8` | 激活 BF16，权重 INT8，KV INT8 |
| `a_bf16_w_int8` | 激活 BF16，权重 INT8 |
| `bf16` | 全 BF16 |

### Distribute Param

```json
"distribute_param": [TP, PP, DP]
```

- TP: Tensor Parallelism
- PP: Pipeline Parallelism (当前仅支持 1)
- DP: Data Parallelism (当前仅支持 1)

## Sampling Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| `n` | ≥1 | 单 prompt 输出数量，默认 1 |
| `presence_penalty` | 任意浮点 | 默认 0.0，>0 鼓励新 token |
| `frequency_penalty` | 任意浮点 | 默认 0.0，>0 鼓励新 token |
| `repetition_penalty` | 任意浮点 | 默认 1.0，>1.0 鼓励未出现 token |
| `temperature` | ≥0 | 温度系数，0 为 greedy search |
| `top_p` | (0, 1] | 累积概率阈值，默认 1 |
| `top_k` | -1 或 1~vocab_size | 候选 token 范围，默认 -1 |
| `stop` | List[str] | 终止字符串 |
| `max_tokens` | ≥1 | 最大输出 tokens 数 |

## API Endpoints

### Chat API

```bash
POST /v1/chat/completions
```

自动添加对话模板。

### Completions API

```bash
POST /v1/completions
```

直接推理（无对话模板）。

### Metrics

```bash
GET http://host_ip:port/metrics
```

获取 vLLM 0.4.0.post1 定义的 Metrics。

## Multi-Service Deployment

1. 配置 `all_models` 字段包含所有服务地址
2. 启动 nginx 转发请求

```bash
# nginx 配置示例
upstream backend {
    server host1:port1;
    server host2:port2;
}
```

## Known Limitations

- 单卡推理只能使用 0 号卡
- 不能开启 graph capture
- build_batch 建议 ≤64
- 遇到 "Error in applying chat template" 表示只能使用 Completions API

## Installation

依赖 suinfer-llm，随 BIRENSUPA SDK 安装。

## Example: Complete Config

```json
{
    "model": "qwen/Qwen2-72B",
    "cached_dir": "/path/to/model",
    "input_name": "input_ids.1",
    "output_name": "logits",
    "vocab_size": 151936,
    "model_file": "/path/to/model.pt",
    "serialize_file": "/path/to/serialize.bin",
    "model_precision": "bf16",
    "build_seq": 4096,
    "build_batch": 64,
    "distribute_param": [1, 1, 1],
    "devices": [0]
}
```

## Example: Server Launch

```bash
br_api_server --config qwen2_72b.json --port 8000
```

## Example: Client Request

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "qwen2_72b",
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 512
    }
)
print(response.json())
```

## Performance Tips

- 合理设置 build_seq 和 build_batch
- 根据显存选择合适的精度
- 使用多卡并行提升吞吐量

## Related Tools

- **suInfer**: 通用推理引擎
- **suInfer-LLM**: LLM 推理引擎
- **suInfer Server**: Triton-based 推理服务