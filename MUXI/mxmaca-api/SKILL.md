---
name: mxmaca-api
description: 沐曦运行时API参考，提供GPU设备管理、内存管理、流管理、事件管理等底层编程接口。
keywords:
  - 沐曦
  - MXMACA
  - API
  - 运行时
  - 设备管理
  - 内存管理
---

# MXMACA 运行时API指南

MXMACA运行时API提供GPU设备管理、内存管理、流管理、事件管理等底层编程接口。

## 快速开始

### 头文件

```c
#include <mxmaca/mxmaca.h>
#include <maca.h>
```

### Hello World

```c
#include <maca.h>

int main() {
    int deviceCount;
    macaGetDeviceCount(&deviceCount);
    printf("Found %d devices\n", deviceCount);
    return 0;
}
```

## 设备管理

### 查询设备

```c
// 获取设备数量
int deviceCount;
macaGetDeviceCount(&deviceCount);

// 获取设备属性
macaDeviceProp_t prop;
macaGetDeviceProperties(&prop, deviceId);

// 获取设备名
char name[256];
macaGetName(deviceId, name);
```

### 设备选择

```c
// 设置当前设备
macaSetDevice(deviceId);

// 获取当前设备
int deviceId;
macaGetDevice(&deviceId);
```

## 内存管理

### 分配内存

```c
// 设备内存分配
void *d_ptr;
macaMalloc(&d_ptr, size);

// 主机内存分配
void *h_ptr;
macaMallocHost(&h_ptr, size);

// 统一内存
void *um_ptr;
macaManagedMalloc(&um_ptr, size);
```

### 内存拷贝

```c
// 设备到主机
macaMemcpy(h_dst, d_src, size, macaMemcpyDeviceToHost);

// 主机到设备
macaMemcpy(d_dst, h_src, size, macaMemcpyHostToDevice);

// 设备到设备
macaMemcpy(d_dst, d_src, size, macaMemcpyDeviceToDevice);

// 异步拷贝
macaMemcpyAsync(d_dst, d_src, size, kind, stream);
```

### 内存释放

```c
macaFree(d_ptr);
macaFreeHost(h_ptr);
macaFree(um_ptr);
```

## 流管理

### 创建流

```c
macaStream_t stream;
macaStreamCreate(&stream);

// 带优先级
macaStreamCreateWithPriority(&stream, 0, -1);
```

### 流操作

```c
// 同步
macaStreamSynchronize(stream);

// 查询
int done;
macaStreamQuery(stream);

// 等待事件
macaStreamWaitEvent(stream, event, flags);
```

### 销毁流

```c
macaStreamDestroy(stream);
```

## 事件管理

### 创建事件

```c
macaEvent_t event;
macaEventCreate(&event);

// 带计时
macaEventCreateWithFlags(&event, macaEventBlockingSync);
```

### 事件操作

```c
// 记录事件
macaEventRecord(event, stream);

// 等待事件
macaStreamWaitEvent(stream, event, 0);

// 同步
macaEventSynchronize(event);

// 获取耗时
float time;
macaEventElapsedTime(&time, startEvent, endEvent);
```

### 销毁事件

```c
macaEventDestroy(event);
```

## 模块管理

### 加载模块

```c
macaModule_t module;
macaModuleLoad(&module, "kernel.co");

// 从内存加载
macaModuleLoadData(&module, data, size);
```

### 获取函数

```c
macaFunction_t func;
macaModuleGetFunction(&module, &func, "kernel_name");
```

### 卸载模块

```c
macaModuleUnload(module);
```

## 内核启动

### 配置线程网格

```c
dim3 grid(256, 1, 1);
dim3 block(256, 1, 1);

// 启动内核
kernel_name<<<grid, block>>>(args);
```

## 错误处理

```c
macaError_t err = macaGetLastError();
if (err != macaSuccess) {
    printf("Error: %s\n", macaGetErrorString(err));
}
```

## 官方参考

- 《曦云系列通用GPU MXMACA运行时API参考》
- MXMACA SDK