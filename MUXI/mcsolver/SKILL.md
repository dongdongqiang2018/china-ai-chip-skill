---
name: mcsolver
description: 沐曦密集与稀疏线性求解器库，提供直接求解器（LU、Cholesky、QR、SVD）和特征值求解器。用于科学计算、计算机视觉、线性优化等领域。
keywords:
  - 沐曦
  - 线性代数
  - 求解器
  - mcsolver
  - LU分解
  - 特征值
---

# mcSOLVER 使用指南

mcSOLVER提供密集和稀疏的直接线性求解器和特征求解器的集合，基于曦云系列GPU，为各种HPC应用提供显著加速。

## 快速开始

### 安装

mcSOLVER随MXMACA SDK默认安装。

### Hello World

```c
#include <mcsolver.h>

int main() {
    mcsolverHandle_t handle;
    mcsolverCreate(&handle);

    // 执行求解...

    mcsolverDestroy(handle);
    return 0;
}
```

## 求解器类型

### 直接求解器

| 类型 | 说明 |
|------|------|
| LU | LU分解 (行 pivoting) |
| Cholesky | Cholesky分解 (对称正定) |
| QR | QR分解 (正交三角) |
| SVD | 奇异值分解 |
| QL | QL分解 |
| RQ | RQ分解 |

### 求解器API

```c
// LU求解
mcsolverStatus_t mcsolverDgesv(mcsolverHandle_t handle,
                                 int n, int nrhs,
                                 double *A, int lda,
                                 int *ipiv,
                                 double *B, int ldb,
                                 int *info);

// Cholesky求解
mcsolverStatus_t mcsolverDposv(mcsolverHandle_t handle,
                                mcsolverUplo_t uplo,
                                int n, int nrhs,
                                double *A, int lda,
                                double *B, int ldb,
                                int *info);

// QR求解
mcsolverStatus_t mcsolverDgeqrf(mcsolverHandle_t handle,
                                  int m, int n,
                                  double *A, int lda,
                                  double *tau,
                                  double *work, int lwork,
                                  int *info);

// SVD求解
mcsolverStatus_t mcsolverDgesvd(mcsolverHandle_t handle,
                                 char jobu, char jobvt,
                                 int m, int n,
                                 double *A, int lda,
                                 double *s,
                                 double *u, int ldu,
                                 double *vt, int ldvt,
                                 double *work, int lwork,
                                 int *info);
```

## 数据类型

### 句柄

```c
mcsolverHandle_t  // mcSOLVER上下文句柄
```

### 枚举

```c
// 矩阵类型
mcsolverUplo_t     // 上三角/下三角
// MCSOLVER_UPPER
// MCSOLVER_LOWER

mcsolverSide_t     // 侧边模式
// MCSOLVER_LEFT
// MCSOLVER_RIGHT

mcsolverDiag_t     // 对角类型
// MCSOLVER_NON_UNIT
// MCSOLVER_UNIT

mcsolverDirection_t  // 方向
// MCSOLVER_COLUMN_MAJOR
// MCSOLVER_ROW_MAJOR
```

### 状态码

```c
mcsolverStatus_t
// MCSOLVER_SUCCESS
// MCSOLVER_INVALID_VALUE
// MCSOLVER_NOT_INITIALIZED
// MCSOLVER_ALLOC_FAILED
// MCSOLVER_INTERNAL_ERROR
// MCSOLVER_MATRIX_TYPE_NOT_SUPPORTED
```

## 核心API

### 生命周期

```c
mcsolverStatus_t mcsolverCreate(mcsolverHandle_t *handle);
mcsolverStatus_t mcsolverDestroy(mcsolverHandle_t handle);
```

### 密集求解

```c
// 线性系统求解
mcsolverStatus_t mcsolverDgesv(...);  // 双精度
mcsolverStatus_t mcsolverSgesv(...);  // 单精度
mcsolverStatus_t mcsolverCgesv(...);  // 单精度复数
mcsolverStatus_t mcsolverZgesv(...);  // 双精度复数

// 正定系统
mcsolverStatus_t mcsolverDposv(...);
mcsolverStatus_t mcsolverSpotrs(...);

// 对称系统
mcsolverStatus_t mcsolverDsysv(...);

// 三对角系统
mcsolverStatus_t mcsolverDgtsv(...);

// 矩阵分解
mcsolverStatus_t mcsolverDgeqrf(...);  // QR
mcsolverStatus_t mcsolverDgetrf(...);  // LU
mcsolverStatus_t mcsolverDpotrf(...);  // Cholesky
mcsolverStatus_t mcsolverDsytrf(...);  // 对称
```

### 特征值

```c
// 特征值求解
mcsolverStatus_t mcsolverDgeev(...);     // 一般矩阵
mcsolverStatus_t mcsolverDsyev(...);      // 对称矩阵
mcsolverStatus_t mcsolverDheev(...);      // Hermitian矩阵

// 广义特征值
mcsolverStatus_t mcsolverDgegv(...);
mcsolverStatus_t mcsolverDsygv(...);
```

### 奇异值

```c
// SVD
mcsolverStatus_t mcsolverDgesvd(...);    // 经典SVD
mcsolverStatus_t mcsolverDgesdd(...);    // 分治SVD
```

### 最小二乘

```c
// 最小二乘
mcsolverStatus_t mcsolverDgels(...);     // QR/LQ
mcsolverStatus_t mcsolverDgelsd(...);    // SVD
mcsolverStatus_t mcsolverDgelsy(...);   // QR with pivoting
```

## 常用示例

### LU求解

```c
void lu_solve_example() {
    mcsolverHandle_t solver;
    mcsolverCreate(&solver);

    int n = 1024;
    double *A, *B;
    int *ipiv;
    int info;

    // A * X = B
    mcsolverDgesv(solver, n, 1,
                   A, n, ipiv,
                   B, n, &info);

    mcsolverDestroy(solver);
}
```

### Cholesky求解

```c
void cholesky_example() {
    mcsolverHandle_t solver;
    mcsolverCreate(&solver);

    int n = 1024;
    double *A, *B;

    // 对称正定矩阵A的Cholesky分解
    mcsolverDpotrf(solver, MCSR_UPPER, n, A, n, &info);
    // 求解
    mcsolverDpotrs(solver, MCSR_UPPER, n, 1, A, n, B, n, &info);

    mcsolverDestroy(solver);
}
```

### SVD

```c
void svd_example() {
    mcsolverHandle_t solver;
    mcsolverCreate(&solver);

    int m = 1000, n = 500;
    double *A, *S, *U, *VT;

    // 奇异值分解 A = U * S * VT
    mcsolverDgesvd(solver, 'A', 'A', m, n, A, m, S, U, m, VT, n,
                   work, lwork, &info);

    mcsolverDestroy(solver);
}
```

## 性能特性

### 支持的矩阵
- 密集矩阵
- 对称矩阵
- Hermitian矩阵
- 正定矩阵

### 数据类型
- 单精度 (float)
- 双精度 (double)
- 复数 (single/double)

### 特性
- 直接求解（一次性分解）
- 高精度数值稳定性
- 优化GPU并行计算

## 官方参考

- 《曦云系列通用GPU mcSOLVER API参考》
- MXMACA SDK