---
name: mxoob
description: 沐曦带外管理工具，通过BMC/IPMI接口远程管理曦云GPU设备，包括开关机、固件更新、状态监控等。
keywords:
  - 沐曦
  - 带外管理
  - mxoob
  - IPMI
  - BMC
  - 远程管理
---

# 带外管理指南

曦云GPU带外管理（OOB）配置和使用。

## 快速开始

### 连接BMC

```bash
# 通过IPMI连接
ipmitool -I lanplus -H <BMC_IP> -U admin -P password chassis status

# 通过Redfish
curl -k https://<BMC_IP>/redfish/v1/Chassis/1
```

## IPMI操作

### 电源管理

```bash
# 查看电源状态
ipmitool -I lanplus -H <BMC_IP> -U admin -P password chassis power status

# 开机
ipmitool -I lanplus -H <BMC_IP> -U admin -P password chassis power on

# 关机
ipmitool -I lanplus -H <BMC_IP> -U admin -P password chassis power off

# 重置
ipmitool -I lanplus -H <BMC_IP> -U admin -P password chassis power reset
```

### 传感器

```bash
# 查看传感器
ipmitool -I lanplus -H <BMC_IP> -U admin -P password sensor list

# 查看温度
ipmitool -I lanplus -H <BMC_IP> -U admin -P password sensor get "GPU Temp"

# 查看功耗
ipmitool -I lanplus -H <BMC_IP> -U admin -P password sensor get "GPU Power"
```

### SEL日志

```bash
# 查看日志
ipmitool -I lanplus -H <BMC_IP> -U admin -P password sel list

# 清空日志
ipmitool -I lanplus -H <BMC_IP> -U admin -P password sel clear
```

## Redfish操作

### 系统信息

```bash
# 获取系统信息
curl -k -u admin:password https://<BMC_IP>/redfish/v1/Systems/1

# 获取GPU信息
curl -k -u admin:password https://<BMC_IP>/redfish/v1/Systems/1/GraphicsCards/1
```

### 电源操作

```bash
# 重启
curl -k -u admin:password \
    -X POST https://<BMC_IP>/redfish/v1/Systems/1/Actions/ComputerSystem.Reset \
    -H "Content-Type: application/json" \
    -d '{"ResetType": "ForceRestart"}'
```

## 固件更新

### 更新BMC固件

```bash
# 通过IPMI
ipmitool -I lanplus -H <BMC_IP> -U admin -P password \
    firmware update /path/to/bmc.bin

# 通过Redfish
curl -k -u admin:password \
    -X POST https://<BMC_IP>/redfish/v1/Managers/1/Actions/Manager.Update \
    -H "Content-Type: application/json" \
    -d '{"ImageURI": "http://server/firmware.bin"}'
```

## 监控脚本

### 监控GPU状态

```bash
#!/bin/bash
BMC_IP=$1
USER=admin
PASS=password

while true; do
    TEMP=$(ipmitool -I lanplus -H $BMC_IP -U $USER -P $PASS sensor get "GPU Temp" | grep "Sensor Reading" | awk '{print $4}')
    POWER=$(ipmitool -I lanplus -H $BMC_IP -U $USER -P $PASS sensor get "GPU Power" | grep "Sensor Reading" | awk '{print $4}')
    echo "GPU Temp: $TEMP, Power: $POWER"
    sleep 60
done
```

## 官方参考

- 《曦云系列通用GPU带外管理手册》