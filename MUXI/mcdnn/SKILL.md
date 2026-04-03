---
name: mcdnn
description: 沐曦深度神经网络库，提供GPU加速的DNN原语实现，包括卷积、池化、归一化、激活函数等。是AI训练和推理的核心计算库。
keywords:
  - 沐曦
  - 深度学习
  - mcdnn
  - DNN库
  - 卷积
  - 神经网络
---

# mcDNN 使用指南

mcDNN是GPU加速的深度神经网络原语库，为标准卷积、池化、归一化和激活层提供高度优化的实现，加速主流深度学习框架。

## 快速开始

### 安装

mcDNN随MXMACA SDK默认安装。

### Hello World

```c
#include <mcdnn.h>

int main() {
    mcdnnHandle_t handle;
    mcdnnCreate(&handle);

    // 执行DNN操作...

    mcdnnDestroy(handle);
    return 0;
}
```

## 数据类型

### 句柄

```c
mcdnnHandle_t  // mcDNN上下文句柄
```

### 描述符类型

```c
mcdnnActivationDescriptor_t      // 激活描述符
mcdnnCTCLossDescriptor_t        // CTC损失描述符
mcdnnDropoutDescriptor_t        // Dropout描述符
mcdnnFilterDescriptor_t         // 滤波器描述符
mcdnnLRNDescriptor_t            // LRN描述符
mcdnnOpTensorDescriptor_t      // 张量操作描述符
mcdnnPoolingDescriptor_t       // 池化描述符
mcdnnReduceTensorDescriptor_t  // 归约描述符
mcdnnSpatialTransformerDescriptor_t  // 空间变换描述符
mcdnnTensorDescriptor_t         // 张量描述符
mcdnnTensorTransformDescriptor_t  // 张量变换描述符
```

### 枚举类型

```c
// 激活模式
mcdnnActivationMode_t  // SIGMOID, RELU, TANH, CLIPPED_RELU, ELU, SWISH

// 数据类型
mcdnnDataType_t  // FLOAT_HALF, FLOAT, INT8, INT32, INT64

// 归一化模式
mcdnnNormMode_t  // SPATIAL, PER_CHANNEL

// 池化模式
mcdnnPoolingMode_t  // MAX, AVERAGE_COUNT_INCLUDE_PADDING, AVERAGE_COUNT_EXCLUDE_PADDING, DETERMINISTIC

// Softmax模式
mcdnnSoftmaxAlgorithm_t  // FAST, ACCURATE, LOG
mcdnnSoftmaxMode_t      // CHANNEL, INSTANCE, SPACE

// 张量格式
mcdnnTensorFormat_t  // NCHW, NHWC, NCHW_VECT_C
```

### 状态码

```c
mcdnnStatus_t
// MCDNN_STATUS_SUCCESS
// MCDNN_STATUS_NOT_INITIALIZED
// MCDNN_STATUS_ALLOC_FAILED
// MCDNN_STATUS_INVALID_VALUE
// MCDNN_STATUS_EXECUTION_FAILED
// MCDNN_STATUS_INTERNAL_ERROR
```

## 核心API

### 生命周期

```c
// 创建/销毁句柄
mcdnnStatus_t mcdnnCreate(mcdnnHandle_t *handle);
mcdnnStatus_t mcdnnDestroy(mcdnnHandle_t handle);
```

### 张量描述符

```c
// 创建/销毁
mcdnnStatus_t mcdnnCreateTensorDescriptor(mcdnnTensorDescriptor_t *tensorDesc);
mcdnnStatus_t mcdnnDestroyTensorDescriptor(mcdnnTensorDescriptor_t tensorDesc);

// 设置/获取维度
mcdnnStatus_t mcdnnSetTensor4dDescriptor(mcdnnTensorDescriptor_t tensorDesc,
                                          mcdnnTensorFormat_t format,
                                          mcdnnDataType_t dataType,
                                          int n, int c, int h, int w);
mcdnnStatus_t mcdnnGetTensor4dDescriptor(mcdnnTensorDescriptor_t tensorDesc,
                                          mcdnnDataType_t *dataType,
                                          int *n, int *c, int *h, int *w,
                                          int *nStride, int *cStride, int *hStride, int *wStride);
```

### 卷积

```c
// 创建卷积描述符
mcdnnStatus_t mcdnnCreateConvolutionDescriptor(mcdnnConvolutionDescriptor_t *convDesc);
mcdnnStatus_t mcdnnSetConvolution2dDescriptor(mcdnnConvolutionDescriptor_t convDesc,
                                               int pad_h, int pad_w,
                                               int stride_h, int stride_w,
                                               int dilation_h, int dilation_w,
                                               mcdnnDataType_t computeType,
                                               mcdnnConvolutionMode_t mode);

// 卷积前向
mcdnnStatus_t mcdnnConvolutionForward(mcdnnHandle_t handle,
                                       const void *alpha,
                                       const mcdnnTensorDescriptor_t inputDesc,
                                       const void *inputData,
                                       const mcdnnFilterDescriptor_t filterDesc,
                                       const void *filterData,
                                       const mcdnnConvolutionDescriptor_t convDesc,
                                       const void *beta,
                                       const mcdnnTensorDescriptor_t outputDesc,
                                       void *outputData);
```

