# vLLM-Ascend Installation Guide

This guide covers installing vLLM-Ascend on Huawei Ascend NPUs.

## Prerequisites

### System Requirements

| Component | Version |
|-----------|---------|
| Python | >= 3.10, < 3.12 |
| CANN | 8.5.0 |
| torch-npu | 2.5.0 (auto-installed) |
| vLLM | 0.14.1 |
| vLLM-Ascend | 0.14.0rc1 |

### Hardware Support

- Atlas A2 (Ascend 910B)
- Atlas A3 (Ascend 910C)
- Atlas 300I (310P)

### Pre-Installation Checklist

1. **Verify CANN Installation**:
   ```bash
   npu-smi info
   ```
   You should see your NPU devices listed.

2. **Verify Python Version**:
   ```bash
   python --version  # Should be 3.10.x or 3.11.x
   ```

3. **Set CANN Environment Variables** (if not already set):
   ```bash
   source /usr/local/Ascend/ascend-toolkit/set_env.sh
   ```

---

## Docker Installation (Recommended)

The easiest way to get started is using the pre-built Docker images.

### Pull the Appropriate Image

Choose the image matching your hardware:

```bash
# For Atlas A2 (Ascend 910B)
docker pull quay.io/ascend/vllm-ascend:v0.14.0rc1

# For Atlas A3 (Ascend 910C)
docker pull quay.io/ascend/vllm-ascend:v0.14.0rc1-a3

# For Atlas 300I (310P)
docker pull quay.io/ascend/vllm-ascend:v0.14.0rc1-310p
```

### Run the Container

```bash
# For Atlas A2/A3
docker run -it --rm \
  --name vllm-ascend \
  --device /dev/davinci0 \
  --device /dev/davinci1 \
  --device /dev/davinci2 \
  --device /dev/davinci3 \
  --device /dev/davinci_manager \
  --device /dev/devmm_svm \
  --device /dev/hisi_hdc \
  -v /usr/local/Ascend:/usr/local/Ascend:ro \
  -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi:ro \
  quay.io/ascend/vllm-ascend:v0.14.0rc1

# For Atlas 300I (single device)
docker run -it --rm \
  --name vllm-ascend \
  --device /dev/davinci0 \
  --device /dev/davinci_manager \
  --device /dev/devmm_svm \
  --device /dev/hisi_hdc \
  -v /usr/local/Ascend:/usr/local/Ascend:ro \
  -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi:ro \
  quay.io/ascend/vllm-ascend:v0.14.0rc1-310p
```

### Docker Compose Example

```yaml
version: '3.8'
services:
  vllm-ascend:
    image: quay.io/ascend/vllm-ascend:v0.14.0rc1
    container_name: vllm-ascend
    devices:
      - /dev/davinci0
      - /dev/davinci1
      - /dev/davinci2
      - /dev/davinci3
      - /dev/davinci_manager
      - /dev/devmm_svm
      - /dev/hisi_hdc
    volumes:
      - /usr/local/Ascend:/usr/local/Ascend:ro
      - /usr/local/bin/npu-smi:/usr/local/bin/npu-smi:ro
      - /data/models:/models:ro
    environment:
      - ASCEND_RT_VISIBLE_DEVICES=0,1,2,3
    ports:
      - "8000:8000"
    command: >
      python -m vllm.entrypoints.openai.api_server
      --model /models/your-model
      --tensor-parallel-size 4
```

---

## Pip Installation

For custom environments or development, install via pip.

### Step 1: Create Virtual Environment

```bash
python3.10 -m venv vllm-ascend-env
source vllm-ascend-env/bin/activate
```

### Step 2: Install vLLM

```bash
pip install vllm==0.14.1
```

### Step 3: Install vLLM-Ascend

```bash
# Install the Ascend plugin
pip install vllm-ascend==0.14.0rc1
```

This will automatically install compatible versions of:
- `torch-npu` (2.5.0)
- `torch` (matching version)

### Step 4: Verify Installation

```bash
python -c "import vllm; print(vllm.__version__)"
python -c "import vllm_ascend; print(vllm_ascend.__version__)"
python -c "import torch_npu; print(torch_npu.__version__)"
```

---

## Build from Source

For development or customizing vLLM-Ascend.

### Prerequisites

```bash
# Install build dependencies
pip install build wheel setuptools
```

### Step 1: Clone vLLM

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
git checkout v0.14.1
```

### Step 2: Clone vLLM-Ascend

```bash
git clone https://github.com/vllm-project/vllm-ascend.git
cd vllm-ascend
git checkout v0.14.0rc1
```

### Step 3: Install vLLM from Source

```bash
cd vllm
pip install -e .
```

### Step 4: Install vLLM-Ascend from Source

```bash
cd vllm-ascend
pip install -e .
```

### Development Workflow

For active development with editable installs:

```bash
# Terminal 1: vllm source
cd ~/src/vllm
pip install -e .

