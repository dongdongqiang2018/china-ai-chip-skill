---
name: mctriton
description: 沐曦Triton后端，支持Triton编译器在曦云GPU上编译和运行Triton内核。用于高效GPU内核开发。
keywords:
  - 沐曦
  - Triton
  - mctriton
  - 内核编程
  - JIT编译
---

# mcTriton 用户指南

mcTriton为Triton提供曦云GPU后端支持，可在曦云GPU上编译和运行Triton内核。

## 快速开始

### 安装

```bash
# 安装Triton
pip install triton

# 安装沐曦后端
pip install mctriton
# 或
pip install /opt/maca/wheel/mctriton-*.whl
```

### 验证安装

```python
import triton
print(triton.runtime.driver.active.get_current_target())
```

## 基本使用

### 编写Triton内核

```python
import triton
import triton.language as tl

@triton.jit
def kernel(
    A, B, C,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr
):
    # 内核实现
    pass
```

### 调用内核

```python
# 配置网格
grid = (triton.cdiv(M, BLOCK_M), triton.cdiv(N, BLOCK_N))

# 启动内核
kernel[grid](
    A, B, C,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_M=128, BLOCK_N=256, BLOCK_K=64
)
```

## 后端配置

### 设置后端

```python
import triton

# 设置使用沐曦后端
triton.runtime.driver.set_active("maca")
```

### 编译选项

```python
@triton.jit
def kernel(A, B, C, M, N):
    # ...
    
# 编译时指定配置
kernel[(M,)](A, B, C, M, N, num_warps=4, num_stages=2)
```

## 内存操作

### 加载

```python
a = tl.load(A + pid_m * BLOCK_M * stride_am + pid_n * BLOCK_N)
```

### 存储

```python
tl.store(C + offs_m * stride_cm + offs_n * stride_cn, c)
```

## 原子操作

```python
# 原子加
tl.atomic_add(ptr, value)
```

## 性能调优

### 配置参数

```python
kernel[grid](
    a, b, c,
    num_warps=4,      # 每SM的warp数
    num_stages=2,      # 软件流水线阶段数
    ipa=True           # 内核间并行
)
```

### 自动调优

```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256}, num_stages=3, num_warps=8),
        triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128}, num_stages=4, num_warps=4),
    ],
    key=['M', 'N']
)
@triton.jit
def kernel(A, B, C, M, N):
    # ...
```

## 官方参考

- 《曦云系列通用GPU mcTriton用户指南》
- Triton官方文档