# mx-smi 命令参考

## 完整命令参数表

### 通用选项

| 命令 | 说明 |
|------|------|
| `mx-smi` | 默认显示GPU主要信息（功耗、内存、温度、版本等） |
| `mx-smi -L` | 列出所有GPU设备 |
| `mx-smi -L -j` | JSON格式列出设备 |
| `mx-smi -h` | 显示帮助 |
| `mx-smi -v` | 显示版本 |
| `mx-smi -i <ID>` | 指定设备 |
| `mx-smi -l <ms>` | 轮询间隔 |
| `mx-smi -o <file>` | 输出到CSV |

### 查询选项

| 命令 | 说明 |
|------|------|
| `--show-temperature` | 温度 |
| `--show-version` | BIOS/驱动/Firmware版本 |
| `--show-hbm-bandwidth` | 显存带宽 |
| `--show-pcie-bandwidth` | PCIe带宽 |
| `--show-usage` | GPU/VPU使用率 |
| `--show-memory` | 显存使用 |
| `--show-board-power` | 板卡功耗 |
| `--show-pmbus-power` | 芯片功耗 |
| `--show-eeprom` | EEPROM信息 |
| `--show-clock` | 时钟信息 |
| `--show-clocks all` | 所有时钟 |
| `--show-dpm cur` | 当前性能等级 |
| `--show-dpm all` | 所有性能等级 |
| `--show-dpm-max` | 最高性能等级 |
| `--show-pcie` | PCIe信息 |
| `--show-sn` | 序列号 |
| `--show-process` | 进程信息 |
| `--show-power-mode` | 电源模式 |
| `--show-persistence-mode` | 持久模式 |
| `--show-event <type>` | PCIe事件 |
| `--show-clk-tr` | 降频原因 |
| `--show-unavailable-reason` | 不可用原因 |
| `--show-hwinfo` | 硬件信息 |
| `--show-sysinfo` | 系统信息 |
| `--count-ecc` | ECC错误计数 |

### 控制选项

| 命令 | 说明 |
|------|------|
| `-u, --vbios-upgrade <file>` | VBIOS升级 |
| `-r, --reset` | Warm Reset |
| `--set-power-mode <0|1>` | 电源模式 |
| `--set-persistence-mode <0|1>` | 持久模式 |
| `--set-dpm-max <IP,Level>` | 最大性能等级 |

### 子命令

| 子命令 | 说明 |
|--------|------|
| `mx-smi topo -m` | 拓扑矩阵 |
| `mx-smi topo -d` | 拓扑距离 |
| `mx-smi topo -t` | 拓扑树 |
| `mx-smi topo -n` | 网卡拓扑 |
| `mx-smi vm --enable-vf <N>` | 开启VF |
| `mx-smi vm --disable-vf` | 关闭VF |
| `mx-smi vm --show-vf` | 显示VF |
| `mx-smi mxlk --show` | MetaXLink带宽 |
| `mx-smi mxlk --show-state` | 连接状态 |
| `mx-smi mxlk --set-state <0|1>` | 启用/禁用 |
| `mx-smi ras --show-count` | RAS计数 |
| `mx-smi ras --show-status` | RAS状态 |
| `mx-smi dmon` | 轮询监控 |
| `mx-smi misc --show-critical-event` | 严重事件 |
| `mx-smi eth --show-bandwidth` | ETH带宽(C600) |

### sGPU子命令

| 命令 | 说明 |
|------|------|
| `mx-smi sgpu --enable` | 启用sGPU |
| `mx-smi sgpu --disable` | 禁用sGPU |
| `mx-smi sgpu --show-mode` | 显示模式 |
| `mx-smi sgpu --create` | 创建子设备 |
| `mx-smi sgpu` | 查看所有子设备 |
| `mx-smi sgpu --set <ID>` | 修改子设备 |
| `mx-smi sgpu --remove <ID>` | 移除子设备 |
| `mx-smi sgpu --set-sched-class` | 设置调度策略 |
| `mx-smi sgpu --set-timeslice` | 设置时间片 |
| `mx-smi sgpu --show-usage` | 查看使用率 |
| `mx-smi sgpu --show-memory` | 查看显存 |
| `mx-smi sgpu --show-remain` | 剩余额度 |