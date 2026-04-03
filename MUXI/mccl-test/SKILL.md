---
name: mccl-test
description: 沐曦MCCL集合通信库的使用指南，包括API接口、环境变量配置、调试方法。用于在曦云GPU上开发多GPU通信程序，进行分布式训练等场景。
keywords:
  - MCCL
  - 集合通信
  - 分布式训练
  - AllReduce
  - AllToAll
  - AllGather
  - GPU通信
  - MetaX
  - 性能测试
  - 带宽测试
---

# MCCL 编程指南

MetaX Collective Communications Library（MCCL，发音为"Mickel"）是一个提供GPU间通信原语的通讯库，这些原语具有拓扑感知能力，并且使用方便。MCCL实现集合通信和点对点发送/接收原语。

## 快速开始

### 基本使用流程

```c
#include <mccl.h>

int main() {
    mcclUniqueId id;
    mcclComm_t comm;
    int rank, nranks;

    // 1. 获取唯一ID（仅rank 0）
    if (rank == 0) {
        mcclGetUniqueId(&id);
    }

    // 2. 广播给所有进程
    MPI_Bcast(&id, sizeof(id), MPI_BYTE, 0, MPI_COMM_WORLD);

    // 3. 初始化通信器
    mcclCommInitRank(&comm, nranks, id, rank);

    // 4. 执行集合通信
    mcclAllReduce(sendbuff, recvbuff, count, mcclFloat, mcclSum, comm, stream);

    // 5. 销毁通信器
    mcclCommDestroy(comm);

    return 0;
}
```

### 编译与运行

```bash
# 编译
gcc example.c -I/opt/maca/include -L/opt/maca/lib -lmccl -o example

# 运行（单节点多卡）
./example

# 运行（多节点）
mpirun -n <进程数> ./example
```

---

## 通信器管理API

### 初始化与销毁

| API | 说明 |
|-----|------|
| `mcclGetVersion(int* version)` | 获取MCCL版本号 |
| `mcclGetUniqueId(mcclUniqueId* uniqueId)` | 获取通信器唯一ID |
| `mcclCommInitRank(mcclComm_t* comm, int nranks, mcclUniqueId id, int rank)` | 初始化通信器 |
| `mcclCommInitAll(mcclComm_t* comm, int ndev, const int* devlist)` | 初始化所有设备通信器 |
| `mcclCommDestroy(mcclComm_t comm)` | 销毁通信器 |
| `mcclCommAbort(mcclComm_t comm)` | 中止通信器 |

### 查询API

| API | 说明 |
|-----|------|
| `mcclGetErrorString(mcclResult_t result)` | 获取错误描述 |
| `mcclCommGetAsyncError(mcclComm_t comm, mcclResult_t* asyncError)` | 获取异步错误 |
| `mcclCommCount(const mcclComm_t comm, int* count)` | 获取设备数 |
| `mcclCommMcDevice(const mcclComm_t comm, int* device)` | 获取设备ID |
| `mcclCommUserRank(const mcclComm_t comm, int* rank)` | 获取用户rank |

---

## 集合通信原语

### AllReduce

```c
mcclResult_t mcclAllReduce(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, mcclRedOp_t op, mcclComm_t comm, mcStream_t stream);
```

所有进程的数据进行归约操作，结果返回给所有进程。

### Broadcast

```c
mcclResult_t mcclBroadcast(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, int root, mcclComm_t comm, mcStream_t stream);
```

将数据从root进程广播到所有进程。

### Reduce

```c
mcclResult_t mcclReduce(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, mcclRedOp_t op, int root, mcclComm_t comm, mcStream_t stream);
```

将数据归约到root进程。

### AllGather

```c
mcclResult_t mcclAllGather(const void* sendbuff, void* recvbuff, size_t sendcount,
    mcclDataType_t datatype, mcclComm_t comm, mcStream_t stream);
```

所有进程的数据收集到一起。

### ReduceScatter

```c
mcclResult_t mcclReduceScatter(const void* sendbuff, void* recvbuff, size_t recvcount,
    mcclDataType_t datatype, mcclRedOp_t op, mcclComm_t comm, mcStream_t stream);
```

先归约再分散到各进程。

### AllToAll

```c
mcclResult_t mcclAllToAll(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, mcclComm_t comm, mcStream_t stream);
```

每个进程向所有其他进程发送数据，并从所有进程接收数据。

### AllToAllv

```c
mcclResult_t mcclAllToAllv(const void* sendbuff, const size_t sendcounts[],
    const size_t sdispls[], void* recvbuff, const size_t recvcounts[],
    const size_t rdispls[], mcclDataType_t datatype, mcclComm_t comm, mcStream_t stream);
```

变长版本的AllToAll。

---

