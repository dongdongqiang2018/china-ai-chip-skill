---
name: mcblas
description: 沐曦BLAS线性代数库，提供GPU加速的基本线性代数子程序（BLAS）实现，支持Level-1/2/3函数。是AI和HPC应用的核心数学库。
keywords:
  - 沐曦
  - BLAS
  - 线性代数
  - mcblas
  - GPU计算
  - 矩阵运算
  - GEMM
---

# mcBLAS 使用指南

mcBLAS提供了基本线性代数子程序（BLAS）的GPU加速实现，完全支持标准BLAS例程，针对曦云系列GPU进行了高度优化。

## 快速开始

### 安装

mcBLAS随MXMACA SDK默认安装，无需单独安装。

### Hello World

```c
#include <mcblas.h>

int main() {
    mcblasHandle_t handle;
    mcblasCreate(&handle);

    // 执行GEMM操作
    // C = alpha * op(A) * op(B) + beta * C

    mcblasDestroy(handle);
    return 0;
}
```

## 数据类型

### 句柄

```c
mcblasHandle_t  // mcBLAS上下文句柄
```

### 数值类型

```c
mcblas_int           // 整数类型
mcblas_stride        // 步长类型
mcblas_half          // 半精度 (FP16)
mcComplex            // 单精度复数
mcDoubleComplex      // 双精度复数
macaDataType_t       // 数据类型枚举
```

### 枚举类型

```c
mcblasOperation_t    // 操作类型: 非转置/转置/共轭转置
mcblasFillMode_t     // 填充模式: 上三角/下三角/全矩阵
mcblasDiagType_t     // 对角类型: 单位/非单位
mcblasSideMode_t     // 侧边模式: 左/右
mcblasPointerMode_t  // 指针模式: 主机/设备
mcblasAtomicsMode_t  // 原子操作模式: 开/关
mcblasGemmAlgo_t     // GEMM算法
mcblasMath_t         // 数学模式: TF32/FP16等
mcblasComputeType_t  // 计算类型
```

### 状态码

```c
mcblasStatus_t  // 函数返回状态
// MCBLAS_STATUS_SUCCESS         - 成功
// MCBLAS_STATUS_NOT_INITIALIZED - 未初始化
// MCBLAS_STATUS_ALLOC_FAILED    - 分配失败
// MCBLAS_STATUS_INVALID_VALUE   - 无效参数
// MCBLAS_STATUS_MAPPING_ERROR   - 映射错误
// MCBLAS_STATUS_EXECUTION_FAILED - 执行失败
// MCBLAS_STATUS_INTERNAL_ERROR  - 内部错误
```

## 辅助函数

### 生命周期

```c
// 创建句柄
mcblasStatus_t mcblasCreate(mcblasHandle_t *handle);

// 销毁句柄
mcblasStatus_t mcblasDestroy(mcblasHandle_t handle);

// 获取版本
int mcblasGetVersion();
```

### 流控制

```c
// 设置CUDA流
mcblasStatus_t mcblasSetStream(mcblasHandle_t handle, cudaStream_t streamId);

// 获取当前流
mcblasStatus_t mcblasGetStream(mcblasHandle_t handle, cudaStream_t *streamId);
```

### 内存操作

```c
// 设置向量
mcblasStatus_t mcblasSetVector(int n, int elemSize, const void *x, int incx,
                                void *deviceX, int incDeviceX);

// 获取向量
mcblasStatus_t mcblasGetVector(int n, int elemSize, const void *deviceX,
                                int incDeviceX, void *x, int incx);

// 设置矩阵
mcblasStatus_t mcblasSetMatrix(int rows, int cols, int elemSize,
                                const void *A, int lda, void *deviceA, int ldda);

// 获取矩阵
mcblasStatus_t mcblasGetMatrix(int rows, int cols, int elemSize,
                                const void *deviceA, int ldda, void *A, int lda);

// 异步版本（带Async后缀）
mcblasStatus_t mcblasSetVectorAsync(...);
mcblasStatus_t mcblasGetVectorAsync(...);
mcblasStatus_t mcblasSetMatrixAsync(...);
mcblasStatus_t mcblasGetMatrixAsync(...);
```

### 模式设置

```c
// 设置/获取指针模式
mcblasStatus_t mcblasSetPointerMode(mcblasHandle_t handle, mcblasPointerMode_t mode);
mcblasStatus_t mcblasGetPointerMode(mcblasHandle_t handle, mcblasPointerMode_t *mode);

// 设置/获取原子操作模式
mcblasStatus_t mcblasSetAtomicsMode(mcblasHandle_t handle, mcblasAtomicsMode_t mode);
mcblasStatus_t mcblasGetAtomicsMode(mcblasHandle_t handle, mcblasAtomicsMode_t *mode);

// 设置/获取数学模式
mcblasStatus_t mcblasSetMathMode(mcblasHandle_t handle, mcblasMath_t mode);
mcblasStatus_t mcblasGetMathMode(mcblasHandle_t handle, mcblasMath_t *mode);
```

