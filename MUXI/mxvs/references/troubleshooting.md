# mxvs 故障排查

## 常见问题

### 1. 命令找不到

**问题**：执行mxvs提示找不到命令

**解决**：
```bash
# 检查mxvs是否安装
ls -la /opt/maca/bin/mxvs

# 检查环境变量
echo $PATH

# 添加到PATH（如果需要）
export PATH=$PATH:/opt/maca/bin
```

### 2. 权限问题

**问题**：Permission denied

**原因**：需要root权限

**解决**：
```bash
sudo mxvs <command>
```

### 3. 驱动未加载

**问题**：无法执行测试

**检查**：
```bash
lsmod | grep metax
```

**解决**：
```bash
# 加载驱动
modprobe metax

# 或重启服务
systemctl restart metax
```

### 4. FUSE未安装

**问题**：AppImage无法运行

**检查**：
```bash
dpkg -l | grep fuse
```

**解决**：
```bash
sudo apt-get install fuse libnss3
```

### 5. 带宽测试结果低

**问题**：实测带宽低于预期

**可能原因**：
- NUMA跨节点访问
- CPU亲和性问题

**解决**：
```bash
# 清理系统缓存
echo 3 > /proc/sys/vm/drop_caches

# 指定CPU核心
--cpu-affinity 0,1,2,3
```

### 6. 眼图测试失败

**问题**：眼图测试无法执行

**可能原因**：
- GPU被占用
- 测试中断

**解决**：
```bash
# 检查GPU进程
mx-smi --show-all-process
mx-smi --show-process

# 停止占用进程
kill <pid>

# 重新测试
```

### 7. 持续监控无输出

**问题**：dashboard命令无输出

**解决**：
```bash
# 指定设备
mxvs dashboard -d 0

# 指定面板
mxvs dashboard -p 0
```

### 8. 跨节点测试失败

**问题**：多机MetaXLink测试失败

**检查**：
```bash
# 检查网络连通性
ping <node_ip>

# 检查防火墙
sudo systemctl status firewalld

# 检查端口9601是否开放
netstat -an | grep 9601
```

### 9. JSON输出失败

**问题**：--json参数报错

**解决**：
```bash
# 检查目录权限
ls -la /path/to/output/

# 使用绝对路径
--json /tmp/result.json
```

### 10. 压力测试异常

**问题**：长时间压力测试失败

**建议**：
- 使用nohup后台运行
- 重定向日志
- 测试后检查日志

```bash
nohup mxvs stress --xcore --xcore-devices 0 --duration 3600 > stress.log 2>&1 &

# 检查日志
tail -f stress.log
```

---

## 诊断流程

```bash
# 1. 检查环境
whoami                    # 确认root权限
lsmod | grep metax        # 确认驱动加载
ls -la /opt/maca/bin/mxvs # 确认工具安装

# 2. 检查设备
mxvs devices              # 查看设备列表
mx-smi -L                 # 查看GPU状态

# 3. 简单测试
mxvs dashboard            # 动态监控
mxvs memory bandwidth --devices 0  # 显存带宽

# 4. 完整测试
# 按需执行各项验收测试
```

---

## 错误信息

| 错误 | 说明 | 解决 |
|------|------|------|
| No such device | 设备不存在 | 检查设备ID |
| Permission denied | 权限不足 | 使用sudo |
| Driver not loaded | 驱动未加载 | 加载驱动 |
| Device busy | 设备忙 | 停止其他进程 |