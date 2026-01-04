# Differences: `dedup_fixed_drift.py` vs `deduplicationoriginal.py`

## Overview

`dedup_fixed_drift.py` improves performance and fixes a sequential chain drift bug present in the original implementation.

---

## 1. Sequential Chain Drift Fix

### Problem (Original)
- **Comparison pattern**: `(i, i+1)` - compares each frame against the immediately previous frame
- **Bug**: Chain drift occurs when:
  - Frame A → Frame B: similar → B dropped
  - Frame B → Frame C: similar → C dropped  
  - But Frame A and C are completely different!
- **Result**: False positives accumulate as the chain drifts away from the original reference

### Solution (Fixed Drift)
- **Comparison pattern**: Each frame compared against **last KEPT frame** (not previous frame)
- **Logic**: 
  - Start with frame 0 as reference
  - Compare frame i against `last_kept_idx`
  - If frame i is kept → update `last_kept_idx = i`
  - If frame i is dropped → keep same reference for next comparison
- **Result**: Prevents drift by maintaining a stable reference point

---

## 2. Metric Weights

### Original
- **Regular**: MTB=0.55, SSIM=0.0, CLIP=0.0, PDQ=0.45
- **Aerial**: MTB=0.55, SSIM=0.0, CLIP=0.0, PDQ=0.45
- **Issue**: Only uses 2 metrics (MTB + PDQ), ignores SSIM/CLIP

### Fixed Drift
- **Regular**: MTB=0.40, SSIM=0.10, CLIP=0.20, PDQ=0.15, **SIFT=0.15**
- **Aerial**: MTB=0.40, SSIM=0.10, CLIP=0.25, PDQ=0.15, **SIFT=0.10**
- **Improvement**: Multi-metric approach with 5 metrics for better accuracy

---

## 3. Threshold Adjustments

### Safety Guardrails

| Metric | Original (Regular) | Fixed Drift (Regular) | Change |
|--------|-------------------|----------------------|--------|
| MTB_HARD_FLOOR | 67.0 | 58.0 | **-9.0** (more lenient) |
| PDQ_HD_CEIL | 115 | 140 | **+25** (more lenient) |

| Metric | Original (Aerial) | Fixed Drift (Aerial) | Change |
|--------|------------------|---------------------|--------|
| MTB_HARD_FLOOR | 62.0 | 55.0 | **-7.0** (more lenient) |
| PDQ_HD_CEIL | 130 | 130 | **No change** |

### Composite Thresholds

| Type | Original | Fixed Drift | Change |
|------|----------|-------------|--------|
| Regular COMPOSITE_DUP_THRESHOLD | 0.35 | 0.55 | **+0.20** (stricter) |
| Aerial COMPOSITE_DUP_THRESHOLD | 0.32 | 0.38 | **+0.06** (stricter) |

**Rationale**: Lower guardrails allow more comparisons, but higher composite threshold requires stronger overall similarity to drop.

---

## 4. SIFT Feature Matching

### New Addition
- **SIFT_MIN_MATCHES**: 150 (regular), 100 (aerial)
- **SIFT weight**: 0.15 (regular), 0.10 (aerial)
- **SIFT score**: `min(sift_matches / 100.0, 1.0)`

### SIFT Override Mechanism
Allows bypassing MTB/PDQ guardrails when:
1. **High SIFT**: `sift_matches >= sift_min * 3.0` (450 for regular, 300 for aerial)
2. **Combo**: `sift_matches >= sift_min` AND `clip >= 92.0`

**Purpose**: Strong feature matches indicate true duplicates even if MTB/PDQ suggest otherwise.

---

## 5. Performance Improvements

### Multi-Metric Scoring
- **Original**: Binary MTB/PDQ check → limited nuance
- **Fixed**: Weighted composite of 5 metrics → better duplicate detection

### Stricter Composite Threshold
- **Original**: 0.35 threshold → more false positives
- **Fixed**: 0.55 threshold → fewer false positives, better precision

### SIFT Override
- Handles edge cases where structural metrics fail but feature matching succeeds
- Prevents false negatives in challenging scenarios (lighting changes, slight rotations)

---

## Summary

| Aspect | Original | Fixed Drift |
|--------|----------|-------------|
| **Comparison** | `(i, i+1)` - chain drift bug | `(last_kept, i)` - stable reference |
| **Metrics** | 2 (MTB, PDQ) | 5 (MTB, SSIM, CLIP, PDQ, SIFT) |
| **Guardrails** | Stricter (67.0, 115) | More lenient (58.0, 140) |
| **Composite Threshold** | Lower (0.35) | Higher (0.55) |
| **SIFT** | ❌ Not used | ✅ With override mechanism |
| **Result** | Chain drift, limited metrics | Stable reference, multi-metric accuracy |

