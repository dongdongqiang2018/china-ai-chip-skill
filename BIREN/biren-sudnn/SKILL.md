---
name: biren-sudnn
description: BIREN suDNN 深度学习算子库参考指南。提供 Eager 和 Graph 两套 API 接口，支持卷积、池化、归一化、激活函数、损失函数、矩阵乘等 42+ 种深度学习算子，用于构建和运行深度神经网络模型。
keywords:
  - sudnn
  - biren
  - 深度学习
  - 神经网络
  - DNN
  - 卷积
  - 池化
  - 壁仞
---

# suDNN Command Reference

suDNN 是壁仞深度学习算子库，提供 Eager 和 Graph 两套 API 接口。

## Quick Start

### Eager API

```c
#include <sudnn.h>

// 创建张量描述符
sudnnTensorDescriptor_t inputDesc, outputDesc;
sudnnCreateTensorDescriptor(&inputDesc);
sudnnSetTensorDescriptor(inputDesc, SUDNN_DATA_FLOAT, SUDNN_NCHW, N, C, H, W);

// 创建算子
sudnnConvolutionDescriptor_t convDesc;
sudnnCreateConvolutionDescriptor(&convDesc);
sudnnSetConvolutionDescriptor(convDesc, SUDNN_CROSS_CORRELATION, SUDNN_PADDING_SAME,
                              1, 1, 1, 1);

// 执行卷积
sudnnConvolutionForward(handle, alpha, inputDesc, inputData, weightDesc, weightData,
                         convDesc, beta, outputDesc, outputData);
```

### Graph API

```c
// 1. 配置张量描述符
// 2. 配置算子描述符
// 3. 构建计算图描述符
// 4. 创建 Engine 描述符
// 5. 配置 Knob 描述符
// 6. 组合 EngineCfg 描述符
// 7. 创建 Plan 和 VariantPack
// 8. 执行
sudnnExecutePlan(plan, variantPack);
```

## Installation

安装路径：`/usr/local/birensupa/sdk/latest/sulib`

运行时依赖：libc.so, libstdc++.so, libgcc_s.so, libboost_regex.so

## Memory Layout

### Layout Types

| Layout | Description |
|--------|-------------|
| `COLMAJOR` / `ROWMAJOR` | 列/行主序 |
| `ACTIVATION` | 神经网络激活值 |
| `WEIGHT` | 卷积权重 |
| `LINEAR` | 偏置/统计量 |
| `IMAGE` | 图像数据 |
| `DEPTHWISE_WEIGHT` | 逐深度卷积权重 |
| `BUFFER` | 通用数据布局 |
| `GROUPED_WEIGHT` | 分组卷积权重 |
| `CHANNEL_FIRST` | 通道优先 |

### Layout Limits

| Layout | Limits |
|--------|--------|
| Matrix | N0≤1024, H≤8192, W≤8192, N1<256 |
| Activation | C,H,W≤8192, N≤1024 |
| Conv Weight | O,I≤8192, H*W≤8192 |
| Vector | L≤8192, N1*N0≤1024 |

## Graph API Operators (42+)

### Convolution

| Operator | Description |
|----------|-------------|
| `Conv Forward` | 卷积前向 |
| `Conv Backward Data` | 卷积反向数据 |
| `Conv Backward Filter` | 卷积反向权重 |

### Pointwise (60+ modes)

ADD, SUB, MUL, DIV, RELU, GELU, SIGMOID, TANH, ELU, SWISH, ERF 等

### Matrix Operations

| Operator | Description |
|----------|-------------|
| `Matmul` | 矩阵乘法 (2D/3D/4D, 支持广播和转置) |

### Normalization

| Operator | Description |
|----------|-------------|
| `Batchnorm Forward/Backward` | 批归一化 |
| `Layernorm Forward/Backward` | 层归一化 |

### Pooling

| Operator | Description |
|----------|-------------|
| `Pooling Forward/Backward` | 池化 (MAX/AVG_INCLUDE/AVG_EXCLUDE/GLOBAL_AVG) |

### Tensor Operations

| Operator | Description |
|----------|-------------|
| `Slice` | 切片 |
| `Concat` | 拼接 |
| `Reshape` | 形状变换 |
| `Permute` | 维度重排 |
| `Resample` | 重采样 |
| `Embedding Forward/Backward` | 嵌入 |
| `Dropout Forward/Backward` | Dropout |
| `MaskedFill` | 掩码填充 |
| `Softmax Forward/Backward` | Softmax |

### Loss Functions

