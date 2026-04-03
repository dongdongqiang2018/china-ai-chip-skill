# vLLM-Ascend Performance Optimization Guide

This guide covers performance optimization for vLLM on Ascend NPUs.

## Key Performance Parameters

The following parameters significantly impact inference performance:

| Parameter | Description | Default | Recommendation |
|-----------|-------------|---------|----------------|
| `--max-model-len` | Maximum context length (input + output tokens) | Model-dependent | 4096-32768 based on use case |
| `--max-num-seqs` | Maximum concurrent sequences in a batch | 256 | 256-1024 for throughput |
| `--gpu-memory-utilization` | NPU memory utilization ratio | 0.90 | 0.85-0.95, leave headroom for overhead |
| `--enforce-eager` | Disable graph mode, use eager execution | False | True for debugging only |
| `--enable-prefix-caching` | Cache common prompt prefixes | False | True for repeated prompts |
| `--enable-chunked-prefill` | Process prefill in chunks | False | True for long contexts |
| `--tensor-parallel-size` | Number of NPUs for tensor parallelism | 1 | Match available NPUs |
| `--pipeline-parallel-size` | Number of pipeline stages | 1 | For very large models |
| `--max-num-batched-tokens` | Maximum tokens in a batch | Model-dependent | Increase for throughput |
| `--swap-space` | CPU swap space size (GiB) | 4 | 4-16 depending on load |

## Optimization Strategies

### Memory Optimization

Memory management is critical for stable performance on Ascend NPUs:

**1. Adjust Memory Utilization**
```bash
# Leave 10-15% headroom for system overhead
--gpu-memory-utilization 0.90
```

**2. Enable Prefix Caching**
```bash
# Cache common prompt prefixes to reduce redundant computation
--enable-prefix-caching
```

**3. Configure Swap Space**
```bash
# Allocate CPU swap space for offloading when NPU memory is full
--swap-space 8
```

**4. Limit Sequence Length**
```bash
# Set appropriate max-model-len to prevent OOM
--max-model-len 4096
```

### Throughput Optimization

Maximize requests processed per second:

**1. Increase Batch Size**
```bash
# Allow more concurrent sequences
--max-num-seqs 512
--max-num-batched-tokens 4096
```

**2. Enable Chunked Prefill**
```bash
# Process prefill and decode together for better pipeline utilization
--enable-chunked-prefill
```

**3. Use Tensor Parallelism**
```bash
# Distribute model across multiple NPUs
--tensor-parallel-size 8
```

**4. Optimize Scheduling**
```bash
# Adjust scheduling delay for batch formation
--scheduling-policy fcfs  # or priority
```

### Latency Optimization

Minimize time-to-first-token and inter-token latency:

**1. Enable CUDA Graph (Ascend Graph Mode)**
```bash
# Use graph mode for faster execution (default behavior)
# Do NOT use --enforce-eager in production
```

**2. Reduce Batch Size**
```bash
# Smaller batches for lower latency
--max-num-seqs 64
```

**3. Optimize Context Length**
```bash
# Process shorter sequences faster
--max-model-len 2048
```

## Benchmarking Guide

### Using benchmark.py

The official benchmark script tests inference performance:

```bash
python scripts/benchmark.py \
  --model /path/to/model \
  --tensor-parallel-size 8 \
  --num-prompts 100 \
  --max-model-len 4096 \
  --max-num-seqs 256
```

### Benchmark Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--model` | Model path or HF name | `/path/to/llama-7b` |
| `--tensor-parallel-size` | NPU count for TP | `8` |
| `--pipeline-parallel-size` | Pipeline stages | `1` |
| `--num-prompts` | Total requests to test | `100` |
| `--max-model-len` | Context length limit | `4096` |
| `--input-len` | Fixed input length | `1024` |
| `--output-len` | Fixed output length | `128` |
| `--seed` | Random seed | `0` |

### Interpreting Results

Typical benchmark output:

```
Throughput: 234.56 requests/s
Latency (mean): 4.32 ms/token
Latency (P50): 4.15 ms/token
Latency (P90): 5.78 ms/token
Latency (P99): 7.23 ms/token
Time to first token: 12.34 ms
```

**Key Metrics:**

- **Throughput**: Higher is better. Depends on batch size and model parallelism.
- **Latency (P50/P90/P99)**: Lower is better. P99 indicates worst-case latency.
- **Time to First Token (TTFT)**: Critical for interactive applications.

### Performance Baselines

Expected performance on Ascend 910B (varies by model):

| Model | TP Size | Throughput | Latency (P50) |
|-------|---------|------------|---------------|
| Llama2-7B | 1 | ~120 req/s | ~4 ms/token |
| Llama2-7B | 8 | ~800 req/s | ~3 ms/token |
| Llama2-70B | 8 | ~150 req/s | ~8 ms/token |
| Qwen2-72B | 8 | ~140 req/s | ~9 ms/token |

## Performance Tuning Tips

### Common Bottlenecks

**1. NPU Memory Exhaustion**
- Symptom: OOM errors, request failures
- Solution: Reduce `--max-model-len`, increase `--swap-space`, or lower `--max-num-seqs`

**2. CPU Overhead**
- Symptom: Low NPU utilization, high scheduling overhead
- Solution: Enable chunked prefill, increase batch sizes

**3. Communication Overhead**
- Symptom: Poor scaling with tensor parallelism
- Solution: Check HCCL configuration, ensure high-bandwidth interconnect

**4. Graph Compilation Time**
- Symptom: Long warmup time on first requests
- Solution: Warm up with representative inputs before serving

### Recommended Configurations

**High Throughput Serving:**
```bash
vllm serve /path/to/model \
  --tensor-parallel-size 8 \
  --max-num-seqs 512 \
  --max-model-len 4096 \
  --enable-prefix-caching \
  --enable-chunked-prefill \
  --gpu-memory-utilization 0.92
```

**Low Latency Serving:**
```bash
vllm serve /path/to/model \
  --tensor-parallel-size 2 \
  --max-num-seqs 64 \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.85
```

**Long Context Serving:**
```bash
vllm serve /path/to/model \
  --tensor-parallel-size 8 \
  --max-model-len 32768 \
  --max-num-seqs 128 \
  --enable-chunked-prefill \
  --gpu-memory-utilization 0.88
```

### Monitoring Performance

Monitor these metrics during serving:

```bash
# NPU utilization
npu-smi info

# Memory usage
npu-smi info -t memory

# Process-level stats
npu-smi info -t processes
```

Key indicators:
- **NPU Utilization**: Should be >80% during load
- **Memory Usage**: Should stay below 95% to avoid OOM
- **Temperature**: Monitor for thermal throttling

## References

- [vLLM Performance Best Practices](https://docs.vllm.ai/en/latest/getting_started/debugging.html)
- [vLLM-Ascend Documentation](https://docs.vllm.ai/projects/ascend/en/latest/)
- [Ascend NPU Performance Guide](https://www.hiascend.com/document/detail/zh/canncommercial/81RC1/envdeployment/instg/instg_0045.html)