## 点对点通信

### Send/Recv

```c
// 发送
mcclResult_t mcclSend(const void* sendbuff, size_t count, mcclDataType_t datatype,
    int peer, mcclComm_t comm, mcStream_t stream);

// 接收
mcclResult_t mcclRecv(void* recvbuff, size_t count, mcclDataType_t datatype,
    int peer, mcclComm_t comm, mcStream_t stream);
```

### 组调用

```c
mcclGroupStart();
mcclSend(sendbuff[0], size, mcclFloat, 1, comms[0], s[0]);
mcclRecv(recvbuff[1], size, mcclFloat, 0, comms[1], s[1]);
mcclGroupEnd();
```

---

## 数据类型与操作

### 数据类型

| MCCL类型 | 对应C类型 |
|----------|-----------|
| mcclInt8 | char |
| mcclChar | char |
| mcclUint8 | unsigned char |
| mcclInt32 | int |
| mcclInt | int |
| mcclUint32 | unsigned int |
| mcclInt64 | long |
| mcclUint64 | unsigned long |
| mcclFloat16 | __half |
| mcclFloat | float |
| mcclDouble | double |

### 归约操作

| 操作 | 说明 |
|------|------|
| mcclSum | 求和 |
| mcclProd | 求积 |
| mcclMax | 最大值 |
| mcclMin | 最小值 |
| mcclAvg | 平均值 |

---

## 环境变量配置

### 网络配置

| 环境变量 | 说明 | 示例 |
|----------|------|------|
| `MCCL_SOCKET_IFNAME` | 指定网卡接口 | `export MCCL_SOCKET_IFNAME=eth0` |
| `MCCL_IB_HCA` | 指定InfiniBand网卡 | `export MCCL_IB_HCA=mlx5_0:1` |
| `MCCL_IB_GID_INDEX` | IB GID索引 | `export MCCL_IB_GID_INDEX=3` |
| `MCCL_IB_DISABLE` | 禁用IB | `export MCCL_IB_DISABLE=1` |
| `MCCL_NET_GDR_LEVEL` | GDR级别 | `export MCCL_NET_GDR_LEVEL=2` |

### 性能配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `MCCL_ENABLE_FC` | 启用Full Chip | 1 |
| `MCCL_FC_BYTE_LIMIT` | FC字节限制 | 1048576 |
| `MCCL_FC_MAX_BLOCKS` | FC最大块数 | 32 |
| `MCCL_MIN_NCHANNELS` | 最小通道数 | 1 |
| `MCCL_MAX_NCHANNELS` | 最大通道数 | 8 |
| `MCCL_BUFFSIZE` | 缓冲区大小 | 1048576 |
| `MCCL_TUNING_MODEL` | 调优模式 | auto |

### 算法配置

| 环境变量 | 说明 |
|----------|------|
| `MCCL_PROTO` | 协议类型 |
| `MCCL_ALGO` | 算法选择 |
| `MCCL_RINGS` | 环数量 |
| `MCCL_DISABLE_CACHEABLE_BUFFER` | 禁用缓存 |

### 调试配置

| 环境变量 | 说明 |
|----------|------|
| `MCCL_DEBUG` | 调试级别 (0-4) |
| `MCCL_DEBUG_SUBSYS` | 调试子系统 |
| `MCCL_DEBUG_FILE` | 调试文件路径 |

---

## 拓扑感知

MCCL自动感知硬件拓扑，优化通信路径：

1. **节点内通信**：通过PCIe或MetaXLink
2. **节点间通信**：通过InfiniBand或以太网

### 查看拓扑

```bash
# 设置环境变量输出拓扑
export MCCL_TOPO_DUMP_FILE=topo.xml
# 运行程序后查看生成的topo.xml
```

### 拓扑优化环境变量

```bash
# 禁用跨节点通信
export MCCL_DISABLE_MULTI_NODE_FABRIC=0

# 禁用P2P
export MCCL_P2P_DISABLE=0

# P2P级别
export MCCL_P2P_LEVEL=1
```

---

## MCCL 性能测试脚本 (mccl.sh)

MCCL性能测试脚本位于 `/opt/maca/samples/mccl_tests/perf/function/mccl.sh`，用于测试集合通信性能。

### 快速开始

```bash
# 进入MCCA目录
cd /opt/maca

# 运行4卡性能测试
bash samples/mccl_tests/perf/function/mccl.sh 4

# 运行8卡性能测试
bash samples/mccl_tests/perf/function/mccl.sh 8
```

### 测试项目

通过修改脚本中的 `BENCH_NAMES` 变量可以选择测试项目：

```bash
BENCH_NAMES="all_reduce_perf all_gather_perf reduce_scatter_perf sendrecv_perf alltoall_perf"
```

