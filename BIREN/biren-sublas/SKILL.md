---
name: biren-sublas
description: BIREN suBLAS 基础线性代数计算库参考指南。提供 Level-1/2/3 BLAS 函数和 suBLASLt 轻量 GEMM API，用于在壁仞 GPU 上高效执行向量运算、矩阵运算、矩阵乘法等线性代数计算。
keywords:
  - sublas
  - biren
  - BLAS
  - 线性代数
  - GEMM
  - 矩阵乘法
  - GPU计算
  - 壁仞
---

# suBLAS Command Reference

suBLAS 是壁仞科技提供的基础线性代数算法计算库。

## Quick Start

```c
#include <sublas.h>

// 创建句柄
sublasHandle_t handle;
sublasCreate(&handle);

// 设置流
sublasSetStream(handle, stream);

// 执行矩阵乘法
sublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, m, n, k,
            &alpha, d_A, lda, d_B, ldb, &beta, d_C, ldc);

// 销毁
sublasDestroy(handle);
```

## Installation

安装路径：`/usr/local/birensupa/sdk/latest/sulib`

## API Types

### suBLAS Standard API

标准 BLAS 库 API。

### suBLASLt API

专门用于 GEMM 计算的轻量 API，支持壁仞自定义数据 layout。

## Level-1 Functions (Vector Operations)

| Function | Description |
|----------|-------------|
| `sublasSamax` | 绝对值最大元素索引 |
| `sublasSamax` | 绝对值最小元素索引 |
| `sublasSasum` | 绝对值求和 |
| `sublasSnrm2` | 2-范数 |
| `sublasSdot` | 点积 |
| `sublasSaxpy` | 向量加法 (y = a*x + y) |
| `sublasScopy` | 向量复制 |
| `sublasSscal` | 向量缩放 |
| `sublasSswap` | 向量交换 |
| `sublasSrot` | 旋转 |
| `sublasSrotg` | 旋转参数生成 |
| `sublasSrotm` | 修改旋转 |
| `sublasSrotmg` | 修改旋转参数生成 |

## Level-2 Functions (Matrix-Vector Operations)

| Function | Description |
|----------|-------------|
| `sublasSgemv` | 通用矩阵向量乘法 |
| `sublasSger` | 秩-1 更新 |
| `sublasSspr` | 对称秩-1 更新 |
| `sublasSspr2` | 对称秩-2 更新 |
| `sublasSsymv` | 对称矩阵向量乘法 |
| `sublasStrmv` | 三角矩阵向量乘法 |
| `sublasStrsv` | 三角矩阵求解 |
| `sublasStbmv` | 带状三角矩阵向量乘法 |
| `sublasStbsv` | 带状三角矩阵求解 |
| `sublasStpmv` | 压缩三角矩阵向量乘法 |
| `sublasStpsv` | 压缩三角矩阵求解 |
| `sublasSsyev` | 对称矩阵特征值 |

## Level-3 Functions (Matrix-Matrix Operations)

| Function | Description |
|----------|-------------|
| `sublasSgemm` | 通用矩阵乘法 |
| `sublasSsymm` | 对称矩阵乘法 |
| `sublasSsyrk` | 对称秩-k 更新 |
| `sublasSsyr2k` | 对称秩-2k 更新 |
| `sublasStrmm` | 三角矩阵乘法 |
| `sublasStrsm` | 三角矩阵求解 |

## BLAS-Like Functions (Batch)

| Function | Description |
|----------|-------------|
| `sublasSgemmBatched` | 批量矩阵乘法 |
| `sublasSgemmStridedBatched` | 分批矩阵乘法 |

## suBLASLt API

### Matrix Layout

```c
sublasLtMatrixLayoutCreate(&layout, m, n, ld, batchStride);
```

### Matmul Descriptor

```c
sublasLtMatmulDescCreate(&desc, computeType, scaleType);
sublasLtMatmulDescSetAttribute(desc, SUBLASLT_MATMUL_DESC_TRANS_A, &transA, sizeof(transA));
sublasLtMatmulDescSetAttribute(desc, SUBLASLT_MATMUL_DESC_TRANS_B, &transB, sizeof(transB));
sublasLtMatmulDescSetAttribute(desc, SUBLASLT_MATMUL_DESC_EPILOGUE, &epilogue, sizeof(epilogue));
```

### Epilogue Types

| Type | Description |
|------|-------------|
| `SUBLASLT_EPILOGUE_DEFAULT` | 无后处理 |
| `SUBLASLT_EPILOGUE_RELU` | RELU 激活 |
| `SUBLASLT_EPILOGUE_BIAS` | 偏置 |
| `SUBLASLT_EPILOGUE_GELU` | GELU 激活 |
| `SUBLASLT_EPILOGUE_BGRADA` | 反向梯度 A |
| `SUBLASLT_EPILOGUE_BGRADB` | 反向梯度 B |

