---
name: fae-skill-generator
description: 从技术文档生成FAE辅助Skills的指南，包含文档处理、Skill结构规划、内容提取和编写规范。用于批量创建领域专用的FAE技能。
keywords:
  - FAE
  - Skill
  - 技术文档
  - 自动化
  - 文档处理
  - 工具指南
---

# FAE Skill 生成指南

本指南用于从技术文档（如PDF手册、API文档等）批量生成FAE辅助Skills。

## 流程概览

```
1. 文档处理 → 2. 内容提取 → 3. 结构规划 → 4. Skill编写 → 5. 验证测试
```

---

## Step 1: 文档处理

### 1.1 提取PDF内容

使用 `pdfplumber` 提取PDF文本和表格：

```python
import pdfplumber

def extract_pdf_content(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            tables = page.extract_tables()
```

### 1.2 生成Markdown

将提取的内容转换为Markdown格式，保留：
- 标题层级 (`#`, `##`, `###`)
- 表格结构
- 代码块
- 列表

### 1.3 搜索关键信息

```bash
# 使用grep搜索
grep -n "命令" output.md
grep -n "参数" output.md
grep -n "示例" output.md
```

---

## Step 2: 内容分析

### 2.1 识别Skill边界

分析文档确定Skill的：
- **核心功能**：工具的主要用途
- **使用场景**：何时使用这个工具
- **目标用户**：FAE还是开发人员
- **依赖项**：需要哪些前置工具

### 2.2 提取关键内容

| 内容类型 | 来源 | 处理方式 |
|----------|------|----------|
| 命令语法 | 文档中的命令表格 | 提取为命令参考 |
| 参数说明 | 参数表格 | 整理为参数表 |
| 示例代码 | 代码块 | 保留原始格式 |
| 故障排查 | 常见问题章节 | 整理为FAQ |
| 环境变量 | 变量说明表格 | 分类整理 |

---

## Step 3: 结构规划

### 3.1 Skill目录结构

```
skill-name/
├── SKILL.md              # 必需：核心内容
├── references/           # 可选：详细参考
│   ├── commands.md       # 命令参考
│   ├── api.md            # API参考
│   └── troubleshooting.md # 故障排查
├── scripts/              # 可选：脚本
└── assets/               # 可选：资源
```

### 3.2 SKILL.md 结构

```yaml
---
name: skill-name
description: 清晰的描述，至少20字符
keywords:
  - 关键词1
  - 关键词2
---

# 标题

## 快速开始
简短示例...

## 内容章节
详细说明...

## 官方参考
- [链接](url)
```

---

## Step 4: Skill编写规范

### 4.1 Frontmatter规则

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 必须与目录名完全一致 |
| `description` | 是 | 至少20字符，含使用场景 |
| `keywords` | 否 | 用于搜索匹配 |

### 4.2 内容规范

- **渐进式披露**：核心内容放SKILL.md，详细内容放references/
- **代码块**：始终指定语言
- **表格**：用于结构化数据
- **链接**：内部链接使用相对路径

### 4.3 命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 目录名 | 小写+连字符 | `mx-smi` |
| Skill名 | 匹配目录名 | `name: mx-smi` |
| 脚本 | kebab-case.sh | `check-env.sh` |
| 参考文档 | 小写+连字符.md | `commands.md` |

---

## Step 5: 典型Skill模板

### 5.1 工具类Skill模板

```yaml
---
name: tool-name
description: 工具描述，说明何时使用
keywords:
  - 关键词
---

# 工具名称

## 快速开始

### 安装/环境
```bash
# 安装命令
```

### 常用命令
```bash
# 基础用法
tool --help
```

## 命令详解

### 查询类
...

### 控制类
...

## 故障排查

### 问题1
解决...

## 官方参考
- [文档](链接)
```

### 5.2 编程类Skill模板

```yaml
---
name: lib-name
description: 库/框架的使用指南
keywords:
  - 关键词
---

# 库名称

## 快速开始

### 安装
```bash
pip install lib-name
```

### 基础示例
```python
import lib
# 示例代码
```

## API参考

### 主要API
...

## 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| VAR | 作用 | 值 |

## 常见问题
...
```

---

## 示例：从沐曦文档创建Skill

### 示例1: mx-smi Skill

**来源文档**: `曦云系列_通用GPU_mx-smi使用手册_CN_V13.pdf`

**分析**:
- 功能：GPU状态查询、功耗管理
- 使用场景：FAE日常运维
- 关键内容：命令、参数、故障排查

**创建**:
```
mx-smi/
├── SKILL.md              # 核心内容
├── references/
│   ├── commands.md       # 命令参数表
│   └── troubleshooting.md # 故障排查
└── scripts/
```

### 示例2: mccl-test Skill

**来源文档**: `曦云系列_通用GPU_MCCL编程指南_CN_V06.pdf` + mccl.sh脚本

**分析**:
- 功能：集合通信编程 + 性能测试
- 使用场景：分布式训练、MCCL开发
- 关键内容：API、环境变量、测试脚本

**创建**:
```
mccl-test/
├── SKILL.md
├── references/
│   ├── api.md            # API参考
│   ├── mccl-sh.md        # 测试脚本详解
│   └── troubleshooting.md
└── scripts/
```

---

## 最佳实践

### 1. 内容精简
- SKILL.md 核心内容不超过500行
- 详细内容放 references/

### 2. 示例驱动
- 每个主要功能提供实际可运行的示例
- 包含完整命令参数

### 3. 故障排查优先
- 整理常见问题和解决方案
- 提供诊断命令汇总

### 4. 链接完整
- 官方文档链接
- 相关Skill交叉引用

### 5. 关键词优化
- keywords包含中英文关键词
- 便于搜索和匹配

---

## 验证清单

创建完成后检查：
- [ ] SKILL.md 存在且格式正确
- [ ] name与目录名一致
- [ ] description至少20字符
- [ ] 快速开始示例可运行
- [ ] 命令参数完整
- [ ] 故障排查内容实用
- [ ] 官方参考链接有效

---

## 相关资源

- [Claude Code Skill规范](./规范)
- [PDF处理工具](./pdf-tool)
- [输出示例](./output.md)