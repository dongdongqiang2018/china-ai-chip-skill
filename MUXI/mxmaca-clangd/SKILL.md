---
name: mxmaca-clangd
description: 沐曦C语言服务工具，提供C/C++代码补全、语法检查、跳转定义等功能。用于IDE集成开发。
keywords:
  - 沐曦
  - clangd
  - 语言服务
  - 代码补全
  - IDE
---

# MXMACA Clangd 用户指南

MXMACA Clangd是C/C++语言服务工具，基于Clang提供代码补全、语法检查、跳转定义等功能。

## 快速开始

### 安装

Clangd随MXMACA SDK默认安装，位于 `$MACA_PATH/bin/clangd`。

### 配置VSCode

```json
// .vscode/settings.json
{
  "clangd.arguments": [
    "--background-index",
    "--compile-commands-dir=${workspaceFolder}",
    "--clang-tidy",
    "--header-insertion=iwyu"
  ],
  "clangd.path": "/opt/maca/bin/clangd"
}
```

## 功能

### 代码补全

- 变量名补全
- 函数名补全
- 宏展开补全
- 代码片段

### 语法检查

- 编译错误检测
- 警告提示
- 静态分析

### 代码导航

- 跳转定义
- 查找引用
- 查找继承关系

### 重构

- 重命名
- 提取函数
- 内联

## 配置

### 编译命令数据库

```bash
# 生成compile_commands.json
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ..
# 或
make compile_commands.json
```

### 配置文件

```yaml
# .clangd
CompileFlags:
  Add:
    - "--maca"
    - "--arch=sm_80"
  Remove:
    - "-W*"
Diagnostics:
  ClangTidy:
    Add:
      - modernize-*
      - performance-*
```

## IDE集成

### VSCode

安装 `clangd` 扩展，配置上述设置。

### JetBrains

配置Clangd作为C/C++语言服务器。

### Vim/Neovim

```vim
" vimrc
let g:clangd#server.startup_options = '--maca --background-index'
```

## 命令行

```bash
# 检查语法
clangd --check=<file>

# 查看版本
clangd --version

# 列出功能
clangd --list-features
```

## 官方参考

- 《曦云系列通用GPU MXMACA Clangd用户手册》