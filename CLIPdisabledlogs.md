# CLIP Disabled Experiment

**Date:** 2025-12-25 04:27:55

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
| 008_Nancy Peppin - IMG_0009 | 050_Scott Wall - DSC_0098 | 46.8 | 11.1 | 6.2 | 0.0 | 144 | 0.26 | No (MTB < 67.0) |
| 008_Nancy Peppin - IMG_0009 | 053_Scott Wall - DSC_0143 | 46.8 | 9.9 | 5.9 | 0.0 | 140 | 0.26 | No (MTB < 67.0) |
| 009_Nancy Peppin - IMG_0003 | 050_Scott Wall - DSC_0098 | 47.0 | 12.8 | 4.0 | 0.0 | 136 | 0.26 | No (MTB < 67.0) |
| 009_Nancy Peppin - IMG_0003 | 053_Scott Wall - DSC_0143 | 47.1 | 13.5 | 3.8 | 0.0 | 128 | 0.26 | No (MTB < 67.0) |
| 050_Scott Wall - DSC_0098 | 053_Scott Wall - DSC_0143 | 57.7 | 5.5 | 11.4 | 0.0 | 136 | 0.32 | No (MTB < 67.0) |

## Summary

- **Input:** 4 groups
- **Output:** 4 groups
- **Duplicates removed:** 0

## Terminal Output

```
2025-12-25 04:27:54,203 [INFO] Number of groups before deduplication: 4
2025-12-25 04:27:54,203 [INFO] [STEP] Pre-computing metrics for 4 middles…
2025-12-25 04:27:55,935 [WARNING] No metadata_dict provided, using empty dict for aerial detection
2025-12-25 04:27:55,935 [INFO] [STEP] Multi-metric dedup (weighted score, full_scan=True)
2025-12-25 04:27:55,943 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 009_Nancy Peppin - IMG_0003 : MTB=61.0  Edge=16.1  SSIM=9.1  CLIP=0.0  PDQ=102  SCORE=0.39 [REGULAR]
2025-12-25 04:27:55,943 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:27:55,943 [INFO]      With:      photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:27:55,949 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 050_Scott Wall - DSC_0098 : MTB=46.8  Edge=11.1  SSIM=6.2  CLIP=0.0  PDQ=144  SCORE=0.26 [REGULAR]
2025-12-25 04:27:55,949 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:27:55,950 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:27:55,956 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 053_Scott Wall - DSC_0143 : MTB=46.8  Edge=9.9  SSIM=5.9  CLIP=0.0  PDQ=140  SCORE=0.26 [REGULAR]
2025-12-25 04:27:55,956 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:27:55,956 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:27:55,964 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 050_Scott Wall - DSC_0098 : MTB=47.0  Edge=12.8  SSIM=4.0  CLIP=0.0  PDQ=136  SCORE=0.26 [REGULAR]
2025-12-25 04:27:55,964 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:27:55,964 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:27:55,970 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 053_Scott Wall - DSC_0143 : MTB=47.1  Edge=13.5  SSIM=3.8  CLIP=0.0  PDQ=128  SCORE=0.26 [REGULAR]
2025-12-25 04:27:55,970 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:27:55,970 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:27:55,977 [INFO]   • 050_Scott Wall - DSC_0098 ↔ 053_Scott Wall - DSC_0143 : MTB=57.7  Edge=5.5  SSIM=11.4  CLIP=0.0  PDQ=136  SCORE=0.32 [REGULAR]
2025-12-25 04:27:55,977 [INFO]      Comparing: photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:27:55,977 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:27:55,977 [INFO] [RESULT] stacks: 4 → 4
2025-12-25 04:27:55,977 [INFO] Number of groups after deduplication: 4
```
