# China AI Chip Skills

国产AI芯片FAE辅助Skills集合，帮助FAE工程师快速掌握各类国产AI芯片的使用方法。

## 项目简介

本项目收集和整理了国产AI芯片厂商的技术文档和使用指南，以Skills的形式组织，方便快速查询和使用。

## 目录结构

```
china-ai-chip-skill/
├── README.md                      # 本文档
├── fae-skill-generator/          # FAE Skill生成指南
├── device-detector/              # GPU设备识别
├── MUXI/                         # 沐曦(MetaX) Skills
│   ├── mx-smi/                   # GPU管理工具
│   ├── mxvs/                     # 验收测试套件
│   └── mccl-test/                # 集合通信库
├── Ascend/                       # 华为昇腾Skills (Forked)
└── BIREN/                        # 壁仞科技Skills (待添加)
```

## Skills说明

### 设备识别

- **[device-detector](./device-detector/)**: 使用lspci命令识别当前系统的GPU厂商类型

### 技能生成

- **[fae-skill-generator](./fae-skill-generator/)**: 从技术文档生成FAE Skills的指南

### 沐曦 (MetaX)

- **[mx-smi](./MUXI/mx-smi/)**: GPU状态查询、功耗管理、固件升级等
- **[mxvs](./MUXI/mxvs/)**: 硬件验收测试、PCIe/显存带宽测试、眼图测试
- **[mccl-test](./MUXI/mccl-test/)**: 集合通信库编程指南

### 华为昇腾 (Ascend) ⚡

> **本目录内容Fork自 [ascend-ai-coding/awesome-ascend-skills](https://github.com/ascend-ai-coding/awesome-ascend-skills)**

- **[Ascend Skills](./Ascend/)**: 昇腾AI处理器Skills集合

包含的主要Skills：

| 目录 | 说明 |
|------|------|
| `npu-smi` | NPU设备管理工具 |
| `atc-model-converter` | ATC离线模型转换 |
| `ascendc` | Ascend C编程 |
| `hccl-test` | 集合通信测试 |
| `mindspeed-llm` | 大模型训练框架 |
| `torch_npu` | PyTorch NPU后端 |
| `vllm-ascend` | vLLM推理框架 |
| `ai-for-science` | AI for Science模型适配 |

### 壁仞科技 (Biren)

- **[BIREN占位符](./BIREN/)**: 壁仞Skills待添加

## 快速开始

### 1. 识别当前设备GPU类型

```bash
# 查看所有GPU设备
lspci | grep -E "VGA|3D|Display"

# 快速识别国产芯片
lspci | grep -i meta    # 沐曦
lspci | grep -i ascend  # 华为昇腾
lspci | grep -i biren   # 壁仞
```

### 2. 根据识别的厂商选择对应Skills

- 沐曦(MetaX) GPU → 参考 `./MUXI/` 目录
- 华为昇腾(Ascend) GPU → 参考 `./Ascend/` 目录
- 壁仞(Biren) GPU → 参考 `./BIREN/` 目录

## 使用方法

### 本地使用

```bash
# 克隆项目
git clone https://github.com/<your-repo>/china-ai-chip-skill.git
cd china-ai-chip-skill

# 查看特定Skill
cat MUXI/mx-smi/SKILL.md

# 或使用Claude Code的Skill功能
```

### Claude Code集成

将Skills目录配置到Claude Code中，可通过自然语言调用：

```
"帮我查看沐曦GPU的温度"
"如何使用mxvs进行PCIe带宽测试"
"配置MCCL的环境变量"
```

## 贡献指南

欢迎贡献新的Skills！

### 添加新Skill步骤

1. 使用 `fae-skill-generator` 创建Skill结构
2. 确保包含完整的 `SKILL.md` 文件
3. 添加相关的参考资料到 `references/` 目录
4. 提交PR到主仓库

### Skill格式要求

- 必须包含 `SKILL.md` 文件
- Frontmatter必须包含 `name` 和 `description`
- `description` 至少20个字符
- 建议包含 `keywords` 字段便于搜索

## 许可证

MIT License

## 更新日志

- 2025-04: 初始版本
  - 添加device-detector技能
  - 添加沐曦(MUXI)三个基础Skills
  - 添加Ascend Skills（Fork自 ascend-ai-coding/awesome-ascend-skills）
  - 创建BIREN占位目录