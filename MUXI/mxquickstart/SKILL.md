---
name: mxquickstart
description: 沐曦快速上手指南，帮助用户快速完成曦云GPU环境搭建和第一个GPU程序运行。包括安装、验证和示例。
keywords:
  - 沐曦
  - 快速上手
  - mxquickstart
  - 入门指南
  - 环境搭建
---

# 快速上手指南

曦云GPU快速入门。

## 环境要求

### 硬件要求

- 曦云C500/C300系列GPU
- PCIe x16插槽
- 电源 >= 750W

### 软件要求

- Linux (Ubuntu 20.04+ / CentOS 8+)
- GCC >= 7.5
- Python >= 3.8

## 安装步骤

### 1. 安装驱动

```bash
# 下载驱动包
wget https://example.com/MXMACA-Driver-*.run

# 安装
sudo chmod +x MXMACA-Driver-*.run
sudo ./MXMACA-Driver-*.run
```

### 2. 安装SDK

```bash
# 下载SDK包
wget https://example.com/MXMACA-SDK-*.run

# 安装
sudo ./MXMACA-SDK-*.run
```

### 3. 验证环境

```bash
# 查看设备
mx-smi -L

# 查看驱动
mx-smi --show-version

# 运行测试
mxvs test
```

## 第一个程序

### Hello GPU (Python)

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device count: {torch.cuda.device_count()}")
print(f"Device name: {torch.cuda.get_device_name(0)}")

# 创建GPU张量
x = torch.randn(1000, 1000).cuda()
y = torch.randn(1000, 1000).cuda()
z = torch.matmul(x, y)
print(f"Result shape: {z.shape}")
```

### Hello GPU (C++)

```cpp
#include <stdio.h>
#include <maca.h>

int main() {
    int deviceCount;
    macaGetDeviceCount(&deviceCount);
    printf("Found %d devices\n", deviceCount);
    return 0;
}
```

编译运行：

```bash
mxcc hello.cu -o hello
./hello
```

## 下一步

- 学习mx-smi使用
- 尝试PyTorch训练
- 探索mcBLAS/mcDNN库

## 官方参考

- 《曦云系列通用GPU快速上手指南》
- 《曦云系列通用GPU用户指南》