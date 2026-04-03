# Diffusers 环境故障排查

本文档汇总了在昇腾 NPU 上配置 Diffusers 环境时的常见问题及其解决方案。

---

## 1. CANN 未找到错误

### 症状

运行环境检查或导入 torch_npu 时出现以下错误：

```
Error: CANN not found at /usr/local/Ascend/cann
Error: CANN not found at /usr/local/Ascend/ascend-toolkit
```

或在 Python 中：

```python
import torch_npu
# RuntimeError: Ascend environment not found
```

### 诊断命令

```bash
# 检查 CANN 安装路径
ls -la /usr/local/Ascend/

# 检查具体目录
ls -la /usr/local/Ascend/cann 2>/dev/null || echo "CANN 8.5+ 路径不存在"
ls -la /usr/local/Ascend/ascend-toolkit 2>/dev/null || echo "CANN 旧版路径不存在"

# 查看已安装的 CANN 版本
find /usr/local/Ascend -name "set_env.sh" 2>/dev/null
```

### 解决方案

**情况一：CANN 已安装但路径不同**

```bash
# 查找实际的 CANN 安装位置
sudo find / -name "set_env.sh" -path "*/Ascend/*" 2>/dev/null

# 然后 source 找到的路径
source /actual/path/to/set_env.sh
```

**情况二：CANN 未安装**

需先安装 CANN Toolkit，参考[官方安装指南](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/80RC2alpha001/envdeployment/instg/instg_0019.html)。

**情况三：使用自定义安装路径**

```bash
# 设置自定义 CANN 路径
export ASCEND_HOME_PATH=/your/custom/path
export ASCEND_OPP_PATH=/your/custom/path/opp
source $ASCEND_HOME_PATH/set_env.sh
```

---

## 2. torch_npu 导入失败

### 症状

```python
import torch_npu
# ImportError: cannot import name 'torch_npu' from 'torch_npu'
# 或
# ImportError: libascendcl.so: cannot open shared object file
# 或
# OSError: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.29' not found
```

### 诊断命令

```bash
# 检查 torch_npu 安装
pip list | grep torch-npu

# 检查 PyTorch 版本
python -c "import torch; print(torch.__version__)"

# 检查 CANN 库文件
ls $ASCEND_HOME_PATH/lib64/libascendcl.so 2>/dev/null || echo "CANN 库文件未找到"

# 检查 GCC 版本
strings /lib64/libstdc++.so.6 | grep GLIBCXX
```

### 解决方案

**版本不匹配**

```bash
# 卸载现有版本
pip uninstall torch-npu torch -y

# 重新安装配套版本
pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
pip install torch-npu==2.7.1
```

**缺少 CANN 库文件**

```bash
# 确认已 source CANN 环境
source /usr/local/Ascend/cann/set_env.sh

# 检查 LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH | grep Ascend

# 手动添加库路径（如需要）
export LD_LIBRARY_PATH=$ASCEND_HOME_PATH/lib64:$LD_LIBRARY_PATH
```

**GCC 版本过低**

```bash
# 检查系统 GCC 版本
gcc --version

# 升级 GCC 或使用 conda 环境的 GCC
conda install -c conda-forge gcc_linux-64
```

---

## 3. NPU 不可见

### 症状

```python
import torch
import torch_npu

print(torch.npu.is_available())  # False
print(torch.npu.device_count())  # 0
```

### 诊断命令

```bash
# 检查 NPU 设备
npu-smi info

# 检查驱动状态
cat /var/log/npu/slog/host-0/*.log 2>/dev/null | tail -20

# 检查设备文件权限
ls -la /dev/davinci*

# 检查内核模块
lsmod | grep drv

# 检查用户组
groups
```

### 解决方案

**驱动未加载**

```bash
# 加载驱动模块
modprobe drv

# 重启驱动服务
npu-smi info  # 如失败，尝试重启
```

**未 source CANN 环境**

```bash
# 激活 CANN 环境
source /usr/local/Ascend/cann/set_env.sh

# 验证环境变量
echo $ASCEND_HOME_PATH
echo $ASCEND_RUNTIME_PATH
```

**设备权限问题**

```bash
# 将用户添加到 HwHiAiUser 组
sudo usermod -a -G HwHiAiUser $USER

# 或修改设备权限（临时）
sudo chmod 666 /dev/davinci*

# 重新登录使组变更生效
```

**硬件未识别**