# Terminal 2: vllm-ascend source
cd ~/src/vllm-ascend
pip install -e .

# Changes to source are immediately reflected
```

---

## Verify Installation

### Python Verification Script

Create `verify_install.py`:

```python
#!/usr/bin/env python3
"""Verify vLLM-Ascend installation."""

import sys

def check_imports():
    """Check all required packages are importable."""
    print("Checking imports...")
    
    try:
        import vllm
        print(f"  vllm: {vllm.__version__}")
    except ImportError as e:
        print(f"  ERROR: vllm import failed: {e}")
        return False
    
    try:
        import vllm_ascend
        print(f"  vllm_ascend: {vllm_ascend.__version__}")
    except ImportError as e:
        print(f"  ERROR: vllm_ascend import failed: {e}")
        return False
    
    try:
        import torch
        print(f"  torch: {torch.__version__}")
    except ImportError as e:
        print(f"  ERROR: torch import failed: {e}")
        return False
    
    try:
        import torch_npu
        print(f"  torch_npu: {torch_npu.__version__}")
    except ImportError as e:
        print(f"  ERROR: torch_npu import failed: {e}")
        return False
    
    return True

def check_npu():
    """Check NPU availability."""
    print("\nChecking NPU availability...")
    
    try:
        import torch
        import torch_npu
        
        npu_count = torch.npu.device_count()
        print(f"  NPU count: {npu_count}")
        
        if npu_count == 0:
            print("  WARNING: No NPUs detected!")
            return False
        
        for i in range(npu_count):
            name = torch.npu.get_device_name(i)
            print(f"  NPU {i}: {name}")
        
        # Test basic operation
        x = torch.randn(2, 3).npu()
        y = x * 2
        print(f"  Basic NPU tensor operation: OK")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: NPU check failed: {e}")
        return False

def check_vllm_ascend():
    """Check vLLM-Ascend plugin registration."""
    print("\nChecking vLLM-Ascend plugin...")
    
    try:
        from vllm import envs
        
        # Check if Ascend platform is registered
        from vllm_ascend.platform import NPUPlatform
        print("  NPUPlatform class: OK")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: vLLM-Ascend check failed: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 50)
    print("vLLM-Ascend Installation Verification")
    print("=" * 50)
    
    results = []
    
    results.append(("Imports", check_imports()))
    results.append(("NPU", check_npu()))
    results.append(("vLLM-Ascend", check_vllm_ascend()))
    
    print("\n" + "=" * 50)
    print("Verification Summary")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("All checks passed! vLLM-Ascend is ready to use.")
        sys.exit(0)
    else:
        print("Some checks failed. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Run Verification

```bash
python verify_install.py
```

Expected output:
```
==================================================
vLLM-Ascend Installation Verification
==================================================
Checking imports...
  vllm: 0.14.1
  vllm_ascend: 0.14.0rc1
  torch: 2.5.0
  torch_npu: 2.5.0

Checking NPU availability...
  NPU count: 4
  NPU 0: Ascend910B
  NPU 1: Ascend910B
  NPU 2: Ascend910B
  NPU 3: Ascend910B
  Basic NPU tensor operation: OK

Checking vLLM-Ascend plugin...
  NPUPlatform class: OK

==================================================
Verification Summary
==================================================
  Imports: PASS
  NPU: PASS
  vLLM-Ascend: PASS
==================================================
All checks passed! vLLM-Ascend is ready to use.
```

---

## Troubleshooting

### ImportError: No module named 'torch_npu'

**Cause**: CANN environment not properly set.

**Solution**:
```bash
source /usr/local/Ascend/ascend-toolkit/set_env.sh
```

### RuntimeError: No NPU devices available

**Cause**: Device permissions or NPU driver issues.

**Solution**:
```bash
# Check NPU status
npu-smi info

# Verify device files exist
ls -la /dev/davinci*

# Check user permissions (should be in hwHiUser group)
groups
```

### Version Mismatch Errors

**Cause**: Incompatible versions of vLLM, vLLM-Ascend, or torch-npu.

**Solution**: Use the exact versions specified:
```bash
pip install vllm==0.14.1
pip install vllm-ascend==0.14.0rc1
```

### Docker: Cannot access NPU devices

**Cause**: Missing device mappings or volume mounts.

**Solution**: Ensure all required devices and volumes are mounted:
- `/dev/davinci*` - NPU devices
- `/dev/davinci_manager` - Device manager
- `/dev/devmm_svm` - Memory management
- `/usr/local/Ascend` - CANN toolkit

---

## Official References

- [vLLM-Ascend Documentation](https://docs.vllm.ai/projects/ascend/en/latest/)
- [vLLM-Ascend GitHub](https://github.com/vllm-project/vllm-ascend)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Ascend CANN Documentation](https://www.hiascend.com/document)
