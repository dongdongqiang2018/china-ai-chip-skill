---
name: mcrand
description: 沐曦随机数生成库，提供GPU加速的高性能随机数生成（RNG），支持多种分布和算法。用于AI训练采样、蒙特卡洛模拟等场景。
keywords:
  - 沐曦
  - 随机数
  - mcrand
  - RNG
  - 蒙特卡洛
  - 采样
---

# mcRAND 使用指南

mcRAND提供高性能GPU加速随机数生成，充分利用曦云系列GPU的高并发能力，以极致的速度提供高质量的随机数。

## 快速开始

### 安装

mcRAND随MXMACA SDK默认安装。

### Hello World

```c
#include <mcrand.h>

int main() {
    mcrandHandle_t rng;
    mcrandCreate(&rng);

    // 生成随机数
    mcrandGenerate(rng, states, N);

    mcrandDestroy(rng);
    return 0;
}
```

## 数据类型

### 句柄

```c
mcrandHandle_t  // mcRAND随机数生成器句柄
mcrandState_t   // 随机状态
```

### 随机数算法

```c
// 随机数生成算法
mcrandRngType_t
// MCRAND_RNG_PSEUDODEFAULT    // 默认
// MCRAND_RNG_MTGP32           // Mersenne Twister
// MCRAND_RNG_MRG32K3A         // 组合多递归
// MCRAND_RNG_MT19937          // Mersenne Twister 19937
// MCRAND_RNG_SOBOL32          // Sobol (32-bit)
// MCRAND_RNG_SOBOL64          // Sobol (64-bit)
// MCRAND_RNG_PHILOX4X32X10   // Philox
// MCRAND_RNG_XORWOW           // XORWOW
```

### 分布类型

```c
// 分布类型
mcrandDistribution_t
// MCRAND_UNIFORM             // 均匀分布
// MCRAND_NORMAL              // 正态分布
// MCRAND_LOG_NORMAL          // 对数正态分布
// MCRAND_POISSON             // 泊松分布
```

### 精度

```c
// 精度类型
mcrandPrecision_t
// MCRAND_DOUBLE              // 双精度
// MCRAND_SINGLE              // 单精度
```

### 状态码

```c
mcrandStatus_t
// MCRAND_SUCCESS
// MCRAND_INVALID_VALUE
// MCRAND_INVALID_HANDLE
// MCRAND_EXECUTION_FAILED
```

## 核心API

### 生命周期

```c
// 创建/销毁
mcrandStatus_t mcrandCreate(mcrandHandle_t *rng);
mcrandStatus_t mcrandDestroy(mcrandHandle_t rng);

// 创建特定算法
mcrandStatus_t mcrandCreateRng(mcrandHandle_t *rng, mcrandRngType_t rngType);
```

### 生成函数

```c
// 生成均匀分布
mcrandStatus_t mcrandGenerate(mcrandHandle_t rng,
                                float *output,
                                size_t n);
mcrandStatus_t mcrandGenerateDouble(mcrandHandle_t rng,
                                      double *output,
                                      size_t n);

// 生成正态分布
mcrandStatus_t mcrandGenerateNormal(mcrandHandle_t rng,
                                      float *output,
                                      size_t n,
                                      float mean,
                                      float stddev);
mcrandStatus_t mcrandGenerateNormalDouble(mcrandHandle_t rng,
                                            double *output,
                                            size_t n,
                                            double mean,
                                            double stddev);

// 生成对数正态分布
mcrandStatus_t mcrandGenerateLogNormal(mcrandHandle_t rng,
                                         float *output,
                                         size_t n,
                                         float mean,
                                         float stddev);

// 生成泊松分布
mcrandStatus_t mcrandGeneratePoisson(mcrandHandle_t rng,
                                       unsigned int *output,
                                       size_t n,
                                       double lambda);
```

### 设备端API

```c
// 设备端随机函数（在GPU内核中使用）
// 需要先初始化状态
mcrandStatus_t mcrandSetPseudoRandomGeneratorSeed(mcrandHandle_t rng,
                                                    unsigned long long seed);

mcrandStatus_t mcrandGenerateInteger(mcrandHandle_t rng,
                                       unsigned int *output,
                                       size_t n);

// 获取工作空间大小
mcrandStatus_t mcrandGetGeneratorSize(mcrandRngType_t rngType,
                                        size_t *size);
```

### 属性

```c
// 获取/设置算法
mcrandStatus_t mcrandGetRngType(mcrandHandle_t rng, mcrandRngType_t *rngType);
mcrandStatus_t mcrandSetRngType(mcrandHandle_t rng, mcrandRngType_t rngType);

// 获取版本
int mcrandGetVersion();
```

## 常用示例

### 均匀分布生成

```c
void uniform_example() {
    mcrandHandle_t rng;
    mcrandCreate(&rng);

    size_t N = 10000;
    float *d_data;
    cudaMalloc(&d_data, N * sizeof(float));

    // 生成[0,1)均匀分布
    mcrandGenerate(rng, d_data, N);

    cudaFree(d_data);
    mcrandDestroy(rng);
}
```

### 正态分布生成

```c
void normal_example() {
    mcrandHandle_t rng;
    mcrandCreate(&rng);

    size_t N = 10000;
    float *d_data;
    cudaMalloc(&d_data, N * sizeof(float));

    // 生成均值为0、标准差为1的正态分布
    mcrandGenerateNormal(rng, d_data, N, 0.0f, 1.0f);

    cudaFree(d_data);
    mcrandDestroy(rng);
}
```

### 泊松分布生成

```c
void poisson_example() {
    mcrandHandle_t rng;
    mcrandCreate(&rng);

    size_t N = 10000;
    unsigned int *d_data;
    cudaMalloc(&d_data, N * sizeof(unsigned int));

    // 生成lambda=5.0的泊松分布
    mcrandGeneratePoisson(rng, d_data, N, 5.0);

    cudaFree(d_data);
    mcrandDestroy(rng);
}
```

### 设备端内联API

```c
// 在GPU内核中使用（需要链接mcrand）
__global__ void kernel_with_random(float *data, mcrandState_t *states, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 使用设备端API
        data[idx] = mcrand_uniform(&states[idx]);
    }
}
```

## 支持的算法

### 高质量算法

| 算法 | 说明 |
|------|------|
| MRG32k3a | 组合多递归发生器 |
| MTGP32 | Mersenne Twister for GPU |
| XORWOW | XOR-shift + Weyl generator |
| Philox4x32x10 | Philox counter-based RNG |
| Sobol | 准随机数生成器 |

### 分布

| 分布 | 说明 |
|------|------|
| 均匀 | [0,1)或[a,b) |
| 正态 | 高斯分布 |
| 对数正态 | 对数正态分布 |
| 泊松 | 离散泊松分布 |

### 精度
- 单精度 (float)
- 双精度 (double)

## 应用场景

- AI训练采样
- 蒙特卡洛模拟
- 贝叶斯推断
- 随机初始化
- 数据增强

## 官方参考

- 《曦云系列通用GPU mcRAND API参考》
- MXMACA SDK