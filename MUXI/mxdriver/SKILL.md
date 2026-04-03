---
name: mxdriver
description: 沐曦GPU驱动安装和管理工具，用于安装、升级、回滚曦云GPU驱动程序。包含KMD/UMD驱动和固件。
keywords:
  - 沐曦
  - 驱动安装
  - mxdriver
  - 固件
  - 驱动管理
---

# 驱动安装指南

曦云系列GPU驱动安装配置指南。

## 快速开始

### 安装驱动

```bash
# 切换到root用户
sudo su

# 运行安装脚本
sudo ./MXMACA-Driver-*.run

# 或使用包管理器
sudo apt install mxmaca-driver
```

### 验证安装

```bash
# 查看驱动状态
lsmod | grep maca

# 查看设备
mx-smi -L
```

## 安装前检查

### 系统要求

- Linux Kernel >= 3.10
- GCC >= 4.8
- CUDA Driver (兼容)

### 检查前置条件

```bash
# 检查内核版本
uname -r

# 检查GCC版本
gcc --version

# 检查已有驱动
lsmod | grep -i nvidia
```

## 安装步骤

### 1. 准备安装环境

```bash
# 禁用nouveau驱动
sudo bash -c 'echo -e "blacklist nouveau\noptions nouveau modeset=0" > /etc/modprobe.d/blacklist-nouveau.conf'

# 更新initramfs
sudo update-initramfs -u

# 重启
sudo reboot
```

### 2. 安装驱动

```bash
# 添加执行权限
chmod +x MXMACA-Driver-*.run

# 静默安装
sudo ./MXMACA-Driver-*.run --silent

# 或交互安装
sudo ./MXMACA-Driver-*.run
```

### 3. 配置环境变量

```bash
# 添加到bashrc
echo 'export MACA_PATH=/opt/maca' >> ~/.bashrc
echo 'export PATH=$MACA_PATH/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 4. 验证

```bash
# 检查驱动加载
lsmod | grep maca

# 检查设备节点
ls -l /dev/mxmaca*

# 使用mx-smi
mx-smi -L
```

## 升级驱动

```bash
# 停止相关服务
sudo systemctl stop mxmaca*

# 卸载旧驱动
sudo ./MXMACA-Driver-old.run --uninstall

# 安装新驱动
sudo ./MXMACA-Driver-new.run --silent

# 重启
sudo reboot
```

## 卸载驱动

```bash
# 卸载
sudo ./MXMACA-Driver-*.run --uninstall

# 或使用包管理器
sudo apt remove mxmaca-driver
```

## 固件更新

```bash
# 更新固件
sudo mx-smi --firmware-update

# 查看固件版本
mx-smi --show-version
```

## 常见问题

### 驱动加载失败

```bash
# 检查dmesg
dmesg | grep -i maca

# 检查依赖
modinfo maca
```

### 权限问题

```bash
# 添加用户组
sudo groupadd maca
sudo usermod -aG maca $USER

# 重新登录
```

## 官方参考

- 《曦云系列通用GPU驱动安装指南》