# GPU Vendor ID 列表

本文档列出常用GPU厂商的PCI Vendor ID，用于通过lspci -nn命令精确识别设备。

## 常用GPU厂商

| 厂商 | Vendor ID | Device ID示例 | 备注 |
|------|-----------|---------------|------|
| **NVIDIA** | 0x10de | 多种 | GeForce/Quadro/Tesla系列 |
| **AMD** | 0x1002 | 多种 | Radeon/Instinct系列 |
| **Intel** | 0x8086 | 多种 | 集成显卡/Arc系列 |
| **沐曦 (MetaX)** | 0x1eae | C500/C600等 | 曦云系列GPU |
| **华为 (Huawei)** | 0x19e5 | Ascend系列 | 昇腾AI处理器 |
| **壁仞 (Biren)** | 0x1e9f | BR系列 | 壁仞GPU |
| **摩尔线程** | 0x1e2b | MTT系列 | 摩尔线程GPU |
| **寒武纪 (Cambricon)** | 0x1b22 | MLU系列 | AI加速器 |

## 使用方法

```bash
# 显示带Vendor ID的完整信息
lspci -nn | grep -E "VGA|3D"

# 示例输出：
# 0000:00:02.0 VGA compatible controller [0300]: Intel Corporation [8086:1234]
# 0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation [10de:1b80]

# 格式：[domain:]bus:device.function]
```

## 国产AI芯片详细ID

### 沐曦 (MetaX)

```
0x1eae - MetaX
  C500系列: 0x1eae:0xD001
  C600系列: 0x1eae:0xD002
```

### 华为昇腾 (Ascend)

```
0x19e5 - Huawei
  Ascend 310: 0x19e5:0x0000
  Ascend 910: 0x19e5:0x0002
```

### 壁仞 (Biren)

```
0x1e9f - Biren
  BR100: 0x1e9f:0xD001
  BR104: 0x1e9f:0xD002
```

### 摩尔线程 (Moore Threads)

```
0x1e2b - Moore Threads
  MTT X400: 0x1e2b:0xD001
```

### 寒武纪 (Cambricon)

```
0x1b22 - Cambricon
  MLU270: 0x1b22:0xD001
  MLU290: 0x1b22:0xD002
```

## 快速识别脚本

```bash
#!/bin/bash
# 精确识别GPU厂商（使用Vendor ID）

GPU_INFO=$(lspci -nn 2>/dev/null | grep -E "VGA|3D|Display")

echo "$GPU_INFO" | while read line; do
    # 提取Vendor ID (格式: [XXXX:YYYY])
    if [[ $line =~ \[([0-9a-f]{4}):([0-9a-f]{4})\] ]]; then
        VENDOR_ID="${BASH_REMATCH[1]}"
        DEVICE_ID="${BASH_REMATCH[2]}"

        case "$VENDOR_ID"" in
            "10de") echo "$line -> NVIDIA" ;;
            "1002") echo "$line -> AMD" ;;
            "8086") echo "$line -> Intel" ;;
            "1eae") echo "$line -> MetaX (沐曦)" ;;
            "19e5") echo "$line -> Huawei Ascend (华为昇腾)" ;;
            "1e9f") echo "$line -> Biren (壁仞)" ;;
            "1e2b") echo "$line -> Moore Threads (摩尔线程)" ;;
            "1b22") echo "$line -> Cambricon (寒武纪)" ;;
            *) echo "$line -> Unknown (Vendor: 0x$VENDOR_ID)" ;;
        esac
    else
        echo "$line"
    fi
done
```

## 参考链接

- [PCI IDs 在线查询](https://pci-ids.ucw.cz/)
- [Linux PCI IDs项目](https://github.com/pciutils/pciids)