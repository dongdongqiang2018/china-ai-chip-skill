---
name: mx-pd-deploy
description: 沐曦（Metax）PD（Prefill-Decode）分离部署 Skill，提供大模型推理的 Prefill 和 Decode 阶段分离部署架构、KV Cache 传输配置、负载均衡和 Kubernetes 编排等完整部署指南。PD 分离可显著提升推理吞吐、缓解资源竞争、支持异构推理，是生产环境部署大模型的标准架构。
keywords:
  - muxi
  - metax
  - PD分离
  - Prefill
  - Decode
  - vLLM
  - SGLang
  - Mooncake
  - 推理部署
  - 负载均衡
---

# mx-pd-deploy PD分离部署

## 功能描述

PD 分离（Prefill-Decode Disaggregation）是一种大模型推理架构，将推理的 Prefill（预填充）阶段和 Decode（解码）阶段分离到不同的 GPU 集群。PD 分离可以显著提升推理吞吐、缓解 Prefill 和 Decode 阶段的资源竞争、支持独立扩展、容错隔离，是生产环境部署大模型的标准架构。

沐曦 C500 系列 GPU 支持基于 Mooncake-transfer-engine 的 KV Cache 传输和 SGLang Router 的请求路由。

## 核心能力

### 1. PD 分离架构概述

```
┌─────────────┐     ┌─────────────┐
│   Prefill   │     │   Decode    │
│   Cluster   │────>│   Cluster   │
│  (多卡TP)   │ KV  │  (多卡TP)   │
└─────────────┘     └─────────────┘
       │                   │
       └─────────┬─────────┘
                 │
          ┌──────▼──────┐
          │ sgl-router  │
          │  (负载均衡) │
          └──────┬──────┘
                 │
          ┌──────▼──────┐
          │   Client    │
          └─────────────┘
```

**PD 分离优势：**
- 缓解资源竞争：Prefill 和 Decode 独立使用 GPU
- 提高吞吐：支持更大 batch size
- 独立扩展：可根据负载单独扩展 Prefill/Decode
- 容错隔离：一个阶段故障不影响另一个
- 异构推理：支持不同规格 GPU 混部

### 2. KV Cache 传输配置

#### 2.1 Mooncake-transfer-engine

Mooncake 是高性能 KV Cache 传输引擎，支持 RDMA 直接传输。

```bash
# 部署 Mooncake（独立 Pod）
# Kubernetes 配置示例：
apiVersion: v1
kind: Pod
metadata:
  name: mooncake-transfer
spec:
  containers:
  - name: mooncake
    image: metax/mooncake-transfer:v0.3.6
    ports:
    - containerPort: 10000
    env:
    - name: TRANSFER_DEVICE
      value: "mlx5_0,mlx5_1,mlx5_2,mlx5_3"
```

#### 2.2 RDMA 设备配置

```yaml
# 在 Prefill/Decode Pod 中配置 RDMA 设备
spec:
  containers:
  - name: sglang
    resources:
      limits:
        amd.com/gpu: 8
        rdma/mlx5: 4  # RDMA 设备
```

### 3. SGLang PD 部署配置

#### 3.1 Prefill 节点配置

```bash
python3 -m sglang.launch_server \
  --model-path /models/Qwen3-32B \
  --disaggregation-mode=prefill \
  --tensor-parallel-size=8 \
  --dp-size=1 \
  --disaggregation-ib-device=mlx5_0,mlx5_1,mlx5_2,mlx5_3 \
  --mem-fraction-static=0.80 \
  --port=30080
```

**关键参数：**
| 参数 | 说明 |
|------|------|
| `--disaggregation-mode` | 设为 `prefill` |
| `--tensor-parallel-size` | 张量并行度 |
| `--disaggregation-ib-device` | RDMA 设备列表 |
| `--mem-fraction-static` | KV Cache 内存占比 |

#### 3.2 Decode 节点配置

