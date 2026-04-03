---
name: mxk8s
description: 沐曦Kubernetes部署工具，用于在K8s集群中部署和管理曦云GPU资源。支持Device Plugin和GPU Sharing。
keywords:
  - 沐曦
  - Kubernetes
  - K8s
  - mxk8s
  - GPU调度
  - 容器
---

# Kubernetes 部署指南

沐曦GPU在Kubernetes集群中的部署配置。

## 快速开始

### 前提条件

- Kubernetes >= 1.19
- NVIDIA Device Plugin (用于参考架构)
- Docker >= 19.03

### 安装步骤

```bash
# 1. 安装GPU节点驱动（见mxdriver）

# 2. 部署Device Plugin
kubectl apply -f https://raw.githubusercontent.com/MetaX-GPU/metax-device-plugin/main/deployments/static/metax-device-plugin-daemonset.yaml

# 3. 验证
kubectl get nodes
kubectl describe node <gpu-node> | grep meta-x.com
```

## 配置详解

### Device Plugin

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: meta-x-gpu-device-plugin
spec:
  selector:
    matchLabels:
      name: meta-x-gpu-device-plugin
  template:
    spec:
      containers:
      - image: metax docker.io/metaxai/metax-device-plugin:latest
        name: meta-x-gpu-device-plugin
        volumeMounts:
        - name: device-plugin
          mountPath: /var/lib/kubelet/device-plugins
      volumes:
      - name: device-plugin
        hostPath:
          path: /var/lib/kubelet/device-plugins
```

### GPU调度

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: gpu-container
    image: gpu-app:latest
    resources:
      limits:
        meta-x.com/gpu: "1"  # 请求1个GPU
```

### GPU Sharing (sGPU)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sgpu-pod
spec:
  containers:
  - name: sgpu-container
    image: gpu-app:latest
    resources:
      limits:
        meta-x.com/sgpu: "1"  # 1个sGPU切片
        meta-x.com/sgpu-memory: "16Gi"  # 16GB显存
```

## 监控

### 添加监控标签

```bash
# 为节点添加标签
kubectl label nodes <node> gpu=metax
```

### 部署Prometheus

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: meta-x-gpu
spec:
  selector:
    matchLabels:
      app: meta-x-exporter
  endpoints:
  - port: metrics
```

## 资源管理

### 资源定义

| 资源名 | 说明 |
|--------|------|
| meta-x.com/gpu | 整卡GPU |
| meta-x.com/sgpu | sGPU切片 |
| meta-x.com/sgpu-memory | 显存大小 |
| meta-x.com/sgpu-compute | 算力比例 |

### 资源配额

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
spec:
  hard:
    meta-x.com/gpu: "4"
    meta-x.com/sgpu: "16"
```

## 官方参考

- 《曦云系列通用GPU Kubernetes部署手册》
- mx-exporter K8s部署手册