# MCCL API 参考

## 通信器管理

### mcclGetVersion
```c
mcclResult_t mcclGetVersion(int* version);
```
获取MCCL版本号，返回格式为 主版本号*1000 + 次版本号

### mcclGetUniqueId
```c
mcclResult_t mcclGetUniqueId(mcclUniqueId* uniqueId);
```
生成通信器唯一ID，需要在所有参与进程间共享

### mcclCommInitRank
```c
mcclResult_t mcclCommInitRank(mcclComm_t* comm, int nranks, mcclUniqueId commId, int rank);
```
- `nranks`: 总进程数
- `commId`: mcclGetUniqueId生成的ID
- `rank`: 当前进程rank (0到nranks-1)

### mcclCommInitAll
```c
mcclResult_t mcclCommInitAll(mcclComm_t* comm, int ndev, const int* devlist);
```
使用设备列表初始化通信器

### mcclCommDestroy
```c
mcclResult_t mcclCommDestroy(mcclComm_t comm);
```
销毁通信器，释放资源

---

## 集合通信API

### mcclAllReduce
```c
mcclResult_t mcclAllReduce(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, mcclRedOp_t op, mcclComm_t comm, mcStream_t stream);
```
- `sendbuff`: 发送缓冲区
- `recvbuff`: 接收缓冲区
- `count`: 元素数量
- `datatype`: 数据类型
- `op`: 归约操作
- `comm`: 通信器
- `stream`: MXMACA流

### mcclBroadcast
```c
mcclResult_t mcclBroadcast(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, int root, mcclComm_t comm, mcStream_t stream);
```
- `root`: 广播源进程rank

### mcclReduce
```c
mcclResult_t mcclReduce(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, mcclRedOp_t op, int root, mcclComm_t comm, mcStream_t stream);
```

### mcclAllGather
```c
mcclResult_t mcclAllGather(const void* sendbuff, void* recvbuff, size_t sendcount,
    mcclDataType_t datatype, mcclComm_t comm, mcStream_t stream);
```

### mcclReduceScatter
```c
mcclResult_t mcclReduceScatter(const void* sendbuff, void* recvbuff, size_t recvcount,
    mcclDataType_t datatype, mcclRedOp_t op, mcclComm_t comm, mcStream_t stream);
```

### mcclAllToAll
```c
mcclResult_t mcclAllToAll(const void* sendbuff, void* recvbuff, size_t count,
    mcclDataType_t datatype, mcclComm_t comm, mcStream_t stream);
```

### mcclAllToAllv
```c
mcclResult_t mcclAllToAllv(const void* sendbuff, const size_t sendcounts[],
    const size_t sdispls[], void* recvbuff, const size_t recvcounts[],
    const size_t rdispls[], mcclDataType_t datatype, mcclComm_t comm, mcStream_t stream);
```
- `sendcounts`: 每个进程的发送元素数
- `sdispls`: 发送偏移量
- `recvcounts`: 每个进程的接收元素数
- `rdispls`: 接收偏移量

---

## 数据类型

| 枚举值 | 说明 |
|--------|------|
| mcclInt8 | 8位整数 |
| mcclUint8 | 8位无符号整数 |
| mcclInt16 | 16位整数 |
| mcclUint16 | 16位无符号整数 |
| mcclInt32 | 32位整数 |
| mcclUint32 | 32位无符号整数 |
| mcclInt64 | 64位整数 |
| mcclUint64 | 64位无符号整数 |
| mcclFloat16 | 半精度浮点 |
| mcclFloat32 | 单精度浮点 |
| mcclFloat64 | 双精度浮点 |

---

## 归约操作

| 枚举值 | 说明 |
|--------|------|
| mcclSum | 求和 |
| mcclProd | 求积 |
| mcclMax | 最大值 |
| mcclMin | 最小值 |
| mcclAvg | 平均值 |

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| mcclSuccess | 成功 |
| mcclUnhandledError | 未处理错误 |
| mcclInvalidArgument | 无效参数 |
| mcclInvalidUsage | 无效使用 |
| mcclCommMismatch | 通信器不匹配 |
| mcclRankMismatch | Rank不匹配 |
| mcclDriverError | 驱动错误 |
| mcclInternalError | 内部错误 |
| mcclTimeout | 超时 |
| mcclNUMARemoteError | NUMA远程错误 |

---

## 返回值检查

```c
mcclResult_t result = mcclAllReduce(...);
if (result != mcclSuccess) {
    printf("MCCL error: %s\n", mcclGetErrorString(result));
    // 处理错误
}
```