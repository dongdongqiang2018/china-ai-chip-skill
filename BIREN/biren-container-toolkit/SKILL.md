---
name: biren-container-toolkit
description: BIREN biren-container-toolkit 容器工具包安装参考指南。用于在容器中使用壁仞通用 GPU，介绍安装、验证、升级、卸载步骤，支持 Ubuntu、openEuler 等操作系统。
keywords:
  - biren-container-toolkit
  - biren
  - 容器
  - container
  - Docker
  - GPU容器
  - 壁仞
---

# biren-container-toolkit Installation Guide

biren-container-toolkit 是容器使用壁仞通用 GPU 所需的工具包。

## Quick Start

```bash
# 获取安装包
chmod a+x biren-container-toolkit_<version>_linux-<arch>.run

# 安装
sudo ./biren-container-toolkit_<version>_linux-<arch>.run

# 验证
brsw
```

## Supported OS

| OS | Kernel Version |
|----|---------------|
| Ubuntu 22.04.4 LTS | 5.15.0-97-generic |
| Ubuntu 20.04.1 LTS | 5.4.0-139-generic |
| openEuler 22.03 LTS | 5.10.0-60.18.0.50.oe2203.x86_64 |
| BigCloud Enterprise Linux For Euler 21.10 LTS | 4.19.90-2107.6.0.0100.oe1.bclinux.x86_64 |

## Installation Steps

### Step 1: 获取安装包

根据 Linux 版本，联系壁仞产品服务部门获取对应的 `.run` 文件安装包。

### Step 2: 增加可执行权限

```bash
chmod a+x biren-container-toolkit_<version>_linux-<arch>.run
```

### Step 3: 安装

安装至默认路径（`/usr/local/birensupa/container-toolkit`）：

```bash
sudo ./biren-container-toolkit_<version>_linux-<arch>.run
```

> 注意：不支持多个进程同时安装同一个 `.run` 文件。

## Verification

### 使用 brsw 命令

```bash
brsw
```

查看系统中当前可使用壁仞模块。

### 检查配置文件

```bash
cat /etc/docker/daemon.json
```

查看配置文件中是否有 biren-container-toolkit 相关的配置。

## Upgrade

联系壁仞产品服务部门，获取目标版本对应的 `.run` 文件，然后重新执行安装步骤。

## Uninstallation

```bash
# 方式一：使用安装包
sudo ./biren-container-toolkit_<version>_linux-<arch>.run --uninstall

# 方式二：使用卸载脚本
sudo /usr/local/birensupa/container-toolkit/scripts/uninstall.sh
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

## Docker Configuration

示例 `/etc/docker/daemon.json`：

```json
{
    "runtimes": {
        "biren": {
            "path": "/usr/local/birensupa/container-toolkit/bin/biren-container-runtime",
            "runtimeArgs": []
        }
    }
}
```

重启 Docker：
```bash
sudo systemctl restart docker
```

## Usage in Container

```bash
# 运行容器时指定 biren 运行时
docker run --runtime=biren -it your_image

# 或
docker run --device=/dev/biren:/dev/biren -it your_image
```

## Notes

- 需要安装 BIRENSUPA Driver
- Docker 需配置 biren 运行时
- 确保主机上已正确安装驱动

## Related Components

- **BIRENSUPA Driver**: GPU 驱动
- **BIRENSUPA SDK**: 开发工具包