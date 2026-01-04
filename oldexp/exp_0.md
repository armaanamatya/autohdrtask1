# Experiment 0 - No CLIP (MTB 0.55, PDQ 0.45, threshold 0.35)

**Date:** 2025-12-26 21:07:09

## Configuration

| Parameter | Value |
|-----------|-------|
| USE_CLIP | False |
| WEIGHT_MTB | 0.55 |
| WEIGHT_SSIM | 0.0 |
| WEIGHT_CLIP | 0.0 |
| WEIGHT_PDQ | 0.45 |
| COMPOSITE_DUP_THRESHOLD | 0.35 |
| MTB_HARD_FLOOR | 67.0 |
| PDQ_HD_CEIL | 115 |

## Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|-------|----------|
| 008_Nancy Peppin - IMG_0009 | 009_Nancy Peppin - IMG_0003 | 61.0 | 16.1 | 9.1 | 0.0 | 102 | 0.39 | No (MTB < 67.0) |
| 009_Nancy Peppin - IMG_0003 | 050_Scott Wall - DSC_0098 | 47.0 | 12.8 | 4.0 | 0.0 | 136 | 0.26 | No (MTB < 67.0) |
| 050_Scott Wall - DSC_0098 | 053_Scott Wall - DSC_0143 | 57.7 | 5.5 | 11.4 | 0.0 | 136 | 0.32 | No (MTB < 67.0) |

## Summary

- **Input:** 4 groups
- **Output:** 4 groups
- **Duplicates removed:** 0

## Terminal Output

```
2025-12-26 21:07:08,138 [INFO] Number of groups before deduplication: 4
2025-12-26 21:07:08,138 [INFO] Using full_scan=False: Only comparing adjacent images (sequential pairs)
2025-12-26 21:07:08,138 [INFO] [STEP] Pre-computing metrics for 4 middles…
2025-12-26 21:07:09,732 [WARNING] No metadata_dict provided, using empty dict for aerial detection
2025-12-26 21:07:09,732 [INFO] [STEP] Multi-metric dedup (weighted score, full_scan=False)
2025-12-26 21:07:09,739 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 009_Nancy Peppin - IMG_0003 : MTB=61.0  Edge=16.1  SSIM=9.1  CLIP=0.0  PDQ=102  SCORE=0.39 [REGULAR]
2025-12-26 21:07:09,739 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-26 21:07:09,739 [INFO]      With:      photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-26 21:07:09,746 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 050_Scott Wall - DSC_0098 : MTB=47.0  Edge=12.8  SSIM=4.0  CLIP=0.0  PDQ=136  SCORE=0.26 [REGULAR]
2025-12-26 21:07:09,747 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-26 21:07:09,747 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-26 21:07:09,753 [INFO]   • 050_Scott Wall - DSC_0098 ↔ 053_Scott Wall - DSC_0143 : MTB=57.7  Edge=5.5  SSIM=11.4  CLIP=0.0  PDQ=136  SCORE=0.32 [REGULAR]
2025-12-26 21:07:09,753 [INFO]      Comparing: photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-26 21:07:09,753 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-26 21:07:09,753 [INFO] [RESULT] stacks: 4 → 4
2025-12-26 21:07:09,753 [INFO] Number of groups after deduplication: 4
```
