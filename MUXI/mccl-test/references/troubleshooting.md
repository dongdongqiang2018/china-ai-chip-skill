# MCCL 故障排查

## 常见问题

### 1. 通信初始化失败

**症状**：mcclCommInitRank 返回错误

**排查步骤**：
```bash
# 1. 检查所有节点是否可以互相通信
ping <other_node_ip>

# 2. 检查MCCL库是否正确安装
ls -la /opt/maca/lib/libmccl*

# 3. 检查环境变量
echo $LD_LIBRARY_PATH
# 确保包含 /opt/maca/lib

# 4. 启用调试输出
export MCCL_DEBUG=4
export MCCL_DEBUG_FILE=mccl.log
```

### 2. 多机通信超时

**症状**：程序hang在集合通信操作

**解决方案**：
```bash
# 1. 设置正确的网卡
export MCCL_SOCKET_IFNAME=eth0  # 或正确的网卡名

# 2. 检查防火墙
sudo systemctl status firewalld

# 3. 增大超时时间
export NCCL_TIMEOUT=3600

# 4. 检查端口是否被占用
netstat -an | grep <port>
```

### 3. 带宽不达预期

**症状**：AllReduce性能差

**排查**：
```bash
# 1. 检查是否启用GDR
echo $MCCL_NET_GDR_LEVEL
# 应设置为2

# 2. 检查网络带宽
# 使用iperf测试网络

# 3. 检查GPU拓扑
nvidia-smi topo -m
# 或使用 mx-smi topo -m
```

**优化建议**：
```bash
# 1. 启用GDR
export MCCL_NET_GDR_LEVEL=2

# 2. 增加通道数
export MCCL_MAX_NCHANNELS=16
export MCCL_MIN_NCHANNELS=4

# 3. 启用Full Chip模式
export MCCL_ENABLE_FC=1
```

### 4. 内存不足

**症状**：OOM错误或通信失败

**解决方案**：
```bash
# 1. 减小批次大小
# 2. 增加缓冲区大小
export MCCL_BUFFSIZE=2097152  # 2MB

# 3. 检查GPU内存
nvidia-smi
mx-smi --show-memory
```

### 5. InfiniBand配置问题

**症状**：IB网络下通信失败

**检查**：
```bash
# 1. 查看IB设备
ibstat

# 2. 设置IB设备
export MCCL_IB_HCA=mlx5_0:1

# 3. 检查GID
ibaddr -g mlx5_0

export MCCL_IB_GID_INDEX=3
```

### 6. 进程挂起

**症状**：程序hang，无错误输出

**排查**：
```bash
# 1. 启用调试
export MCCL_DEBUG=4

# 2. 检查进程是否还在运行
ps aux | grep <program>

# 3. 使用strace跟踪
strace -f -o strace.log ./program
```

---

## 调试命令

### 检查MCCL版本
```bash
# 通过程序
./program 2>&1 | grep MCCL
# 或
ldd <program> | grep mccl
```

### 检查拓扑
```bash
# 生成拓扑文件
MCCL_TOPO_DUMP_FILE=topo.xml mpirun -n 4 ./program
cat topo.xml
```

### 网络诊断
```bash
# 检查网络连接
ping -c 3 <node_ip>

# 检查网卡状态
ip link show

# 检查IB状态
ibstatus
```

---

## 性能调优参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| MCCL_ENABLE_FC | Full Chip模式 | 1 |
| MCCL_FC_BYTE_LIMIT | FC阈值 | 1048576 |
| MCCL_MIN_NCHANNELS | 最小通道数 | 4 |
| MCCL_MAX_NCHANNELS | 最大通道数 | 16 |
| MCCL_NET_GDR_LEVEL | GDR级别 | 2 |
| MCCL_BUFFSIZE | 缓冲区大小 | 1048576 |