### Execution

```c
sublasLtMatmul(handle, desc, &alpha, A, B, &beta, C, D, workspace, &workspaceSize, stream);
```

## Key Enumerations

### sublasOperation_t

| Value | Description |
|-------|-------------|
| `SUBLAS_OP_N` | 未转置 |
| `SUBLAS_OP_T` | 转置 |
| `SUBLAS_OP_C` | 共轭转置 |
| `SUBLAS_OP_HERMITAN` | Hermitian |
| `SUBLAS_OP_CONJG` | 共轭 |

### sublasFillMode_t

| Value | Description |
|-------|-------------|
| `SUBLAS_FILL_MODE_LOWER` | 下三角 |
| `SUBLAS_FILL_MODE_UPPER` | 上三角 |
| `SUBLAS_FILL_MODE_FULL` | 完整 |

### sublasDiagType_t

| Value | Description |
|-------|-------------|
| `SUBLAS_DIAG_TYPE_NON_UNIT` | 非单位 |
| `SUBLAS_DIAG_TYPE_UNIT` | 单位 |

### sublasSideMode_t

| Value | Description |
|-------|-------------|
| `SUBLAS_SIDE_MODE_LEFT` | 左侧 |
| `SUBLAS_SIDE_MODE_RIGHT` | 右侧 |

### sublasPointerMode_t

| Value | Description |
|-------|-------------|
| `SUBLAS_POINTER_MODE_HOST` | 主机端 |
| `SUBLAS_POINTER_MODE_DEVICE` | 设备端 |

### sublasComputeType_t

| Value | Description |
|-------|-------------|
| `SUBLAS_COMPUTE_16F` | 半精度 |
| `SUBLAS_COMPUTE_16BF` | Brain Float 16 |
| `SUBLAS_COMPUTE_32F` | 单精度 |
| `SUBLAS_COMPUTE_32F_FAST_16BF` | 快速单精度 BF16 |
| `SUBLAS_COMPUTE_32F_FAST_TF32P` | 快速单精度 TF32 |

## Helper Functions

| Function | Description |
|----------|-------------|
| `sublasCreate` | 创建句柄 |
| `sublasDestroy` | 销毁句柄 |
| `sublasSetStream` | 设置流 |
| `sublasGetStream` | 获取流 |
| `sublasSetWorkspace` | 设置工作空间 |
| `sublasSetPointerMode` | 设置指针模式 |
| `sublasGetPointerMode` | 获取指针模式 |
| `sublasSetVector` | 主存→显存向量复制 |
| `sublasGetVector` | 显存→主存向量复制 |
| `sublasSetMatrix` | 主存→显存矩阵复制 |
| `sublasGetMatrix` | 显存→主存矩阵复制 |

## Return Codes

| Code | Description |
|------|-------------|
| `SUBLAS_STATUS_SUCCESS` | 成功 |
| `SUBLAS_STATUS_NOT_INITIALIZED` | 未初始化 |
| `SUBLAS_STATUS_INVALID_VALUE` | 无效值 |
| `SUBLAS_STATUS_ARCH_MISMATCH` | 架构不匹配 |
| `SUBLAS_STATUS_INTERNAL_ERROR` | 内部错误 |

## Example: GEMM

```c
#include <sublas.h>

int main() {
    sublasHandle_t handle;
    sublasCreate(&handle);

    int m = 1024, n = 1024, k = 1024;
    float alpha = 1.0f, beta = 0.0f;

    // 分配设备内存
    // ...

    // 执行矩阵乘法
    sublasSgemm(handle,
                SUBLAS_OP_N, SUBLAS_OP_N,
                m, n, k,
                &alpha,
                d_A, k,
                d_B, k,
                &beta,
                d_C, n);

    sublasDestroy(handle);
    return 0;
}
```

## Features

- 线程安全（多线程可使用相同 handle）
- 结果可重现（bit-wise 一致）
- 支持标量在 Host 和 Device 端传参
- 支持 SUPA 流式并行
- 支持批处理矩阵乘法

## Notes

- 当前仅支持 Float 和部分 suComplex 类型
- suBLASLt 仅支持壁仞自定义排布数据
- 调用前后需进行 reorder

## Related Libraries

- **BPP**: 图像处理
- **suDNN**: 深度学习
- **suFFT**: 快速傅里叶变换
- **suRAND**: 随机数生成