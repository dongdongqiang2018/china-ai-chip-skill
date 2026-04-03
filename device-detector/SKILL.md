---
name: device-detector
description: 使用lspci命令识别当前设备的GPU类型和厂商，支持沐曦(MetaX)、华为(Ascend)、壁仞(Biren)等国产AI芯片及NVIDIA、AMD、Intel等国际厂商
keywords:
  - lspci
  - GPU识别
  - 设备检测
  - 国产芯片
  - MetaX
  - Ascend
  - Biren
---

# GPU设备识别

本Skill用于识别当前服务器/工作站的GPU设备类型和厂商，帮助快速定位应该使用哪个芯片厂商的技能集。

## 快速开始

### 基础识别

```bash
# 查看所有显示设备（GPU/集成显卡）
lspci | grep -i vga

# 或者使用更通用的方式
lspci | grep -E "VGA|3D|Display"
```

### 按厂商筛选

```bash
# 识别NVIDIA
lspci | grep -i nvidia

# 识别AMD (包括Radeon系列)
lspci | grep -i amd

# 识别Intel (集成显卡)
lspci | grep -i intel

# 识别沐曦 (MetaX)
lspci | grep -i meta

# 识别华为昇腾 (Ascend)
lspci | grep -i ascend
lspci | grep -i huawei

# 识别壁仞 (Biren)
lspci | grep -i biren

# 识别摩尔线程 (Moore Threads)
lspci | grep -i "moore threads"

# 识别寒武纪 (Cambricon)
lspci | grep -i cambricon
```

### 完整系统检测脚本

```bash
#!/bin/bash
# 检测当前系统的GPU厂商

echo "========== GPU设备检测 =========="
echo ""

# 收集所有显示控制器信息
VGA_DEVICES=$(lspci | grep -E "VGA|3D|Display" | grep -v "Bridge")

if [ -z "$VGA_DEVICES" ]; then
    echo "未检测到GPU设备"
    exit 1
fi

echo "检测到的GPU设备:"
echo "$VGA_DEVICES"
echo ""

# 厂商检测
echo "========== 厂商识别 =========="

if echo "$VGA_DEVICES" | grep -qi "nvidia"; then
    echo "✓ 检测到: NVIDIA GPU"
    echo "  相关Skills: 请参考 NVIDIA 官方文档"
fi

if echo "$VGA_DEVICES" | grep -qi "amd"; then
    echo "✓ 检测到: AMD GPU"
    echo "  相关Skills: 请参考 AMD ROCm 文档"
fi

if echo "$VGA_DEVICES" | grep -qi "intel"; then
    echo "✓ 检测到: Intel GPU (集成显卡)"
fi

if echo "$VGA_DEVICES" | grep -qi "meta"; then
    echo "✓ 检测到: 沐曦(MetaX) GPU"
    echo "  相关Skills: 参考 ./MUXI/ 目录"
fi

if echo "$VGA_DEVICES" | grep -qi "ascend"; then
    echo "✓ 检测到: 华为昇腾(Ascend) GPU"
    echo "  相关Skills: 参考 ./Ascend/ 目录"
fi

if echo "$VGA_DEVICES" | grep -qi "biren"; then
    echo "✓ 检测到: 壁仞(Biren) GPU"
    echo "  相关Skills: 参考 ./BIREN/ 目录"
fi

if echo "$VGA_DEVICES" | grep -qi "moore"; then
    echo "✓ 检测到: 摩尔线程 GPU"
fi

if echo "$VGA_DEVICES" | grep -qi "cambricon"; then
    echo "✓ 检测到: 寒武纪(Cambricon) AI加速器"
fi

echo ""
echo "========== 详细信息 =========="
# 显示完整的PCIe设备列表（包含厂商ID）
lspci -nn | grep -E "VGA|3D|Display"
```

## 常用Vendor ID参考

| 厂商 | Vendor ID | 关键字 | 对应目录 |
|------|-----------|--------|----------|
| NVIDIA | 0x10de | nvidia | (外部) |
| AMD | 0x1002 | amd, radeon | (外部) |
| Intel | 0x8086 | intel | (外部) |
| 沐曦 | 0x1eae | meta, metax | ./MUXI/ |
| 华为 | 0x19e5 | ascend, huawei | ./Ascend/ |
| 壁仯 | 0x1e9f | biren | ./BIREN/ |
| 摩尔线程 | 0x1e2b | moore threads | (待添加) |
| 寒武纪 | 0x1b22 | cambricon | (待添加) |

## 与Skills联动

检测到GPU厂商后，可以调用对应的Skills：

### 沐曦 (MetaX)

```bash
# 进入MUXI Skills目录
cd MUXI/mx-smi

# 使用mx-smi工具
mx-smi -L
```

### 华为昇腾 (Ascend)

```bash
# Ascend技能目录
cd Ascend/

# 常用命令示例
ascend-info --query-device  # 查询设备信息
npu-smi info               # 查看NPU状态
```

## 故障排查

### 问题：lspci命令不存在

```bash
# Ubuntu/Debian
sudo apt-get install pciutils

# CentOS/RHEL
sudo yum install pciutils

# SUSE
sudo zypper install pciutils
```

### 问题：权限不足

某些lspci操作需要root权限：

```bash
sudo lspci -nn  # 显示完整的vendor ID
```

### 问题：GPU未被识别

```bash
# 检查是否加载了驱动
lsmod | grep -E "nvidia|amdgpu|i915|meta"

# 检查设备是否被系统识别
dmesg | grep -i gpu
dmesg | grep -i pci
```

## 官方参考

- [lspci手册](https://linux.die.net/man/8/lspci)
- [PCI IDs数据库](https://pci-ids.ucw.cz/)
- 沐曦官方文档：参考 `./MUXI/` 目录
- 昇腾官方文档：参考 `./Ascend/` 目录