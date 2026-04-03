---
name: biren-bpp
description: BIREN BPP (BIREN Performance Primitives) 图像处理库参考指南。用于图像和视频处理的 GPU 加速函数库，包含矩阵变换、图像质量、颜色空间转换、融合操作、裁剪、翻转、填充、缩放、旋转、直方图均衡化、仿射/透视变换、混合、滤波、边缘检测、形态学、阈值、归一化、算术运算、统计等 728+ 个函数。
keywords:
  - bpp
  - biren
  - 图像处理
  - 视频处理
  - GPU加速
  - 加速库
  - 壁仞
---

# BPP Command Reference

BPP 是壁仞 GPU 加速图像和视频处理的函数库，面向图像处理领域的专业开发人员。

## Quick Start

```c
#include <bpp.h>

// 初始化
BppStream stream;
BppStreamCreate(&stream);

// 创建图像描述符
BppiImgDescriptor src, dst;
BppiImgDescriptorCreate(&src, width, height, BppiImgFormat::NV12);
BppiImgDescriptorCreate(&dst, width, height, BppiImgFormat::RGB);

// 图像缩放
bppiResize(stream, src, dst, BppiInterpolationMode::NEAREST);

// 同步
BppStreamSynchronize(stream);
```

## Installation

| Type | Path |
|------|------|
| Header | `/usr/local/birensupa/all/latest/brbpp/include/bpp.h`, `bppi.h` 等 |
| Library | `/usr/local/birensupa/all/latest/brbpp/lib/x86_64-linux-gnu/libbpp.so` |

```bash
source /usr/local/birensupa/all/latest/scripts/brsw_set_env.sh
```

## Key Enumerations

### BppBitDepth

| Value | Description |
|-------|-------------|
| `BppBitDepth::8S` | 8 位有符号 |
| `BppBitDepth::8U` | 8 位无符号 |
| `BppBitDepth::16S` | 16 位有符号 |
| `BppBitDepth::16U` | 16 位无符号 |
| `BppBitDepth::32S` | 32 位有符号 |
| `BppBitDepth::32U` | 32 位无符号 |
| `BppBitDepth::BF16` | Brain Float 16 |
| `BppBitDepth::32F` | Float 32 |
| `BppBitDepth::64F` | Float 64 |

### BppiMemType

| Value | Description |
|-------|-------------|
| `BppiMemType::UMA` | 统一内存访问 |
| `BppiMemType::NUMA` | 非统一内存访问 |

### BppiLayoutType

| Value | Description |
|-------|-------------|
| `BppiLayoutType::Activation` | 激活值布局 |
| `BppiLayoutType::Matrix` | 矩阵布局 |
| `BppiLayoutType::PlainBuffer` | 朴素缓冲区 |

### BppiTensorFormat

| Value | Description |
|-------|-------------|
| `BppiTensorFormat::NHW` | NHW |
| `BppiTensorFormat::NHWC` | NHWC |
| `BppiTensorFormat::NCHW` | NCHW |
| `BppiTensorFormat::COL_MAJOR` | 列主序 |
| `BppiTensorFormat::ROW_MAJOR` | 行主序 |

### BppiInterpolationMode

| Value | Description |
|-------|-------------|
| `BppiInterpolationMode::NEAREST` | 最近邻 |
| `BppiInterpolationMode::LINEAR` | 双线性 |
| `BppiInterpolationMode::CUBIC` | 双三次 |
| `BppiInterpolationMode::AREA` | 区域 |

### BppiBorderType

| Value | Description |
|-------|-------------|
| `BppiBorderType::CONSTANT` | 常量 |
| `BppiBorderType::REPLICATE` | 复制 |
| `BppiBorderType::REFLECT` | 反射 |
| `BppiBorderType::REPEAT` | 重复 |
| `BppiBorderType::REFLECT_101` | 反射 101 |

### BppiImgFormat

| Value | Description |
|-------|-------------|
| `BppiImgFormat::GRAY` | 灰度 |
| `BppiImgFormat::RGB` | RGB |
| `BppiImgFormat::BGR` | BGR |
| `BppiImgFormat::RGBA` | RGBA |
| `BppiImgFormat::BGRA` | BGBA |
| `BppiImgFormat::NV12` | NV12 |
| `BppiImgFormat::NV21` | NV21 |
| `BppiImgFormat::YU12` | YU12 |
| `BppiImgFormat::YV12` | YV12 |

## Key Classes

### BppiImgDescriptor

图像信息描述符，包含尺寸、格式、位深等。

### BppiImgBuffer

图像各平面信息：
- 尺寸 (width, height)
- 格式 (format)
- 位深 (bitDepth)
- 数据指针 (plane[0-3])
- stride
- offset

### BppiTensorDescriptor

张量描述信息。

### BppStream

异步并行处理流。

### BppStreamAccessor

BppStream ↔ suStream 转换器。

## API Functions (728+)

### Matrix Transformations

| Function | Description |
|----------|-------------|
| `bppiFindRotationMatrix` | 查找旋转矩阵 |
| `bppiTransform` | 2D 变换 |
| `bppiWarpAffine` | 仿射变换 |
| `bppiWarpPerspective` | 透视变换 |
| `bppiSimilarityMatrix` | 相似度矩阵 |
| `bppiRigidMatrix` | 刚体变换 |

### Image Quality