```bash
# 检查 PCIe 设备
lspci | grep Huawei

# 如未显示，检查物理连接或联系硬件管理员
```

---

## 4. numpy 版本冲突

### 症状

```
RuntimeError: module compiled against API version 0x10 but this version of numpy is 0xe
ValueError: numpy.ndarray size changed, may indicate binary incompatibility
AttributeError: module 'numpy' has no attribute 'object'
```

### 诊断命令

```bash
# 检查 numpy 版本
python -c "import numpy; print(numpy.__version__)"

# 检查依赖 numpy 的包
pip show torch torch-npu diffusers | grep -i numpy

# 检查 numpy ABI 版本
python -c "import numpy; print(numpy.core.multiarray._ARRAY_API)"
```

### 解决方案

**降级 numpy**

```bash
# 卸载现有 numpy
pip uninstall numpy -y

# 安装兼容版本（必须 < 2.0）
pip install "numpy<2.0"

# 验证版本
python -c "import numpy; print(numpy.__version__)"
```

**重新编译依赖包**

```bash
# 如果降级后仍有冲突，重新安装依赖包
pip uninstall torch torch-npu -y
pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
pip install torch-npu==2.7.1
pip install "numpy<2.0" --force-reinstall
```

**锁定 numpy 版本**

```bash
# 在 requirements.txt 中指定
numpy==1.26.4

# 或使用 conda
conda install numpy=1.26
```

---

## 5. 权限错误

### 症状

```
PermissionError: [Errno 13] Permission denied: '/dev/davinci0'
RuntimeError: Initialize acl failed, ret = 507899
OSError: [Errno 13] Permission denied: '/var/log/npu'
```

### 诊断命令

```bash
# 检查设备权限
ls -la /dev/davinci*
ls -la /dev/hisi_hdc

# 检查用户组
groups $USER
id $USER

# 检查日志目录权限
ls -ld /var/log/npu

# 检查进程权限
ps aux | grep $(whoami) | grep python
```

### 解决方案

**添加到 HwHiAiUser 组**

```bash
# 添加用户到组
sudo usermod -a -G HwHiAiUser $USER

# 检查是否添加成功
grep HwHiAiUser /etc/group

# 重新登录生效
exit  # 重新 SSH 登录
```

**临时修改权限（仅测试用）**

```bash
# 修改设备权限
sudo chmod 666 /dev/davinci*
sudo chmod 666 /dev/hisi_hdc

# 创建日志目录并授权
sudo mkdir -p /var/log/npu/slog
sudo chmod 755 /var/log/npu
sudo chown -R $USER:$USER /var/log/npu
```

**使用 root 运行（不推荐长期）**

```bash
sudo -E python your_script.py
```

---

## 6. 环境变量问题

### 症状

```python
import torch_npu
# RuntimeError: ASCEND_HOME_PATH is not set
# 或
# RuntimeError: Initialize op failed
```

或在脚本中：

```
ERROR: Cannot find op implementation for ...
```

### 诊断命令

```bash
# 检查关键环境变量
echo "ASCEND_HOME_PATH: $ASCEND_HOME_PATH"
echo "ASCEND_OPP_PATH: $ASCEND_OPP_PATH"
echo "ASCEND_AICPU_PATH: $ASCEND_AICPU_PATH"
echo "PYTHONPATH: $PYTHONPATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

# 检查环境变量来源
env | grep -i ascend

# 查看 set_env.sh 内容
cat $ASCEND_HOME_PATH/set_env.sh 2>/dev/null || echo "set_env.sh 未找到"
```

### 解决方案

**正确 source CANN 环境**

```bash
# CANN 8.5+
source /usr/local/Ascend/cann/set_env.sh

# CANN 8.5 之前
source /usr/local/Ascend/ascend-toolkit/set_env.sh

# 自动检测版本
if [ -d "/usr/local/Ascend/cann" ]; then
    source /usr/local/Ascend/cann/set_env.sh
elif [ -d "/usr/local/Ascend/ascend-toolkit" ]; then
    source /usr/local/Ascend/ascend-toolkit/set_env.sh
fi
```

**手动设置环境变量**

