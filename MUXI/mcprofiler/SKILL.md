---
name: mcprofiler
description: 沐曦GPU性能分析工具，提供可视化的GPU性能指标分析界面，支持RoofLine视图、Memory/Computing/Scheduling性能指标分析。用于GPU程序性能调优。
keywords:
  - 沐曦
  - 性能分析
  - mcprofiler
  - GPU调优
  - RoofLine
  - 性能指标
---

# mcProfiler 使用指南

mcProfiler是MXMACA软件栈中的可视化GPU性能指标分析工具，提供可定制的、数据驱动的用户界面和度量集合，为开发人员提供GPU核函数详细的性能视图。

## 快速开始

### 安装

mcProfiler包含在win-perf-kit工具包内，是一个Windows上的UI程序。

1. 解压mcProfiler压缩包
2. 双击gui-profiler.exe即可直接使用

### 创建度量任务

1. 点击左上角的 **+ExecPerf** 图标，创建任务
2. 配置任务参数
3. 点击Confirm开始任务

### 前置要求

#### GUI平台（Windows）
- 需要对应的网络权限
- 建议关闭防火墙拦截

#### MXMACA平台（Linux）
- 需要开放SSH权限
- 若使用私钥登录，需确保：
  - 用户目录权限为700
  - 公钥文件权限为600

#### 程序编译
被度量目标程序需要链接libmcToolsExt.so动态库：

```bash
# 编译时链接调试库
g++ your_program.cpp -o your_program -lmctools_ext
```

## 任务配置

### 创建任务参数

| 参数 | 说明 |
|------|------|
| Metrics | 度量指标（多选），指标越多，采集时间越长 |
| EnvironmentVariables | 环境变量设置（MACA_PATH、动态库路径等） |
| CommandLine | 目标程序执行命令，支持多条bash语句（用;分隔） |
| CaseName | perf任务名称，用于区分任务标识 |
| RemoteIP | 远程MXMACA平台IP地址 |
| RemotePort | 远程节点SSH端口号 |
| RemoteUser | 远程节点登录用户名 |
| RemotePassword | 远程节点登录密码 |
| Run in host/docker | 选择目标程序执行环境（宿主机/容器） |
| ContainerNameorID | 容器环境执行时必填 |

### 环境变量配置示例

```bash
# 设置MACA路径和动态库路径
MACA_PATH=/opt/maca
LD_LIBRARY_PATH=/opt/maca/lib:$LD_LIBRARY_PATH
```

### 执行命令示例

```bash
# 单条命令
./your_gpu_program

# 多条命令（设置环境后执行）
cd /path/to/program; ./your_program
```

## 执行度量

### 任务状态

- **executing**: 任务执行中
- **done**: 任务完成

### 多轮测量

当选择多个度量指标时，mcProfiler会执行多轮测量，每轮执行信息会在ExecuteLoop n标签栏内显示。

## 分析结果

任务执行完成后，在左侧导航栏点击CaseReport，可获取详细的性能分析报告。

### 分析视角

| 视角 | 说明 |
|------|------|
| SOL视角 | 系统整体视角 |
| RoofLine视图 | 各子模块的RoofLine性能分析 |
| Memory | 内存相关性能指标 |
| Computing | 计算相关性能指标 |
| Scheduling | 调度相关性能指标 |

### 深度分析

每个类别提供：
- 相关模块资源使用情况
- 详细性能指标分析

## 功能特性

### 全局视角
- SOL视角和各个子模块的RoofLine视图

### 性能指标分类
- **Memory**: 内存带宽、访问模式等
- **Computing**: 计算利用率、算子性能等
- **Scheduling**: 调度效率、任务排队等

### 深度分析
- 相关模块资源使用情况
- 详细性能指标数据

## 卸载

mcProfiler为纯绿色免安装软件，删除整个mcProfiler文件夹即可卸载。

## 注意事项

1. mcProfiler采用Windows GUI + Linux采样的方式工作
2. 被测程序需链接 `-lmctoolsExt` 调试库
3. 度量指标越多，采集和分析时间越长
4. 需要Windows到Linux的SSH访问权限

## 官方参考

- MXMACA软件包
- win-perf-kit工具包