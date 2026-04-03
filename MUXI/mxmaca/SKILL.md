---
name: mxmaca
description: 沐曦GPU软件栈核心，包括驱动、编译器、数学库和工具链。提供完整的GPU编程环境，支持C/C++/CUDA异构计算。
keywords:
  - 沐曦
  - MXMACA
  - 软件栈
  - GPU编程
  - 异构计算
  - 驱动
---

# MXMACA 软件栈指南

MXMACA是沐曦推出的GPU软件栈，包含底层驱动、编译器、数学库及整套软件工具套件。

## 快速开始

### 安装

```bash
# 安装MXMACA SDK
sudo ./MXMACA-*-linux-x86_64.run

# 验证安装
mx-smi -L
```

### 环境配置

```bash
# 设置环境变量
export MACA_PATH=/opt/maca
export PATH=$MACA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$MACA_PATH/lib:$LD_LIBRARY_PATH
```

## 架构

### 软件栈层次

```
┌─────────────────────────────────────┐
│         应用层 (AI/科学计算)         │
├─────────────────────────────────────┤
│      框架层 (PyTorch/TensorFlow)     │
├─────────────────────────────────────┤
│    高性能库 (mcDNN/mcBLAS/mcFFT)    │
├─────────────────────────────────────┤
│    编程接口 (CUDA/OPENCL/MXMACA)    │
├─────────────────────────────────────┤
│        工具链 (mxcc/mxvs)           │
├─────────────────────────────────────┤
│       运行时 (MACA Runtime)         │
├─────────────────────────────────────┤
│          驱动层 (Kernel)            │
├─────────────────────────────────────┤
│           硬件 (曦云GPU)             │
└─────────────────────────────────────┘
```

## 核心组件

### 驱动

| 组件 | 说明 |
|------|------|
| KMD | 内核态驱动 |
| UMD | 用户态驱动 |
| Firmware | 固件 |

### 编译器

| 组件 | 说明 |
|------|------|
| mxcc | C/C++编译器 |
| mxclang | Clang前端 |
| ptxas | PTX汇编器 |

### 数学库

| 库 | 说明 |
|----|------|
| mcBLAS | 线性代数 |
| mcDNN | 深度神经网络 |
| mcFFT | 快速傅里叶变换 |
| mcRAND | 随机数生成 |
| mcSOLVER | 求解器 |
| mcSPARSE | 稀疏矩阵 |

### 工具

| 工具 | 说明 |
|------|------|
| mx-smi | 设备管理 |
| mxvs | 测试工具套件 |
| mcprofiler | 性能分析 |
| mx-diagease | 诊断工具 |

## 编程接口

### CUDA兼容层

```cpp
#include <maca.h>

int main() {
    int deviceCount;
    macaGetDeviceCount(&deviceCount);
    // ...
}
```

### MXMACA原生API

```cpp
#include <mxmaca/mxmaca.h>

int main() {
    mxmaca_init();
    // ...
}
```

## 版本信息

```bash
# 查看版本
mxcc --version

# 查看SDK版本
cat $MACA_PATH/version

# 查看驱动版本
mx-smi --show-version
```

## 常见问题

### 驱动加载

```bash
# 检查驱动状态
lsmod | grep maca

# 加载驱动
sudo modprobe maca
```

### 权限问题

```bash
# 添加用户组
sudo groupadd maca
sudo usermod -aG maca $USER

# 设置设备权限
sudo chmod 666 /dev/mxmaca*
```

## 官方参考

- 《曦云系列通用GPU用户指南》
- 《曦云系列通用GPU快速上手指南》
- MXMACA SDK