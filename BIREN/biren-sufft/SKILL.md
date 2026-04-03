---
name: biren-sufft
description: BIREN suFFT 快速傅里叶变换库参考指南。提供 C2C、R2C、C2R 类型的一维和多维 FFT 变换，支持批量处理、实数/复数变换、任意长度（2^a × 3^b × 5^c × 7^d × 11^e × 13^f 组合）变换，用于信号处理、图像处理等领域。
keywords:
  - sufft
  - biren
  - FFT
  - 傅里叶变换
  - 信号处理
  - 频域变换
  - 壁仞
---

# suFFT Command Reference

suFFT 是壁仞 GPU 加速的快速傅里叶变换库。

## Quick Start

```c
#include <sufft.h>

// 创建 Plan
sufftPlan1d(&plan, nx, SUFFT_C2C, batch);

// 执行
sufftExecC2C(plan, idata, odata, SUFFT_FORWARD);

// 销毁
sufftDestroy(plan);
```

## Installation

安装路径：`/usr/local/birensupa/sdk/latest/sulib`

## Transform Types

| Type | Description | Input → Output |
|------|-------------|----------------|
| `SUFFT_C2C` | 复数到复数 | suComplex → suComplex |
| `SUFFT_R2C` | 实数到复数 | suReal → suComplex |
| `SUFFT_C2R` | 复数到实数 | suComplex → suReal |

当前仅支持单精度（FP32）。

## Supported Lengths

支持的变换长度为 2^a × 3^b × 5^c × 7^d × 11^e × 13^f 的组合（a,b,c,d,e,f ≥ 0）。

| Parameter | Limit |
|-----------|-------|
| 变换长度 | 上述质因数组合 |
| batch | 支持批量处理 |
| stride | 支持自定义步长 |
| 精度 | 单精度（FP32） |

## Key APIs

### Plan Management

| Function | Description |
|----------|-------------|
| `sufftPlan1d` | 创建 1D FFT 计划 |
| `sufftPlan2d` | 创建 2D FFT 计划 |
| `sufftPlan3d` | 创建 3D FFT 计划 |
| `sufftPlanMany` | 创建高级 FFT 计划（支持 stride/dist/embed） |
| `sufftDestroy` | 销毁计划 |
| `sufftGetVersion` | 获取版本号 |

### Stream Control

| Function | Description |
|----------|-------------|
| `sufftSetStream` | 绑定 SUPA 流 |

### Execution

| Function | Description |
|----------|-------------|
| `sufftExecC2C` | 执行复数到复数变换 |
| `sufftExecR2C` | 执行实数到复数变换 |
| `sufftExecC2R` | 执行复数到实数变换 |

### Utility

| Function | Description |
|----------|-------------|
| `sufftGetVersion` | 获取版本号 |

## Plan-based Programming Model

```c
// 1. 创建 Plan
sufftPlan1d(&plan, nx, type, batch);

// 2. 配置（可选）
sufftSetStream(plan, stream);

// 3. 执行
sufftExecC2C(plan, idata, odata, direction);  // SUFFT_FORWARD / SUFFT_INVERSE
sufftExecR2C(plan, idata, odata);
sufftExecC2R(plan, idata, odata);

// 4. 销毁
sufftDestroy(plan);
```

## Direction

| Value | Description |
|-------|-------------|
| `SUFFT_FORWARD` | 正变换 |
| `SUFFT_INVERSE` | 逆变换 |

## Example: 1D FFT

```c
#include <sufft.h>

int main() {
    sufftPlan1d_t plan;
    int nx = 1024;
    int batch = 1;

    // 创建 Plan
    sufftPlan1d(&plan, nx, SUFFT_C2C, batch);

    // 分配内存
    // ... (分配 idata, odata)

    // 执行正变换
    sufftExecC2C(plan, idata, odata, SUFFT_FORWARD);

    // 执行逆变换
    sufftExecC2C(plan, odata, result, SUFFT_INVERSE);

    // 归一化
    // result[i] /= nx;

    // 销毁
    sufftDestroy(plan);
    return 0;
}
```

## Example: R2C Transform

```c
#include <sufft.h>

int main() {
    sufftPlan1d_t plan;
    int nx = 1024;
    int batch = 1;

    // 创建 R2C Plan
    sufftPlan1d(&plan, nx, SUFFT_R2C, batch);

    // 输入: nx 个实数
    // 输出: nx/2+1 个复数

    // 执行
    sufftExecR2C(plan, realInput, complexOutput);

    sufftDestroy(plan);
    return 0;
}
```

## Example: 2D FFT

```c
#include <sufft.h>

int main() {
    sufftPlan2d_t plan;
    int nx = 512, ny = 512;

    // 创建 2D Plan
    sufftPlan2d(&plan, nx, ny, SUFFT_C2C);

    // 执行
    sufftExecC2C(plan, input, output, SUFFT_FORWARD);

    sufftDestroy(plan);
    return 0;
}
```

## Example: Batch Processing

```c
#include <sufft.h>

int main() {
    sufftPlan1d_t plan;
    int nx = 1024;
    int batch = 16;  // 16 个独立信号

    // 创建带 batch 的 Plan
    sufftPlan1d(&plan, nx, SUFFT_C2C, batch);

    // 执行批量变换
    sufftExecC2C(plan, input, output, SUFFT_FORWARD);

    sufftDestroy(plan);
    return 0;
}
```

## Important Notes

### R2C Output

- R2C 输出利用共轭对称性
- 输出长度为 N/2+1

### C2R Input

- C2R 是 R2C 的逆变换
- 输入长度 N/2+1，输出长度 N

### C2R Behavior

- C2R 变换会覆盖输入数据
- 逆变换结果未归一化，需手动除以 N

### Data Layout

- 输入输出使用不同的数据布局
- 需要注意内存对齐

## Return Codes

| Code | Description |
|------|-------------|
| `SUFFT_SUCCESS` | 成功 |
| `SUFFT_INVALID_VALUE` | 无效值 |
| `SUFFT_INVALID_PLAN` | 无效计划 |
| `SUFFT_ALLOC_FAILED` | 分配失败 |
| `SUFFT_INTERNAL_ERROR` | 内部错误 |

## Performance Tips

- 复用 Plan 可以提高性能
- 使用批量变换可以提高 GPU 利用率
- 合理选择精度平衡性能和精度
- 避免频繁创建和销毁 Plan

## Related Libraries

- **BPP**: 图像处理
- **suBLAS**: 线性代数
- **suDNN**: 深度学习
- **suRAND**: 随机数生成