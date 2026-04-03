---
name: mceid
description: 沐曦设备标识管理工具，用于管理GPU设备的电子ID（EID），支持设备发现、标识查询和绑定配置。
keywords:
  - 沐曦
  - EID
  - mceid
  - 设备标识
  - 设备管理
---

# EID 设备管理指南

EID（Electronic ID）是曦云GPU的电子标识，用于设备管理和识别。

## 快速开始

### 查看EID

```bash
# 查看所有设备EID
mx-smi --show-eid

# 查看指定设备
mx-smi --id=0 --show-eid
```

### 查询设备

```bash
# 通过EID查询设备
mceid --find=<EID>

# 列出所有EID
mceid --list
```

## 功能

### 设备绑定

```bash
# 绑定EID到应用
mceid --bind=<EID> --app=<app_id>

# 解绑
mceid --unbind=<EID>
```

### 设备发现

```bash
# 扫描新设备
mceid --scan

# 刷新设备列表
mceid --refresh
```

## 配置

### 配置文件

```json
{
  "eid_mappings": {
    "0": "EID-2024-001",
    "1": "EID-2024-002"
  }
}
```

## 官方参考

- 《曦云系列通用GPU EID手册》