| Operator | Description |
|----------|-------------|
| `MSELoss Fwd/Bwd` | 均方误差损失 |
| `BCELoss Fwd/Bwd` | 二元交叉熵损失 |
| `BCEWithLogitsLoss Fwd/Bwd` | 带 logits 二元交叉熵损失 |

### Other Operations

| Operator | Description |
|----------|-------------|
| `Gather` | 索引收集 |
| `Scatter` | 索引散布 |
| `Reduce` | 归约 |
| `Broadcast` | 广播 |
| `Pad` | 填充 |
| `TypeCast` | 类型转换 |
| `Clamp` | 截断 |
| `Trilu` | 三角矩阵 |
| `Where` | 条件选择 |
| `Arange` | 序列生成 |

## Matmul Support

### Data Types

- BF16×BF16→BF16/FP32
- FP32×FP32→FP32
- S8/U8×S8/U8→BF16/FP32
- S8×BF16→BF16/FP32

### Shape Support

- 2D: (H,W), H/W≤8192
- 3D: (B,H,W), B≤64K (H/W≤8192时)
- 4D: (B1,B2,H,W), B1≤64*spc数, B2≤1024, H/W≤8192

## Conv2d Support

- stride: (1,1) 或 (2,2)
- filter_size: kh(1~7), kw(1~7, 300)
- padding: same mode 或 valid mode
- dilation: (1,1) 或 (2,2) 或 (4,4)
- Data types: BF16, FP32, UINT8, INT8
- Support Grouped Conv and Depthwise Conv

## Eager API Operators

| Category | Operators |
|----------|-----------|
| Activation | ActivationForward / ActivationBackward |
| Tensor Ops | OpTensor / AddTensor / ScaleTensor |
| Softmax | SoftmaxForward / SoftmaxBackward |
| Convolution | ConvolutionForward / BackwardData / BackwardFilter |
| Reduce | ReduceTensor |
| CTC Loss | CTCLoss |
| BatchNorm | ForwardInference / ForwardTraining / Backward |
| Pooling | PoolingForward / PoolingBackward |
| Dropout | DropoutForward / DropoutBackward |
| LayerNorm | LayerNormForward / LayerNormBackward |

## Backend API

底层实现接口，使用描述符模式：

```c
sudnnBackendCreateDescriptor(SUDNN_BACKEND_TENSOR_DESCRIPTOR, &desc);
sudnnBackendSetAttribute(desc, attrName, attrType, count, &value);
sudnnBackendFinalize(desc);
sudnnBackendGetAttribute(desc, attrName, attrType, count, &elemCount, &value);
sudnnBackendDestroyDescriptor(desc);
```

## Memory Architecture

| Type | Description |
|------|-------------|
| `suMemArchTypeNUMA` | 非统一内存访问 |
| `suMemArchTypeUMA` | 统一内存访问 |
| `suMemArchTypeUMA4` | 4-SPC 统一内存访问 |
| `suMemArchTypeUMA8` | 8-SPC 统一内存访问 |
| `suMemArchTypeUMA16` | 16-SPC 统一内存访问 |

## Return Codes

| Code | Description |
|------|-------------|
| `SUDNN_STATUS_SUCCESS` | 成功 |
| `SUDNN_STATUS_NOT_INITIALIZED` | 未初始化 |
| `SUDNN_STATUS_INVALID_VALUE` | 无效值 |
| `SUDNN_STATUS_ARCH_MISMATCH` | 架构不匹配 |
| `SUDNN_STATUS_INTERNAL_ERROR` | 内部错误 |

## Example: Convolution

```c
#include <sudnn.h>

int main() {
    sudnnHandle_t handle;
    sudnnCreate(&handle);

    // 创建描述符
    sudnnTensorDescriptor_t inputDesc, weightDesc, outputDesc;
    sudnnConvolutionDescriptor_t convDesc;

    // 配置
    sudnnSetTensorDescriptor(inputDesc, SUDNN_DATA_FLOAT, SUDNN_NCHW,
                             batch, channels, height, width);
    sudnnSetConvolutionDescriptor(convDesc, SUDNN_CROSS_CORRELATION,
                                  SUDNN_PADDING_SAME, 1, 1, 1, 1);

    // 执行
    sudnnConvolutionForward(handle, alpha, inputDesc, input,
                            weightDesc, weight, convDesc, beta,
                            outputDesc, output);

    sudnnDestroy(handle);
    return 0;
}
```

## Notes

- Eager API 提供易用的 C++ 接口
- Graph API 提供声明式编程方法
- 支持多种数据类型和布局
- 建议使用 Graph API 获得更好性能

## Related Libraries

- **BPP**: 图像处理
- **suBLAS**: 线性代数
- **suFFT**: 快速傅里叶变换
- **suRAND**: 随机数生成