| Function | Description |
|----------|-------------|
| `bppiImgPSNR` | 峰值信噪比计算 |

### Color Space Conversion

| Function | Description |
|----------|-------------|
| `bppiCvtColor` | 颜色空间转换 |
| `bppiCvtColorEx` | 扩展颜色空间转换 |
| `bppiCvtColorAsync` | 异步颜色空间转换 |

### Fusion Operations

| Function | Description |
|----------|-------------|
| `bppiFusedNv12ToRgb` | NV12→RGB 融合 |
| `bppiFusedCropResize` | 裁剪+缩放融合 |
| `bppiFusedCropResizeMirror` | 裁剪+缩放+镜像融合 |

### Resize

| Function | Description |
|----------|-------------|
| `bppiResize` | 图像缩放 |
| `bppiResizeBatch` | 批量缩放 |

### Crop

| Function | Description |
|----------|-------------|
| `bppiCrop` | 图像裁剪 |
| `bppiCropBatch` | 批量裁剪 |

### Flip

| Function | Description |
|----------|-------------|
| `bppiFlip` | 图像翻转 |

### Pad

| Function | Description |
|----------|-------------|
| `bppiPad` | 边界填充 |

### Rotate

| Function | Description |
|----------|-------------|
| `bppiRotate` | 图像旋转 |

### Histogram

| Function | Description |
|----------|-------------|
| `bppiEqualizeHist` | 直方图均衡化 |

### Filtering

| Function | Description |
|----------|-------------|
| `bppiGaussianBlur` | 高斯滤波 |
| `bppiBilateralFilter` | 双边滤波 |
| `bppiBoxFilter` | 盒式滤波 |
| `bppiFilterMedian` | 中值滤波 |
| `bppiFilterMax` | 最大滤波 |
| `bppiFilterMin` | 最小滤波 |

### Edge Detection

| Function | Description |
|----------|-------------|
| `bppiFilterPrewitt` | Prewitt 边缘检测 |
| `bppiFilterScharr` | Scharr 边缘检测 |
| `bppiFilterRoberts` | Roberts 边缘检测 |
| `bppiFilterSobel` | Sobel 边缘检测 |

### Morphology

| Function | Description |
|----------|-------------|
| `bppiDilate` | 膨胀 |
| `bppiErode` | 腐蚀 |

### Threshold

| Function | Description |
|----------|-------------|
| `bppiThreshold` | 阈值处理 |
| `bppiAdaptiveThreshold` | 自适应阈值 |

### Normalize

| Function | Description |
|----------|-------------|
| `bppiNormalize` | 图像归一化 |

### Arithmetic Operations

| Function | Description |
|----------|-------------|
| `bppiAdd` | 加法 |
| `bppiSub` | 减法 |
| `bppiMul` | 乘法 |
| `bppiDiv` | 除法 |
| `bppiAnd` | 与运算 |
| `bppiOr` | 或运算 |
| `bppiXor` | 异或运算 |
| `bppiAbs` | 绝对值 |
| `bppiSqr` | 平方 |
| `bppiExp` | 指数 |
| `bppiLn` | 对数 |

### Statistics

| Function | Description |
|----------|-------------|
| `bppiMinMaxLoc` | 最值定位 |
| `bppiBoundingRect` | 外接矩形 |
| `bppiHistogramEven` | 直方图 |
| `bppiMean` | 均值 |
| `bppiAverageError` | 平均误差 |

## Example: Resize Image

```c
#include <bpp.h>
#include <stdio.h>

int main() {
    BppStream stream;
    BppStreamCreate(&stream);

    // 创建图像描述符
    BppiImgDescriptor src, dst;
    BppiImgDescriptorCreate(&src, 1920, 1080, BppiImgFormat::NV12);
    BppiImgDescriptorCreate(&dst, 640, 480, BppiImgFormat::NV12);

    // 分配内存
    // ... (分配 src 和 dst 缓冲区)

    // 缩放
    bppiResize(stream, src, dst, BppiInterpolationMode::LINEAR);

    // 同步
    BppStreamSynchronize(stream);

    // 清理
    BppImgDescriptorDestroy(&src);
    BppImgDescriptorDestroy(&dst);
    BppStreamDestroy(&stream);

    return 0;
}
```

## Asynchronous Operations

所有函数均提供同步版本和异步版本（带 `Asyn` 后缀）：

```c
// 同步
bppiResize(stream, src, dst, BppiInterpolationMode::LINEAR);

// 异步
bppiResizeAsyn(stream, src, dst, BppiInterpolationMode::LINEAR);
```

## Return Codes

| Code | Description |
|------|-------------|
| `BPP_SUCCESS` | 成功 |
| `BPP_ERROR_INVALID_PARAMETER` | 无效参数 |
| `BPP_ERROR_INVALID_HANDLE` | 无效句柄 |
| `BPP_ERROR_OUT_OF_MEMORY` | 内存不足 |
| `BPP_ERROR_NOT_SUPPORTED` | 不支持 |

## Notes

- BPP 已包含在 BIRENSUPA SDK 中
- 所有函数支持 BppStream 流式执行
- 需要正确设置环境变量
- 某些操作需要足够的 GPU 内存

## Related Libraries

- **suBLAS**: 基础线性代数
- **suDNN**: 深度学习
- **suFFT**: 快速傅里叶变换
- **suRAND**: 随机数生成