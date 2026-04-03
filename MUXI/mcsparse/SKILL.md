---
name: mcsparse
description: 沐曦稀疏矩阵库，提供GPU加速的稀疏矩阵操作，包括CSR/CSC格式、稀疏BLAS、稀疏求解器。用于大规模稀疏线性代数计算。
keywords:
  - 沐曦
  - 稀疏矩阵
  - mcsparse
  - CSR
  - 稀疏BLAS
---

# mcSPARSE 使用指南

mcSPARSE提供GPU加速的稀疏矩阵操作，支持多种稀疏矩阵格式和稀疏BLAS例程。

## 快速开始

### 安装

mcSPARSE随MXMACA SDK默认安装。

### Hello World

```c
#include <mcsparse.h>

int main() {
    mcsparseHandle_t handle;
    mcsparseCreate(&handle);

    // 执行稀疏操作...

    mcsparseDestroy(handle);
    return 0;
}
```

## 数据类型

### 句柄

```c
mcsparseHandle_t         // mcSPARSE上下文句柄
mcsparseMatDescr_t       // 矩阵描述符
mcsparseDnVecDescr_t    // 密集向量描述符
mcsparseSpVecDescr_t    // 稀疏向量描述符
mcsparseSpMatDescr_t   // 稀疏矩阵描述符
```

### 矩阵格式

```c
// 稀疏矩阵格式
mcsparseIndexBase_t
// MCSPARSE_INDEX_BASE_ZERO  // 0-based
// MCSPARSE_INDEX_BASE_ONE   // 1-based

// 矩阵类型
mcsparseMatrixType_t
// MCSPARSE_MATRIX_TYPE_GENERAL   // 一般
// MCSPARSE_MATRIX_TYPE_SYMMETRIC  // 对称
// MCSPARSE_MATRIX_TYPE Hermitian  // Hermitian
// MCSPARSE_MATRIX_TYPE_TRIANGULAR // 三角

// 填充模式
mcsparseFillMode_t
// MCSPARSE_FILL_MODE_UPPER
// MCSPARSE_FILL_MODE_LOWER

// 对角类型
mcsparseDiagType_t
// MCSPARSE_DIAG_TYPE_NON_UNIT
// MCSPARSE_DIAG_TYPE_UNIT
```

### 状态码

```c
mcsparseStatus_t
// MCSPARSE_SUCCESS
// MCSPARSE_NOT_INITIALIZED
// MCSPARSE_ALLOC_FAILED
// MCSPARSE_INVALID_VALUE
// MCSPARSE_EXECUTION_FAILED
// MCSPARSE_INTERNAL_ERROR
```

## 核心API

### 生命周期

```c
// 创建/销毁
mcsparseStatus_t mcsparseCreate(mcsparseHandle_t *handle);
mcsparseStatus_t mcsparseDestroy(mcsparseHandle_t handle);

// 创建矩阵描述符
mcsparseStatus_t mcsparseCreateMatDescr(mcsparseMatDescr_t *descr);
mcsparseStatus_t mcsparseDestroyMatDescr(mcsparseMatDescr_t descr);
```

### CSR格式操作

```c
// 创建CSR格式稀疏矩阵
mcsparseStatus_t mcsparseCreateCsr(...);

// 转换为CSR
mcsparseStatus_t mcsparseCooToCsr(...);
mcsparseStatus_t mcsparseCsrToCoo(...);

// 获取/设置属性
mcsparseStatus_t mcsparseSetMatType(mcsparseMatDescr_t descr, mcsparseMatrixType_t type);
mcsparseStatus_t mcsparseSetMatFillMode(mcsparseMatDescr_t descr, mcsparseFillMode_t mode);
mcsparseStatus_t mcsparseSetMatDiagType(mcsparseMatDescr_t descr, mcsparseDiagType_t diag);
```

### 稀疏BLAS

```c
// 稀疏向量-密集向量乘法
mcsparseStatus_t mcsparseSgemv(mcsparseHandle_t handle,
                                 char transA,
                                 int m, int n,
                                 const float *alpha,
                                 const mcsparseMatDescr_t descrA,
                                 const float *csrValA,
                                 const int *csrRowPtrA,
                                 const int *csrColIndA,
                                 const float *x,
                                 const float *beta,
                                 float *y);

// 稀疏矩阵-密集矩阵乘法
mcsparseStatus_t mcsparseSgemm(...);
```

### 稀疏求解器

```c
// LU分解
mcsparseStatus_t mcsparseDcsrilu0(...);

// 三角求解
mcsparseStatus_t mcsparseDcsrsv(...);  // 行格式
mcsparseStatus_t mcsparseDcsrcsc(...);  // 格式转换
```

## 常用示例

### 创建CSR矩阵

```c
void csr_example() {
    mcsparseHandle_t handle;
    mcsparseCreate(&handle);

    // 4x4稀疏矩阵
    // [1 0 2 0]
    // [0 3 0 0]
    // [0 0 4 0]
    // [5 0 0 6]

    int m = 4, n = 4, nnz = 7;
    int *csrRowPtr = {0, 2, 3, 4, 7};
    int *csrColInd = {0, 2, 1, 2, 0, 3, 3};
    float *csrVal = {1, 2, 3, 4, 5, 6, 7};

    mcsparseSpMatDescr_t mat;
    mcsparseCreateCsr(&handle, m, n, nnz, csrRowPtr, csrColInd, csrVal,
                      &mat);

    mcsparseDestroy(handle);
}
```

### 稀疏矩阵-向量乘法

```c
void spmv_example() {
    mcsparseHandle_t handle;
    mcsparseCreate(&handle);

    // 假设已创建CSR矩阵和描述符
    float alpha = 1.0f, beta = 0.0f;
    float *x, *y;

    // y = alpha * A * x + beta * y
    mcsparseSgemv(handle, 'N', m, n, &alpha, descr, val, rowPtr, colInd,
                   x, &beta, y);

    mcsparseDestroy(handle);
}
```

## 支持的格式

| 格式 | 说明 |
|------|------|
| COO | 坐标格式 |
| CSR | 压缩稀疏行 |
| CSC | 压缩稀疏列 |

## 功能特性

### 稀疏BLAS
- 稀疏向量-向量乘法 (SpMV)
- 稀疏矩阵-矩阵乘法 (SpMM)
- 稀疏三角求解

### 稀疏求解器
- 不完全LU分解 (ILU0)
- 稀疏三角求解器

### 格式转换
- COO ↔ CSR
- CSR ↔ CSC
- 批量转换

## 官方参考

- 《曦云系列通用GPU mcSPARSE API参考》
- MXMACA SDK