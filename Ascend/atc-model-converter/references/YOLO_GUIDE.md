# YOLO Model Guide for Ascend NPU

Detailed guide for converting and running YOLO models on Huawei Ascend NPU.

---

## Supported YOLO Versions & Tasks

| Version | Detection | Pose | Segmentation | OBB | Classification |
|---------|-----------|------|--------------|-----|----------------|
| YOLOv5 | ✅ | - | ✅ | - | - |
| YOLOv8 | ✅ | ✅ | ✅ | ✅ | ✅ |
| YOLO11 | ✅ | ✅ | ✅ | ✅ | ✅ |
| YOLO26 | ✅ | ✅ | ✅ | ✅ | ✅ |

> **Note:** This guide focuses on detection, pose, segmentation, and OBB tasks. Classification is a simple forward pass.

---

## YOLO Output Format Reference

Understanding YOLO ONNX output formats is critical for correct post-processing.

### Detection Output

**Shape:** `(1, 84, 8400)` for YOLOv8/v11/YOLO26 with 80 COCO classes

**Format:**
- 84 channels = 4 (box) + 80 (class scores)
- 8400 anchors = (640/8)² + (640/16)² + (640/32)² = 64 + 256 + 1024 = 1344 (for 640 input)

**Layout:**
```
output[0, 0:4, :]    → Box coordinates (cx, cy, w, h) for each anchor
output[0, 4:84, :]   → Class scores for each anchor
```

**Post-processing Steps:**
1. Transpose to `(8400, 84)`
2. Extract boxes: `predictions[:, :4]` (cx, cy, w, h)
3. Extract class scores: `predictions[:, 4:]`
4. Get best class: `scores = class_scores.max(axis=1)`
5. Filter by confidence threshold
6. Convert boxes to xyxy format
7. Apply NMS (Non-Maximum Suppression)

### Pose Output

**Shape:** `(1, 300, 57)` for COCO 17 keypoints

**Format:**
- 300 = top-k detections (already sorted by confidence)
- 57 = 4 (box) + 1 (box conf) + 1 (class) + 51 (17 keypoints × 3)

**Layout:**
```
output[0, :, 0:4]    → Box coordinates (x1, y1, x2, y2) - already in corner format
output[0, :, 4]      → Box confidence
output[0, :, 5]      → Class score (always 0 for person)
output[0, :, 6:57]   → Keypoints: (x, y, conf) × 17
```

**Post-processing Steps:**
1. Filter by confidence (no NMS needed - already top-k)
2. Parse keypoints: reshape `output[:, 6:]` to `(N, 17, 3)`
3. Scale boxes and keypoints to original image size

**COCO Keypoints (17):**
```
0: nose        5: left_shoulder   9: left_wrist    13: left_ankle
1: left_eye    6: right_shoulder  10: right_wrist  14: right_ankle
2: right_eye   7: left_elbow      11: left_hip     15: left_knee
3: left_ear    8: right_elbow     12: right_hip    16: right_knee
4: right_ear
```

### Segmentation Output

**Shape:** `(1, 116, 8400)` for 80 classes + 32 mask coefficients

**Format:**
- 116 = 4 (box) + 80 (class) + 32 (mask coefficients)
- Two outputs possible: (detection_output, mask_protos)

**Layout:**
```
output[0, 0:4, :]     → Box coordinates (cx, cy, w, h)
output[0, 4:84, :]    → Class scores
output[0, 84:116, :]  → Mask coefficients (32 values per anchor)
```

**Post-processing Steps:**
1. Same as detection for boxes
2. Extract mask coefficients
3. If mask_protos available, compute masks: `masks = sigmoid(mask_protos @ mask_coeffs.T)`

### OBB (Oriented Bounding Box) Output

**Shape:** `(1, 15, 8400)` for DOTA 15 classes

**Format:**
- 15 = 4 (box) + 1 (angle) + 10 (class scores) or similar

**Layout:**
```
output[0, 0:4, :]    → Box coordinates (cx, cy, w, h)
output[0, 4, :]      → Rotation angle in radians
output[0, 5:15, :]   → Class scores
```

**Post-processing Steps:**
1. Same as detection for filtering
2. Keep angle information with boxes
3. Draw rotated rectangles using angle

---

## Post-Processing Code Examples

### Detection Post-Processing

