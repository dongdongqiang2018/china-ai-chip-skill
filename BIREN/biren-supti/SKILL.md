---
name: biren-supti
description: BIREN suPTI 性能追踪接口参考指南。提供 Activity API、Callback API、Event API、Metric API 四类接口，用于追踪和分析 BIRENSUPA 程序的性能，可采集 API 调用、Kernel 执行、硬件计数器等数据。
keywords:
  - supti
  - biren
  - 性能追踪
  - profiler
  - 硬件计数器
  - 回调
  - 壁仞
---

# suPTI Command Reference

suPTI 提供追踪和分析 BIRENSUPA 程序的应用程序接口。

## Quick Start

```c
#include <supti.h>

// 注册回调
suptiSubscribe(&subscriber, cb_func, nullptr);
suptiEnableDomain(subscriber, SUPTI_API_CB_DOMAIN_SUPA, 1);

// Activity API
suptiActivityRegisterCallbacks(bufferMgr, nullptr);
suptiActivityEnable(SUPTI_ACTIVITY_KIND_KERNEL);
```

## Installation

- Header: `/usr/local/birensupa/sdk/latest/supti/include/`
- Library: `/usr/local/birensupa/sdk/latest/supti/lib/`

## API Categories

### Activity API

异步记录 SUPA activities（API 调用、Kernel Launch、Memory Copy）。

### Callback API

SUPA event 回调机制，通知特定事件完成。

### Event API

收集单 kernel 执行的 performance counters。

### Metric API

基于 Event 数据计算 performance metrics。

## Activity API

### Key Functions

| Function | Description |
|----------|-------------|
| `suptiActivityRegisterCallbacks` | 注册缓冲区管理回调 |
| `suptiActivityEnable` | 使能指定类型的 activity 采集 |
| `suptiActivityDisable` | 停止指定类型的 activity 采集 |
| `suptiActivityFlushAll` | 返回已写满和正在使用的缓冲区 |
| `suptiActivityGetNextRecord` | 从缓冲区解析 activity 数据 |
| `suptiProfilerStart` / `suptiProfilerStop` | 动态开启/关闭跟踪 |

### Activity Kind

| Kind | Description |
|------|-------------|
| `SUPTI_ACTIVITY_KIND_KERNEL` | 同步核函数执行 |
| `SUPTI_ACTIVITY_KIND_CONCURRENT_KERNEL` | 异步核函数执行 |
| `SUPTI_ACTIVITY_KIND_MEMCPY` | 内存拷贝操作 |
| `SUPTI_ACTIVITY_KIND_MEMSET` | 内存设置操作 |
| `SUPTI_ACTIVITY_KIND_GRAPH` | 计算图执行 |
| `SUPTI_ACTIVITY_KIND_SUPA` | SUPA 运行时 API |
| `SUPTI_ACTIVITY_KIND_SUDRV` | SUPA 驱动层 API |
| `SUPTI_ACTIVITY_KIND_HOST_FUNCTION` | 主机函数执行 |
| `SUPTI_ACTIVITY_KIND_SYNCHRONIZATION` | 同步操作 |

### Key Structures

| Structure | Description |
|-----------|-------------|
| `SuptiActivityBase` | 基类 (kind, correlationId) |
| `SuptiActivityApi` | SUPA 函数执行 |
| `SuptiActivityKernel` | 核函数执行 |
| `SuptiActivityMemcpy` | 内存拷贝 |
| `SuptiActivityMemset` | 内存设置 |
| `SuptiActivityGraph` | 计算图执行 |

## Callback API

### Setup

```c
SuptiSubscriberHandle subscriber;
suptiSubscribe(&subscriber, cb_func, nullptr);
suptiEnableDomain(subscriber, SUPTI_API_CB_DOMAIN_SUPA, 1);
```

### Callback Function

```c
void cb_func(void *userdata, SuptiCallbackDomain domain,
             SuptiCallbackId cbid, const SuptiCallbackData *cbdata) {
    if (cbdata->site == SUPTI_API_ENTER) {
        // 函数入口
    } else {
        // 函数出口
    }
}
```

### Callback Domain

| Domain | Description |
|--------|-------------|
| `SUPTI_API_CB_DOMAIN_SUPA` | SUPA 运行时 API |
| `SUPTI_API_CB_DOMAIN_SUDRV` | SUPA 驱动层 API |
| `SUPTI_API_CB_DOMAIN_SUTX` | SUTX API |

## Event API

### Usage

```c
// 获取 Event ID
suptiEventGetIdFromName(device, "cbi_active_cycles_spc", &eventId);

// 创建 Event Group
suptiEventGroupCreate(context, &eventGroup, 0);
suptiEventGroupAddEvent(eventGroup, eventId);

// 使能采集
suptiEventGroupEnable(eventGroup);
// ... kernel execution ...
suDeviceSynchronize();
suptiEventGroupReadEvent(eventGroup, SUPTI_EVENT_READ_FLAG_NONE, eventId, &size, &value);
suptiEventGroupDisable(eventGroup);
```

### Available Events

| Event | Description |
|-------|-------------|
| `cbi_active_cycles_spc` | SPC 有效工作指令周期 |
| `tcore_cycles_active_gemm` | GEMM 有效工作指令周期 |
| `eu_cycles_active` | EU 有效工作指令周期 |

## Metric API

### Usage

```c
// 获取 Metric ID
suptiMetricGetIdFromName(dev, "sm_occupancy", &metricId);

// 查询所需 Event 数量
suptiMetricGetNumEvents(metricId, &numEvents);

// 创建 Event Group Sets
suptiMetricCreateEventGroupSets(context, sizeof(metricIdArray), metricIdArray, &sets);

// 采集所有 Event 后计算 Metric
suptiMetricGetValue(dev, metricId, eventIdArraySize, eventIdArray,
                    eventValueArraySize, eventValueArray, timeDuration, &metricValue);
```

### Available Metrics

| Metric | Description |
|--------|-------------|
| `spc_active_cycles` | SPC 执行指令周期 |
| `gemm_usage` | GEMM 使用率 |
| `eu_usage` | EU 使用率 |
| `sm_occupancy` | SM 任务占用率 |
| `sm_efficiency` | SM 使用率 |

## suTX API

### Functions

| API | Description |
|-----|-------------|
| `sutxMark(msg)` | 创建即时标记 |
| `sutxRangeBegin(msg)` | 标记代码段开始 |
| `sutxRangeEnd(msg, activityId)` | 标记代码段结束 |
| `sutxRangePush(msg)` | 开始线程内嵌套代码段 |
| `sutxRangePop()` | 结束线程内嵌套代码段 |

### Python Usage

```python
from libsutx import sutx
stx = sutx.sutx()
stx.sutxMark("Entry")
stx.sutxRangeBegin("begin")
stx.sutxRangeEnd("end", 1)
```

### C++ Usage

```cpp
#include "sutx.h"
sutxMark("mark");
int ret = sutxRangeBegin("begin");
sutxRangeEnd("end", ret);
```

### Combined Usage

```cpp
suProfilerStart();
sutxRangePush("show-me(testAdd-bf16)");
pass &= testAdd<BF16>(1.0f, 1.5f);
sutxRangePop();
suProfilerStop();
```

Command:
```bash
suprof -c supaProfilerApi -t sutx ./a.out
```

## Notes

- 需要初始化 SUPA 运行时
- 某些 API 需要设备上下文
- 合理管理内存缓冲区

## Related Tools

- **suProfiler**: 性能分析工具
- **suPerfViz**: 可视化分析工具
- **suProfilerStart/Stop**: 代码级控制