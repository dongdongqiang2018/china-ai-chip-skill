---
name: mcfft
description: 沐曦FFT快速傅里叶变换库，提供GPU加速的FFT实现，支持1D/2D/3D复数和实数变换。用于信号处理、图像处理、科学计算等领域。
keywords:
  - 沐曦
  - FFT
  - 快速傅里叶变换
  - mcfft
  - 信号处理
  - 频域变换
---

# mcFFT 使用指南

mcFFT是基于曦云系列GPU的快速傅里叶变换(FFT)实现，用于构建深度学习、计算机视觉、计算物理、分子动力学等应用。

## 快速开始

### 安装

mcFFT随MXMACA SDK默认安装。

### Hello World

```c
#include <mcfft.h>

int main() {
    mcfftHandle_t plan;
    int n = 1024;

    // 创建执行计划
    mcfftPlan1d(&plan, n, MCFFT_C2C, 1);

    // 执行FFT
    mcfftExecC2C(plan, input, output, MCFFT_FORWARD);

    // 销毁计划
    mcfftDestroy(plan);
    return 0;
}
```

## 数据类型

### 句柄

```c
mcfftHandle_t  // mcFFT执行计划句柄
```

### 变换类型

```c
// 变换类型
MCFFT_R2C  // 实数到复数
MCFFT_C2R  // 复数到实数
MCFFT_C2C  // 复数到复数

// 方向
MCFFT_FORWARD  // 正变换
MCFFT_INVERSE  // 逆变换
```

### 工作模式

```c
// 结果缩放模式
MCFFT_FFTW_FOURNIE
MCFFT_FFTW_DESTROY_INPUT
```

### 状态码

```c
mcfftResult_t
// MCFFT_SUCCESS
// MCFFT_INVALID_PLAN
// MCFFT_ALLOC_FAILED
// MCFFT_INVALID_TYPE
// MCFFT_INVALID_DFT_ROOTS
// MCFFT_INVALID_STRIDE
// MCFFT_INVALID_N
```

## 核心API

### 生命周期

```c
// 创建/销毁句柄
mcfftResult_t mcfftCreate(mcfftHandle_t *handle);
mcfftResult_t mcfftDestroy(mcfftHandle_t handle);

// 获取版本
int mcfftGetVersion();
```

### 1D变换

```c
// 创建1D计划
mcfftResult_t mcfftPlan1d(mcfftHandle_t *plan,
                          int nx,
                          mcfftType type,
                          int batch);

// 执行1D变换
mcfftResult_t mcfftExecR2C(mcfftHandle_t plan,
                            const float *input,
                            mcfftComplex *output);
mcfftResult_t mcfftExecC2R(mcfftHandle_t plan,
                            const mcfftComplex *input,
                            float *output);
mcfftResult_t mcfftExecC2C(mcfftHandle_t plan,
                            const mcfftComplex *input,
                            mcfftComplex *output,
                            int direction);
```

### 2D变换

```c
// 创建2D计划
mcfftResult_t mcfftPlan2d(mcfftHandle_t *plan,
                          int nx, int ny,
                          mcfftType type);

// 批量2D
mcfftResult_t mcfftPlanMany2d(mcfftHandle_t *plan,
                               int nx, int ny,
                               mcfftType type,
                               int batch);
```

### 3D变换

```c
// 创建3D计划
mcfftResult_t mcfftPlan3d(mcfftHandle_t *plan,
                          int nx, int ny, int nz,
                          mcfftType type);

// 批量3D
mcfftResult_t mcfftPlanMany3d(mcfftHandle_t *plan,
                               int nx, int ny, int nz,
                               mcfftType type,
                               int batch);
```

### 高级计划

```c
// 灵活维度计划
mcfftResult_t mcfftPlanMany(mcfftHandle_t *plan,
                            int rank,
                            const int *n,
                            const int *inembed,
                            int istride, int idist,
                            const int *onembed,
                            int ostride, int odist,
                            mcfftType type,
                            int batch);

// 设置流
mcfftResult_t mcfftSetStream(mcfftHandle_t plan, cudaStream_t stream);

// 获取工作空间大小
mcfftResult_t mcfftGetSize(mcfftHandle_t plan, size_t *workSize);
```

### 销毁

```c
// 销毁计划
mcfftResult_t mcfftDestroy(mcfftHandle_t plan);

// 清理所有
mcfftResult_t mcfftCleanup();
```

## 常用示例

### 1D复数变换

```c
void fft_1d_example() {
    int N = 1024;
    mcfftHandle_t plan;

    // 创建复数到复数计划
    mcfftPlan1d(&plan, N, MCFFT_C2C, 1);

    // 分配内存
    mcfftComplex *input, *output;
    cudaMalloc(&input, N * sizeof(mcfftComplex));
    cudaMalloc(&output, N * sizeof(mcfftComplex));

    // 执行正变换
    mcfftExecC2C(plan, input, output, MCFFT_FORWARD);

    // 执行逆变换
    mcfftExecC2C(plan, output, input, MCFFT_INVERSE);

    // 缩放
    // output[i] /= N;

    cudaFree(input);
    cudaFree(output);
    mcfftDestroy(plan);
}
```

### 2D实数变换

```c
void fft_2d_example() {
    int N = 256, M = 256;
    mcfftHandle_t plan;

    // 创建R2C计划（输出为N x (M/2+1)复数）
    mcfftPlan2d(&plan, N, M, MCFFT_R2C);

    float *input;
    mcfftComplex *output;
    cudaMalloc(&input, N * M * sizeof(float));
    cudaMalloc(&output, N * (M/2+1) * sizeof(mcfftComplex));

    // 执行正变换
    mcfftExecR2C(plan, input, output);

    cudaFree(input);
    cudaFree(output);
    mcfftDestroy(plan);
}
```

### 批量1D变换

```c
void fft_batch_example() {
    int N = 1024;
    int batch = 64;
    mcfftHandle_t plan;

    // 批量变换
    mcfftPlan1d(&plan, N, MCFFT_C2C, batch);

    mcfftComplex *input, *output;
    cudaMalloc(&input, batch * N * sizeof(mcfftComplex));
    cudaMalloc(&output, batch * N * sizeof(mcfftComplex));

    mcfftExecC2C(plan, input, output, MCFFT_FORWARD);

    cudaFree(input);
    cudaFree(output);
    mcfftDestroy(plan);
}
```

## 数据布局

### 输入/输出布局

| 变换类型 | 输入 | 输出 |
|----------|------|------|
| R2C | N 实数 | N/2+1 复数 |
| C2R | N/2+1 复数 | N 实数 |
| C2C | N 复数 | N 复数 |

### 2D布局

| 变换类型 | 输入 | 输出 |
|----------|------|------|
| R2C | NxM 实数 | Nx(M/2+1) 复数 |
| C2R | Nx(M/2+1) 复数 | NxM 实数 |

## 功能特性

### 支持的变换
- 1D/2D/3D复数变换
- 1D/2D/3D实数变换
- 批量变换
- 分块批量变换

### 数据类型
- 单精度 (float)
- 双精度 (double)
- 半精度 (half)

### 特性
- 与FFTW类似的API
- 灵活的数据布局
- 流式异步执行
- 线程安全

## 官方参考

- 《曦云系列通用GPU mcFFT API参考》
- MXMACA SDK