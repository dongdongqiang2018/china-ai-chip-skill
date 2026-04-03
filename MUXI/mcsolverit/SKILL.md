---
name: mcsolverit
description: 沐曦迭代求解器库，提供AMG、Jacobi、CG、GMRES等迭代求解器和预条件器。用于大规模稀疏线性系统求解。
keywords:
  - 沐曦
  - 迭代求解器
  - mcsolverit
  - CG
  - GMRES
  - AMG
  - 预条件子
---

# mcSolverIT 使用指南

mcSolverIT提供密集和稀疏的迭代求解器和预条件器集合，基于曦云系列GPU，为计算机视觉、CFD、ODE、计算化学和线性优化应用提供显著加速。

## 快速开始

### 安装

mcSolverIT随MXMACA SDK默认安装。

### Hello World

```c
#include <mcsolverit.h>

int main() {
    mcsolveritHandle_t handle;
    mcsolveritCreate(&handle);

    // 执行迭代求解...

    mcsolveritDestroy(handle);
    return 0;
}
```

## 求解器类型

### 迭代求解器

| 类型 | 说明 |
|------|------|
| CG | 共轭梯度 (对称正定) |
| GMRES | 广义最小残差 |
| BiCGSTAB | 双共轭梯度稳定 |
| PCG | 预条件共轭梯度 |
| PGMRES | 预条件GMRES |

### 预条件器

| 类型 | 说明 |
|------|------|
| Jacobi | Jacobi迭代 |
| Gauss-Seidel | 高斯-赛德尔 |
| AMG | 代数多网格 |
| 聚合AMG | 聚合型多网格 |
| ILU | 不完全LU |
| ICC | 不完全Cholesky |

### 松弛求解器

| 类型 | 说明 |
|------|------|
| Jacobi | Jacobi迭代 |
| Gauss-Seidel | 高斯-赛德尔 |
| SOR | 逐次超松弛 |
| Chebyshev | 切比雪夫多项式 |

## 数据类型

### 句柄

```c
mcsolveritHandle_t      // mcSolverIT上下文句柄
mcsolveritPrecond_t     // 预条件器句柄
mcsolveritSolver_t      // 求解器句柄
```

### 枚举

```c
// 求解器类型
mcsolveritSolverType_t
// MCSOLVERIT_SOLVER_CG
// MCSOLVERIT_SOLVER_GMRES
// MCSOLVERIT_SOLVER_BICGSTAB

// 预条件器类型
mcsolveritPrecondType_t
// MCSOLVERIT_PRECOND_NONE
// MCSOLVERIT_PRECOND_JACOBI
// MCSOLVERIT_PRECOND_GAUSS_SEIDEL
// MCSOLVERIT_PRECOND_AMG
// MCSOLVERIT_PRECOND_ILU

// 收敛模式
mcsolveritConv_t
// MCSOLVERIT_CONV_RELATIVE
// MCSOLVERIT_CONV_ABSOLUTE
// MCSOLVERIT_CONV_MAXITER
```

### 状态码

```c
mcsolveritStatus_t
// MCSOLVERIT_SUCCESS
// MCSOLVERIT_NOT_INITIALIZED
// MCSOLVERIT_ALLOC_FAILED
// MCSOLVERIT_INVALID_VALUE
// MCSOLVERIT_CONVERGENCE_FAILURE
// MCSOLVERIT_DIVERGENCE
// MCSOLVERIT_INTERNAL_ERROR
```

## 核心API

### 生命周期

```c
// 创建/销毁
mcsolveritStatus_t mcsolveritCreate(mcsolveritHandle_t *handle);
mcsolveritStatus_t mcsolveritDestroy(mcsolveritHandle_t handle);

// 获取版本
int mcsolveritGetVersion();
```

### CG求解器

```c
mcsolveritStatus_t mcsolveritCg(mcsolveritHandle_t handle,
                                  int n,
                                  const float *A,
                                  float *x,
                                  const float *b,
                                  int maxIter,
                                  float tol,
                                  int *iter,
                                  float *resid);
```

### GMRES求解器

```c
mcsolveritStatus_t mcsolveritGmres(mcsolveritHandle_t handle,
                                    int n,
                                    const float *A,
                                    float *x,
                                    const float *b,
                                    int restart,
                                    int maxIter,
                                    float tol,
                                    int *iter,
                                    float *resid);
```

