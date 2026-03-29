---
name: mx-smi
description: 沐曦（Metax）国产GPU芯片专用设备管理 Skill，提供实时监控、健康诊断、驱动信息查询、功耗/温度/利用率查询、多卡拓扑配置等专家级能力，支持 AI Agent 自动运维场景。Muxi mx-smi 是沐曦 C500 系列 GPU 的官方管理工具，类似 NVIDIA nvidia-smi。
keywords:
  - muxi
  - metax
  - mx-smi
  - 沐曦
  - GPU监控
  - 设备管理
  - C500
  - 曦云
---

# mx-smi 沐曦GPU设备管理

## 功能描述

mx-smi 是沐曦（Metax）国产GPU芯片的官方设备管理工具，用于监控和管理沐曦 C500 系列 GPU 设备。本 Skill 提供完整的设备查询、状态监控、拓扑查看、故障诊断等能力，支持 AI 训练和推理场景的自动化运维。

## 核心能力

### 1. 设备基础信息查询

查询当前系统中沐曦 GPU 设备的基本信息。

```bash
# 查看所有 GPU 设备概览
mx-smi

# 查看指定 GPU 设备详细信息
mx-smi -i 0

# 查看所有 GPU 完整信息
mx-smi -a
```

**输出示例：**
```
+------------------------------------------------------------------------------+
| GPU  Id  |     Name     | Mode | Mem Total | Mem Used | Mem Free | Util  |
|==============================================================================|
|   0      | C500X        | N/A  |  64 GB    |  12 GB   |  52 GB   | 15%   |
|   1      | C500X        | N/A  |  64 GB    |  14 GB   |  50 GB   | 18%   |
...
+------------------------------------------------------------------------------+
```

### 2. GPU 状态实时监控

实时监控 GPU 核心指标，包括利用率、显存、温度、功耗等。

```bash
# 实时监控，每秒刷新
mx-smi dmon

# 监控指定 GPU
mx-smi dmon -i 0,1,2,3

# 设置刷新间隔（毫秒）
mx-smi dmon -s 500
```

**关键指标说明：**
| 指标 | 说明 |
|------|------|
| gpu  | GPU 设备编号 |
| sm   | 流多处理器利用率 (%) |
| mem  | 显存利用率 (%) |
| enc  | 编码器利用率 (%) |
| dec  | 解码器利用率 (%) |
| temp | GPU 核心温度 (°C) |
| power | 功耗 (W) |

### 3. 显存使用详情

查看 GPU 显存详细使用情况。

```bash
# 查看显存使用详情
mx-smi memory

# 查看指定 GPU 显存
mx-smi memory -i 0
```

### 4. GPU 拓扑结构查看

查看多 GPU 之间的拓扑连接关系，对于分布式训练至关重要。

```bash
# 查看完整拓扑信息
mx-smi topo

# 查看 MXLK 互联拓扑（沐曦超节点架构）
mx-smi topo --show-mxlk

# 查看 NVLink 类似连接（仅显示 P2P 拓扑）
mx-smi topo --matrix
```

**拓扑类型说明：**
- **MXLK (Metax Link)**：沐曦 GPU 互联技术
- **P2P (Peer-to-Peer)**：GPU 直连通信
- **PIX**：同一 PCIe  switch 内通信
- **PHB**：跨 PCIe 主桥通信
- **SYS**：跨 NUMA 节点通信

### 5. 进程与应用监控

查看哪些进程正在使用 GPU。

```bash
# 查看所有 GPU 进程
mx-smi process

# 查看指定 GPU 进程
mx-smi process -i 0
```

### 6. 性能计数器查询

查看 GPU 性能数据计数器。

```bash
# 查看性能计数器
mx-smi pm

# 查看指定计数器
mx-smi pm -i 0 --query-gpu sm_efficiency
```

### 7. 设备配置与管理

```bash
# 查看 GPU 参数配置
mx-smi q

# 设置 GPU 持久模式（适合多任务场景）
mx-smi -i 0 -pm 1

# 查看驱动版本信息
mx-smi -v

# 查看 CUDA 兼容层信息
mx-smi --query-cuda-version
```

## 常见场景

### 场景1：训练前集群状态检查

大规模 AI 训练前验证所有 GPU 正常可用。

```bash
# 快速检查所有 GPU 状态
mx-smi

# 检查显存是否充足（训练需要足够显存）
mx-smi memory

# 检查 GPU 互联拓扑是否正常
mx-smi topo --show-mxlk
```

**检查清单：**
- [ ] 所有 GPU 显示为 Available 状态
- [ ] 显存充足（建议至少预留 20%）
- [ ] MXLK 互联正常（超节点架构）
- [ ] GPU 间 P2P 带宽正常（≥44GB/s）

### 场景2：推理服务健康监控

生产环境推理服务持续监控。

```bash
# 持续监控 GPU 利用率和显存
mx-smi dmon -s 1000

# 监控特定 GPU
mx-smi dmon -i 0,1,2,3 -s 1000
```