```python
import numpy as np

def postprocess_detect(output, conf_thres=0.25, iou_thres=0.45):
    """
    Post-process YOLO detection output.
    
    Args:
        output: Model output of shape (1, 84, 8400)
        conf_thres: Confidence threshold
        iou_thres: IoU threshold for NMS
    
    Returns:
        boxes_xyxy: (N, 4) array of boxes in xyxy format
        scores: (N,) array of confidence scores
        class_ids: (N,) array of class indices
    """
    # Transpose to (num_anchors, 4+classes)
    predictions = output[0].T  # (8400, 84)
    
    # Extract boxes and class scores
    boxes_cxcywh = predictions[:, :4]  # cx, cy, w, h
    class_scores = predictions[:, 4:]
    
    # Get best class for each anchor
    scores = class_scores.max(axis=1)
    class_ids = class_scores.argmax(axis=1)
    
    # Filter by confidence
    mask = scores >= conf_thres
    boxes_cxcywh = boxes_cxcywh[mask]
    scores = scores[mask]
    class_ids = class_ids[mask]
    
    if len(boxes_cxcywh) == 0:
        return np.array([]), np.array([]), np.array([])
    
    # Convert cx, cy, w, h to x1, y1, x2, y2
    boxes_xyxy = np.zeros_like(boxes_cxcywh)
    boxes_xyxy[:, 0] = boxes_cxcywh[:, 0] - boxes_cxcywh[:, 2] / 2  # x1
    boxes_xyxy[:, 1] = boxes_cxcywh[:, 1] - boxes_cxcywh[:, 3] / 2  # y1
    boxes_xyxy[:, 2] = boxes_cxcywh[:, 0] + boxes_cxcywh[:, 2] / 2  # x2
    boxes_xyxy[:, 3] = boxes_cxcywh[:, 1] + boxes_cxcywh[:, 3] / 2  # y2
    
    # Apply NMS
    keep = nms_numpy(boxes_xyxy, scores, iou_thres)
    
    return boxes_xyxy[keep], scores[keep], class_ids[keep]

def nms_numpy(boxes, scores, iou_threshold):
    """Non-Maximum Suppression using NumPy."""
    if len(boxes) == 0:
        return np.array([], dtype=np.int64)
    
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        
        # Calculate IoU
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        
        iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]
    
    return np.array(keep, dtype=np.int64)
```

### Pose Post-Processing

```python
def postprocess_pose(output, conf_thres=0.25, num_keypoints=17):
    """
    Post-process YOLO pose output.
    
    Args:
        output: Model output of shape (1, 300, 57)
        conf_thres: Confidence threshold
        num_keypoints: Number of keypoints (17 for COCO)
    
    Returns:
        boxes: (N, 4) array in xyxy format
        scores: (N,) confidence scores
        keypoints: (N, 17, 3) array of (x, y, conf) per keypoint
    """
    predictions = output[0]  # (300, 57)
    
    # Parse output
    boxes = predictions[:, :4]  # Already xyxy
    box_conf = predictions[:, 4]
    class_scores = predictions[:, 5]
    keypoints_flat = predictions[:, 6:]
    
    # Combined score
    scores = box_conf * class_scores
    
    # Filter by confidence
    mask = scores >= conf_thres
    boxes = boxes[mask]
    scores = scores[mask]
    keypoints_flat = keypoints_flat[mask]
    
    # Reshape keypoints to (N, 17, 3)
    keypoints = keypoints_flat.reshape(-1, num_keypoints, 3)
    
    return boxes, scores, keypoints
```

---

## Common Issues and Solutions

### Issue: Confidence > 1.0 for Pose Model

**Symptom:** Detection confidence shows values like 58.16

**Cause:** Using detection post-processing on pose output

**Solution:** Pose output format is different. Use `--task pose` flag:
```bash
python3 scripts/yolo_om_infer.py --model yolo-pose.om --source image.jpg --task pose
```

### Issue: No Detections Found

**Possible causes:**
1. Confidence threshold too high - try `--conf 0.1`
2. Wrong task type - verify model type and use correct `--task`
3. SoC version mismatch - check `npu-smi info` matches `--soc_version`

### Issue: Boxes Not Aligned with Objects

**Cause:** Letterbox padding not removed correctly

**Solution:** Ensure post-processing removes padding offset:
```python
# Calculate padding (letterbox centers image)
pad_h = (input_height - original_height * ratio) / 2
pad_w = (input_width - original_width * ratio) / 2

# Remove padding and scale
x1 = (x1 - pad_w) / ratio
y1 = (y1 - pad_h) / ratio
x2 = (x2 - pad_w) / ratio
y2 = (y2 - pad_h) / ratio
```

### Issue: ONNX Opset Version Error

**Symptom:** `RuntimeError: unsupported operator: ...`

**Solution:** Export with opset 11 for CANN 8.1.RC1:
```python
model.export(format='onnx', imgsz=640, opset=11)
```

---

## Performance Tips

### 1. Use FP16 Precision

```bash
atc --model=yolo.onnx --framework=5 --output=yolo_fp16 \
    --soc_version=Ascend910B3 \
    --precision_mode=force_fp16
```

### 2. Enable Parallel Compilation

```bash
export TE_PARALLEL_COMPILER=16
atc --model=yolo.onnx ...
```

### 3. Batch Processing

For batch inference, modify input shape:
```bash
atc --model=yolo.onnx --framework=5 --output=yolo_batch4 \
    --soc_version=Ascend910B3 \
    --input_shape="images:4,3,640,640"
```

### 4. AIPP for On-Device Preprocessing

Use AIPP to offload preprocessing to NPU:
```bash
atc --model=yolo.onnx --framework=5 --output=yolo_aipp \
    --soc_version=Ascend910B3 \
    --insert_op_conf=aipp.cfg
```

See [AIPP_CONFIG.md](AIPP_CONFIG.md) for AIPP configuration details.

---

## Verification Checklist

Before deploying YOLO models, verify:

- [ ] SoC version matches exactly (`npu-smi info` → `--soc_version`)
- [ ] ONNX opset version is compatible (11 for CANN 8.1.RC1)
- [ ] Python version is 3.7-3.10
- [ ] NumPy version is < 2.0
- [ ] Using correct `--task` parameter for model type
- [ ] Confidence threshold is appropriate (default 0.25)
- [ ] Test with sample images before deployment
