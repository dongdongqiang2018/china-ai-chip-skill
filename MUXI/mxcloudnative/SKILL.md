---
name: mxcloudnative
description: 沐曦云原生参考手册，包含容器化部署、Docker/Kubernetes集成、Helm Chart配置等云原生场景最佳实践。
keywords:
  - 沐曦
  - 云原生
  - Docker
  - Kubernetes
  - 容器化
  - Helm
---

# 云原生部署指南

沐曦GPU云原生场景部署参考。

## Docker部署

### 构建镜像

```dockerfile
FROM ubuntu:20.04

# 安装依赖
RUN apt-get update && apt-get install -y \
    libmaca2 \
    libmcblas3 \
    libmcdnn3 \
    && rm -rf /var/lib/apt/lists/*

# 设置环境
ENV MACA_PATH=/opt/maca
ENV LD_LIBRARY_PATH=$MACA_PATH/lib:$LD_LIBRARY_PATH

WORKDIR /app
COPY . .
CMD ["python", "train.py"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t metax-ai:latest .

# 运行
docker run --device=/dev/dri --device=/dev/mxgvm \
    -v /opt/maca:/opt/maca \
    metax-ai:latest
```

## Kubernetes部署

### Operator

```yaml
apiVersion: metax.com/v1
kind: MetaXGPU
metadata:
  name: metax-gpu
spec:
  devicePlugin:
    enabled: true
  version: "2.31"
```

### Helm Chart

```bash
# 添加仓库
helm repo add metax https://metax-gpu.github.io/charts

# 安装
helm install metax-gpu metax/gpu-operator \
    --set devicePlugin.enabled=true
```

## 资源调度

### 节点选择

```yaml
nodeSelector:
    gpu-type: metax-c500
```

### 亲和性

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: gpu-type
          operator: In
          values:
          - metax-c500
```

### 污点和容忍

```yaml
# 节点污点
kubectl taint nodes gpu-node gpu=metax:NoSchedule

# Pod容忍
tolerations:
- key: "gpu"
  operator: "Equal"
  value: "metax"
  effect: "NoSchedule"
```

## 网络配置

### 主机网络

```yaml
hostNetwork: true
dnsPolicy: ClusterFirstWithHostNet
```

## 存储

### 挂载驱动

```yaml
volumes:
- name: maca
  hostPath:
    path: /opt/maca
```

## 官方参考

- 《曦云系列通用GPU云原生参考手册》