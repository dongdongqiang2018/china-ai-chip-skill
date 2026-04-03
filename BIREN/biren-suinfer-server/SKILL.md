---
name: biren-suinfer-server
description: BIREN suInfer Server 推理服务器参考指南。基于 Triton Inference Server 开发的推理服务器，支持 RESTful API 和 gRPC API，用于壁仞通用 GPU 的推理服务部署，支持异步推理、多节点多 GPU、容器化部署。
keywords:
  - suinfer-server
  - biren
  - Triton
  - 推理服务
  - 部署
  - gRPC
  - RESTful
  - 壁仞
---

# suInfer Server Command Reference

suInfer Server 是基于 Triton Inference Server 开发的推理服务器。

## Quick Start

```bash
# 加载镜像
docker load -i birensupa-infer_server_xx.xx.xx.tar

# 启动容器
docker run -id --name <name> --shm-size="16g" --network=host \
    --device=/dev/biren:/dev/biren \
    -v /suServer_dataset:/home/mlperf/workspace/data/scratch \
    birensupa-infer_server:xx.xx.xx bash

# 启动服务
/opt/tritonserver/start_server.sh
```

## Architecture

基于 Triton Inference Server，支持：
- RESTful API
- gRPC API
- 异步推理
- 多节点多 GPU
- 容器化部署
- Triton 原生 API

## Environment Requirements

支持的操作系统：
- Ubuntu 22.04/20.04
- CGSL 6.06
- Bclinux-Euler 21.10
- OpenEuler 22.03

## Port Configuration

| Port | Protocol | Description |
|------|----------|-------------|
| 8000 | HTTP | RESTful API |
| 8001 | gRPC | gRPC API |
| 8002 | HTTP | Metrics |

## Client Commands

```bash
infer_client.sh [options]
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-i` | 服务器 IP | localhost |
| `-n` | 端口 | 8001 |
| `-p` | 协议 (http/grpc) | grpc |
| `-m` | 指定模型 | - |
| `-c` | 操作 (load/unload/infer) | - |
| `-q` | 查询支持模型列表 | - |
| `-b` | batch size | - |
| `-r` | 请求数量 | - |

### Examples

```bash
# 查询模型
infer_client.sh -q

# 加载模型
infer_client.sh -m bert_crf_bf16 -c load

# 推理
infer_client.sh -m bert_crf_bf16 -c infer -b 2 -r 2
```

## Model Configuration

### config.pbtxt

```protobuf
name: "model_name"
platform: "onnxruntime"  # 或 "pytorch_libtorch"
max_batch_size: 8

input [
  {
    name: "input"
    data_type: TYPE_FP32
    dims: [1, 3, 224, 224]
  }
]

output [
  {
    name: "output"
    data_type: TYPE_FP32
    dims: [1, 1000]
  }
]
```

### Multi-GPU Setting

修改 `instance_group` 的 `gpus` 列表：

```protobuf
instance_group {
  kind: KIND_GPU
  gpus: [0, 1, 2, 3]
}
```

## Multi-Node Deployment

通过 nginx 负载均衡实现多节点：

1. 在各节点启动 suInfer Server
2. 配置 nginx upstream 指向各节点端口
3. Client 请求发送至 nginx 地址

```bash
# nginx 配置
upstream inference_backend {
    server node1:8001;
    server node2:8001;
    server node3:8001;
}

server {
    location / {
        proxy_pass http://inference_backend;
    }
}
```

## Supported Models (17 models)

推荐模型：
- bert_base_sst2
- crnn_resnet_bf16
- dbnet_bf16
- mobilenetv3_bf16
- yolov5s_bf16

## Metrics

### Endpoint

```
http://<host>:8002/metrics
```

### GPU Metrics

| Metric | Description |
|--------|-------------|
| `br_gpu_utilization` | GPU 利用率 |
| `br_gpu_memory_used_bytes` | 已用显存 |
| `br_gpu_memory_total_bytes` | 总显存 |
| `br_gpu_power_usage` | 功耗 |
| `br_gpu_power_limit` | 功耗限制 |

### Performance Metrics

| Metric | Description |
|--------|-------------|
| `inference_request_duration_us` | 推理请求耗时 |
| `inference_count` | 推理次数 |
| `duration` | 耗时 |

### Throughput Calculation

```bash
throughput = inference_count / duration
```

## Docker Deployment

### Load Image

```bash
docker load -i birensupa-infer_server_xx.xx.xx.tar
```

### Run Container

```bash
docker run -id --name <name> \
    --shm-size="16g" \
    --network=host \
    --device=/dev/biren:/dev/biren \
    -v /suServer_dataset:/home/mlperf/workspace/data/scratch \
    birensupa-infer_server:xx.xx.xx bash
```

### Start Server

```bash
/opt/tritonserver/start_server.sh
```

### Interactive Mode

```bash
docker run -it --name <name> \
    --shm-size="16g" \
    --network=host \
    --device=/dev/biren:/dev/biren \
    -v /suServer_dataset:/home/mlperf/workspace/data/scratch \
    birensupa-infer_server:xx.xx.xx bash
```

## Model Loading

```bash
infer_client.sh -m <model_name> -c load
```

## Model Inference

```bash
infer_client.sh -m <model_name> -c infer -b <batch_size> -r <num_requests>
```

## Health Check

```bash
curl http://<host>:8000/v2/health/ready
```

## Model Repository Structure

```
model_repository/
└── <model_name>/
    ├── config.pbtxt
    └── 1/
        └── model.onnx
```

## Performance Tuning

- 调整 batch size
- 优化模型
- 使用 INT8 量化
- 多 GPU 并行

## Known Limitations

- 需要正确配置模型路径
- 确保 GPU 驱动已安装
- 检查显存是否足够

## Return Codes

| Code | Description |
|------|-------------|
| SUCCESS | 成功 |
| ERROR | 失败 |

## Related Tools

- **suInfer**: 通用推理引擎
- **brvllm**: vLLM-based 推理服务
- **suInfer-LLM**: LLM 推理引擎