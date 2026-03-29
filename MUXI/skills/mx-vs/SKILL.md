---
name: mx-vs
description: 沐曦（Metax）GPU 算力测试与压力测试工具 Skill，提供 GPU 算力基准测试、stress 压力测试、性能验证等能力，用于验证沐曦 C500 系列 GPU 硬件健康状态和计算性能是否符合出厂标准，是集群部署验收和故障诊断的必备工具。
keywords:
  - muxi
  - metax
  - mxvs
  - 算力测试
  - 压力测试
  - GPU性能
  - C500
---

# mx-vs 沐曦GPU算力测试工具

## 功能描述

muxi-vs（简称 mxvs）是沐曦官方提供的 GPU 算力测试与压力测试工具，用于验证 C500 系列 GPU 的计算性能、显存带宽和硬件稳定性。支持 FP16/BF16/FP32 等多种精度的算力测试，以及持续压力测试，是集群部署验收和故障诊断的必备工具。

## 核心能力

### 1. GPU 算力基准测试

测试 GPU 的实际算力性能，验证是否达到规格要求。

```bash
# FP16 算力测试（最常用）
mxvs ops -m fp16

# BF16 算力测试
mxvs ops -m bf16

# FP32 算力测试
mxvs ops -m fp32

# 测试所有精度
mxvs ops -m all

# 测试指定 GPU
mxvs ops -i 0 -m fp16
mxvs ops -i 0,1,2,3 -m fp16

# 持续测试模式（用于稳定性验证）
mxvs ops -m fp16 -l 100
```

**C500X 算力规格参考：**
| 精度 | 理论算力 | 验收阈值 |
|------|----------|----------|
| FP16 | ≥239 TFLOPS | ≥230 TFLOPS |
| BF16 | ≥239 TFLOPS | ≥230 TFLOPS |
| FP32 | ≥60 TFLOPS | ≥55 TFLOPS |

**输出示例：**
```
[INFO] Testing GPU 0 FP16 ...
[INFO] GPU 0: FP16 Peak Performance = 241.5 TFLOPS
[INFO] GPU 1: FP16 Peak Performance = 240.8 TFLOPS
...
[SUCCESS] All GPUs passed the performance test
```

### 2. GPU 压力测试

对 GPU 进行持续高负载测试，验证硬件稳定性。

```bash
# 默认压力测试（无参数）
mxvs stress

# 指定测试精度
mxvs stress -m fp16
mxvs stress -m bf16

# 指定 GPU 列表
mxvs stress -i 0,1,2,3

# 指定运行时间（秒）
mxvs stress -t 300

# 指定测试次数
mxvs stress -n 1000

# 显存测试模式
mxvs stress -v

# 组合参数：8卡 FP16 压力测试 10 分钟
mxvs stress -i 0,1,2,3,4,5,6,7 -m fp16 -t 600
```

**压力测试参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-m, --mode` | 测试精度 (fp16/bf16/fp32/all) | fp16 |
| `-i, --id` | GPU ID 列表 | 所有 GPU |
| `-t, --time` | 运行时间（秒） | 60 |
| `-n, --num` | 迭代次数 | - |
| `-v, --vmmode` | 显存压力测试模式 | false |

### 3. 显存带宽测试

```bash
# 显存带宽测试
mxvs bw

# 指定 GPU
mxvs bw -i 0
```

### 4. 算子性能测试

```bash
# 测试 GEMM 算子
mxvs gemm

# 测试卷积算子
mxvs conv

# 测试 Attention 算子
mxvs attention
```

### 5. 多卡联合测试

```bash
# 多卡并行算力测试
mxvs ops -i 0,1,2,3,4,5,6,7 -m fp16

# 多卡压力测试
mxvs stress -i 0,1,2,3,4,5,6,7 -t 300
```

## 常见场景

### 场景1：集群部署验收

新机器上架或集群部署完成后，进行算力验收测试。

```bash
# 1. 单卡算力测试
for i in {0..7}; do
  mxvs ops -i $i -m fp16
done

# 2. 全量 8 卡算力测试
mxvs ops -i 0,1,2,3,4,5,6,7 -m fp16

