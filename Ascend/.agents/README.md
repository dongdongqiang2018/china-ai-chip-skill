# .agents 目录

本目录用于存放项目相关的 AI Agent Skills 和辅助文件。

## 目录结构

```
.agents/
├── README.md           # 本文件
└── skills/             # 本地 Skills 目录
    └── skill-creator/  # Skill 创建指南（复用 OpenCode 内置 Skill）
```

## 用途说明

推荐将实用的 Skills 和相关文件放在此目录下：

- **本地开发 Skills**: 项目特定的 Skill 可以放在 `skills/` 子目录
- **复用已有 Skills**: 可以从 `~/.config/opencode/skills/` 复制通用 Skills
- **项目专属配置**: Agent 相关的配置文件可以放在此目录

## Skills 使用

### OpenCode / Claude Code

Skills 会自动从以下位置加载：
1. `~/.config/opencode/skills/` - 全局 Skills
2. `.agents/skills/` - 项目本地 Skills（如有）

### 添加新 Skill

1. 从已有 Skills 复制到 `.agents/skills/`
2. 或按照 `skill-creator` 指南创建新 Skill

## 参考

- [Awesome Ascend Skills](../README.md) - 华为昇腾 NPU Skills 仓库
- [skill-creator](./skills/skill-creator/SKILL.md) - Skill 创建指南
- [create-pr](./skills/create-pr/SKILL.md) - 创建 PR 指南
