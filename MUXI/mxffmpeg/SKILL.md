---
name: mxffmpeg
description: 沐曦FFmpeg编解码工具，支持GPU加速的视频编解码，用于视频处理、 transcoding、流媒体等场景。
keywords:
  - 沐曦
  - FFmpeg
  - mxffmpeg
  - 视频编解码
  - GPU加速
  - transcoding
---

# FFmpeg GPU编解码指南

沐曦FFmpeg GPU加速视频编解码配置。

## 快速开始

### 安装

```bash
# 使用沐曦版本
pip install metax-ffmpeg
# 或下载预编译版本
```

### 基本用法

```bash
# 查看版本
ffmpeg -version | grep MetaX

# GPU解码
ffmpeg -c:v mxvideocodec -i input.mp4 -c:v copy output.mp4

# GPU编码
ffmpeg -i input.mp4 -c:v mxvideocodec -b:v 5M output.mp4
```

## 硬件加速

### 解码器

| 名称 | 说明 |
|------|------|
| mxvideocodec | 沐曦视频解码器 |
| h264_mf | H.264解码 |
| hevc_mf | H.265/HEVC解码 |

### 编码器

| 名称 | 说明 |
|------|------|
| mxvideocodec | 沐曦视频编码器 |
| h264_mx | H.264编码 |
| hevc_mx | H.265/HEVC编码 |

## 常用命令

### 视频转码

```bash
# H.264 GPU编码
ffmpeg -i input.mp4 -c:v h264_mx -preset fast -b:v 5M output.mp4

# H.265 GPU编码
ffmpeg -i input.mp4 -c:v hevc_mx -preset fast -b:v 3M output.mp4
```

### 视频截图

```bash
# GPU解码截图
ffmpeg -i input.mp4 -vframes 1 -c:v mxvideocodec screenshot.jpg
```

### 视频裁剪

```bash
# GPU加速裁剪
ffmpeg -i input.mp4 -c:v mxvideocodec -ss 00:01:00 -t 00:01:00 -c:v copy output.mp4
```

### 滤镜

```bash
# GPU缩放
ffmpeg -i input.mp4 -vf "hwupload,scale=1920:1080,hwdownload" output.mp4
```

## 官方参考

- 《曦云系列通用GPU FFmpeg命令行使用手册》