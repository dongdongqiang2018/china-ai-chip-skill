# mx-smi 故障排查指南

## 常见问题与解决方案

### 1. 设备不可用 (Not Available)

**问题**：设备状态显示为 not available

**排查步骤**：
```bash
# 1. 查看不可用原因
mx-smi --show-unavailable-reason

# 2. 查看严重事件
mx-smi misc --show-critical-event

# 3. 检查驱动是否加载
lsmod | grep metax

# 4. 检查PCIe状态
mx-smi --show-pcie
```

**常见原因**：
- 驱动未正确加载
- PCIe链接失败
- 固件异常

### 2. 温度过高

**问题**：GPU温度超过阈值

**排查步骤**：
```bash
# 1. 查看当前温度
mx-smi --show-temperature

# 2. 查看温度历史（如有）
# 3. 检查散热系统
```

**解决方案**：
- 检查机箱风扇
- 清理散热器灰尘
- 降低环境温度

### 3. Warm Reset失败

**问题**：执行Warm Reset失败

**排查步骤**：
```bash
# 1. 确认无进程占用
mx-smi --show-all-process
mx-smi --show-process

# 2. 查看设备状态
mx-smi -L
```

**注意事项**：
- Warm Reset仅在H3C UniServer R5300G6验证过
- 需要root权限
- 对MetaXLink连接的卡只需做一次Reset

### 4. 显存不足

**问题**：显存使用率100%或显示不足

**原因**：
- 驱动与固件会预留约1GB显存
- 进程占用过多显存

**排查**：
```bash
# 查看显存使用
mx-smi --show-memory

# 查看进程
mx-smi --show-process
```

### 5. PCIe带宽异常

**问题**：PCIe带宽低于预期

**排查**：
```bash
# 1. 查看实时带宽
mx-smi --show-pcie-bandwidth

# 2. 查看PCIe配置
mx-smi --show-pcie
```

### 6. 虚拟化启用失败

**问题**：sGPU或VM虚拟化无法启用

**检查**：
```bash
# sGPU - 检查是否支持
mx-smi --show-hwinfo | grep -i virtual

# VM - 需要物理机环境
# 虚拟化模式不支持sGPU
```

### 7. MetaXLink连接异常

**问题**：多GPU通信失败

**排查**：
```bash
# 1. 查看连接状态
mx-smi mxlk --show-state

# 2. 查看带宽
mx-smi mxlk --show

# 3. 重置连接
mx-smi mxlk --set-state 0  # 禁用
mx-smi mxlk --set-state 1  # 启用
```

### 8. ECC错误

**问题**：ECC错误计数增加

**查看**：
```bash
# 查看ECC状态
mx-smi misc --show-ecc-state

# 查看ECC计数
mx-smi --count-ecc
```

**注意**：计数重启后清零，坏页计数不清零

### 9. 固件升级失败

**问题**：VBIOS升级失败

**检查**：
- 权限（需要root）
- 固件文件路径
- BAR空间是否足够

### 10. 性能降频

**问题**：GPU自动降频

**查看原因**：
```bash
mx-smi --show-clk-tr
```

**状态说明**：
- Active：该项为降频原因
- Not Active：当前未降频

---

## 诊断命令汇总

```bash
# 完整系统诊断
mx-smi -L                          # 设备列表
mx-smi --show-version              # 版本信息
mx-smi --show-temperature          # 温度
mx-smi --show-board-power          # 功耗
mx-smi --show-usage                # 使用率
mx-smi --show-memory               # 显存
mx-smi --show-process              # 进程
mx-smi --show-pcie                 # PCIe
mx-smi --show-event all            # 事件
mx-smi --count-ecc                 # ECC
mx-smi topo -m                     # 拓扑
```