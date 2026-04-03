# BIREN Skills 技能集合

本目录包含壁仞（BIREN）科技 GPU 相关的 FAE（现场应用工程师）技能，用于支持壁仞通用 GPU 的开发、部署和运维工作。

## 概述

BIREN Skills 基于壁仞官方技术文档（V1.6.0）创建，涵盖了从环境安装、编程开发、加速库使用、推理部署到性能分析的完整软件栈。

## 技能分类

### 1. GPU 管理与监控 (4 个)
| Skill | 描述 |
|--------|------|
| [biren-brsmi](./biren-brsmi) | BRsmi 命令行 GPU 管理工具，查询设备状态、温度、功耗、显存等 |
| [biren-brml](./biren-brml) | BRML C 语言管理库，编程方式管理 GPU |
| [biren-sudcgm](./biren-sudcgm) | suDCGM 数据中心 GPU 管理器，C/S 架构监控 |
| [biren-suvs](./biren-suvs) | suVS GPU 验证测试套件，硬件检测和压力测试 |

### 2. 安装与部署 (3 个)
| Skill | 描述 |
|--------|------|
| [biren-driver](./biren-driver) | BIRENSUPA Driver 驱动安装（KMD/UMD/bev） |
| [biren-sdk](./biren-sdk) | BIRENSUPA SDK 完整开发工具链安装 |
| [biren-container-toolkit](./biren-container-toolkit) | 容器工具包，Docker 中使用壁仞 GPU |

### 3. 编译器与开发工具 (4 个)
| Skill | 描述 |
|--------|------|
| [biren-brcc](./biren-brcc) | BRCC 编译器，基于 Clang/LLVM 的 SUPA 编译工具链 |
| [biren-brsimulator](./biren-brsimulator) | brSimulator 仿真器，无硬件运行程序 |
| [biren-sudebugger](./biren-sudebugger) | suDebugger 调试器，基于 LLDB 的 GPU 调试 |
| [biren-susanitizer](./biren-susanitizer) | suSanitizer 检查工具，内存/同步/竞争检测 |

### 4. 加速库 (5 个)
| Skill | 描述 |
|--------|------|
| [biren-bpp](./biren-bpp) | BPP 图像处理库，728+ 个图像处理函数 |
| [biren-sublas](./biren-sublas) | suBLAS 基础线性代数库，GEMM 优化 |
| [biren-sudnn](./biren-sudnn) | suDNN 深度学习算子库，42+ 种算子 |
| [biren-sufft](./biren-sufft) | suFFT 快速傅里叶变换库 |
| [biren-surand](./biren-surand) | suRAND 随机数生成库 |

### 5. 推理框架 (3 个)
| Skill | 描述 |
|--------|------|
| [biren-suinfer](./biren-suinfer) | suInfer 深度学习推理引擎 |
| [biren-brvllm](./biren-brvllm) | brvllm 大模型推理服务（基于 vLLM） |
| [biren-suinfer-server](./biren-suinfer-server) | suInfer Server 部署（Triton-based） |

### 6. 性能分析 (3 个)
| Skill | 描述 |
|--------|------|
| [biren-suprof](./biren-suprof) | suProfiler 性能分析工具 |
| [biren-supti](./biren-supti) | suPTI 性能追踪接口 |
| [biren-superfviz](./biren-superfviz) | suPerfViz 可视化分析工具 |

### 7. 多媒体 (1 个)
| Skill | 描述 |
|--------|------|
| [biren-video-sdk](./biren-video-sdk) | Video SDK 视频编解码硬件加速 |

## 快速开始

### 查看 GPU 状态

```bash
brsmi
brsmi gpu list
brsmi gpu dmon -s p,u,c
```

### 编译 SUPA 程序

```bash
brcc -x supa source.su -o output
```

### 运行推理

```bash
# 方式一：使用 suInfer
./suinfer_demo model.onnx

# 方式二：使用 brvllm
br_api_server --config config.json --port 8000
```

### 性能分析

```bash
suprof --process-filter=python --collect-counter=hbmc python train.py
doctor_perf -i suprof_spc_counter-xxxx.raw -o output.db
drperfviz_srv -d output.db -p 8087
```

## 依赖关系

```
BIRENSUPA Driver
    ↓
BIRENSUPA SDK (包含以下组件)
    ├── BRCC (编译器)
    ├── SUPA (运行时)
    ├── 加速库 (BPP/suBLAS/suDNN/suFFT/suRAND)
    └── 工具 (suProfiler/suVS/suDebugger/suSanitizer)
    ↓
应用层 (suInfer/brvllm/suInfer Server)
```

## 版本信息

- 文档版本：V1.6.0
- 发布日期：2024-11
- 参考硬件：壁砺™106B/106C

## 官方文档

- BIRENSUPA 官方文档
- 壁仞产品服务部门

## 目录结构

```
BIREN/
├── SKILL.md                    # 技能索引
├── biren-brsmi/                # GPU 管理
├── biren-brml/
├── biren-sudcgm/
├── biren-suvs/
├── biren-driver/                # 驱动安装
├── biren-sdk/                   # SDK 安装
├── biren-container-toolkit/     # 容器支持
├── biren-brcc/                  # 编译器
├── biren-brsimulator/          # 仿真器
├── biren-sudebugger/           # 调试器
├── biren-susanitizer/          # 检查工具
├── biren-bpp/                   # 加速库
├── biren-sublas/
├── biren-sudnn/
├── biren-sufft/
├── biren-surand/
├── biren-suinfer/               # 推理框架
├── biren-brvllm/
├── biren-suinfer-server/
├── biren-suprof/                # 性能分析
├── biren-supti/
├── biren-superfviz/
└── biren-video-sdk/             # 多媒体
```

## 创建说明

这些 Skills 基于 `fae-skill-generator` 技能指南创建，参考了 Ascend 目录中现有 skills 的格式规范。每个 SKILL.md 包含：

- Frontmatter (name, description, keywords)
- 快速开始示例
- 核心 API/命令参考
- 使用示例
- 注意事项

---

*本技能集合基于壁仞官方文档整理，仅供 FAE 技能支持使用。*