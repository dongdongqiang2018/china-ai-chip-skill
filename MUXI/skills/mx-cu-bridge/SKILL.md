---
name: mx-cu-bridge
description: 沐曦（Metax）CUDA 兼容层 Skill，提供 cu-bridge 源码编译安装、环境配置、版本管理和故障排查能力。cu-bridge 是沐曦 GPU 实现 CUDA 生态兼容的核心组件，让基于 CUDA 编写的 AI 框架和模型代码可以在沐曦 C500 系列 GPU 上运行，是使用 PyTorch、TensorFlow 等框架的前提。
keywords:
  - muxi
  - metax
  - cu-bridge
  - CUDA兼容层
  - MACA
  - 编译安装
  - PyTorch
---

# mx-cu-bridge CUDA兼容层

## 功能描述

cu-bridge 是沐曦官方的 CUDA 兼容层，实现了 CUDA Runtime 和 Driver API 的兼容接口，使基于 CUDA 编写的 AI 框架和模型代码可以在沐曦 C500 系列 GPU 上运行。cu-bridge 是使用 PyTorch、TensorFlow 等深度学习框架的前提，需要从源码编译安装。

## 核心能力

### 1. 源码获取与编译

从 gitee 获取 cu-bridge 源码并编译安装。

```bash
# 1. 克隆源码
git clone https://gitee.com/metax-tech/cu-bridge.git
cd cu-bridge

# 2. 创建编译目录
mkdir build && cd build

# 3. 配置编译选项
cmake .. \
  -DCMAKE_INSTALL_PREFIX=/opt/maca/tools/cu-bridge \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_TESTING=OFF

# 4. 编译（使用多核加速）
make -j$(nproc)

# 5. 安装
sudo make install
```

### 2. 环境配置

配置环境变量使 cu-bridge 生效。

```bash
# 方式一：临时生效（当前 shell）
export PATH=/opt/maca/tools/cu-bridge/bin:$PATH
export LD_LIBRARY_PATH=/opt/maca/tools/cu-bridge/lib:$LD_LIBRARY_PATH

# 方式二：永久生效（~/.bashrc 或 /etc/profile）
echo 'export PATH=/opt/maca/tools/cu-bridge/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/opt/maca/tools/cu-bridge/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 验证安装
nvcc --version  # 应该显示 cu-bridge 版本
```

### 3. cu-bridge 目录结构

```
/opt/maca/tools/cu-bridge/
├── bin/                    # 可执行文件
│   └── nvcc               # CUDA 编译器
├── include/               # 头文件
│   ├── cuda/
│   └── cupti/
├── lib/                   # 库文件
│   ├── libcudart.so
│   ├── libcuda.so
│   └── libcupti.so
└── lib64/                # 64位库（兼容）
```

### 4. 常用 API 兼容说明

cu-bridge 支持的主要 CUDA API：

| 模块 | 支持状态 | 说明 |
|------|----------|------|
| CUDA Runtime | ✓ 完整支持 | cudaRuntime.h |
| CUDA Driver | ✓ 完整支持 | cuda.h |
| cuBLAS | ✓ 完整支持 | 矩阵运算 |
| cuFFT | ✓ 完整支持 | 傅里叶变换 |
| cuDNN | ✓ 完整支持 | 深度学习算子 |
| cuPTI | ✓ 完整支持 | 性能分析工具 |
| cuSPARSE | ✓ 完整支持 | 稀疏矩阵 |
| NVTX | ✓ 完整支持 | 性能标记 |

### 5. 与 MACA SDK 集成

cu-bridge 需要与 MACA SDK 配合使用。

```bash
# MACA SDK 路径
ls /opt/maca/

# 完整环境变量配置
export MACA_HOME=/opt/maca
export MACA_INSTALL_DIR=/opt/maca
export PATH=$MACA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACA_HOME/lib:$MACA_HOME/lib64:$LD_LIBRARY_PATH
export LIBRARY_PATH=$MACA_HOME/lib:$LIBRARY_PATH
export C_INCLUDE_PATH=$MACA_HOME/include:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=$MACA_HOME/include:$CPLUS_INCLUDE_PATH
```

## 常见场景

### 场景1：从零搭建开发环境

全新的沐曦 GPU 服务器配置完整的开发环境。

```bash
# 1. 安装驱动（参考驱动安装指南）
# ...

# 2. 克隆并编译 cu-bridge
git clone https://gitee.com/metax-tech/cu-bridge.git
cd cu-bridge
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/opt/maca/tools/cu-bridge
make -j$(nproc)
sudo make install

# 3. 配置环境变量
cat > /etc/profile.d/maca.sh << 'EOF'
export MACA_HOME=/opt/maca
export PATH=$MACA_HOME/bin:/opt/maca/tools/cu-bridge/bin:$PATH
export LD_LIBRARY_PATH=$MACA_HOME/lib:$MACA_HOME/lib64:/opt/maca/tools/cu-bridge/lib:$LD_LIBRARY_PATH
EOF

# 4. 验证
nvcc --version
nvidia-smi  # 或 mx-smi
```

### 场景2：PyTorch 环境配置

配置使用 cu-bridge 的 PyTorch 环境。

```bash
# 方式一：使用预编译的 MACA PyTorch
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/maca

# 方式二：从源码编译 PyTorch
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
export MACA_HOME=/opt/maca
export CMAKE_PREFIX_PATH=/opt/maca/tools/cu-bridge
python setup.py install

# 验证
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.cuda.device_count())"
```

