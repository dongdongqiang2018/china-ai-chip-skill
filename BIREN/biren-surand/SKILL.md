---
name: biren-surand
description: BIREN suRAND 随机数生成库参考指南。提供 XORWOW、Philox4x32-10、MTGP32 三种随机数生成算法，支持均匀分布、正态分布、对数正态分布、泊松分布、二项分布等，可在主机端或设备端生成高质量随机数。
keywords:
  - surand
  - biren
  - 随机数
  - RNG
  - GPU随机数
  - Monte Carlo
  - 壁仞
---

# suRAND Command Reference

suRAND 是壁仞 GPU 加速的随机数生成库。

## Quick Start

### Host API

```c
#include <surand.h>

// 创建生成器
surandGenerator_t gen;
surandCreateGenerator(&gen, SURAND_RNG_PSEUDO_XORWOW);

// 设置种子
surandSetPseudoRandomGeneratorSeed(gen, 12345);

// 生成随机数
surandGenerateUniform(gen, d_data, n);

// 销毁
surandDestroyGenerator(gen);
```

### Device API

```c
// 在 kernel 中使用
__device__ void my_kernel() {
    surandStateXORWOW_t state;
    surand_init(seed, tid, offset, &state);
    float val = surand_uniform(&state);
}
```

## Installation

安装路径：`/usr/local/birensupa/sdk/latest/sulib`

## Random Number Algorithms

| Algorithm | Enum | Description |
|------------|------|-------------|
| XORWOW | `SURAND_RNG_PSEUDO_XORWOW` | 默认伪随机数生成器 |
| Philox4x32-10 | `SURAND_RNG_PSEUDO_PHILOX4_32_10` | 基于计数器的生成器 |
| MTGP32 | `SURAND_RNG_PSEUDO_MTGP32` | Mersenne Twister for GPU |

## Distributions

### Host API

| Distribution | Function |
|--------------|----------|
| 均匀分布 | `surandGenerateUniform` |
| 双精度均匀分布 | `surandGenerateUniformDouble` |
| 正态分布 | `surandGenerateNormal` |
| 双精度正态分布 | `surandGenerateNormalDouble` |
| 对数正态分布 | `surandGenerateLogNormal` |
| 双精度对数正态分布 | `surandGenerateLogNormalDouble` |
| 泊松分布 | `surandGeneratePoisson` |

### Device API

| Distribution | Function |
|--------------|----------|
| 均匀分布 | `surand_uniform` |
| 双精度均匀分布 | `uniform_double` |
| 正态分布 | `surand_normal` |
| 双精度正态分布 | `normal_double` |
| 对数正态分布 | `surand_log_normal` |
| 泊松分布 | `surand_poisson` |
| 二项分布 | `surand_binomial` |

## Host API Functions

### Generator Management

| Function | Description |
|----------|-------------|
| `surandCreateGenerator` | 创建生成器 |
| `surandDestroyGenerator` | 销毁生成器 |
| `surandSetStream` | 绑定 SUPA 流 |
| `surandSetGeneratorSeed` | 设置种子 |
| `surandSetGeneratorOffset` | 设置偏移量 |
| `surandSetGeneratorOrdering` | 设置排序方式 |
| `surandGenerate` | 生成 32 位无符号整数 |

### Distribution Generation

| Function | Description |
|----------|-------------|
| `surandGenerateUniform` | 生成均匀分布 |
| `surandGenerateNormal` | 生成正态分布 |
| `surandGenerateLogNormal` | 生成对数正态分布 |
| `surandGeneratePoisson` | 生成泊松分布 |

## Device API Functions

### Initialization

| Algorithm | Function |
|-----------|----------|
| XORWOW | `surand_init` |
| Philox4x32-10 | `surand_init` |
| MTGP32 | `surand_init` |

### Jump

| Algorithm | Skip | Skip Ahead Sequence |
|-----------|------|---------------------|
| XORWOW | `skipahead` | `skipahead_sequence` |
| Philox4x32-10 | `skipahead` | `skipahead_sequence` |
| MTGP32 | `skipahead` | - |

### Generation

| Algorithm | Single | Quad |
|-----------|--------|------|
| XORWOW | `surand` | `surand4` |
| Philox4x32-10 | `surand` | `surand4` |
| MTGP32 | `surand` | - |

## Example: Host API

```c
#include <surand.h>

int main() {
    surandGenerator_t gen;
    int n = 1000;
    float *d_data;

    // 创建设备内存
    // ...

    // 创建生成器
    surandCreateGenerator(&gen, SURAND_RNG_PSEUDO_XORWOW);

    // 设置种子
    surandSetPseudoRandomGeneratorSeed(gen, 12345);

    // 生成均匀分布 [0,1)
    surandGenerateUniform(gen, d_data, n);

    // 生成正态分布 (mean=0, stddev=1)
    surandGenerateNormal(gen, d_data, n, 0.0f, 1.0f);

    // 销毁
    surandDestroyGenerator(gen);

    return 0;
}
```

## Example: Device API

```c
// Kernel 中使用
__global__ void generate_kernel(unsigned int seed, int n, float *output) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    surandStateXORWOW_t state;
    surand_init(seed, tid, 0, &state);

    // 生成 (0,1] 均匀分布
    output[tid] = surand_uniform(&state);
}
```

## Device API with Philox

```c
__global__ void philox_kernel(unsigned long long seed, int n, float *output) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    surandStatePhilox4x32_10_t state;
    surand_init(seed, tid, 0, &state);
    output[tid] = surand_uniform(&state);
}
```

## Important Notes

### Range Differences

- **Host API** `surandGenerateUniform`: 生成 [0,1) 范围
- **Device API** `surand_uniform`: 生成 (0,1] 范围（注意区间差异）

### Distribution Requirements

- 正态分布和对数正态分布要求生成数量为偶数

### MTGP32 Requirements

- MTGP32 的 Device API 需要先在 Host 端加载预计算参数

### Thread Safety

- Host API 是线程安全的
- 每个线程应使用独立的 state

## Return Codes

| Code | Description |
|------|-------------|
| `SURAND_STATUS_SUCCESS` | 成功 |
| `SURAND_STATUS_NOT_INITIALIZED` | 未初始化 |
| `SURAND_STATUS_INVALID_VALUE` | 无效值 |
| `SURAND_STATUS_ALLOC_FAILED` | 分配失败 |
| `SURAND_STATUS_INTERNAL_ERROR` | 内部错误 |

## Performance Tips

- 批量生成时使用 Host API
- Kernel 内频繁生成时使用 Device API
- 复用 state 可以提高性能
- 合理选择算法平衡质量和性能

## Use Cases

- Monte Carlo 模拟
- 神经网络 Dropout
- 数据增强
- 随机初始化
- 密码学应用（需要额外处理）

## Related Libraries

- **BPP**: 图像处理
- **suBLAS**: 线性代数
- **suDNN**: 深度学习
- **suFFT**: 快速傅里叶变换