## Level-1 函数（向量-向量）

| 函数 | 说明 |
|------|------|
| `mcblasI<t>amax()` | 查找最大绝对值索引 |
| `mcblasI<t>amin()` | 查找最小绝对值索引 |
| `mcblas<t>asum()` | 计算向量L1范数（绝对值和） |
| `mcblas<t>axpy()` | 向量加法: y = αx + y |
| `mcblas<t>copy()` | 向量复制 |
| `mcblas<t>dot()` | 点积 |
| `mcblas<t>nrm2()` | 计算向量L2范数 |
| `mcblas<t>rot()` | 平面旋转变换 |
| `mcblas<t>rotg()` | 生成旋转变换参数 |
| `mcblas<t>scal()` | 向量数乘 |
| `mcblas<t>swap()` | 向量交换 |

## Level-2 函数（矩阵-向量）

| 函数 | 说明 |
|------|------|
| `mcblas<t>gbmv()` | 带状矩阵-向量乘法 |
| `mcblas<t>gemv()` | 通用矩阵-向量乘法 |
| `mcblas<t>ger()` | 秩-1更新 |
| `mcblas<t>sbmv()` | 对称带状矩阵-向量乘法 |
| `mcblas<t>spmv()` | 对称压缩矩阵-向量乘法 |
| `mcblas<t>symv()` | 对称矩阵-向量乘法 |
| `mcblas<t>tbmv()` | 三角带状矩阵-向量乘法 |
| `mcblas<t>tbsv()` | 三角带状矩阵求解 |
| `mcblas<t>tpmv()` | 三角压缩矩阵-向量乘法 |
| `mcblas<t>tpsv()` | 三角压缩矩阵求解 |
| `mcblas<t>trmv()` | 三角矩阵-向量乘法 |
| `mcblas<t>trsv()` | 三角矩阵求解 |
| `mcblas<t>gemvBatched()` | 批量矩阵-向量乘法 |
| `mcblas<t>gemvStridedBatched()` | 分块批量矩阵-向量乘法 |

## Level-3 函数（矩阵-矩阵）

| 函数 | 说明 |
|------|------|
| `mcblas<t>gemm()` | 通用矩阵乘法 |
| `mcblas<t>gemm3m()` | 3M算法矩阵乘法（更高精度） |
| `mcblas<t>gemmBatched()` | 批量矩阵乘法 |
| `mcblas<t>gemmStridedBatched()` | 分块批量矩阵乘法 |
| `mcblas<t>symm()` | 对称矩阵乘法 |
| `mcblas<t>syrk()` | 对称秩-k更新 |
| `mcblas<t>syr2k()` | 对称秩-2k更新 |
| `mcblas<t>syrkx()` | 扩展对称秩-k更新 |
| `mcblas<t>trmm()` | 三角矩阵乘法 |
| `mcblas<t>trsm()` | 三角矩阵求解 |

## 常用示例

### GEMM矩阵乘法

```c
void gemm_example() {
    int M = 1024, N = 1024, K = 1024;
    float alpha = 1.0f, beta = 0.0f;

    // 分配设备内存
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, M * K * sizeof(float));
    cudaMalloc(&d_B, K * N * sizeof(float));
    cudaMalloc(&d_C, M * N * sizeof(float));

    mcblasHandle_t handle;
    mcblasCreate(&handle);

    // 执行 C = alpha * A * B + beta * C
    mcblasSgemm(handle,
                MCBLAS_OP_N, MCBLAS_OP_N,
                M, N, K,
                &alpha,
                d_A, M,
                d_B, K,
                &beta,
                d_C, M);

    mcblasDestroy(handle);
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
}
```

### 批量GEMM

```c
void gemm_batched_example() {
    int batchCount = 10;
    int M = 1024, N = 1024, K = 1024;
    float alpha = 1.0f, beta = 0.0f;

    float **d_Aarray = ...;
    float **d_Barray = ...;
    float **d_Carray = ...;

    mcblasHandle_t handle;
    mcblasCreate(&handle);

    mcblasSgemmBatched(handle,
                        MCBLAS_OP_N, MCBLAS_OP_N,
                        M, N, K,
                        &alpha,
                        d_Aarray, M,
                        d_Barray, K,
                        &beta,
                        d_Carray, M,
                        batchCount);

    mcblasDestroy(handle);
}
```

## 性能特性

### 支持的数据类型
- FP32 (单精度)
- FP16 (半精度)
- BF16 (Brain Float)
- TF32 (Tensor Float)
- INT8 (整数)
- 复数 (FP32/FP64)

### 硬件加速
- 张量核心 (Tensor Core) 加速
- 硬件优化BLAS实现
- 流并发操作支持

## 官方参考

- 《曦云系列通用GPU mcBLAS API参考》
- MXMACA SDK