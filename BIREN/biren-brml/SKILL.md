---
name: biren-brml
description: BIREN BRML (BIREN Management Library) C语言管理库参考指南。用于通过编程方式监控和管理 GPU 状态，包括设备查询、温度监控、功耗管理、内存信息、时钟控制、ECC 错误、P2P 拓扑等。
keywords:
  - brml
  - biren
  - GPU管理
  - C语言库
  - 设备监控
  - 编程接口
  - 壁仞
---

# BRML Command Reference

BRML 是壁仞 GPU 的 C 语言管理库，提供编程接口用于监控和管理 GPU 状态。BRsmi 命令行工具基于 BRML 构建。

## Quick Start

```c
#include "brml.h"

brmlInit();
brmlDeviceGetCount(&device_count);
for (int i = 0; i < device_count; ++i) {
    brmlDeviceGetHandleByIndex(i, &device);
    brmlDeviceGetPciInfo(device, &pciInfo);
    printf("GPU %d: %s\n", i, pciInfo.busId);
}
brmlShutdown();
```

编译：`gcc get_gpu_busid.c -o get_gpu_busid -lbiren-ml`

## API Categories

### Initialization

| API | Description |
|-----|-------------|
| `brmlInit()` | 初始化 BRML 库 |
| `brmlShutdown()` | 关闭 BRML 库 |

### Error Handling

| API | Description |
|-----|-------------|
| `brmlErrorString()` | 获取错误信息字符串 |

### System Information (13 APIs)

| API | Description |
|-----|-------------|
| `brmlSystemGetDriverVersion()` | 获取驱动版本 |
| `brmlDeviceGetMemoryInfo()` | 获取内存信息 |
| `brmlDeviceGetUUID()` | 获取 UUID |

### Device Information (51 APIs)

| API | Description |
|-----|-------------|
| `brmlDeviceGetCount()` | 获取设备数量 |
| `brmlDeviceGetTemperature()` | 获取温度 |
| `brmlDeviceGetPowerUsage()` | 获取功耗 |
| `brmlDeviceGetClockInfo()` | 获取时钟信息 |

### Memory & Codec (13 APIs)

| API | Description |
|-----|-------------|
| `brmlDeviceGetUtilizationRates()` | 获取利用率 |
| `brmlDeviceGetEccMode()` | 获取 ECC 模式 |
| `brmlDeviceGetHealthStatus()` | 获取健康状态 |

### Process Information

| API | Description |
|-----|-------------|
| `brmlDeviceGetProcessUtilization()` | 获取进程利用率 |

### GPU Topology (16 APIs)

| API | Description |
|-----|-------------|
| `brmlDeviceGetTopologyCommonAncestor()` | 获取拓扑共同祖先 |
| `brmlDeviceGetP2PStatus_v2()` | 获取 P2P 状态 |
| `brmlDeviceGetBrLinkNumber()` | 获取 BLink 数量 |

### Device Settings (22 APIs)

| API | Description |
|-----|-------------|
| `brmlDeviceGet/SetL2padSize()` | 获取/设置 L2 pad 大小 |
| `brmlDeviceGet/SetDtgMode()` | 获取/设置 DTG 模式 |
| `brmlDeviceGet/SetHealthCheckMode()` | 获取/设置健康检查模式 |

## Key Enumerations

### Temperature Sensors (11 types)

| Enum | Description |
|------|-------------|
| `BRML_TEMPERATURE_GPU` | GPU 温度 |
| `BRML_TEMPERATURE_MEMORY` | 显存温度 |
| `BRML_TEMPERATURE_SPC` | SPC 温度 |
| `BRML_TEMPERATURE_BOARD_SENSOR_0-3` | 板级传感器 |
| `BRML_TEMPERATURE_DIODE_SENSOR_0-3` | 二极管传感器 |

### Clock Types (5 types)

| Enum | Description |
|------|-------------|
| `BRML_CLOCK_TYPE_SOC` | SOC 时钟 |
| `BRML_CLOCK_TYPE_CORE` | 核心时钟 |
| `BRML_CLOCK_TYPE_MEMORY` | 显存时钟 |
| `BRML_CLOCK_TYPE_ENCODE` | 编码器时钟 |
| `BRML_CLOCK_TYPE_DECODE` | 解码器时钟 |

### Health Status

| Enum | Description |
|------|-------------|
| `BRML_GPU_HEALTH_STATUS_OK` | 正常 |
| `BRML_GPU_HEALTH_STATUS_WARNING` | 警告 |
| `BRML_GPU_HEALTH_STATUS_CRITICAL_WARNING` | 严重警告 |
| `BRML_GPU_HEALTH_STATUS_ERROR` | 错误 |

