---
name: mxcc
description: 沐曦C/C++编译器，用于编译曦云系列GPU的CUDA/HIP/异构计算程序。基于LLVM架构，支持GPU内核开发。
keywords:
  - 沐曦
  - 编译器
  - mxcc
  - CUDA
  - 异构计算
  - GPU编译
---

# mxcc 编译器指南

mxcc是沐曦基于LLVM架构开发的C/C++编译器，用于编译曦云系列GPU的异构计算程序。

## 快速开始

### 基本用法

```bash
# 编译CUDA程序
mxcc -o output input.cu

# 编译并指定GPU架构
mxcc -o output input.cu --arch=sm_80

# 编译并生成PTX
mxcc -o output input.cu -ptx
```

### 编译选项

| 选项 | 说明 |
|------|------|
| `-o <file>` | 指定输出文件 |
| `-c` | 只编译不链接 |
| `-arch=<arch>` | 指定目标GPU架构 |
| `-code=<code>` | 指定生成的code |
| `-ptx` | 生成PTX中间代码 |
| `-g` | 生成调试信息 |
| `-O0/-O1/-O2/-O3` | 优化级别 |
| `-lineinfo` | 生成行信息 |

## 常用命令

### Hello World

```bash
# 编译简单CUDA程序
mxcc hello.cu -o hello

# 运行
./hello
```

### 链接库

```bash
# 链接CUDA库
mxcc program.cu -o program -lcuda -lcudart

# 链接多个库
mxcc program.cu -o program -L/opt/maca/lib -lmaca -lmcdnn -lmcblas
```

### 混合编译

```bash
# 编译CPU和GPU代码
mxcc main.cpp helper.cu -o program -lmaca
```

## 编译配置

### 环境变量

```bash
# 设置MACA路径
export MACA_PATH=/opt/maca

# 添加库路径
export LD_LIBRARY_PATH=$MACA_PATH/lib:$LD_LIBRARY_PATH
```

### 交叉编译

```bash
# 为目标设备交叉编译
mxcc --target=arm64-linux-gnu input.cu -o output
```

## 优化选项

### 性能优化

```bash
# 最高优化
mxcc -O3 input.cu -o output

# 使用-fast-math
mxcc -O3 -fast-math input.cu -o output

# 展开循环
mxcc -O3 -funroll-loops input.cu -o output
```

### GPU特定优化

```bash
# 指定共享内存大小
mxcc -Xmxcc -mhwjoin -Xmxcc -fremap-arrays

# 优化寄存器使用
mxcc -maxrregcount=128 input.cu -o output
```

## 调试

### 调试信息

```bash
# 生成调试信息
mxcc -g input.cu -o output

# 生成行信息
mxcc -lineinfo input.cu -o output

# 生成PDB文件
mxcc -g input.cu -o output -lineinfo
```

## 错误处理

### 常见错误

```bash
# 查看详细错误信息
mxcc -v input.cu -o output

# 显示所有警告
mxcc -Wall input.cu -o output

# 视为错误处理警告
mxcc -Werror input.cu -o output
```

## 官方参考

- 《曦云系列通用GPU mxcc编译器用户指南》
- MXMACA SDK