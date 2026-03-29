---
name: brsmi
description: 壁仞（BIREN）GPU 设备管理 Skill，提供实时监控、健康诊断、GPU状态查询、功耗/温度/利用率查询、多卡拓扑配置等专家级能力。brsmi 是壁仞 BIRENSUPA GPU 的官方管理工具，基于 BRML 库构建，功能类似 NVIDIA nvidia-smi。
keywords:
  - biren
  - 壁仞
  - brsmi
  - GPU监控
  - 设备管理
  - BRML
---

# brsmi 壁仞GPU设备管理

## 功能描述

brsmi（BIREN System Management Interface）是壁仞官方提供的 GPU 管理命令行工具，基于 BRML（BIREN Management Library）构建，用于监控和管理壁仞 BIRENSUPA 系列 GPU 设备。本 Skill 提供完整的设备查询、状态监控、拓扑查看、故障诊断等能力，支持 AI 训练和推理场景的自动化运维。

## 核心能力

### 1. 基础信息查询

```bash
# 查看所有 GPU 设备概览
brsmi

# 查看版本信息
brsmi --version

# 列出所有 GPU 设备
brsmi gpu list

# 查询 GPU 详细信息
brsmi gpu query -i 0
```

**输出示例：**
```
+-------------------------------------------------------------------------------+
| GPU  Id  |     Name     |  Mode  |  Temperature  |  Power  |  Memory      |
|===============================================================================|
|   0      | BIREN GPU    |  N/A   |   45°C       |  250W   |  32GB/64GB   |
|   1      | BIREN GPU    |  N/A   |   47°C       |  245W   |  40GB/64GB   |
+-------------------------------------------------------------------------------+
```

### 2. 实时监控

```bash
# 滚动显示 GPU 统计信息 (Device Monitor)
brsmi gpu dmon

# 监控指定 GPU
brsmi gpu dmon -i 0,1

# 设置刷新间隔
brsmi gpu dmon -d 1000  # 1000ms

# 按指标过滤 (-s 参数)
brsmi gpu dmon -s p        # 功耗和温度
brsmi gpu dmon -s u        # SPC/Memory利用率
brsmi gpu dmon -s c        # 时钟信息
brsmi gpu dmon -s m        # 内存信息
brsmi gpu dmon -s e        # ECC错误
brsmi gpu dmon -s t        # PCIe吞吐量
brsmi gpu dmon -s b        # P2P吞吐量
brsmi gpu dmon -s d        # 显存带宽

# 组合示例
brsmi gpu dmon -s pu       # 功耗+利用率
```

### 3. 进程监控

```bash
# Process Monitor
brsmi gpu pmon

# 查询进程信息
brsmi gpu query --process -i 0
```

### 4. 拓扑查看

```bash
# GPU 拓扑互联信息
brsmi topo -m

# P2P 连接信息
brsmi topo --p2p

# 显示完整拓扑矩阵
brsmi topo --matrix
```

### 5. GPU 状态与配置

```bash
# 显示 GPU 状态
brsmi gpu stats

# 显示 FRU 信息
brsmi gpu fru

# 显示 BAR 空间配置
brsmi gpu conf

# 显示光模块信息
brsmi gpu optm
```

### 6. GPU 参数设置

```bash
# 设置计算模式
brsmi gpu set -c exclusive_process   # 独占进程模式
brsmi gpu set -c prohibited          # 禁止使用

# 设置持久模式
brsmi gpu set -p 1                  # 开启持久模式
brsmi gpu set -p 0                  # 关闭持久模式

# 设置 SVI 模式（虚拟化）
brsmi gpu set -s 0                  # 关闭
brsmi gpu set -s 1                  # 二切
brsmi gpu set -s 2                  # 四切

# 设置 SPC 频率
brsmi gpu set --pclk 1000           # 1000MHz

# 设置性能级别
brsmi gpu set --perf 0              # 性能模式
```

### 7. GPU 复位

```bash
# 复位 GPU
brsmi reset -g 0                    # 复位 GPU 0

# 复位 ECC 计数器
brsmi reset -e 0
```

## 常见场景

### 场景1：训练前集群状态检查

大规模 AI 训练前验证所有 GPU 正常可用。

```bash
# 快速检查所有 GPU 状态
brsmi

# 检查显存是否充足
brsmi gpu query -i 0 --memory

# 检查 GPU 拓扑
brsmi topo --p2p
```

