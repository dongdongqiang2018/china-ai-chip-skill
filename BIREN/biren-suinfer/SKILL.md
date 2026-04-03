---
name: biren-suinfer
description: BIREN suInfer 深度学习推理引擎参考指南。基于壁仞通用 GPU 的深度学习推理引擎框架，提供 C++ 和 Python API，支持 ONNX 和 PyTorch 模型，用于构建高性能推理引擎。
keywords:
  - suinfer
  - biren
  - 推理
  - 深度学习
  - ONNX
  - PyTorch
  - 推理引擎
  - 壁仞
---

# suInfer Command Reference

suInfer 是基于壁仞通用 GPU 的深度学习推理引擎框架。

## Quick Start

### C++ API

```cpp
#include <suinfer.h>

// 创建 builder
auto builder = suinfer::Builder(suinfer::Logger::Level::INFO);
auto parser = builder.create_parser();
auto network = parser->parse_from_file(onnx_path, nullptr);
network->get_input(0)->shape = {1, 3, 224, 224};

auto engine = builder.create_engine();
engine->build(network);

auto stream = engine->create_stream();
auto bindings = engine->create_bindings({data.data(), output.data()});
engine->run_async(bindings, stream);
stream->synchronize();
```

### Python API

```python
import suinfer

builder = suinfer.Builder(suinfer.Logger(suinfer.Logger.Warning), None)
parser = builder.create_parser()
network = parser.parse_from_file(onnx_path, None)
network.get_input(0).shape = (1, 3, 224, 224)

engine = builder.create_engine()
engine.build(network)

data = np.fromfile(input_file, dtype=np.uint8)
output_data = np.zeros((1, 1000), dtype=np.float32)

stream = engine.create_stream()
bindings = engine.create_bindings([data.ctypes.data, output_data.ctypes.data])
engine.run_async(bindings, stream)
stream.synchronize()
```

## Environment Setup

```bash
# 激活环境
source /usr/local/birensupa/suinfer/latest/scripts/brsw_set_env.sh
bash /usr/local/birensupa/suinfer/latest/scripts/brsw_version.sh
```

## Build Flow

1. 创建 builder
2. 配置 config
3. 创建 parser
4. 解析 net
5. 创建 engine
6. 运行推理

## Key APIs (C++)

| API | Description |
|-----|-------------|
| `CreateInferBuilder` | 创建 builder |
| `builder->createParser` | 创建 ONNX 解析器 |
| `builder->createEngine` | 创建推理引擎 |
| `builder->createBackend` | 创建后端 |
| `config.requestProcessUnits(n)` | 设置 SPC 数量（必须） |
| `config.setPrecisionMode(mode)` | 设置精度（BF16/FP32） |
| `parser->parseFromFile(file)` | 解析 ONNX 文件 |
| `net->shapeInference()` | Shape 推断验证 |
| `engine->build(net)` | 构建可执行算子列表 |
| `engine->run(bindings)` | 执行推理 |

## suInferSession (Python)

| API | Description |
|-----|-------------|
| `suInferSession(device_index)` | 创建会话 |
| `Build(model_file, ...)` | 构建模型 |
| `Init(serialize_file)` | 初始化 |
| `SetInputInformation(...)` | 设置输入 |
| `SetOutputInformation(...)` | 设置输出 |
| `Run()` / `RunAsyn()` | 执行推理 |

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `device_index` | 设备序号，默认 0 |
| `logger_file` | log 输出路径 |
| `spc_mask` | 掩码指定部分卡资源 |
| `log_level` | 日志等级 (3=Error, 6=Info, 8=Verbose) |
| `model_file` | ONNX 模型文件路径 |
| `input_shape_max` | 输入最大 shape |
| `to_serialize_file` | 序列化文件保存路径 |
| `dynamic_shape` | 动态 shape 标识 |
| `simulator_inference` | CPU 仿真推理 |
| `dry_run` | 算子扫描模式 |
| `mp_mode` | 模型并行模式 |
| `link_mode` | 链接模式/优化级别 |

## Dry Run Mode

打开后不执行 build，直接扫描模型算子支持情况：

```python
session.Build(model_file, input_shape_max, serialize_file, dry_run=True)
```

结果保存在 `suinfer_dry_run*.log`。

## Example: ResNet50 (C++)

```cpp
#include <suinfer.h>

int main() {
    // 构建 builder
    std::unique_ptr<IBuilder> builder(CreateInferBuilder(SUINFER_GetDefaultLogger("rn50_demo.log")));
    IAppConfigs& app_configs = builder->getAppConfigs();
    IBuilderConfig& config = app_configs.getBuilderConfig();
    config.requestProcessUnits(spc_num);

    // 创建 parser 并解析
    std::unique_ptr<parsers::IParser> parser(builder->createParser());
    net.reset(parser->parseFromFile(onnx_file));

    // 创建 engine 并 build
    engine.reset(builder->createEngine());
    engine->build(*net);

    // 分配 device buffer 并运行
    suMallocDevice(&addr, real_size);
    suMemcpy(addr, inputs.data(), inputs.size());
    engine->run(mem_handles.data());
    suMemcpy(outputs.data(), mem_handles[input_cnt], output_size);

    return 0;
}
```

编译：
```bash
g++ rn50_demo.cpp -g -o rn50_demo \
    -L/usr/local/birensupa/sdk/latest/supa/lib \
    -lsupa-runtime -lsuinfer \
    -std=c++17 -lstdc++fs \
    -I/usr/local/birensupa/sdk/latest/supa/include
```

运行：`./rn50_demo ./resnet50-v1-12.onnx cat224.bin 1x3x224x224`

## Custom Operators (Plugin)

```bash
# 编译 SUPA kernel
brcc -x supa -fgpu-rdc -fPIC -O2 -std=c++14 -shared \
    -o output/libcustomized_plugins_kernels.so kernels/ele_mul_cpu.su

# 编译 plugin
g++ -fPIC -shared -g -o output/libcustomized_plugins.so \
    src/customized_plugins.cpp src/ele_mul_cpu_plugin.cpp \
    -L./output -lcustomized_plugins_kernels

# 加载 plugin
suinfer::SUINFER_LoadPlugin(nullptr, "libcustomized_plugins.so");
```

## Model Format Support

- ONNX (.onnx)
- PyTorch TorchScript (.pt)

## Precision Modes

| Mode | Description |
|------|-------------|
| `bf16` | BFloat16 |
| `fp32` | Float32 |

## Python Installation

```python
import suinfer
```

注意：与 PyTorch 一起使用需安装 2.1.0 带 abi 的版本。

## Return Codes

| Code | Description |
|------|-------------|
| `SUINFER_SUCCESS` | 成功 |
| `SUINFER_ERROR_INVALID_VALUE` | 无效值 |
| `SUINFER_ERROR_INVALID_MODEL` | 无效模型 |
| `SUINFER_ERROR_OUT_OF_MEMORY` | 内存不足 |

## Performance Tips

- 合理设置 SPC 数量
- 使用序列化文件加速启动
- 启用合适的精度模式
- 优化模型结构

## Related Tools

- **suInfer-LLM**: 大语言模型推理
- **brvllm**: vLLM-based 推理服务
- **suInfer Server**: Triton-based 推理服务器