### GPU State

| Enum | Description |
|------|-------------|
| `BRML_GPU_STATE_NORMAL` | 正常 |
| `BRML_GPU_STATE_HANG` | 挂起 |
| `BRML_GPU_STATE_RESETING` | 复位中 |
| `BRML_GPU_STATE_REMOVED` | 已移除 |
| `BRML_GPU_STATE_RECOVERY` | 恢复中 |

### Compute Mode

| Enum | Description |
|------|-------------|
| `BRML_COMPUTE_MODE_DEFAULT` | 默认模式 |
| `BRML_COMPUTE_MODE_EXCLUSIVE_PROCESS` | 独占进程 |
| `BRML_COMPUTE_MODE_PROHIBITED` | 禁止使用 |

### Virtualization Mode

| Enum | Description |
|------|-------------|
| `BRML_GPU_VIRTUALIZATION_MODE_NONE` | 无虚拟化 |
| `BRML_GPU_VIRTUALIZATION_MODE_PASSTHROUGH` | 直通模式 |
| `BRML_GPU_VIRTUALIZATION_MODE_VGPU` | VGPU 模式 |
| `BRML_GPU_VIRTUALIZATION_MODE_HYPERVISOR_HOST` | 超 Hypervisor 主机 |

## Key Structures

### brmlPciInfo_st

```c
typedef struct {
    unsigned int domain;
    unsigned int bus;
    unsigned int device;
    unsigned int function;
    unsigned int pciDeviceId;
    char busId[32];
} brmlPciInfo_st;
```

### brmlMemory_st

```c
typedef struct {
    unsigned long long total;   // bytes
    unsigned long long free;    // bytes
    unsigned long long used;    // bytes
} brmlMemory_st;
```

### brmlUtilization_st

```c
typedef struct {
    unsigned int gpu;   // percentage
    unsigned int memory; // percentage
} brmlUtilization_st;
```

### brmlGpuUtilization_st

```c
typedef struct {
    unsigned int spc;   // SPC 利用率
    unsigned int cp;    // CP 利用率
    unsigned int sdma;  // SDMA 利用率
    unsigned int vdcp; // VDCP 利用率
    unsigned int vecp;  // VECP 利用率
    unsigned int vdec;  // 视频解码利用率
    unsigned int venc;  // 视频编码利用率
} brmlGpuUtilization_st;
```

## Return Codes

| Code | Description |
|------|-------------|
| `BRML_SUCCESS` | 成功 |
| `BRML_ERROR_UNINITIALIZED` | 未初始化 |
| `BRML_ERROR_INVALID_ARGUMENT` | 无效参数 |
| `BRML_ERROR_TIMEOUT` | 超时 |
| `BRML_ERROR_UNKNOWN` | 未知错误 |

## Example: Get GPU Temperature

```c
#include "brml.h"
#include <stdio.h>

int main() {
    brmlInit();

    int device_count;
    brmlDeviceGetCount(&device_count);

    for (int i = 0; i < device_count; i++) {
        brmlDeviceHandle_t device;
        brmlDeviceGetHandleByIndex(i, &device);

        unsigned int temperature;
        brmlDeviceGetTemperature(device, BRML_TEMPERATURE_GPU, &temperature);
        printf("GPU %d Temperature: %u C\n", i, temperature);
    }

    brmlShutdown();
    return 0;
}
```

## Example: Get GPU Memory

```c
#include "brml.h"
#include <stdio.h>

int main() {
    brmlInit();

    brmlDeviceHandle_t device;
    brmlDeviceGetHandleByIndex(0, &device);

    brmlMemory_st memory;
    brmlDeviceGetMemoryInfo(device, &memory);

    printf("Total: %llu MB\n", memory.total / 1024 / 1024);
    printf("Used: %llu MB\n", memory.used / 1024 / 1024);
    printf("Free: %llu MB\n", memory.free / 1024 / 1024);

    brmlShutdown();
    return 0;
}
```

## Installation

| Type | Path |
|------|------|
| Header | `/usr/local/birensupa/driver/biren-smi/include/brml.h` |
| Library | `/usr/local/birensupa/driver/biren-smi/libbiren-ml.so.1.6.0` |

## Notes

- 需要 root 权限访问 GPU 设备
- 使用前必须调用 `brmlInit()` 初始化
- 使用完成后调用 `brmlShutdown()` 释放资源
- 某些 API 需要管理员权限

## Official Documentation

- BIRENSUPA Driver Documentation
- BRsmi User Guide (brsmi 基于 BRML 构建)