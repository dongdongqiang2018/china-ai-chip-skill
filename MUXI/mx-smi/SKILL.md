---
name: mx-smi
description: 沐曦GPU设备管理工具，用于查询GPU状态、功耗、温度、版本信息，执行固件升级、Warm Reset、虚拟化配置等操作。是FAE日常工作中最常用的GPU管理命令行工具。
keywords:
  - 沐曦
  - GPU管理
  - mx-smi
  - 设备查询
  - 功耗管理
  - 固件升级
  - 虚拟化
---

# mx-smi 使用指南

mx-smi（MetaX System Management Interface）是用于管理曦云®系列GPU的命令行工具，可以实时查询GPU的信息，包括版本，温度，使用率，功耗，时钟频率等，并具有启用和禁用GPU配置选项，执行固件升降级等功能。

## 快速开始

### 查看GPU列表
```bash
# 查看所有GPU设备
mx-smi -L

# 以JSON格式显示
mx-smi -L -j
```

### 常用查询命令
```bash
# 查看GPU温度
mx-smi --show-temperature

# 查看GPU功耗
mx-smi --show-board-power

# 查看GPU显存使用
mx-smi --show-memory

# 查看版本信息（BIOS、驱动、Firmware）
mx-smi --show-version

# 查看GPU使用率
mx-smi --show-usage

# 查看进程信息
mx-smi --show-process

# 查看所有设备系统信息
mx-smi --show-sysinfo
```

### 持续监控
```bash
# 每500ms刷新显示温度、功耗、使用率
mx-smi --show-temperature --show-board-power --show-usage -l 500

# 轮询设备状态，每秒一次
mx-smi dmon --show-temperature --show-board-power -i 0 -c 100
```

---

## 命令详解

### 1. 通用选项

| 参数 | 说明 |
|------|------|
| `-h, --help` | 打印使用帮助信息 |
| `-v, --version` | 打印mx-smi的版本信息 |
| `-j, --json` | 以JSON格式显示板卡信息 |
| `-i <GPU-ID>` | 指定设备ID，默认显示全部 |
| `-l ms` | 以特定间隔周期持续显示 |
| `-o filename` | 将输出写入CSV文件 |

### 2. 查询选项

#### 温度与功耗
```bash
# 温度
mx-smi --show-temperature

# 板卡功耗（电压、电流、功耗）
mx-smi --show-board-power

# 芯片内功耗（支持C588分die显示）
mx-smi --show-pmbus-power
```

#### 存储与带宽
```bash
# 显存使用情况
mx-smi --show-memory

# 显存动态带宽
mx-smi --show-hbm-bandwidth

# PCIe带宽
mx-smi --show-pcie
```

#### 时钟与性能
```bash
# 时钟信息
mx-smi --show-clock
mx-smi --show-clocks all

# 当前性能等级
mx-smi --show-dpm cur

# 支持的性能等级
mx-smi --show-dpm all
mx-smi --show-dpm-max
```

#### 设备信息
```bash
# 序列号信息
mx-smi --show-sn

# EEPROM信息（板卡版本、序列号）
mx-smi --show-eeprom

# 硬件汇总信息
mx-smi --show-hwinfo

# 电源模式
mx-smi --show-power-mode

# 持久模式
mx-smi --show-persistence-mode
```

#### 错误与事件
```bash
# PCIe错误事件
mx-smi --show-event aer_ue    # 不可纠正错误
mx-smi --show-event aer_ce    # 可纠正错误
mx-smi --show-event all       # 所有错误

# 降频原因
mx-smi --show-clk-tr

# 设备不可用原因
mx-smi --show-unavailable-reason

# ECC错误计数
mx-smi --count-ecc
```

### 3. 控制选项

#### Warm Reset
```bash
# 对指定卡执行Warm Reset
mx-smi -r -i <GPU-ID>

# 对所有GPU卡执行Warm Reset
mx-smi -r -i all
```

#### 固件升级
```bash
# 升级VBIOS（需root权限）
sudo mx-smi -u /lib/firmware/metax/$chip_type/mxvbios-xxx.bin -t 600

# 指定设备升级
sudo mx-smi -U /lib/firmware/metax/$chip_type/mxvbios-xxx.bin -t 600 -i ID
```

#### 性能配置
```bash
# 设置电源模式（0:Normal, 1:High）
mx-smi --set-power-mode {0|1} -i <GPU-ID>

# 设置持久模式（0:关闭, 1:打开）
mx-smi --set-persistence-mode {0|1} -i <GPU-ID>

# 设置最大性能等级
mx-smi --set-dpm-max xcore,7 -i 1
```

### 4. sGPU虚拟化（仅C500）

