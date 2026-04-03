---
name: biren-driver
description: BIRENSUPA Driver 驱动安装参考指南。用于安装壁仞内核层驱动 KMD、虚拟化驱动 bev、biren_fs、用户层驱动 UMD 等，包含 brsmi、brmsg、biren_fs 等工具模块，支持 Ubuntu、CentOS、openEuler 等操作系统。
keywords:
  - biren-driver
  - biren
  - 驱动安装
  - KMD
  - UMD
  - GPU驱动
  - 壁仞
---

# BIRENSUPA Driver Installation Guide

BIRENSUPA Driver 中打包了壁仞的众多软件模块。

## Quick Start

```bash
# 增加可执行权限
chmod a+x biren-driver_<version>_linux-<arch>.run

# 安装
sudo ./biren-driver_<version>_linux-<arch>.run

# 查看版本
brsmi
brsw
```

## Components

| Module | Description | Related Docs |
|--------|-------------|---------------|
| KMD | 壁仞内核层驱动 | - |
| bev | 壁仞虚拟化驱动 | - |
| brsmi | 获取 GPU 各种级别信息 | 《壁仞 BRsmi 用户指南》 |
| brmsg | 解析内核日志错误 | 《壁仞 brmsg 用户指南》 |
| biren_fs | GPU 内存与存储之间直接协调 IO | - |

## Supported OS

| OS | Kernel Version |
|----|-----------------|
| Ubuntu 22.04.4 LTS | 5.15.0-97-generic |
| Ubuntu 20.04.1 LTS | 5.4.0-139-generic |
| openEuler 22.03 LTS | 5.10.0-60.18.0.50.oe2203.x86_64 |
| BigCloud Enterprise Linux For Euler 21.10 LTS | 4.19.90-2107.6.0.0100.oe1.bclinux.x86_64 |

## Installation Steps

### Step 1: 安装驱动源码编译所需依赖

**Ubuntu：**

```bash
# 查看是否已安装
dpkg --list | grep dkms
dpkg --list | linux-headers-$(uname -r)

# 安装依赖
apt-get install -y dkms linux-headers-$(uname -r)
```

**CentOS/Kylin/CGSL/openEuler/BC-Linux：**

```bash
# 查看是否已安装
rpm -qa | grep dkms
rpm -qa | grep kernel-devel

# 安装依赖
yum install --enablerepo=extras epel-release
yum install -y dkms kernel-devel-$(uname -r)

# 或使用 rpm 包安装
rpm -ivh {package_name}.rpm
```

> 注意：仅安装非 Kernel 模块，无需安装以上依赖。

### Step 2: 安装驱动

```bash
# 增加可执行权限
chmod a+x biren-driver_<version>_linux-<arch>.run

# 【选择一】仅安装 kmd（同步安装 brsmi 和 brmsg）
sudo ./biren-driver_<version>_linux-<arch>.run

# 【选择二】仅安装 bev
sudo ./biren-driver_<version>_linux-<arch>.run --bev-only

# 【选择三】仅安装 biren_fs
sudo ./biren-driver_<version>_linux-<arch>.run --brfs-only

# 【选择四】仅安装非 kernel 模块（brsmi 和 brmsg）
sudo ./biren-driver_<version>_linux-<arch>.run --no-kernel-modules
```

> 注意：
> 1. Docker 容器里不支持安装内核模块（kmd、bev、biren_fs）
> 2. 不支持多进程同时安装
> 3. 推荐安装前先卸载已有版本

### Step 3: 查看版本信息

```bash
# 查看 Driver 版本
brsmi

# 查看软件包版本
brsw
```

## Uninstallation

```bash
# 【选择一】卸载所有模块
sudo ./biren-driver_<version>_linux-<arch>.run --uninstall
# 或
sudo /usr/local/birensupa/driver/scripts/uninstall.sh

# 【选择二】仅卸载 bev
sudo ./biren-driver_<version>_linux-<arch>.run --uninstall --bev-only

# 【选择三】仅卸载 biren_fs
sudo ./biren-driver_<version>_linux-<arch>.run --uninstall --brfs-only

# 【选择四】仅卸载非 kernel 模块
sudo ./biren-driver_<version>_linux-<arch>.run --uninstall --no-kernel-modules
```

## Upgrade and Rollback

联系壁仞产品服务部门，获取目标版本对应的 `.run` 文件，然后重新执行安装步骤。

## KMD Operations

```bash
# 查看 KMD(biren) Linux 内核模块加载情况
lsmod | grep biren

# 加载 biren module
sudo modprobe biren

# 卸载 biren module
sudo rmmod biren
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--help, -h` | 查看帮助信息 |
| `-x, --extract-only [path]` | 解压软件包中文件到指定目录 |
| `--check` | 检查软件包的一致性和完整性 |
| `--pre-check` | 检查系统是否满足安装的环境要求 |
| `--info` | 显示软件包的相关信息 |
| `--uninstall` | 卸载软件包相关的模块 |
| `--bev-only, --brfs-only, --no-kernel-modules` | 设置安装或卸载的模式 |

## Verification

```bash
# 查看驱动模块
lsmod | grep biren

# 查看设备
brsmi

# 查看版本
brsw
```

## Notes

- 需要 root 权限安装
- 不支持多进程同时安装
- 不可同时安装内核模块 bev 与 kmd
- 若已安装 kmd，需先卸载再安装 bev

## Related Tools

- **brsmi**: GPU 管理工具
- **brmsg**: 日志解析工具
- **brsw**: 软件包管理工具