**告警阈值建议：**
| 指标 | 告警阈值 |
|------|----------|
| GPU 利用率 | > 95% 持续 5min |
| 显存使用 | > 90% |
| GPU 温度 | > 85°C |
| GPU 功耗 | > 350W |

### 场景3：故障定位与诊断

GPU 异常时的故障诊断流程。

```bash
# 1. 查看设备状态
mx-smi -a

# 2. 查看错误日志
mx-smi -i 0 --query-gpu error

# 3. 检查进程占用
mx-smi process

# 4. 检查拓扑连接
mx-smi topo --show-mxlk

# 5. 如果需要压力测试验证
mxvs stress
mxvs ops -m fp16
```

### 场景4：多卡训练并行配置验证

验证分布式训练的 GPU 配置是否正确。

```bash
# 验证 8 卡机器的 P2P 互联
mx-smi topo --matrix

# 检查 MXLK 互联状态（超节点架构）
mx-smi topo --show-mxlk

# 确认 NCCL 通信测试通过
# 参考环境变量配置
# MCCL_IB_HCA=mlx5_0,mlx5_1
# MCCL_P2P_LEVEL=LOC
```

## 故障排查

### 问题1：GPU 不可见或未识别

**症状：** `mx-smi` 显示无可用设备

**排查步骤：**
```bash
# 1. 检查驱动加载
lsmod | grep mx

# 2. 检查设备节点
ls -la /dev/dri/
ls -la /dev/mxcd*

# 3. 检查驱动状态
systemctl status metax-driver

# 4. 重新加载驱动
sudo rmmod metax_driver
sudo modprobe metax_driver
```

### 问题2：GPU 利用率异常低

**症状：** 训练/推理性能差，GPU 利用率持续偏低

**排查步骤：**
```bash
# 1. 检查数据加载是否瓶颈
mx-smi dmon  # 观察 mem 利用率

# 2. 检查 CPU 是否瓶颈
htop

# 3. 检查网络通信
# 分布式训练时网络延迟

# 4. 检查 PCIe 拓扑
mx-smi topo
# 确认 PCIe ACS 未启用（影响 P2P 性能）
```

### 问题3：多卡通信异常

**症状：** 分布式训练卡死或通信超时

**排查步骤：**
```bash
# 1. 检查 GPU 拓扑
mx-smi topo --show-mxlk
mx-smi topo --matrix

# 2. 测试 P2P 连通性
# 参考: /opt/maca/tools/mccl/inspector/mx-cci

# 3. 检查 MCCL 环境变量
echo $MCCL_IB_HCA
echo $MCCL_P2P_LEVEL

# 4. 运行 MCCL 测试
bash /opt/maca/tools/mccl/test/cluster.sh
```

### 问题4：显存不足

**症状：** 训练时 OOM 或显存查询显示不足

**排查步骤：**
```bash
# 1. 查看显存使用详情
mx-smi memory -i 0

# 2. 查看占用进程
mx-smi process

# 3. 清理不使用的进程
kill <pid>

# 4. 调整 batch size 或使用梯度累积
```

### 问题5：GPU 温度过高

**症状：** GPU 温度超过 85°C，性能降频

**排查步骤：**
```bash
# 1. 查看温度监控
mx-smi dmon

# 2. 检查散热设备
ipmi_sensor | grep -i temp

# 3. 调整风扇转速
ipmi raw ...

# 4. 降低功耗墙
mx-smi -i 0 -pl 300  # 限制功耗 300W
```

## 相关文档

- [沐曦官方文档](https://www.metax-tech.com/)
- [C500X 产品介绍](https://www.metax-tech.com/product/c500x)
- [曦云系列GPU用户指南](../china-ai-chip-docs/MUXI/972_曦云系列通用GPU用户指南.md)
- [曦云系列GPU驱动安装指南](../china-ai-chip-docs/MUXI/971_曦云系列通用GPU驱动安装指南.md)
- [曦云系列GPU快速上手指南](../china-ai-chip-docs/MUXI/970_曦云系列通用GPU快速上手指南.md)

## 环境变量参考

| 变量 | 说明 |
|------|------|
| `MACA_GRAPH_LAUNCH_MODE=5` | 图启动模式优化 |
| `MACA_SMALL_PAGESIZE_ENABLE=1` | 小页面优化 |
| `MACA_DIRECT_DISPATCH=1` | 直接调度 |
| `MCCL_IB_HCA` | MCCL 计算网卡 |
| `MCCL_P2P_LEVEL` | P2P 通信层级 |

## 配套工具

| 工具 | 用途 |
|------|------|
| `mxvs` | 沐曦 GPU 算力测试工具 |
| `mx-smi` | GPU 设备管理 |
| `mccl` | 沐曦 NCCL 通信库 |
| `mctrace` | 性能分析工具 |
| `mx-cci` | 集群检查工具 |