### 池化

```c
// 创建池化描述符
mcdnnStatus_t mcdnnCreatePoolingDescriptor(mcdnnPoolingDescriptor_t *poolingDesc);
mcdnnStatus_t mcdnnSetPooling2dDescriptor(mcdnnPoolingDescriptor_t poolingDesc,
                                            mcdnnPoolingMode_t mode,
                                            mcdnnNanPropagation_t maxpoolingNanOpt,
                                            int windowHeight, int windowWidth,
                                            int pad_h, int pad_w,
                                            int stride_h, int stride_w);

// 池化前向
mcdnnStatus_t mcdnnPoolingForward(mcdnnHandle_t handle,
                                  const mcdnnPoolingDescriptor_t poolingDesc,
                                  const void *alpha,
                                  const mcdnnTensorDescriptor_t inputDesc,
                                  const void *inputData,
                                  const void *beta,
                                  const mcdnnTensorDescriptor_t outputDesc,
                                  void *outputData);
```

### 激活函数

```c
// 创建激活描述符
mcdnnStatus_t mcdnnCreateActivationDescriptor(mcdnnActivationDescriptor_t *actDesc);
mcdnnStatus_t mcdnnSetActivationDescriptor(mcdnnActivationDescriptor_t actDesc,
                                              mcdnnActivationMode_t mode,
                                              mcdnnNanPropagation_t reluNanOpt,
                                              double CeilValue);

// 激活前向
mcdnnStatus_t mcdnnActivationForward(mcdnnHandle_t handle,
                                      const mcdnnActivationDescriptor_t actDesc,
                                      const void *alpha,
                                      const mcdnnTensorDescriptor_t inputDesc,
                                      const void *inputData,
                                      const void *beta,
                                      const mcdnnTensorDescriptor_t outputDesc,
                                      void *outputData);
```

### 批量归一化

```c
mcdnnStatus_t mcdnnBatchNormalizationForwardInference(...);
mcdnnStatus_t mcdnnBatchNormalizationForwardTraining(...);
mcdnnStatus_t mcdnnBatchNormalizationBackward(...);
```

### Softmax

```c
mcdnnStatus_t mcdnnSoftmaxForward(mcdnnHandle_t handle,
                                   const mcdnnTensorDescriptor_t inputDesc,
                                   const void *inputData,
                                   const mcdnnSoftmaxAlgorithm_t algo,
                                   const mcdnnSoftmaxMode_t mode,
                                   const mcdnnTensorDescriptor_t outputDesc,
                                   void *outputData);
```

### 张量操作

```c
// 加法
mcdnnStatus_t mcdnnAddTensor(mcdnnHandle_t handle,
                              const void *alpha,
                              const mcdnnTensorDescriptor_t aDesc,
                              const void *a,
                              const void *beta,
                              const mcdnnTensorDescriptor_t cDesc,
                              void *c);

// 归约
mcdnnStatus_t mcdnnReduceTensor(mcdnnHandle_t handle,
                                 const mcdnnReduceTensorDescriptor_t reduceDesc,
                                 const void *alpha,
                                 const mcdnnTensorDescriptor_t aDesc,
                                 const void *a,
                                 const void *beta,
                                 const mcdnnTensorDescriptor_t cDesc,
                                 void *c);
```

## 常用示例

### 卷积前向

```c
void convolution_forward_example() {
    mcdnnHandle_t handle;
    mcdnnCreate(&handle);

    // 输入: NCHW 32x3x224x224
    mcdnnTensorDescriptor_t inputDesc, outputDesc;
    mcdnnFilterDescriptor_t filterDesc;
    mcdnnConvolutionDescriptor_t convDesc;

    mcdnnSetTensor4dDescriptor(inputDesc, MCDNN_TENSOR_NCHW,
                                MCDNN_DATA_FLOAT, 32, 3, 224, 224);
    mcdnnSetFilter4dDescriptor(filterDesc, MCDNN_TENSOR_NCHW,
                                MCDNN_DATA_FLOAT, 64, 3, 7, 7);
    mcdnnSetConvolution2dDescriptor(convDesc, 3, 3, 1, 1, 1, 1,
                                     MCDNN_DATA_FLOAT, MCDNN_CONVOLUTION);

    float alpha = 1.0f, beta = 0.0f;
    mcdnnConvolutionForward(handle, &alpha, inputDesc, inputData,
                            filterDesc, filterData, convDesc,
                            &beta, outputDesc, outputData);

    mcdnnDestroy(handle);
}
```

## 功能特性

### 支持的操作
- 卷积 (1D/2D/3D)
- 池化 (Max/Average)
- 归一化 (BatchNorm, LRN, InstanceNorm)
- 激活函数 (ReLU, Sigmoid, TanH, ELU, Swish)
- Softmax
- CTC Loss
- 空间变换 (Attention, GridGen)
- 张量运算 (Add, Mul, Reduce)

### 数据格式
- FP32 (单精度)
- FP16 (半精度)
- BF16 (Brain Float)
- INT8 (量化)
- NCHW / NHWC

### 硬件加速
- 张量核心加速
- 2D/3D卷积
- 分组卷积
- 深度可分离卷积

## 官方参考

- 《曦云系列通用GPU mcDNN API参考》
- MXMACA SDK