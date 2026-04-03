---
name: mccl
description: 沐曦集合通信库，提供多GPU间通信原语（AllReduce/Broadcast/AllGather等），用于分布式AI训练。
keywords:
  - 沐曦
  - 集合通信
  - mccl
  - NCCL
  - 分布式训练
  - 多卡通信
---

# MCCL 编程指南

沐曦MCCL（MetaX Collective Communication Library）提供多GPU间集合通信原语。

## 快速开始

### 安装

MCCL随MXMACA SDK默认安装。

### 基本使用

```c
#include <mccl.h>

int main() {
    mcclComm_t comm;
    ncclCommInitRank(&comm, nranks, rank, 0);

    // 执行AllReduce
    ncclAllReduce(sendbuff, recvbuff, count, ncclFloat, ncclSum, comm, stream);

    ncclCommDestroy(comm);
    return 0;
}
```

## 通信原语

### Broadcast

```c
// 广播数据到所有进程
mcclBroadcast(sendbuff, recvbuff, count, dtype, root, comm, stream);
```

### AllReduce

```c
// 所有进程执行归约操作
mcclAllReduce(sendbuff, recvbuff, count, dtype, ncclSum, comm, stream);
```

### Reduce

```c
// 归约到根进程
mcclReduce(sendbuff, recvbuff, count, dtype, ncclSum, root, comm, stream);
```

### AllGather

```c
// 收集所有进程数据
mcclAllGather(sendbuff, recvbuff, count, dtype, comm, stream);
```

### Gather

```c
// 收集到根进程
mcclGather(sendbuff, recvbuff, count, dtype, root, comm, stream);
```

### Scatter

```c
// 分发数据到所有进程
mcclScatter(sendbuff, recvbuff, count, dtype, root, comm, stream);
```

### ReduceScatter

```c
// 归约后分发
mcclReduceScatter(sendbuff, recvbuff, count, dtype, ncclSum, comm, stream);
```

### Send/Recv

```c
// 点对点通信
mcclSend(sendbuff, count, dtype, dest, comm, stream);
mcclRecv(recvbuff, count, dtype, src, comm, stream);
```

## 分布式训练

### 数据并行

```python
import torch.distributed as dist

# 初始化
dist.init_process_group(backend='mccl')

# AllReduce梯度
dist.all_reduce(gradient, op=dist.ReduceOp.SUM)
```

### 模型并行

```python
# 使用Horovod或DeepSpeed
import horovod.torch as hvd

hvd.init()
```

## 性能优化

### 拓扑感知

```c
// 查询GPU拓扑
mcclGetCliqueSize()
```

### 集合通信调优

```c
// 设置超时
ncclCommSetOpt(handle, ncclOptTimeout, 300);
```

## 环境变量

| 变量 | 说明 |
|------|------|
| MCCL_DEBUG | 调试级别 |
| MCCL_BUFFSIZE | 缓冲区大小 |
| NCCL_NTHREADS | 线程数 |

## 官方参考

- 《曦云系列通用GPU MCCL编程指南》