**检查清单：**
- [ ] 所有 GPU 状态为 NORMAL
- [ ] 显存充足（建议至少预留 20%）
- [ ] 温度正常（< 85°C）
- [ ] P2P 互联正常

### 场景2：推理服务健康监控

生产环境推理服务持续监控。

```bash
# 持续监控 GPU 利用率和显存
brsmi gpu dmon -s u -d 1000

# 监控功耗和温度
brsmi gpu dmon -s p -d 1000
```

**告警阈值建议：**
| 指标 | 告警阈值 |
|------|----------|
| GPU 利用率 | > 95% 持续 5min |
| 显存使用 | > 90% |
| GPU 温度 | > 85°C |
| GPU 功耗 | > 350W |

### 场景3：故障定位与诊断

GPU 异常时的故障诊断流程。

```bash
# 1. 查看 GPU 状态
brsmi gpu stats

# 2. 查看错误信息
brsmi gpu dmon -s e

# 3. 查看进程占用
brsmi gpu pmon

# 4. 检查拓扑
brsmi topo --p2p
```

### 场景4：GPU 参数调优

优化 GPU 性能参数。

```bash
# 开启持久模式（适合多任务场景）
brsmi gpu set -p 1

# 设置性能模式
brsmi gpu set --perf 0

# 调整 SPC 频率
brsmi gpu set --pclk 1200
```

## BRML API 编程

壁仞还提供 BRML C API 供程序调用。

```c
#include "brml.h"

int main() {
    brmlInit();

    int device_count;
    brmlDeviceGetCount(&device_count);
    printf("Found %d GPUs\n", device_count);

    for (int i = 0; i < device_count; ++i) {
        brmlDeviceHandle device;
        brmlDeviceGetHandleByIndex(i, &device);

        // 获取温度
        int temp;
        brmlDeviceGetTemperature(device, BRML_TEMP_GPU, &temp);
        printf("GPU %d Temperature: %d°C\n", i, temp);

        // 获取显存
        brmlMemory memory;
        brmlDeviceGetMemoryInfo(device, &memory);
        printf("GPU %d Memory: %lu/%lu MB\n",
               memory.used / 1024 / 1024,
               memory.total / 1024 / 1024);
    }

    brmlShutdown();
    return 0;
}
```

编译：`gcc gpu_info.c -o gpu_info -lbiren-ml`

## 故障排查

### 问题1：GPU 不可见

**症状：** `brsmi` 显示无设备

**排查步骤：**
```bash
# 1. 检查驱动加载
lsmod | grep biren

# 2. 检查设备节点
ls -la /dev/dri/

# 3. 检查驱动状态
systemctl status biren-driver

# 4. 重新加载驱动
sudo rmmod biren_driver
sudo modprobe biren_driver
```

### 问题2：GPU 利用率异常低

**症状：** 训练/推理性能差，GPU 利用率持续偏低

**排查步骤：**
```bash
# 1. 检查数据加载
brsmi gpu dmon -s u

# 2. 检查 CPU
htop

# 3. 检查网络
# 分布式训练时网络延迟

# 4. 检查 PCIe 拓扑
brsmi topo --matrix
```

### 问题3：多卡通信异常

**症状：** 分布式训练卡死或通信超时

**排查步骤：**
```bash
# 1. 检查 GPU 拓扑
brsmi topo --p2p

# 2. 检查 P2P 带宽
brsmi gpu dmon -s b

# 3. 检查 PCIe 状态
brsmi gpu conf
```

### 问题4：显存不足

**症状：** 训练时 OOM

**排查步骤：**
```bash
# 1. 查看显存使用
brsmi gpu query -i 0 --memory

# 2. 查看占用进程
brsmi gpu pmon

# 3. 清理进程
kill <pid>
```

## 相关文档

- [壁仞_07GPU管理与测试](../../china-ai-chip-docs/BIREN/壁仞_07GPU管理与测试.md)
- [壁仞_01安装（环境搭建）](../../china-ai-chip-docs/BIREN/壁仞_01安装（环境搭建）.md)

## 环境变量参考

| 变量 | 说明 |
|------|------|
| `BRML_DEBUG` | 调试模式 (0/1) |
| `CUDA_VISIBLE_DEVICES` | 指定可见 GPU |

## 配套工具

| 工具 | 用途 |
|------|------|
| `brsmi` | GPU 设备管理 |
| `brml.h` | C 管理库 |
| `suDCGM` | 数据中心 GPU 监控 |
| `suCCL` | 通信库 |