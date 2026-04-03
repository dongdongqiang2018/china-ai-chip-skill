---
name: mcpy
description: 沐曦Python绑定库，提供Python接口访问MXMACA功能。支持Python环境快速部署和GPU编程。
keywords:
  - 沐曦
  - Python
  - mcpy
  - Python绑定
  - GPU编程
---

# mcPy 使用指南

mcPy提供Python接口访问MXMACA功能。

## 快速开始

### 安装

```bash
pip install mcpy
# 或
pip install /opt/maca/wheel/mcpy-*.whl
```

### 验证安装

```python
import mcpy
print(mcpy.get_device_count())
```

## 设备管理

```python
import mcpy

# 获取设备数量
print(mcpy.get_device_count())

# 获取设备属性
prop = mcpy.get_device_properties(0)
print(prop.name, prop.total_memory)

# 设置当前设备
mcpy.set_device(0)
```

## 内存管理

```python
import mcpy

# 分配设备内存
d_ptr = mcpy.device_alloc(size)

# 分配主机内存
h_ptr = mcpy.host_alloc(size)

# 分配统一内存
um_ptr = mcpy.managed_alloc(size)

# 内存拷贝
mcpy.memcpy(dst, src, size, mcpy.MEMCPY_D2H)
```

## 数组接口

```python
import mcpy

# 创建设备数组
arr = mcpy.array(shape=(1024, 1024), dtype='float32')

# 从主机传输
import numpy as np
data = np.zeros((1024, 1024), dtype='float32')
arr = mcpy.asarray(data)

# 转回numpy
result = arr.to_numpy()
```

## 官方参考

- 《曦云系列通用GPU mcPy使用手册》