```bash
python3 -m sglang.launch_server \
  --disaggregation-mode=decode \
  --tensor-parallel-size=8 \
  --dp-size=1 \
  --enable-hierarchical-cache \
  --hicache-size=30 \
  --mem-fraction-static=0.7 \
  --cuda-graph-max-bs=32 \
  --port=30080
```

**关键参数：**
| 参数 | 说明 |
|------|------|
| `--disaggregation-mode` | 设为 `decode` |
| `--enable-hierarchical-cache` | 启用分层 KV Cache |
| `--hicache-size` | 分层缓存大小（GB） |

#### 3.3 Router 配置

```bash
# 部署 sgl-router
python3 -m sglang.router \
  --prefill-endpoints http://prefill-1:30080,http://prefill-2:30080 \
  --decode-endpoints http://decode-1:30080,http://decode-2:30080 \
  --port=8000
```

**路由策略：**
| 策略 | 说明 |
|------|------|
| `random` | 随机选择 |
| `round-robin` | 轮询 |
| `power-of-two-choices` | 最小负载 |
| `cache-aware` | Cache 感知（默认） |

### 4. Kubernetes 编排

#### 4.1 Prefill Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: prefill
  namespace: llm-inference
spec:
  serviceName: prefill
  replicas: 4
  selector:
    matchLabels:
      app: prefill
  template:
    metadata:
      labels:
        app: prefill
    spec:
      containers:
      - name: sglang
        image: metax/sglang:latest
        command: ["python3", "-m", "sglang.launch_server"]
        args:
        - --model-path
        - /models/Qwen3-32B
        - --disaggregation-mode=prefill
        - --tensor-parallel-size=8
        - --mem-fraction-static=0.80
        resources:
          limits:
            amd.com/gpu: 8
        volumeMounts:
        - name: model
          mountPath: /models
      volumes:
      - name: model
        persistentVolumeClaim:
          claimName: model-pvc
```

#### 4.2 Decode Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: decode
  namespace: llm-inference
spec:
  serviceName: decode
  replicas: 18
  selector:
    matchLabels:
      app: decode
  # ... 类似 Prefill，mode 改为 decode
```

#### 4.3 Router Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sgl-router
  namespace: llm-inference
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: router
```

### 5. 资源配置参考

#### 5.1 DeepSeek 模型配置

| 精度 | Prefill | Decode | Mooncake | Router |
|------|---------|--------|----------|--------|
| BF16 | 4台32卡 | 18台144卡 | 1台(CPU) | 1台(CPU) |
| W8A8 | 2台16卡 | 10台80卡 | 1台(CPU) | 1台(CPU) |
| W4A16 | 1台8卡 | 4台32卡 | 1台(CPU) | 1台(CPU) |

#### 5.2 Qwen3-8B 小模型配置

```bash
# Prefill: 4 卡
--tensor-parallel-size=4
--mem-fraction-static=0.80

# Decode: 4 卡
--tensor-parallel-size=4
--mem-fraction-static=0.7
```

### 6. 性能优化

#### 6.1 通信优化

```bash
# 启用 P2P+RDMA 传输
--disaggregation-ib-device=mlx5_0,mlx5_1

# 优化 KV Cache 传输
--enable-hierarchical-cache
--hicache-size=50
```

#### 6.2 批处理优化

```bash
# Prefill 批处理
--max-running-requests 64
--max-total-tokens 32768

# Decode 批处理
--max-running-requests 128
--max-prefill-tokens 8192
```

#### 6.3 显存优化

```bash
# 调整 KV Cache 比例
--mem-fraction-static 0.85  # Prefill 端
--mem-fraction-static 0.75  # Decode 端
```

## 常见场景

### 场景1：DeepSeek V3/R1 671B 部署

大规模模型 PD 部署。

```bash
# 1. 准备 Kubernetes 集群
# 2. 部署 Mooncake
kubectl apply -f mooncake.yaml