```bash
# 如果 set_env.sh 失效，手动设置
export ASCEND_HOME_PATH=/usr/local/Ascend/cann
export ASCEND_OPP_PATH=$ASCEND_HOME_PATH/opp
export ASCEND_AICPU_PATH=$ASCEND_OPP_PATH/op_impl/built-in/ai_core/tbe/op_tiling
export PATH=$ASCEND_HOME_PATH/compiler/ccec_compiler/bin:$PATH
export LD_LIBRARY_PATH=$ASCEND_HOME_PATH/lib64:$ASCEND_HOME_PATH/lib64/stub:$LD_LIBRARY_PATH
export PYTHONPATH=$ASCEND_HOME_PATH/python/site-packages:$PYTHONPATH
```

**持久化环境变量**

```bash
# 添加到 ~/.bashrc
echo 'source /usr/local/Ascend/cann/set_env.sh' >> ~/.bashrc

# 或添加完整配置
cat >> ~/.bashrc << 'EOF'
# Ascend CANN Environment
if [ -d "/usr/local/Ascend/cann" ]; then
    source /usr/local/Ascend/cann/set_env.sh
elif [ -d "/usr/local/Ascend/ascend-toolkit" ]; then
    source /usr/local/Ascend/ascend-toolkit/set_env.sh
fi
EOF

source ~/.bashrc
```

---

## 7. Diffusers 安装问题

### 症状

```python
from diffusers import StableDiffusionPipeline
# ImportError: cannot import name 'StableDiffusionPipeline' from 'diffusers'
# 或
# ModuleNotFoundError: No module named 'diffusers'
# 或
# ImportError: cannot import name 'EulerDiscreteScheduler' from 'diffusers'
```

### 诊断命令

```bash
# 检查 diffusers 版本
pip show diffusers

# 检查 transformers 版本
pip show transformers

# 检查 accelerate
pip show accelerate

# 查看 diffusers 内容
python -c "import diffusers; print(diffusers.__file__); print(dir(diffusers))"

# 检查依赖冲突
pip check
```

### 解决方案

**重新安装 diffusers**

```bash
# 卸载旧版本
pip uninstall diffusers transformers accelerate -y

# 标准安装
pip install diffusers["torch"] transformers accelerate

# 或使用国内镜像加速
pip install diffusers["torch"] transformers accelerate -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**安装特定版本**

```bash
# 如需特定版本
pip install diffusers==0.30.0 transformers==4.40.0 accelerate==0.30.0

# 开发版
pip install git+https://github.com/huggingface/diffusers.git
```

**修复损坏的安装**

```bash
# 强制重新安装
pip install diffusers --force-reinstall --no-cache-dir

# 清理 pip 缓存
pip cache purge

# 检查是否有命名冲突
pip list | grep -i diff
```

**检查 Python 环境**

```bash
# 确认使用的是正确的 Python
which python
python -c "import sys; print(sys.executable)"

# 检查是否在 conda 环境中
conda info --envs
conda list diffusers

# 如果使用 conda
conda install -c conda-forge diffusers
```

---

## 快速诊断清单

运行以下命令快速排查环境问题：

```bash
#!/bin/bash
echo "=== Diffusers 环境快速诊断 ==="

echo -e "\n[1] Python 环境:"
python --version
which python

echo -e "\n[2] CANN 路径:"
ls -d /usr/local/Ascend/cann 2>/dev/null && echo "✓ CANN 8.5+ 路径存在"
ls -d /usr/local/Ascend/ascend-toolkit 2>/dev/null && echo "✓ CANN 旧版路径存在"

echo -e "\n[3] 环境变量:"
echo "ASCEND_HOME_PATH=${ASCEND_HOME_PATH:-未设置}"
echo "ASCEND_OPP_PATH=${ASCEND_OPP_PATH:-未设置}"

echo -e "\n[4] NPU 设备:"
npu-smi info 2>/dev/null | head -5 || echo "✗ npu-smi 失败"

echo -e "\n[5] 关键包版本:"
pip show torch torch-npu numpy diffusers 2>/dev/null | grep -E "^(Name|Version):"

echo -e "\n[6] 导入测试:"
python -c "import torch; import torch_npu; print(f'torch: {torch.__version__}'); print(f'NPU可用: {torch.npu.is_available()}')" 2>&1
python -c "import diffusers; print(f'diffusers: {diffusers.__version__}')" 2>&1

echo -e "\n诊断完成"
```

---

## 相关资源

- [CANN 版本说明](./cann-versions.md) - CANN 版本检测和环境配置
- [SKILL.md](../SKILL.md) - 完整环境配置指南
- [昇腾官方文档](https://www.hiascend.com/document)
- [Diffusers 官方文档](https://huggingface.co/docs/diffusers)