# 3. 压力测试验证稳定性
mxvs stress -i 0,1,2,3,4,5,6,7 -t 600 -m fp16

# 4. 验收标准：所有 GPU FP16 算力 ≥ 230 TFLOPS
```

**验收检查清单：**
- [ ] 单卡 FP16 算力 ≥ 230 TFLOPS
- [ ] 8 卡算力平均值 ≥ 230 TFLOPS
- [ ] 压力测试 10 分钟无错误
- [ ] 温度控制在 85°C 以下

### 场景2：故障 GPU 定位

GPU 异常时快速定位故障卡。

```bash
# 逐卡测试定位问题
mxvs ops -i 0 -m fp16
mxvs ops -i 1 -m fp16
mxvs ops -i 2 -m fp16
# ...

# 或并行测试所有卡
mxvs ops -i 0,1,2,3,4,5,6,7 -m fp16
```

### 场景3：性能对比基线

建立性能基线，用于后续性能回归分析。

```bash
# 记录基线数据
mxvs ops -m all -o baseline_$(date +%Y%m%d).json

# 对比当前与基线
mxvs ops -m all --compare baseline_20240101.json
```

### 场景4：驱动/固件升级验证

驱动或固件升级后验证性能无损。

```bash
# 升级前测试
mxvs ops -m fp16 -o before_upgrade.json

# 升级驱动/固件
sudo apt update && sudo apt upgrade metax-driver

# 重启后测试
mxvs ops -m fp16 -o after_upgrade.json

# 对比结果
mxvs ops -m fp16 --compare before_upgrade.json
```

## 故障排查

### 问题1：算力测试结果偏低

**症状：** FP16 算力低于 230 TFLOPS

**排查步骤：**
```bash
# 1. 检查 GPU 状态
mx-smi

# 2. 检查温度（过热会降频）
mx-smi dmon

# 3. 检查功耗墙设置
mx-smi -i 0 --query-gpu power_limit

# 4. 检查 PCIe 带宽
mx-smi topo --matrix

# 5. 如果温度过高，降低环境温度或检查散热
```

### 问题2：压力测试失败

**症状：** stress 测试报错或卡死

**排查步骤：**
```bash
# 1. 检查显存是否正常
mx-smi memory -i 0

# 2. 检查驱动日志
dmesg | grep -i metax

# 3. 降低压力测试强度重试
mxvs stress -i 0 -m fp16 -t 30

# 4. 尝试单卡测试
mxvs stress -i 0 -m fp16
```

### 问题3：多卡测试性能不均

**症状：** 部分 GPU 性能明显偏低

**排查步骤：**
```bash
# 1. 检查拓扑
mx-smi topo --matrix

# 2. 检查 MXLK 连接
mx-smi topo --show-mxlk

# 3. 测试单卡性能
for i in 0 1 2 3 4 5 6 7; do
  mxvs ops -i $i -m fp16
done

# 4. 检查 PCIe 拓扑是否一致
```

### 问题4：GPU 掉卡

**症状：** 测试过程中 GPU 消失

**排查步骤：**
```bash
# 1. 检查驱动状态
systemctl status metax-driver

# 2. 检查硬件健康
mxvs stress -v -i 0

# 3. 检查 dmesg 日志
dmesg | tail -100

# 4. 检查电源供应
ipmi sensor | grep -i psu
```

## 环境变量参考

| 变量 | 说明 |
|------|------|
| `MACA_GRAPH_LAUNCH_MODE=5` | 图启动模式优化，提升算力 |
| `MACA_DIRECT_DISPATCH=1` | 直接调度，减少延迟 |

## 相关文档

- [曦云系列GPU用户指南](../china-ai-chip-docs/MUXI/972_曦云系列通用GPU用户指南.md)
- [曦云系列GPU快速上手指南](../china-ai-chip-docs/MUXI/970_曦云系列通用GPU快速上手指南.md)
- [mx-smi](./mx-smi/) - GPU 设备管理工具

## 配套工具

| 工具 | 用途 |
|------|------|
| `mx-smi` | GPU 设备状态监控 |
| `mxvs` | 算力测试与压力测试 |
| `mctrace` | 性能分析trace工具 |