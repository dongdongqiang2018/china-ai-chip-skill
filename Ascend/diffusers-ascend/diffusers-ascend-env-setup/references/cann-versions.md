# CANN 环境变量配置

本文档指导检查和配置 CANN 环境变量。

> **注意**：本文档仅涵盖环境变量配置，不包含 CANN 安装教程。

## 环境变量检查

运行以下命令检查 CANN 环境变量是否已设置：

```bash
echo "ASCEND_HOME_PATH: $ASCEND_HOME_PATH"
echo "ASCEND_TOOLKIT_HOME: $ASCEND_TOOLKIT_HOME"
echo "ASCEND_OPP_PATH: $ASCEND_OPP_PATH"
echo "ASCEND_AICPU_PATH: $ASCEND_AICPU_PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
echo "PYTHONPATH: $PYTHONPATH"
```

**正常输出**：所有变量应显示具体路径，而非空值。

## 配置环境变量

### 情况 1：CANN 安装在默认路径

默认路径为 `/usr/local/Ascend/`，运行以下命令：

```bash
# CANN 8.5+
source /usr/local/Ascend/cann/set_env.sh

# CANN 8.5 之前
source /usr/local/Ascend/ascend-toolkit/set_env.sh
```

### 情况 2：CANN 安装在自定义路径

如果 CANN 安装在其他位置，直接 source 对应的 `set_env.sh`：

```bash
# 替换为实际的 set_env.sh 路径
source /your/custom/path/to/cann/set_env.sh
```

### 永久配置

将 CANN 的 `set_env.sh` 添加到 `~/.bashrc`：

```bash
# 编辑 ~/.bashrc，添加以下内容（选择对应路径）

# CANN 8.5+
source /usr/local/Ascend/cann/set_env.sh

# 或 CANN 8.5 之前
# source /usr/local/Ascend/ascend-toolkit/set_env.sh

# 或自定义路径
# source /your/custom/path/to/cann/set_env.sh
```

然后执行：

```bash
source ~/.bashrc
```

## 环境变量说明

| 环境变量 | 说明 |
|----------|------|
| `ASCEND_HOME_PATH` | CANN 安装根目录 |
| `ASCEND_TOOLKIT_HOME` | CANN 工具包目录 |
| `ASCEND_OPP_PATH` | 算子库路径 |
| `ASCEND_AICPU_PATH` | AI CPU 运行时路径 |
| `LD_LIBRARY_PATH` | 动态库搜索路径 |
| `PYTHONPATH` | Python 模块搜索路径 |

## 常见问题

### 环境变量未设置

**症状**：`echo $ASCEND_HOME_PATH` 输出为空

**解决**：
1. 确认 CANN 安装位置
2. 执行 `source /path/to/cann/set_env.sh`
3. 如需永久生效，添加到 `~/.bashrc`

### CANN 路径不确定

**症状**：不知道 CANN 安装在哪里

**解决**：

```bash
# 查找 CANN 安装位置
find / -name "set_env.sh" -path "*/Ascend/*" 2>/dev/null

# 常见安装位置
ls -la /usr/local/Ascend/
ls -la /opt/Ascend/
ls -la ~/Ascend/
```

### Python 无法导入 CANN 模块

**症状**：`ModuleNotFoundError: No module named 'acl'`

**解决**：

```bash
# 检查 PYTHONPATH
echo $PYTHONPATH

# 手动添加
export PYTHONPATH=${ASCEND_HOME_PATH}/python/site-packages:${PYTHONPATH}
```

## 参考文档

- [华为昇腾官方文档](https://www.hiascend.com/document)
- [CANN 环境变量说明](https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/envdeployment/instg/instg_0045.html)
