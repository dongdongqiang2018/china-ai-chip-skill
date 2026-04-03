---
name: mx-exporter
description: 沐曦GPU监控指标导出工具，用于Kubernetes集群环境中收集曦云GPU设备指标数据，支持Prometheus拉取。是集群监控部署的必备工具。
keywords:
  - 沐曦
  - GPU监控
  - mx-exporter
  - Prometheus
  - Kubernetes
  - 指标导出
  - 云原生监控
---

# mx-exporter 使用指南

mx-exporter是用于在集群环境中收集曦云®GPU设备指标数据的工具。Prometheus等集群监控系统可以通过HTTP从运行于每个节点的mx-exporter拉取设备指标数据。

## 快速开始

### Wheel包安装（主机部署）

```bash
# 1. 安装依赖
pip3 install prometheus_client grpcio protobuf

# 2. 安装mx-exporter（MXMACA SDK安装后）
sudo pip3 install /opt/maca/wheel/mx_exporter_*.whl

# 3. 启动mx-exporter
sudo mx-exporter -p 8000
```

### Docker镜像部署

```bash
# 1. 加载镜像
cd mx-exporter
./mxexporter-images.x.x.x.run --load

# 2. 启动容器
docker run -d \
  --device=/dev/dri \
  --device=/dev/mxgvm \
  -v /var/log:/host/var/log \
  -v /var/lib/kubelet/pod-resources:/var/lib/kubelet/pod-resources \
  --name=mx-exporter \
  -p 0.0.0.0:8000:8000 \
  mx-exporter:latest
```

### 查看指标数据

```bash
# 通过HTTP获取指标
curl http://localhost:8000/metrics

# 或浏览器访问
http://<host_ip>:8000/metrics
```

## 启动参数

### Wheel包参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -p, --port | HTTP端口号 | 8000 |
| -i, --interval | 指标收集间隔(毫秒) | 10000ms |
| -c, --config-file | 指标配置文件 | /opt/maca/etc/default-counters.csv |

### Docker部署参数

| 参数 | 说明 |
|------|------|
| -p, --port | 容器端口号 |
| -i, --interval | 收集间隔，需与Prometheus拉取周期一致 |
| -c, --config-file | 自定义指标配置文件 |
| -mp, --mount-point | 容器挂载路径 |
| -kp, --kubelet-path | kubelet路径，默认/var/lib/kubelet/pod-resources |
| -kd, --k8s-domains | GPU域名，默认metax-tech |

### Docker启动参数

| 参数 | 说明 |
|------|------|
| -d | 后台运行容器 |
| --device=/dev/dri | 挂载GPU设备 |
| --device=/dev/mxgvm | 挂载虚拟化设备（VF指标） |
| -v /var/log:/host/var/log | 挂载日志目录 |
| -v /var/lib/kubelet/pod-resources | 挂载K8s资源目录 |

## 常用命令示例

### Wheel包启动示例

```bash
# 使用自定义配置文件启动
sudo mx-exporter -c /home/user/counters.csv

# 指定端口和收集间隔
sudo mx-exporter -p 8002 -i 5000
```

### Docker启动示例

```bash
# 基础启动
docker run -d \
  --device=/dev/dri \
  --name=mx-exporter \
  -p 8000:8000 \
  mx-exporter:latest

# 完整参数启动
docker run -d \
  --device=/dev/dri \
  --device=/dev/mxgvm \
  -v /var/log:/host/var/log \
  -v /var/lib/kubelet/pod-resources:/var/lib/kubelet/pod-resources \
  --name=mx-exporter \
  -p 0.0.0.0:8000:8000 \
  -e INTERVAL=10000 \
  mx-exporter:latest
```

### 使用启动脚本

```bash
# 修改启动脚本配置
vim mx-exporter/start_mxexporter.sh

# 执行启动
./start_mxexporter.sh
```

## 指标配置

### 默认配置文件

配置文件位于：`/opt/maca/etc/default-counters.csv`

### 自定义指标集

1. 基于默认配置文件修改
2. 可启用/禁用特定指标
3. 可修改指标名称、描述和标签

```csv
# 示例：启用sGPU指标
# 去掉指标前#注释即可启用
mx_sgpu_memory_used
mx_sgpu_memory_total
```

## 常见指标说明

### 温度相关
| 指标名 | 说明 |
|--------|------|
| mx_chip_hotspot_temp | 芯片热点温度 |
| mx_chip_temperature | 芯片温度 |
| mx_board_temperature | 板卡温度 |

### 功耗相关
| 指标名 | 说明 |
|--------|------|
| mx_board_power | 板卡功耗 |
| mx_power_limit | 功耗限制 |

### 内存相关
| 指标名 | 说明 |
|--------|------|
| mx_memory_used | 已用显存 |
| mx_memory_total | 总显存 |
| mx_memory_free | 空闲显存 |

### 利用率相关
| 指标名 | 说明 |
|--------|------|
| mx_gpu_util | GPU利用率 |
| mx_memory_util | 显存利用率 |

### 标签说明

| 标签 | 说明 |
|------|------|
| deviceId | GPU设备ID |
| uuid | GPU唯一标识 |
| modelName | 型号名称 |
| Hostname | 主机名 |
| driver_version | 驱动版本 |
| bios_version | BIOS版本 |

## Prometheus集成

### 配置Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'mx-exporter'
    static_configs:
      - targets: ['localhost:8000']
```

### 指标输出格式

```prometheus
#HELP mx_chip_hotspot_temp Chip hotspot temperature
#TYPE mx_chip_hotspot_temp gauge
mx_chip_hotspot_temp{Hostname="xx",bios_version="1.16.0.0",deviceId="0",driver_version="2.6.0",modelName="MXC500",uuid="xx"} 35.75
```

## sGPU监控配置

1. 修改配置文件启用sGPU指标
2. 执行sGPU切分（参考mx-smi手册）
3. 启动mx-exporter

```bash
# 启用sGPU指标
sed -i 's/^#mx_sgpu/mx_sgpu/' /opt/maca/etc/default-counters.csv

# 启动监控
sudo mx-exporter
```

## 注意事项

1. 需使用sudo启动（默认监控kernel日志）
2. 容器部署需要挂载GPU设备(/dev/dri)
3. 收集间隔需与Prometheus拉取周期一致
4. 虚拟化场景需同时挂载/dev/mxgvm

## 官方参考

- 《曦云系列通用GPU mx-exporter Kubernetes集群监控部署手册》
- 《曦云系列通用GPU mx-smi使用手册》
- MXMACA SDK (>=2.25.2)