### 场景3：TensorFlow 环境配置

```bash
# 安装 TensorFlow
pip install tensorflow

# 配置环境
export TF_CPP_MIN_LOG_LEVEL=1

# 验证
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### 场景4：CUDA 程序开发

使用 cu-bridge 编译 CUDA 程序。

```bash
# 编写测试程序
cat > test.cu << 'EOF'
#include <stdio.h>
#include <cuda_runtime.h>

__global__ void hello_kernel() {
    printf("Hello from Metax GPU!\n");
}

int main() {
    hello_kernel<<<1, 1>>>();
    cudaDeviceSynchronize();
    return 0;
}
EOF

# 编译
nvcc test.cu -o test

# 运行
./test

# 预期输出：Hello from Metax GPU!
```

### 场景5：验证 cu-bridge 功能

```bash
# 1. 编译测试
cd /opt/maca/tools/cu-bridge/build
make tests -j$(nproc)

# 2. 运行单元测试
ctest

# 3. 运行示例程序
./bin/deviceQuery
./bin/bandwidthTest
```

## 故障排查

### 问题1：nvcc 找不到

**症状：** `nvcc: command not found`

**排查步骤：**
```bash
# 1. 检查 cu-bridge 安装
ls /opt/maca/tools/cu-bridge/bin/

# 2. 检查环境变量
echo $PATH

# 3. 重新配置环境变量
export PATH=/opt/maca/tools/cu-bridge/bin:$PATH
export LD_LIBRARY_PATH=/opt/maca/tools/cu-bridge/lib:$LD_LIBRARY_PATH

# 4. 验证
which nvcc
nvcc --version
```

### 问题2：编译链接错误

**症状：** 链接时找不到库

**排查步骤：**
```bash
# 1. 检查库路径
ls /opt/maca/tools/cu-bridge/lib/

# 2. 配置链接路径
export LD_LIBRARY_PATH=/opt/maca/tools/cu-bridge/lib:$LD_LIBRARY_PATH

# 3. 使用 LDD 检查依赖
ldd your_program

# 4. 重新编译
nvcc your_code.cu -L/opt/maca/tools/cu-bridge/lib -o your_program
```

### 问题3：运行时库找不到

**症状：** 运行时 `libcudart.so not found`

**排查步骤：**
```bash
# 1. 检查库文件
ls -la /opt/maca/tools/cu-bridge/lib/libcudart.so*

# 2. 设置库路径
export LD_LIBRARY_PATH=/opt/maca/tools/cu-bridge/lib:$LD_LIBRARY_PATH

# 3. 确认加载
ldd your_program | grep cuda

# 4. 永久配置
echo "/opt/maca/tools/cu-bridge/lib" | sudo tee /etc/ld.so.conf.d/maca.conf
sudo ldconfig
```

### 问题4：CUDA 版本不匹配

**症状：** API 版本不兼容

**排查步骤：**
```bash
# 1. 查看 cu-bridge 版本
cat /opt/maca/tools/cu-bridge/version.txt

# 2. 查看编译的 CUDA 版本
nvcc --version

# 3. 检查 PyTorch CUDA 版本
python -c "import torch; print(torch.version.cuda)"

# 4. 必要时重新编译
# 确保所有组件使用相同的 CUDA 版本
```

### 问题5：cu-bridge 与驱动版本不匹配

**症状：** 驱动初始化失败

**排查步骤：**
```bash
# 1. 检查驱动版本
mx-smi -v
# 或
nvidia-smi

# 2. 检查 cu-bridge 兼容的驱动版本
cat /opt/maca/tools/cu-bridge/compatibility.txt

# 3. 升级/降级驱动
sudo apt update
sudo apt upgrade metax-driver

# 4. 重启后验证
reboot
mx-smi
```

## 环境变量完整配置

```bash
# 完整环境变量配置（添加到 ~/.bashrc）
cat >> ~/.bashrc << 'EOF'

# ====== Metax/MACA Environment ======
export MACA_HOME=/opt/maca
export MACA_INSTALL_DIR=/opt/maca

# CUDA 兼容层 (cu-bridge)
export CUBRIDGE_HOME=/opt/maca/tools/cu-bridge

# PATH
export PATH=$MACA_HOME/bin:$CUBRIDGE_HOME/bin:$PATH

# 库路径
export LD_LIBRARY_PATH=$MACA_HOME/lib:$MACA_HOME/lib64:$CUBRIDGE_HOME/lib:$LD_LIBRARY_PATH

# 编译搜索路径
export LIBRARY_PATH=$MACA_HOME/lib:$MACA_HOME/lib64:$LIBRARY_PATH

# 头文件搜索路径
export C_INCLUDE_PATH=$MACA_HOME/include:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=$MACA_HOME/include:$CPLUS_INCLUDE_PATH

# 运行时库
export CUBRIDGE_LIB=$CUBRIDGE_HOME/lib

EOF

source ~/.bashrc
```

## 相关文档

- [cu-bridge 项目](https://gitee.com/metax-tech/cu-bridge)
- [沐曦官方文档](https://www.metax-tech.com/)
- [曦云系列GPU驱动安装指南](../china-ai-chip-docs/MUXI/971_曦云系列通用GPU驱动安装指南.md)
- [曦云系列GPU快速上手指南](../china-ai-chip-docs/MUXI/970_曦云系列通用GPU快速上手指南.md)
- [muxi-npu-smi](./muxi-npu-smi/) - GPU 设备管理
- [muxi-vs](./muxi-vs/) - 算力测试