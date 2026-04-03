---
name: biren-brcc
description: BIREN BRCC (BIREN Compiler Collection) 编译器参考指南。基于 Clang 和 LLVM 开发的编译器，提供完整的 SUPA 编译工具链，用于编译 C/C++/SUPA 源代码生成主机端和设备端可执行文件。
keywords:
  - brcc
  - biren
  - 编译器
  - SUPA
  - CUDA迁移
  - 异构计算
  - 壁仞
---

# BRCC Command Reference

BRCC（Biren Compiler Collection）是基于 Clang 和 LLVM 开发的编译器。

## Quick Start

```bash
# 编译 .su 文件
brcc a.su b.su -c

# 编译 C++ 文件
brcc -x supa c.cpp -c

# 链接
brcc --supa-link a.o b.o c.o -o vectorAdd

# 运行
./vectorAdd
```

## Installation

安装路径：`/usr/local/birensupa/sdk/latest/brcc`

```bash
brcc --version
```

## Predefined Macros

| Macro | Description |
|-------|-------------|
| `__BRCC__` | 编译任意源文件时定义 |
| `__SUPA__` | 编译 SUPA 源文件时定义 |
| `__SUPACC__` | 编译 SUPA 源文件时定义 |
| `__SUPA_ARCH__` | 编译 SUPA 设备端代码时定义 |
| `__BRCC_VERSION__` | BRCC 版本号 |
| `__BRCC_VER_MAJOR__` | BRCC 主版本号 |
| `__BRCC_VER_MINOR__` | BRCC 次版本号 |
| `__BRCC_VER_PATCHLEVEL__` | BRCC 补丁版本号 |

## File Extensions

| Extension | Description |
|-----------|-------------|
| `.c` | C 语言源文件 |
| `.cc, .cxx, .cpp` | C++ 语言源文件 |
| `.su` | SUPA 源文件 |
| `.o, .obj` | 目标文件 |
| `.a, .lib` | 静态库 |
| `.so` | 动态库 |
| `.bc` | LLVM bitcode |

## Compilation Stages

| Option | Stage | Default Output |
|--------|-------|----------------|
| `-E` | 预处理 | 屏幕输出 |
| `-c` | 预处理、编译、汇编 | `src.o` |
| `-emit-llvm -S` | 预处理和编译 | `src.ll` |

## Key Options

### File and Path

| Option | Description |
|--------|-------------|
| `-o <file>` | 输出文件 |
| `-D <macro>=<value>` | 定义宏 |
| `-U <macro>` | 取消宏定义 |
| `-I <dir>` | 添加头文件路径 |
| `-include <file>` | 预先包含头文件 |
| `-L <dir>` | 添加库路径 |
| `-l` | 链接库 |
| `-save-temps` | 保存中间文件 |

### Compiler Behavior

| Option | Description |
|--------|-------------|
| `-std=<value>` | C++ 版本 (c++14, c++17, c++20) |
| `-x supa` | 指定 SUPA 语言 |
| `--supa-link` | 链接 SUPA Object |

### GPU Configuration

| Option | Description |
|--------|-------------|
| `--supa-gpu-arch=<value>` | 指定 GPU 架构 |
| `--supa-host-only` | 只编译主机端 |
| `--supa-device-only` | 只编译设备端 |

### Debugging

| Option | Description |
|--------|-------------|
| `-g` | 生成主机端调试信息 |
| `-gsupa (-G)` | 生成设备端调试信息 |
| `-fsupa-device-opt` | 设备端代码优化 |

### Optimization

| Option | Description |
|--------|-------------|
| `-O<value>` | 主机端优化级别 |
| `-maxregcount` | 最大寄存器数量 |
| `-print-reg-count` | 打印寄存器使用 |

## Example: Vector Addition

```cpp
//---------- a.h ----------
__device__ void funcAdd(int i, float *x, float *y);

//---------- a.su ----------
__device__ void funcAdd(int i, float *x, float *y) {
    y[i] = x[i] + y[i];
}

//---------- b.su ----------
__global__ void vectorAdd(int n, float *x, float *y) {
    int index = block_idx.x * block_dim.x + thread_idx.x;
    int stride = block_dim.x * grid_dim.x;
    for (int i = index; i < n; i += stride)
        funcAdd(i, x, y);
}

int foo() {
    // 分配内存、复制数据、启动 kernel
    // ...
}

//---------- c.cpp ----------
int main(){ return foo(); }
```

### Compile and Link

```bash
# 一步完成
brcc a.su b.su -x supa c.cpp -o vectorAdd

# 分步编译
brcc a.su b.su -c
brcc -x supa c.cpp -c
brcc --supa-link a.o b.o c.o -o vectorAdd
```

## Example: Static Library

```bash
# 编译静态库
brcc a.su -c -o a.o
ar rcs libstatic_a.a a.o
brcc b.su -x supa c.cpp -L . -lstatic_a -o vectorAdd
```

## Example: Dynamic Library

```bash
# 编译动态库
brcc -fPIC a.su b.su -c
brcc --supa-link -shared a.o b.o -o libshared_ab.so
brcc c.cpp -L . -lshared_ab -o vectorAdd -Wl,-rpath .
```

## Example: Host/Device Only

```bash
# 只编译主机端
brcc vectorAdd.su -c --supa-host-only -o vectorAdd-host.o

# 只编译设备端
brcc vectorAdd.su -c --supa-device-only -o vectorAdd-device.bc
```

## Link Cache

```bash
# 开启缓存
export BRCC_THINLTO_CACHE=ON

# 设置缓存目录
export BRCC_THINLTO_CACHE_DIR=/path/to/cache

# 设置缓存大小
export BRCC_THINLTO_CACHE_SIZE=10G
```

## GCC Path

```bash
# 指定 gcc 路径
brcc -v --gcc-install-dir=/usr/lib/gcc/x86_64-linux-gnu/9
```

## SUPA Programming Model

### Function Qualifiers

| Qualifier | Description |
|-----------|-------------|
| `__global__` | 核函数（主机端调用） |
| `__device__` | 设备端函数 |
| `__host__` | 主机端函数 |

### Memory

| Qualifier | Description |
|-----------|-------------|
| `__device__` | 设备端全局变量 |
| `__constant__` | 常量内存 |
| `__shared__` | 共享内存 |

### Built-in Variables

- `grid_dim` - 网格维度
- `block_idx` - 线程块索引
- `block_dim` - 线程块维度
- `thread_idx` - 线程索引
- `warp_size` - 线程束大小 (32)

## Compilation Workflow

```
Host: Source → Preprocess → Compile → Assemble → Link → Executable
Device: Source → Preprocess → Compile → Link → Subin → Fatbinary → Embedded
```

## CUDA Compatibility

BRCC 支持 CUDA 代码迁移，使用 `suLaunchKernel` 替代 `<<<...>>>`。

```cpp
// CUDA
kernel<<<dimGrid, dimBlock>>>(args);

// SUPA
suLaunchKernel(kernel, dimGrid, dimBlock, 0, stream, args);
```

## Notes

- 不支持多进程同时安装
- 不支持多进程同时安装同一个 .run 文件
- 缓存文件有效期一周
- 需要设置环境变量 `source /usr/local/birensupa/sdk/latest/scripts/brsw_set_env.sh`

## Related Tools

- **brSimulator**: 仿真器
- **suDebugger**: 调试器
- **suSanitizer**: 检查工具
- **BIRENSUPA SDK**: 完整 SDK