| 测试项目 | 说明 |
|----------|------|
| `all_reduce_perf` | AllReduce 性能测试 |
| `all_gather_perf` | AllGather 性能测试 |
| `reduce_scatter_perf` | ReduceScatter 性能测试 |
| `sendrecv_perf` | Send/Recv 性能测试 |
| `alltoall_perf` | AllToAll 性能测试 |

### 使用示例

```bash
# 1. 设置环境变量
export MACA_PATH=/opt/maca
export LD_LIBRARY_PATH=${MACA_PATH}/lib:${MACA_PATH}/ompi/lib
export FORCE_ACTIVE_WAIT=2

# 2. 运行默认测试（仅 all_reduce_perf）
bash /opt/maca/samples/mccl_tests/perf/function/mccl.sh 8

# 3. 修改测试项目（可选）
# 编辑 /opt/maca/samples/mccl_tests/perf/function/mccl.sh
# 修改 BENCH_NAMES="all_reduce_perf" 为需要的测试
```

### 单独运行各测试项

默认脚本只测试 `all_reduce_perf`，如需单独运行其他测试项：

```bash
export MACA_PATH=/opt/maca
export LD_LIBRARY_PATH=${MACA_PATH}/lib:${MACA_PATH}/ompi/lib
export FORCE_ACTIVE_WAIT=2
TEST_DIR=${MACA_PATH}/samples/mccl_tests/perf/mccl_perf
MPI_PROCESS_NUM=8
MPI_RUN_OPT="--allow-run-as-root -mca pml ^ucx -mca osc ^ucx -mca btl ^openib"

# AllToAll 测试
${MACA_PATH}/ompi/bin/mpirun -np ${MPI_PROCESS_NUM} ${MPI_RUN_OPT} \
  /opt/maca/samples/mccl_tests/perf/function/per_rank.sh \
  "${TEST_DIR}/alltoall_perf -b 1K -e 1G -d bfloat16 -f 2 -g 1 -n 10"

# AllGather 测试
${MACA_PATH}/ompi/bin/mpirun -np ${MPI_PROCESS_NUM} ${MPI_RUN_OPT} \
  /opt/maca/samples/mccl_tests/perf/function/per_rank.sh \
  "${TEST_DIR}/all_gather_perf -b 1K -e 1G -d bfloat16 -f 2 -g 1 -n 10"

# ReduceScatter 测试
${MACA_PATH}/ompi/bin/mpirun -np ${MPI_PROCESS_NUM} ${MPI_RUN_OPT} \
  /opt/maca/samples/mccl_tests/perf/function/per_rank.sh \
  "${TEST_DIR}/reduce_scatter_perf -b 1K -e 1G -d bfloat16 -f 2 -g 1 -n 10"
```

### 测试参数说明

脚本默认参数：
- `-b 1K` : 起始数据大小 1KB
- `-e 1G` : 结束数据大小 1GB
- `-d bfloat16` : 数据类型 bfloat16
- `-f 2` : 迭代因子
- `-g 1` : GPU数量
- `-n 10` : 迭代次数

### 测试输出

测试会输出类似以下格式的结果：
```
The test is all_reduce_perf, the maca version is /opt/maca
[size]     [avg time(us)]   [avg bandwidth(GB/s)]
1K          100              10.5
4K          150              28.3
...
```

---

## P2P硬件验证

注意：MCCL的 `sendrecv_perf` 用于软件开发测试。如需验证GPU硬件P2P通信能力，请使用 `mxvs p2p` 命令：

```bash
# P2P硬件带宽测试
mxvs p2p --src-devices all --dst-devices all
```

详见 [mxvs技能](../mxvs/SKILL.md#p2p验收测试)

---

## 常见问题

### 通信超时

**问题**：多机训练时通信超时

**解决**：
```bash
# 检查网络连接
ping <其他节点IP>

# 配置正确的网卡
export MCCL_SOCKET_IFNAME=eth0

# 增加超时时间
export NCCL_TIMEOUT=3600
```

### 带宽不达预期

**解决**：
```bash
# 启用GDR
export MCCL_NET_GDR_LEVEL=2

# 调整通道数
export MCCL_MAX_NCHANNELS=16

# 禁用自动调优，手动指定
export MCCL_TUNING_MODEL=manual
```

### 内存不足

**解决**：
```bash
# 减小批次大小
# 或增加环境变量
export MCCL_BUFFSIZE=2097152
```

---

## 官方参考

- [曦云系列通用GPU MCCL编程指南_CN_V06.pdf](../文档/MCCL编程指南_CN_V06.pdf)
- [曦云系列通用GPU AI训练用户手册_CN_V05.pdf](../文档/AI训练用户手册_CN_V05.pdf)