---
name: biren-video-sdk
description: BIREN Video SDK 视频编解码参考指南。提供基于壁仞通用 GPU 的视频编解码硬件加速功能，支持 H.264/H.265/JPEG/MPEG2 解码和编码，支持 VAAPI 标准流程和壁仞 HLA 高层 API，用于视频处理应用开发。
keywords:
  - video-sdk
  - biren
  - 视频编解码
  - 编码器
  - 解码器
  - VAAPI
  - 壁仞
---

# Video SDK Command Reference

壁仞 Video SDK 提供基于壁仞通用 GPU 的视频编解码硬件加速功能。

## Quick Start

### VAAPI Standard

```bash
# 解码
ffmpeg -hwaccel vaapi -i test.h264 out.yuv

# 编码（H.265）
ffmpeg -hwaccel vaapi -s 1920x1080 -pix_fmt nv12 -i out.yuv \
  -c:v hevc_vaapi -b:v 500k -vf 'format=nv12,hwupload' \
  -g 30 -bf 0 -refs 1 -vsync drop out.h265 -y
```

### HLA API

```c
bevc_dec_get_capability(device_id, &caps);
bevc_dec_create(device_id, &dec, &attr);
bevc_dec_decode(dec, packet, &frame);
```

## Supported Codecs

### Decoding

- HEVC main10 profile
- Progressive H.264 & SVC base layer & MVC
- JPEG
- MPEG2

### Encoding

- HEVC (H.265)
- H.264
- JPEG

## Decoding Capability (BR106)

| Format | Max Resolution | Max Channels (1080p@30) |
|--------|----------------|------------------------|
| MJPEG/JPEG | 16384×16384 | 200 |
| AVC (H.264) | 4096×2160 | 200 |
| HEVC (H.265) | 4096×2160 | 200 |
| MPEG2 | 1920×1080 | 64 |

## Encoding Capability (BR106)

| Format | Max Resolution | Max Channels (1080p@30) |
|--------|----------------|------------------------|
| MJPEG/JPEG | 16384×16384 | 20 |
| AVC (H.264) | 4096×2160 | 20 |
| HEVC (H.265) | 4096×2160 | 20 |

## Environment Setup

```bash
# Ubuntu
export LIBVA_DRIVER_NAME=bevc
export LIBVA_DRIVERS_PATH="/usr/local/birensupa/sdk/latest/bevc/lib/dri/"
export LD_LIBRARY_PATH="/usr/local/birensupa/sdk/latest/bevc/lib/"

# CentOS / Kylin OS
export LIBVA_DRIVERS_PATH="/usr/local/birensupa/sdk/latest/bevc/lib64/dri/"
export LD_LIBRARY_PATH="/usr/local/birensupa/sdk/latest/bevc/lib64/"
```

## Optimization Tools

### br_decode (Multi-thread Decoding)

```bash
br_decode -c 16 -loop 100 -i ./test.h264 -o ./
```

| Parameter | Description |
|-----------|-------------|
| `-c` | 并发路数 |
| `-loop` | 循环次数 |
| `-i` | 输入文件 |
| `-o` | 输出目录 |

### br_encode (Encoding)

```bash
br_encode -c 1 -loop 1 -i ./test_1920x1080.yuv -w 1920 -h 1080 \
  -rc_mode CBR -r 30 -b 3000000 -g 30 -enc_fmt h265 -o ./
```

| Parameter | Description |
|-----------|-------------|
| `-c` | 并发路数 |
| `-loop` | 循环次数 |
| `-i` | 输入文件 |
| `-w/-h` | 宽度/高度 |
| `-rc_mode` | 码率控制 (CBR/VBR/CQP) |
| `-r` | 帧率 |
| `-b` | 码率 |
| `-g` | GOP 大小 |
| `-enc_fmt` | 编码格式 (h265/h264) |

### br_transcode (Transcoding)

```bash
br_transcode -c 1 -loop 1 -i ./test.h264 -enc_fmt h265 \
  -rc_mode CBR -b 3000000 -r 50 -g 30 -o /tmp
```

## VAAPI Standard Flow

```
vaInitialize → vaQueryConfigEntrypoints → vaGetConfigAttributes 
→ vaCreateConfig → vaCreateSurfaces → vaCreateContext 
→ vaCreateBuffer → vaBeginPicture/vaRenderPicture/vaEndPicture 
→ vaSyncSurface
```

## HLA API Flow

```
bevc_dec_get_capability() → bevc_dec_create() 
→ bevc_dec_decode()/bevc_dec_get_frame()/bevc_dec_release_frame() 
→ bevc_dec_destroy()
```

## Supported Formats

### Pixel Formats

| Format | Description |
|--------|-------------|
| BEVC_FMT_YUV420SP | NV12 |
| BEVC_FMT_YUV420P | I420 |
| BEVC_FMT_YUV420SP_10BIT | P010 |
| BEVC_FMT_YUV420P_10BIT | I010 |
| BEVC_FMT_YUV420SP_12BIT | P012 |
| BEVC_FMT_YUV420P_12BIT | I012 |
| BEVC_FMT_RGB | RGB24 |
| BEVC_FMT_BGR | BGR24 |
| BEVC_FMT_ARGB | ARGB32 |
| BEVC_FMT_ABGR | ABGR32 |

### Chroma Sampling

| Format | Description |
|--------|-------------|
| BEVC_YUV400 | 只有 Y 分量 |
| BEVC_YUV420 | 4:2:0 |
| BEVC_YUV422 | 4:2:2 |
| BEVC_YUV444 | 4:4:4 |

## Notes

- 需要安装 BIRENSUPA SDK
- FFmpeg 4.1+ 版本支持
- 硬件加速需要正确的驱动配置

## Related Tools

- **bevc_decoder**: 视频解码器
- **bevc_encoder**: 视频编码器
- **FFmpeg**: 主流多媒体框架