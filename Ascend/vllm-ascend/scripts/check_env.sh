#!/bin/bash
set -e
echo "Checking environment..."

# Check CANN installation
if [ -f /usr/local/Ascend/ascend-toolkit/set_env.sh ]; then
    source /usr/local/Ascend/ascend-toolkit/set_env.sh
    echo "✓ CANN environment loaded"
else
    echo "✗ CANN environment not found at /usr/local/Ascend/ascend-toolkit/set_env.sh"
    exit 1
fi

# Check torch-npu installation
if python -c "import torch_npu" 2>/dev/null; then
    echo "✓ torch-npu installed"
else
    echo "✗ torch-npu not installed"
    exit 1
fi

# Check vllm-ascend installation
if python -c "import vllm_ascend" 2>/dev/null; then
    echo "✓ vllm-ascend installed"
else
    echo "✗ vllm-ascend not installed"
    exit 1
fi

# Check NPU devices via npu-smi
if command -v npu-smi &> /dev/null; then
    npu-smi info
    echo "✓ NPU devices available"
else
    echo "✗ npu-smi command not found"
    exit 1
fi

echo "Environment check complete!"