# 3. 部署 Prefill
kubectl apply -f prefill-deepseek.yaml

# 4. 部署 Decode
kubectl apply -f decode-deepseek.yaml

# 5. 部署 Router
kubectl apply -f router.yaml

# 6. 验证
curl http://<router-ip>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### 场景2：Qwen3-8B 小模型部署

低成本小模型 PD 部署。

```bash
# 1 机 8 卡部署
# Prefill: 4 卡
# Decode: 4 卡

# Prefill 启动
python3 -m sglang.launch_server \
  --model-path /models/Qwen3-8B \
  --disaggregation-mode=prefill \
  --tensor-parallel-size=4 \
  --port=30080

# Decode 启动
python3 -m sglang.launch_server \
  --disaggregation-mode=decode \
  --tensor-parallel-size=4 \
  --port=30080

# Router
python3 -m sglang.router \
  --prefill-endpoints http://localhost:30080 \
  --decode-endpoints http://localhost:30080
```

### 场景3：动态扩缩容

根据负载自动调整 Prefill/Decode 副本数。

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: prefill-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: prefill
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: amd.com/gpu
      target:
        type: Utilization
        averageUtilization: 80
```

### 场景4：故障恢复

PD 分离的容错机制。

```bash
# Prefill 故障：请求重路由到其他 Prefill 实例
# Decode 故障：请求重新生成
# Mooncake 故障：降级为 HTTP 传输（延迟增加）
```

## 故障排查

### 问题1：Prefill/Decode 通信失败

**症状：** 请求超时或卡死

**排查步骤：**
```bash
# 1. 检查 Mooncake 服务
kubectl get pods -n llm-inference | grep mooncake

# 2. 检查 RDMA 设备
kubectl exec -it prefill-pod -- rdma link show

# 3. 检查网络连通性
kubectl exec -it prefill-pod -- ping decode-pod

# 4. 查看日志
kubectl logs -f prefill-pod
kubectl logs -f decode-pod
```

### 问题2：KV Cache 传输慢

**症状：** 推理延迟高

**排查步骤：**
```bash
# 1. 检查 RDMA 带宽
ib_write_bw -d mlx5_0

# 2. 检查 Mooncake 配置
# 确保使用 RDMA 而非 HTTP

# 3. 调整缓存大小
--hicache-size 50  # 增大
```

### 问题3：负载不均

**症状：** 部分 Decode 节点负载高

**排查步骤：**
```bash
# 1. 检查 Router 路由策略
# 使用 cache-aware 策略

# 2. 调整 Prefill/Decode 比例
# Prefill:Decode = 1:4 ~ 1:8

# 3. 监控节点负载
kubectl top pods -n llm-inference
```

### 问题4：显存不足 OOM

**症状：** KV Cache 溢出

**排查步骤：**
```bash
# 1. 降低显存占比
--mem-fraction-static 0.7

# 2. 减少 batch size
--max-running-requests 64

# 3. 启用分层缓存
--enable-hierarchical-cache
--hicache-size 30
```

## 相关文档

- [SGLang PD 部署指南](../china-ai-chip-docs/MUXI/试运行-SGLang的PD部署实操.pdf)
- [P2P+NCCL PD 部署](../china-ai-chip-docs/MUXI/基于P2P+NCCL的PD部署.pdf)
- [vLLM 推理部署](../china-ai-chip-docs/MUXI/612_曦云系列通用计算GPU AI推理用户手册.md)
- [muxi-npu-smi](./muxi-npu-smi/) - GPU 设备管理

## 部署组件总览

| 组件 | 用途 | 数量 |
|------|------|------|
| SGLang Prefill | 预填充阶段 | N 台 |
| SGLang Decode | 解码阶段 | M 台 |
| Mooncake | KV Cache 传输 | 1 台 |
| sgl-router | 请求路由 | 1 台 |
| Kubernetes | 容器编排 | 集群 |