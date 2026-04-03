# mxvs 命令参考

## 完整命令列表

### 设备命令

| 命令 | 说明 |
|------|------|
| `mxvs devices` | 显示所有设备信息 |
| `mxvs dashboard` | 动态监控GPU状态 |

---

### PCIe命令

| 命令 | 说明 |
|------|------|
| `mxvs pcie bandwidth --devices <ID>` | PCIe实时带宽 |
| `mxvs pcie bandwidth --devices <ID> --continuous` | 持续监控 |
| `mxvs pcie benchmark unidirection --src-devices <S> --dst-devices <D>` | 单向带宽测试 |
| `mxvs pcie benchmark bidirection --devices <ID1>,<ID2>` | 双向带宽测试 |
| `mxvs eye --devices <ID> --phys <P> --lanes <L>` | PCIe眼图测试 |

### PCIe参数

| 参数 | 说明 |
|------|------|
| `-d, --devices` | 设备ID |
| `-s, --data-sizes` | 数据大小（KB/MB/GB） |
| `--cpu-affinity` | CPU亲和度 |
| `--bref` | 仅显示结果 |
| `--json` | JSON输出 |
| `--pre-malloc` | 预分配显存 |
| `-i, --iteration` | 迭代次数 |
| `--parallel` | 并行执行 |
| `--monitor-log` | 监控日志 |
| `--no-check` | 关闭数据校验 |
| `--detail` | 详细结果 |

---

### 显存命令

| 命令 | 说明 |
|------|------|
| `mxvs memory bandwidth --devices <ID>` | 显存实时带宽 |
| `mxvs memory benchmark --devices <ID>` | 显存带宽测试 |

### 显存参数

| 参数 | 说明 |
|------|------|
| `--kernel-copy` | 读写模式 |
| `-s, --data-sizes` | 数据大小 |

---

### MetaXLink命令

| 命令 | 说明 |
|------|------|
| `mxvs metaxlink bandwidth --devices <ID>` | MetaXLink实时带宽 |
| `mxvs metaxlink benchmark --devices <ID>` | MetaXLink带宽测试 |
| `mxvs eye --metaxlink --metaxlink-ports <P> --devices <ID> --lanes <L>` | 眼图测试 |

### MetaXLink参数

| 参数 | 说明 |
|------|------|
| `--mode` | 模式（ingress/egress） |

---

### P2P命令

| 命令 | 说明 |
|------|------|
| `mxvs p2p --src-devices <S> --dst-devices <D>` | P2P带宽测试 |

---

### 压力测试命令

| 命令 | 说明 |
|------|------|
| `mxvs stress --xcore --xcore-devices <ID>` | XCore压力测试 |
| `mxvs stress --metaxlink` | MetaXLink压力测试 |
| `mxvs stress --eth` | ETH压力测试 |

### 压力测试参数

| 参数 | 说明 |
|------|------|
| `--duration` | 持续时间（秒） |
| `--iterations` | 迭代次数 |

---

### ETH命令

| 命令 | 说明 |
|------|------|
| `mxvs eye --eth --devices <ID> --lanes <L>` | ETH眼图测试 |

---

### 光模块命令

| 命令 | 说明 |
|------|------|
| `mxvs om client --src-devices <S> --dst-devices <D>` | 光模块客户端 |
| `mxvs om server` | 光模块服务端 |

### 光模块参数

| 参数 | 说明 |
|------|------|
| `--dst-addr` | 目标地址 |
| `-P, --mxvs-port` | 端口（默认9601） |

---

## 设备ID指定方式

| 方式 | 示例 | 说明 |
|------|------|------|
| 单个设备 | `0` | 设备0 |
| 多个设备 | `0,1,2` | 设备0,1,2 |
| 范围 | `0-3` | 设备0,1,2,3 |
| 混合 | `0-2,4,6` | 设备0,1,2,4,6 |
| 全部 | `all` | 所有设备 |

---

## 数据大小格式

```bash
--data-sizes 1KB
--data-sizes 1MB
--data-sizes 1GB
--data-sizes 1KB,1MB,1GB  # 多值
```

---

## 输出格式

### JSON输出
```bash
--json result.json
```

### CSV输出
```bash
--json result.csv  # mx-smi命令
```