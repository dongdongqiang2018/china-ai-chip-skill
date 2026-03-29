---
name: biren-sdk
description: 壁仞（BIREN）BIRENSUPA SDK 安装与环境配置 Skill，提供 BIRENSUPA 软件栈的完整安装、升级、卸载和验证流程。BIRENSUPA 是壁仞 GPU 的基础软件平台，包含驱动、运行时、工具链等，是使用壁仞 GPU 进行 AI 训练和推理的前提。
keywords:
  - biren
  - 壁仞
  - BIRENSUPA
  - SDK
  - 安装
  - 驱动
---

# biren-sdk BIRENSUPA SDK

## 功能描述

BIRENSUPA 是壁仞官方的 GPU 软件平台，提供驱动、运行时、工具链和加速库。本 Skill 详细介绍 BIRENSUPA 的安装、环境配置和版本管理，帮助用户快速搭建壁仞 GPU 开发环境。

## 核心能力

### 1. 组件总览

BIRENSUPA SDK 主要包含：

| 组件 | 说明 |
|------|------|
| 驱动 | BIREN GPU 驱动 |
| BIREN Runtime | CUDA 兼容层 |
| brsmi | GPU 管理工具 |
| BRML | C 管理库 |
| suCCL | 通信库 |
| suDNN | 深度学习加速库 |
| 工具链 | 编译器、调试器 |

### 2. 安装前检查

```bash
# 检查操作系统版本
cat /etc/os-release

# 支持的操作系统：
# - Ubuntu 22.04.4 LTS
# - Ubuntu 20.04.1 LTS
# - openEuler 22.03 LTS
# - NewStart Carrier Grade Server Linux 6.06

# 检查内核版本
uname -r

# 检查 GCC 版本
gcc --version

# 检查 GPU 硬件
lspci | grep -i biren
```

### 3. 安装 BIRENSUPA

#### 方式一：使用 .run 安装包

```bash
# 1. 获取安装包
# 联系壁仞产品服务部门获取 .run 文件
# 文件命名格式：birensupa_<version>_linux-<arch>.run

# 2. 增加可执行权限
chmod a+x birensupa_<version>_linux-x86_64.run

# 3. 执行安装
sudo ./birensupa_<version>_linux-x86_64.run

# 4. 验证安装
brsmi --version
```

#### 方式二：使用容器工具包

```bash
# 安装 biren-container-toolkit
chmod a+x biren-container-toolkit_<version>_linux-x86_64.run
sudo ./biren-container-toolkit_<version>_linux-x86_64.run

# 验证
brsw list
```

### 4. 环境变量配置

```bash
# 方式一：临时生效
export BIRENSUPA_HOME=/usr/local/birensupa
export PATH=$BIRENSUPA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$BIRENSUPA_HOME/lib:$BIRENSUPA_HOME/lib64:$LD_LIBRARY_PATH

# 方式二：永久生效
echo 'export BIRENSUPA_HOME=/usr/local/birensupa' >> ~/.bashrc
echo 'export PATH=$BIRENSUPA_HOME/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$BIRENSUPA_HOME/lib:$BIRENSUPA_HOME/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### 5. 驱动验证

```bash
# 检查驱动版本
brsmi --version

# 检查 GPU 设备
brsmi gpu list

# 查看驱动日志
dmesg | grep -i biren

# 检查驱动服务
systemctl status biren-driver
```

### 6. 版本升级

```bash
# 获取新版本安装包
# 联系壁仞产品服务部门

# 停止运行中的进程
# ...

# 卸载旧版本
sudo ./birensupa_<old_version>_linux-x86_64.run --uninstall

# 安装新版本
sudo ./birensupa_<new_version>_linux-x86_64.run

# 重启
sudo reboot

# 验证
brsmi --version
```

### 7. 卸载

```bash
# 使用安装包卸载
sudo ./birensupa_<version>_linux-x86_64.run --uninstall

# 或使用卸载脚本
sudo /usr/local/birensupa/scripts/uninstall.sh

# 重启
sudo reboot
```

## Docker 环境配置

### 1. 安装容器工具包

```bash
# 安装 biren-container-toolkit
chmod a+x biren-container-toolkit_<version>_linux-x86_64.run
sudo ./biren-container-toolkit_<version>_linux-x86_64.run
```

### 2. 配置 Docker

```bash
# 编辑 Docker 配置文件
sudo vim /etc/docker/daemon.json

# 添加壁仞配置
{
    "runtimes": {
        "biren": {
            "path": "/usr/local/birensupa/container-toolkit/bin/biren-container-runtime",
            "runtimeArgs": []
        }
    }
}

# 重启 Docker
sudo systemctl restart docker
```

### 3. 启动壁仞容器

```bash
# 使用壁仞运行时启动容器
docker run --rm --gpus all --runtime biren nvidia-smi

# 或使用 nvidia-container-runtime 兼容模式
docker run --rm --gpus all nvidia-smi
```

### 4. 验证容器环境

```bash
# 在容器内验证
brsmi
python3 -c "import biren; print('BIREN SDK OK')"
```

## 常见场景

### 场景1：全新服务器环境配置

```bash
# 1. 检查硬件
lspci | grep -i biren

# 2. 检查操作系统兼容性
cat /etc/os-release

# 3. 安装 BIRENSUPA
sudo ./birensupa_1.6.0_linux-x86_64.run

# 4. 配置环境变量
source ~/.bashrc

# 5. 验证
brsmi
```

### 场景2：开发环境配置

```bash
# 1. 安装 BIRENSUPA（如果未安装）

# 2. 配置开发工具
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++

# 3. 编译示例程序
cd /usr/local/birensupa/samples
make

# 4. 运行测试
./bin/gpu_info
```

### 3. Docker 生产环境

```bash
# 1. 安装容器工具包

# 2. 配置 Docker

# 3. 拉取壁仞基础镜像
docker pull biren/base:1.6.0

# 4. 启动训练容器
docker run -d --name training \
  --gpus all --runtime biren \
  -v /data:/data \
  biren/training:latest
```

## 故障排查

### 问题1：安装失败

**症状：** 安装过程报错

**排查步骤：**
```bash
# 1. 检查依赖
./birensupa_<version>_linux-x86_64.run --pre-check

# 2. 检查权限
ls -la birensupa_*.run

# 3. 查看详细日志
./birensupa_<version>_linux-x86_64.run --check

# 4. 查看系统日志
dmesg | tail
```

### 问题2：GPU 不识别

**症状：** brsmi 无设备

**排查步骤：**
```bash
# 1. 检查驱动
lsmod | grep biren

# 2. 检查固件
dmesg | grep -i firmware

# 3. 重启驱动
sudo rmmod biren_driver
sudo modprobe biren_driver
```

### 问题3：容器无法使用 GPU

**症状：** 容器内无法访问 GPU

**排查步骤：**
```bash
# 1. 检查 Docker 配置
cat /etc/docker/daemon.json

# 2. 检查运行时
docker info | grep -i biren

# 3. 重新安装容器工具包
sudo ./biren-container-toolkit_<version>_linux-x86_64.run --uninstall
sudo ./biren-container-toolkit_<version>_linux-x86_64.run
```

## 相关文档

- [壁仞_01安装（环境搭建）](../../china-ai-chip-docs/BIREN/壁仞_01安装（环境搭建）.md)
- [壁仞_07GPU管理与测试](../../china-ai-chip-docs/BIREN/壁仞_07GPU管理与测试.md)