### 预条件CG

```c
mcsolveritStatus_t mcsolveritCgPrec(mcsolveritHandle_t handle,
                                      int n,
                                      const float *A,
                                      float *x,
                                      const float *b,
                                      mcsolveritPrecond_t precond,
                                      int maxIter,
                                      float tol,
                                      int *iter,
                                      float *resid);
```

### 预条件器设置

```c
// 创建预条件器
mcsolveritStatus_t mcsolveritPrecondCreate(mcsolveritPrecond_t *precond);

// 设置Jacobi预条件器
mcsolveritStatus_t mcsolveritPrecondSetType(mcsolveritPrecond_t precond,
                                             mcsolveritPrecondType_t type);

// 设置AMG参数
mcsolveritStatus_t mcsolveritPrecondSetAMG(mcsolveritPrecond_t precond,
                                            int smoothLevels,
                                            float smoothWeight);

// 销毁预条件器
mcsolveritStatus_t mcsolveritPrecondDestroy(mcsolveritPrecond_t precond);
```

### 求解器参数

```c
// 设置收敛标准
mcsolveritStatus_t mcsolveritSolverSetTol(mcsolveritSolver_t solver, float tol);
mcsolveritStatus_t mcsolveritSolverSetMaxIter(mcsolveritSolver_t solver, int maxIter);

// 获取求解信息
mcsolveritStatus_t mcsolveritSolverGetResidualNorm(mcsolveritSolver_t solver, float *residual);
mcsolveritStatus_t mcsolveritSolverGetIteration(mcsolveritSolver_t solver, int *iter);
```

## 常用示例

### CG求解

```c
void cg_example() {
    mcsolveritHandle_t handle;
    mcsolveritCreate(&handle);

    int n = 1000;
    float *A, *x, *b;
    float tol = 1e-6;
    int maxIter = 1000;
    int iter;
    float resid;

    // 求解 A * x = b
    mcsolveritCg(handle, n, A, x, b, maxIter, tol, &iter, &resid);

    printf("CG迭代次数: %d, 残差: %f\n", iter, resid);

    mcsolveritDestroy(handle);
}
```

### 带预条件器的CG

```c
void pcg_example() {
    mcsolveritHandle_t handle;
    mcsolveritPrecond_t precond;
    mcsolveritCreate(&handle);

    // 创建Jacobi预条件器
    mcsolveritPrecondCreate(&precond);
    mcsolveritPrecondSetType(precond, MCSOLVERIT_PRECOND_JACOBI);

    // 使用预条件CG求解
    mcsolveritCgPrec(handle, n, A, x, b, precond, maxIter, tol, &iter, &resid);

    mcsolveritPrecondDestroy(precond);
    mcsolveritDestroy(handle);
}
```

### GMRES求解

```c
void gmres_example() {
    mcsolveritHandle_t handle;
    mcsolveritCreate(&handle);

    int restart = 50;
    int maxIter = 1000;
    float tol = 1e-6;

    // GMRES求解 (适合非对称矩阵)
    mcsolveritGmres(handle, n, A, x, b, restart, maxIter, tol, &iter, &resid);

    mcsolveritDestroy(handle);
}
```

## 求解器选择指南

### 对称正定矩阵
- CG (首选)
- PCG (更快收敛)

### 非对称矩阵
- GMRES
- BiCGSTAB
- PGMRES

### 对角占优/简单结构
- Jacobi
- Gauss-Seidel
- SOR

### 大规模稀疏矩阵
- AMG预条件 + CG
- 聚合AMG

## 功能特性

### 迭代求解器
- CG (共轭梯度)
- GMRES (广义最小残差)
- BiCGSTAB (双共轭梯度稳定)

### 预条件器
- Jacobi
- Gauss-Seidel
- 代数多网格 (AMG)
- 聚合AMG
- 不完全LU/Cholesky
- 多项式预条件器

### 求解选项
- 相对/绝对收敛
- 残差阈值
- 最大迭代次数
- 重启参数 (GMRES)

## 官方参考

- 《曦云系列通用GPU mcSolverIT API参考》
- MXMACA SDK