```bash
# 启用sGPU功能
mx-smi sgpu --enable -i <GPU-ID>

# 查看sGPU模式
mx-smi sgpu --show-mode

# 禁用sGPU功能
mx-smi sgpu --disable -i <GPU-ID>

# 创建子设备
mx-smi sgpu -i <GPU-ID> --create --vram 4G --compute 5 --alias sgpu-test

# 查看子设备信息
mx-smi sgpu

# 修改子设备资源配置
mx-smi sgpu -i <GPU-ID> --set <SGPU-ID> --vram 4G --compute 10

# 设置调度策略（0:争抢模式, 1:固定配额, 2:保证配额+弹性）
mx-smi sgpu --set-sched-class {0|1|2} -i <GPU-ID>

# 设置时间片大小
mx-smi sgpu --set-timeslice 20 -i <GPU-ID>

# 移除子设备
mx-smi sgpu --remove <SGPU-ID> -i <GPU-ID>
```

### 5. VM虚拟化

```bash
# 开启虚拟化（支持1,2,4,8个VF）
mx-smi vm --enable-vf {1|2|4|8}

# 关闭虚拟化
mx-smi vm --disable-vf

# 显示虚拟化后的GPU信息
mx-smi vm --show-vf
```

### 6. 拓扑查询

```bash
# 显示连接方式及CPU/NUMA亲和性
mx-smi topo -m

# 显示相对距离
mx-smi topo -d

# 显示拓扑树
mx-smi topo -t

# 显示与网卡连接方式
mx-smi topo -n
```

### 7. MetaXLink相关

```bash
# 显示带宽和速率
mx-smi mxlk --show

# 显示连接状态
mx-smi mxlk --show-state

# 启用/禁用连接
mx-smi mxlk --set-state {0|1}

# 显示错误统计
mx-smi mxlk --show-aer

# 显示流量统计
mx-smi mxlk --show-traffic-stat
```

### 8. RAS相关

```bash
# 显示错误计数
mx-smi ras --show-count -i 0

# 显示错误状态
mx-smi ras --show-status -i 0
```

### 9. ETH相关（仅C600）

```bash
# ETH带宽
mx-smi eth --show-bandwidth

# ETH使用率
mx-smi eth --show-usage

# MAC地址
mx-smi eth --show-mac-addr

# ETH错误统计
mx-smi eth --show-ras-count

# ETH时钟
mx-smi eth --show-clock
```

---

## 故障排查

### 设备不可用
```bash
# 查看不可用原因
mx-smi --show-unavailable-reason
```

### 查看严重事件
```bash
# 显示PCIe及MetaXLink严重错误
mx-smi misc --show-critical-event

# 显示MMIO状态
mx-smi misc --show-mmio-state

# 显示PCIe日志事件
sudo mx-smi misc --show-pcie-event --detail
```

### 温度异常
```bash
# 监控温度变化
mx-smi --show-temperature -l 1000
```

### 进程占用
```bash
# 查看GPU上运行的进程
mx-smi --show-all-process
```

---

## 在容器中使用

```bash
# 基础挂载（仅查询类命令）
docker run -v --device=/dev/dri -v /opt/mxdriver/bin/mx-smi:/opt/mxdriver/bin/mx-smi <IMAGE-ID>

# 完整权限（执行设置类命令）
docker run --privileged=true -v --device=/dev/dri -v /opt/mxdriver/bin/mx-smi:/opt/mxdriver/bin/mx-smi <IMAGE-ID>
```

---

## 编程接口

### Python (pymxsml)

```python
from pymxsml import *

# 初始化
mxSmlInit()

# 获取设备数量
device_num = mxSmlGetDeviceCount()

# 获取设备信息
for i in range(device_num):
    device_info = mxSmlGetDeviceInfo(i)
    print(f"device id: {i}, bdf id: {device_info.bdfId}, type: {device_info.deviceName}")
```

### C/C++

```c
#include "MxSml.h"

// 初始化
mxSmlReturn_t ret = mxSmlInit();

// 获取设备数量
int deviceNum = mxSmlGetDeviceCount();

// 获取设备信息
for(int i = 0; i < deviceNum; i++) {
    mxSmlDeviceInfo_t deviceInfo;
    if(mxSmlGetDeviceInfo(i, &deviceInfo) == MXSML_Success) {
        printf("device id: %d, bdf: %s, type: %s\n", i, deviceInfo.bdfId, deviceInfo.deviceName);
    }
}
```

---

## 官方参考

- [曦云系列通用GPU mx-smi使用手册_CN_V13.pdf](../文档/mx-smi使用手册_CN_V13.pdf)
- [曦云系列通用GPU 驱动安装指南_CN_V11.pdf](../文档/驱动安装指南_CN_V11.pdf)
- [曦云系列通用GPU Warm Reset使用指南_CN_V05.pdf](../文档/Warm%20Reset使用指南_CN_V05.pdf)