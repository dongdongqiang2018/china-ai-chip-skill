---
name: biren-sdk
description: BIRENSUPA SDK 安装参考指南。包含 SUPA 编程核心、tensor-engine AI 编译器、brVideo 视频编解码、suVS 验证工具、suPTI 性能追踪、suProfiler 性能分析、suCCL 集合通信、suDNN/suBLAS/suFFT/suRAND 加速库等完整开发工具链。
keywords:
  - biren-sdk
  - biren
  - SDK安装
  - 开发工具
  - 加速库
  - 编译器
  - 壁仞
---

# BIRENSUPA SDK Installation Guide

BIRENSUPA SDK 中包含了壁仞的众多软件模块。

## Quick Start

```bash
# 获取安装包
chmod a+x birensupa-sdk_<version>_<os>_linux-<arch>.run

# 安装
sudo ./birensupa-sdk_<version>_<os>_linux-<arch>.run

# 设置环境变量
source /usr/local/birensupa/sdk/latest/scripts/brsw_set_env.sh

# 验证
brcc --version
brsmi
```

## Components

| Module | Description | Related Docs |
|--------|-------------|---------------|
| SUPA | 编程核心，抽象硬件细节，提供 C++ 扩展和运行时 API | 《BIRENSUPA 编程指南》 |
| tensor-engine | AI 编译器，支持算子和子图自动生成优化 | - |
| brVideo | 基于 VAAPI 的视频编解码 | 《壁仞 Video 用户指南》 |
| suVS | GPU 验证和测试工具 | 《壁仞 suVS 用户手册》 |
| libsutx | 调试分析工具 | 《壁仞 suPTI & suTX 用户指南》 |
| suPTI | 性能数据采集 | 《壁仞 suPTI & suTX 用户指南》 |
| sudbg | GPU 调试和诊断 | 《gpu_debugger 工具用户指南》 |
| suFile | GPU 内存和存储 DMA 传输 | 《壁仞 suFile 用户指南》 |
| suProfiler | 性能分析工具 | 《壁仞 suProfiler 用户指南》 |
| br_perfworks | GPU 性能指标评估工具 | - |
| suCCL | 集合通信原语库 | 《壁仞 suCCL 用户指南》 |
| suRAND | 随机数生成库 | 《壁仞 suRAND 用户指南》 |
| suFFT | 快速傅里叶变换库 | 《壁仞 suFFT 用户指南》 |
| suPerfviz | 性能指标可视化工具 | 《壁仞 DrPerfViz 用户指南》 |
| UMD | 用户层驱动 | - |
| supa-sanitizer | 代码检查工具 | 《壁仞 suSanitizer 用户指南》 |
| brBPP | 图像处理函数库 | 《壁仞 BPP 用户指南》 |
| BRCC | 编译器 | 《壁仞 BRCC 用户指南》 |
| suDNN | 深度学习算子库 | 《壁仞 suDNN 用户指南》 |
| sudnn-eager | GPU 加速原语库 | 《壁仞 suDNN 用户指南》 |
| suBLAS | 线性代数计算库 | 《壁仞 suBLAS 用户指南》 |
| sutlass | GEMM/Conv 模板抽象 | - |

## Supported OS

| OS | Kernel Version |
|----|-----------------|
| Ubuntu 22.04.4 LTS | 5.15.0-97-generic |
| Ubuntu 20.04.1 LTS | 5.4.0-139-generic |
| openEuler 22.03 LTS | 5.10.0-60.18.0.50.oe2203.x86_64 |
| BigCloud Enterprise Linux For Euler 21.10 LTS | 4.19.90-2107.6.0.0100.oe1.bclinux.x86_64 |

## Installation Steps

### Step 1: 安装运行时依赖

**Ubuntu：**

```bash
apt-get install -y python3-pip dkms libsndio7.0 libxv1 libxfixes3 \
    libglib2.0-dev libsdl2-2.0-0 libsdl2-dev liborc-0.4-dev \
    ocl-icd-opencl-dev libopencv-dev libboost-regex-dev libgoogle-glog-dev
```

**CentOS、Kylin：**

```bash
yum install -y python3-pip dkms dracut glib2-devel SDL2-devel \
    orc-devel ocl-icd-devel systemd-devel boost-regex glog-devel
```

### Step 2: 安装 SDK

```bash
# 增加可执行权限
chmod a+x birensupa-sdk_<version>_<os>_linux-<arch>.run

# 安装至默认路径（/usr/local/birensupa/sdk）
sudo ./birensupa-sdk_<version>_<os>_linux-<arch>.run
```

### Step 3: 设置环境变量

```bash
source /usr/local/birensupa/sdk/latest/scripts/brsw_set_env.sh
```

### Step 4: 验证安装结果

```bash
# 查看可用模块
brsw

# 验证 SDK 组件
brcc --version
```

## Environment Setup

```bash
# 设置环境变量（添加到 ~/.bashrc 或 /etc/profile）
source /usr/local/birensupa/sdk/latest/scripts/brsw_set_env.sh
```

## Upgrade

联系壁仞产品服务部门，获取目标版本对应的 `.run` 文件，然后重新执行安装步骤。

## Uninstallation

```bash
# 方式一：使用安装包
sudo ./birensupa-sdk_<version>_<os>_linux-<arch>.run --uninstall

# 方式二：使用卸载脚本
sudo /usr/local/birensupa/sdk/latest/scripts/uninstall.sh
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--help, -h` | 查看帮助信息 |
| `-x, --extract-only [path]` | 解压软件包中文件到指定目录 |
| `--check` | 检查软件包的一致性和完整性 |
| `--pre-check` | 检查系统是否满足安装的环境要求 |
| `--version` | 显示软件包的版本信息 |
| `--info` | 显示软件包的相关信息 |
| `--uninstall` | 卸载软件包 |

## Post-Installation

### 验证 BRCC

```bash
brcc --version
```

### 验证 suDNN

```bash
# 检查库文件
ls -la /usr/local/birensupa/sdk/latest/sulib/
```

### 验证工具

```bash
# suProfiler
suprof --help

# suVS
suvs --help
```

## Notes

- 需要先安装 BIRENSUPA Driver
- 不支持多个进程同时安装
- 某些组件需要额外的许可证

## Related Components

- **BIRENSUPA Driver**: GPU 驱动
- **biren-container-toolkit**: 容器工具包