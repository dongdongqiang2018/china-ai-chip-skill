---
name: biren-container
description: 壁仞（BIREN）容器工具包 Skill，提供 biren-container-toolkit 的安装、Docker 集成、容器启动和验证等完整流程。biren-container-toolkit 是壁仞 GPU 容器化部署的核心组件，支持在 Docker 容器中使用壁仞 GPU 进行 AI 训练和推理。
keywords:
  - biren
  - 壁仞
  - container
  - docker
  - 容器
  - biren-container-toolkit
---

# biren-container 壁仞容器工具包

## 功能描述

biren-container-toolkit 是壁仞官方提供的容器工具包，用于在 Docker 容器中运行 BIRENSUPA GPU 工作负载。本 Skill 提供完整的安装、配置和使用指南。

## 核心能力

### 1. 安装 biren-container-toolkit

```bash
# 1. 获取安装包
# 联系壁仞产品服务部门获取 .run 文件
# 文件命名格式：biren-container-toolkit_<version>_linux-<arch>.run

# 2. 增加可执行权限
chmod a+x biren-container-toolkit_<version>_linux-x86_64.run

# 3. 执行安装
sudo ./biren-container-toolkit_<version>_linux-x86_64.run

# 4. 验证安装
brsw list
```

### 2. Docker 配置

```bash
# 编辑 Docker 配置文件
sudo vim /etc/docker/daemon.json

# 添加壁仞运行时
{
    "runtimes": {
        "biren": {
            "path": "/usr/local/birensupa/container-toolkit/bin/biren-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia"
}

# 重启 Docker
sudo systemctl restart docker

# 验证
docker info | grep -i biren
```

### 3. 启动壁仞容器

```bash
# 使用 biren 运行时
docker run -it --rm \
  --gpus all \
  --runtime biren \
  ubuntu:22.04 \
  bash

# 使用 nvidia-container-runtime（需壁仞支持）
docker run -it --rm \
  --gpus all \
  ubuntu:22.04 \
  bash

# 映射设备
docker run -it --rm \
  --device=/dev/dri \
  --device=/dev/birendrm \
  --runtime biren \
  ubuntu:22.04 \
  bash
```

### 4. 容器内验证

```bash
# 在容器内验证 GPU 访问
brsmi

# 验证 CUDA 兼容层
nvidia-smi

# 验证 PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"
```

### 5. Docker Compose 示例

```yaml
version: '3.8'

services:
  training:
    image: biren/training:latest
    runtime: biren
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 8
              capabilities: [gpu]
    volumes:
      - /data:/data
    environment:
      - SUCCL_IB_HCA=mlx5_0,mlx5_1
```

### 6. Kubernetes 部署

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: biren-training
spec:
  runtimeClassName: biren
  containers:
  - name: training
    image: biren/training:latest
    resources:
      limits:
        biren.com/gpu: 8
```

## 常见场景

### 场景1：单机训练容器

```bash
# 启动训练容器
docker run -d --name training \
  --gpus all \
  --runtime biren \
  -v /data:/data \
  -v /model:/model \
  biren/training:latest

# 进入容器
docker exec -it training bash

# 运行训练
python train.py
```

### 场景2：多机分布式训练

```bash
# 启动主节点
docker run -d --name master \
  --gpus all --runtime biren \
  --network host \
  biren/training:latest \
  torchrun --master_addr=master ...

# 启动从节点
docker run -d --name worker1 \
  --gpus all --runtime biren \
  --network host \
  biren/training:latest \
  torchrun --master_addr=master --rank=1 ...
```

## 故障排查

### 问题1：容器无法启动

**症状：** Docker 报错 runtime not found

**排查步骤：**
```bash
# 1. 检查 Docker 配置
cat /etc/docker/daemon.json

# 2. 检查运行时文件
ls -la /usr/local/birensupa/container-toolkit/bin/

# 3. 重启 Docker
sudo systemctl restart docker

# 4. 验证运行时
docker info | grep -i biren
```

### 问题2：容器内无法访问 GPU

**症状：** brsmi 无输出

**排查步骤：**
```bash
# 1. 检查主机端 GPU
brsmi

# 2. 检查容器权限
ls -la /dev/dri/

# 3. 重新安装容器工具包
sudo ./biren-container-toolkit_<version>_linux-x86_64.run --uninstall
sudo ./biren-container-toolkit_<version>_linux-x86_64.run
```

## 相关文档

- [壁仞_01安装（环境搭建）](../../china-ai-chip-docs/BIREN/壁仞_01安装（环境搭建）.md)
- [brsmi](./brsmi/) - GPU 设备管理
- [biren-sdk](./biren-sdk/) - SDK 安装