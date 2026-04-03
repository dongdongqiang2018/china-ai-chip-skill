---
name: mx-diagease
description: 沐曦GPU一键诊断工具，用于对曦云系列GPU设备进行PCIe诊断、内存诊断、功耗监测、GPU压测等。是FAE现场问题排查的常用工具。
keywords:
  - 沐曦
  - 诊断工具
  - mx-diagease
  - GPU诊断
  - 内存诊断
  - PCIe诊断
  - 压测
  - 监控
---

# mx-diagease 使用指南

mx-diagease（沐曦一键诊断工具）提供对单节点曦云®系列设备进行一键诊断的功能，支持PCIe诊断、MetaXLink诊断、内存诊断、电源功耗诊断和GPU压测。

## 快速开始

### 基本诊断

```bash
# 查看所有GPU设备列表
mx-diagease -L

# 对所有板卡执行诊断（需要sudo）
sudo mx-diagease

# 对指定设备进行诊断
sudo mx-diagease -i 0

# 对多个指定设备诊断（逗号分隔）
sudo mx-diagease -i 0,1,5

# 设备ID范围诊断
sudo mx-diagease -i 0-2
```

### 监控模式

```bash
# 监控模式，持续监控100秒
sudo mx-diagease -m -t 100

# 监控模式，指定1小时22分35秒
sudo mx-diagease -m -t 01:22:35

# 持续监控直到Ctrl+C退出
sudo mx-diagease -m
```

## 诊断模式

### 诊断项目

| 诊断项目 | 说明 |
|----------|------|
| 内存诊断 | 诊断设备内存完整性、稳定性和可靠性，可发现坏页、位错误等问题 |
| PCIe诊断 | 诊断PCIe链路完整性，包含H2D/D2H带宽、P2P诊断 |
| GPU压测 | GPU及CPU压测，诊断高负载下整卡稳定性和AP稳定性 |
| MetaXLink诊断 | 诊断设备间MetaXLink链路完整性和带宽 |
| 电源管理诊断 | 诊断功耗、温度及动态电源管理相关指标 |
| PCIeACS检查 | 检查PCIe ACS状态（建议关闭） |
| IOMMU检查 | 检查IOMMU状态（建议关闭） |
| CPU工作模式 | 检查主机CPU工作模式（建议performance） |

### 生成诊断配置文件

```bash
# 生成默认配置文件
mx-diagease --generate-template
```

配置文件示例 (diagease-config.json):

```json
{
  "pcie": {
    "speed": 32,
    "width": 16,
    "bw_h2d": 47000,
    "bw_d2h": 52000,
    "bw_h2d_d2h": 77000,
    "bw_uni_p2p": 36000,
    "bw_bi_p2p": 73000
  },
  "metaxlink": {
    "bw_uni_p2p": 49000,
    "bw_bi_p2p": 90000
  },
  "memorytest": {
    "test_indexes": [0,1,2,3,4,5,6,7,8,9,10],
    "mc_stress_cycles": 20
  },
  "stress": {
    "runtime": 300,
    "cpu_stress_enable": 1,
    "mxlk_stress_enable": 1
  }
}
```

### 使用自定义配置诊断

```bash
sudo mx-diagease --configfile /path/to/diagease-config.json
```

## 监控模式

### 监控项目

| 监测类别 | 异常类型 | 日志信息 |
|----------|----------|----------|
| 功耗监测 | 超功耗 | Device(xxx) powerexceedslimit |
| 过温监测 | 过温/CTF | Device(xxx) chiptemperatureexceedslimit |
| PCC监测 | 异常 | warningPcc / criticalPcc |
| Powerbrake | 异常 | warningPwrbrk / criticalPwrbrk |
| DI/DT监测 | 异常 | warningDidt / criticalDidt |
| Powerstate | 异常 | criticalpowerstateerror |

### 监控命令示例

```bash
# 拉起GPU压测并监控
sudo mx-diagease -m -r "/opt/maca/bin/mxvs stress --xcore"

# 监控并设置日志级别
sudo mx-diagease -m --set-loglevel 4
```

## 无驱动检查

在未加载驱动时，可以查看设备基本信息：

```bash
# 查看设备BDF ID
mx-diagease -L

# 检查指定设备信息（无驱动）
mx-diagease --check <bdfid>
```

输出示例：

```
Smp0 Init.All.Finish
PCIe link speed: Gen5
PCIe link width: x16
MetaX link4 speed: Gen5
MetaX link4 width: x16
Vbios Version: 1.23.0.0-7066
Vbios Binary Name: C500
```

## 参数说明

| 参数 | 说明 |
|------|------|
| -i, --index | 指定设备ID，默认所有设备 |
| -m, --monitor | 进入监控模式 |
| -t, --time | 监控时长，支持秒或hh:mm:ss格式 |
| -r, --run | 监控模式下拉起程序 |
| -c, --configfile | 指定诊断配置文件 |
| -g, --generate-template | 生成默认配置文件 |
| --check | 检查PCIe/MetaXLink速率和smp状态 |
| -L, --list | 列出所有设备 |
| --set-loglevel | 设置日志级别 (0-4) |
| -q, --quiet | 静默模式，不打印输出 |

## 日志文件

诊断日志默认保存在运行目录 `mxdiag-log/mxdiag_<date>.log` 下。

## 注意事项

1. 使用前需确认已加载曦云系列GPU驱动
2. 一键诊断时确保诊断程序单独运行，避免其他进程影响结果
3. 可用 `mx-smi --show-all-process` 查看是否有用户进程
4. 不支持虚拟化后的GPU或sGPU切分后的检测
5. 执行诊断命令需要sudo权限

## 官方参考

- 《曦云系列通用GPU驱动安装指南》
- 《曦云系列通用GPU快速上手指南》
- MXMACA SDK安装包 (>=2.27.0)