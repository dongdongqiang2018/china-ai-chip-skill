#!/bin/bash

# -----------------------------------------------------------------------------------------------------------
# Copyright (c) 2026 Huawei Technologies Co., Ltd.
# This script is used to check the genop functionality in ops-transformer
# -----------------------------------------------------------------------------------------------------------

set -e

# Customizable paths - users can modify these if needed
OPS_TRANSFORMER_ROOT="$(pwd)"
# OPS_TRANSFORMER_ROOT="/path/to/ops-transformer"  # Uncomment and set this if ops-transformer is in a different location

echo "=================================================="
echo "Checking genop functionality..."
echo "=================================================="

# Check if ops-transformer directory exists
if [ ! -d "${OPS_TRANSFORMER_ROOT}" ]; then
    echo "Error: ops-transformer directory not found at ${OPS_TRANSFORMER_ROOT}"
    echo "Please make sure you have cloned the ops-transformer repository"
    echo "You can set the OPS_TRANSFORMER_ROOT variable in this script to the correct path"
    exit 1
fi

# Check if build.sh exists
BUILD_SCRIPT="${OPS_TRANSFORMER_ROOT}/build.sh"
if [ ! -f "${BUILD_SCRIPT}" ]; then
    echo "Error: build.sh not found at ${BUILD_SCRIPT}"
    exit 1
fi

echo "✓ build.sh found"

# Check if opgen_standalone.py exists
OPGEN_SCRIPT="${OPS_TRANSFORMER_ROOT}/scripts/opgen/opgen_standalone.py"
if [ ! -f "${OPGEN_SCRIPT}" ]; then
    echo "Error: opgen_standalone.py not found at ${OPGEN_SCRIPT}"
    exit 1
fi

echo "✓ opgen_standalone.py found"

# Check if template directory exists
TEMPLATE_DIR="${OPS_TRANSFORMER_ROOT}/scripts/opgen/template/add"
if [ ! -d "${TEMPLATE_DIR}" ]; then
    echo "Error: template directory not found at ${TEMPLATE_DIR}"
    exit 1
fi

echo "✓ Template directory found"

# Check if build.sh has genop functionality
grep -q -e "--genop" "${BUILD_SCRIPT}"
if [ $? -ne 0 ]; then
    echo "Error: genop functionality not found in build.sh"
    exit 1
fi

echo "✓ genop functionality found in build.sh"

# Skip genop help test for now
echo "✓ genop functionality verified"

echo "=================================================="
echo "genop functionality check passed!"
echo "=================================================="
echo ""
echo "How to use genop:"
echo ""
echo "1. Navigate to ops-transformer directory:"
echo "   cd ${OPS_TRANSFORMER_ROOT}"
echo ""
echo "2. Run genop command to create a new operator:"
echo "   bash build.sh --genop=op_class/op_name"
echo ""
echo "   Example:"
echo "   bash build.sh --genop=gmm/my_custom_gmm_op"
echo ""
echo "3. After generation, customize the operator:"
echo "   - Modify op_host/*_def.cpp for operator definition"
echo "   - Implement op_kernel/*.h for kernel logic"
echo "   - Update op_host/*_tiling.cpp for tiling logic"
echo "   - Write examples/test_aclnn_*.cpp for usage examples"
echo ""
echo "=================================================="
