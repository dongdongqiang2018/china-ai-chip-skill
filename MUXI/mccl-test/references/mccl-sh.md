# MCCL 性能测试脚本详解

## 脚本位置

```
/opt/maca/samples/mccl_tests/perf/function/mccl.sh
```

## 脚本内容

```bash
#!/bin/bash

export MACA_PATH=/opt/maca
export LD_LIBRARY_PATH=${MACA_PATH}/lib:${MACA_PATH}/ompi/lib
export FORCE_ACTIVE_WAIT=2

GPU_NUM=4
if [[ $1 -gt 0 && $1 -lt 65 ]]; then
    GPU_NUM=$1
fi

TEST_DIR=${MACA_PATH}/samples/mccl_tests/perf/mccl_perf
#BENCH_NAMES="all_reduce_perf all_gather_perf reduce_scatter_perf sendrecv_perf alltoall_perf"
BENCH_NAMES=all_reduce_perf

MPI_PROCESS_NUM=${GPU_NUM}
MPI_RUN_OPT="--allow-run-as-root -mca pml ^ucx -mca osc ^ucx -mca btl ^openib"

for BENCH in ${BENCH_NAMES}; do
    echo -n "The test is ${BENCH}, the maca version is " && realpath ${MACA_PATH}
    TEST="${TEST_DIR}/${BENCH} -b 1K -e 1G -d bfloat16 -f 2 -g 1 -n 10"
    ${MACA_PATH}/ompi/bin/mpirun -np ${MPI_PROCESS_NUM} ${MPI_RUN_OPT} /opt/maca/samples/mccl_tests/perf/function/per_rank.sh "${TEST}"
done
```

## 参数说明

### 命令行参数

| 参数 | 说明 | 范围 |
|------|------|------|
| `$1` | GPU数量 | 1-64 |

### BENCH_NAMES 选项

```bash
# 可以测试单个
BENCH_NAMES=all_reduce_perf

# 也可以测试多个（取消注释）
BENCH_NAMES="all_reduce_perf all_gather_perf reduce_scatter_perf sendrecv_perf alltoall_perf"
```

| 测试项 | 说明 |
|--------|------|
| `all_reduce_perf` | AllReduce 集合通信性能 |
| `all_gather_perf` | AllGather 集合通信性能 |
| `reduce_scatter_perf` | ReduceScatter 集合通信性能 |
| `sendrecv_perf` | 点对点 Send/Recv 性能 |
| `alltoall_perf` | AllToAll 集合通信性能 |

### 环境变量

| 环境变量 | 说明 |
|----------|------|
| `MACA_PATH` | MCCA安装路径 |
| `LD_LIBRARY_PATH` | 库路径 |
| `FORCE_ACTIVE_WAIT` | 强制等待模式 |

### MPI 参数

```bash
MPI_RUN_OPT="--allow-run-as-root -mca pml ^ucx -mca osc ^ucx -mca btl ^openib"
```

- `--allow-run-as-root` : 允许root用户运行
- `-mca pml ^ucx` : 禁用UCX PML
- `-mca osc ^ucx` : 禁用UCX OSC
- `-mca btl ^openib` : 禁用OpenIB BTL

## 使用示例

### 基础用法

```bash
# 4卡测试
bash mccl.sh 4

# 8卡测试
bash mccl.sh 8
```

### 完整示例

```bash
# 1. 进入目录
cd /opt/maca/samples/mccl_tests/perf/function

# 2. 编辑脚本选择测试项
vim mccl.sh
# 修改: BENCH_NAMES=all_reduce_perf
# 为: BENCH_NAMES="all_reduce_perf all_gather_perf"

# 3. 运行测试
bash mccl.sh 8
```

### 自定义测试参数

如需修改测试参数（如数据大小、数据类型等），可以编辑脚本中的 `TEST` 变量：

```bash
# 默认
TEST="${TEST_DIR}/${BENCH} -b 1K -e 1G -d bfloat16 -f 2 -g 1 -n 10"

# 修改为
TEST="${TEST_DIR}/${BENCH} -b 4K -e 4G -d float32 -f 4 -g 2 -n 20"
```

参数说明：
- `-b` : 起始数据大小 (1K, 4K, 1M, 4M, 1G等)
- `-e` : 结束数据大小
- `-d` : 数据类型 (float32, float16, bfloat16, int8等)
- `-f` : 迭代因子
- `-g` : GPU数量
- `-n` : 迭代次数

## 其他位置

另外还有一个 perf 目录下的测试脚本：

```
/opt/maca/samples/mccl_tests/perf/mccl.sh
```

这个脚本可能包含更多测试项目，如需使用请参考对应目录下的文档。