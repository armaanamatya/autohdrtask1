# SSIM Enabled No SIFT Override

**Date:** 2025-12-29 00:32:59

## Configuration

| Parameter | Value |
|-----------|-------|
| USE_CLIP | True |
| WEIGHT_MTB | 0.3 |
| WEIGHT_SSIM | 0.1 |
| WEIGHT_CLIP | 0.25 |
| WEIGHT_PDQ | 0.25 |
| WEIGHT_SIFT | 0.1 |
| COMPOSITE_DUP_THRESHOLD | 0.35 |
| MTB_HARD_FLOOR | 67.0 |
| PDQ_HD_CEIL | 115 |
| SIFT_MIN_MATCHES | 50 |

## Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|
| 008_Nancy Peppin - IMG_0009 | 009_Nancy Peppin - IMG_0003 | 61.0 | 16.1 | 9.1 | 95.8 | 102 | 1982 | 0.56 | No (MTB < 67.0) |
| 009_Nancy Peppin - IMG_0003 | 050_Scott Wall - DSC_0098 | 47.0 | 12.8 | 4.0 | 72.0 | 136 | 225 | 0.43 | No (MTB < 67.0) |
| 050_Scott Wall - DSC_0098 | 053_Scott Wall - DSC_0143 | 57.7 | 5.5 | 11.4 | 98.2 | 136 | 3128 | 0.53 | No (MTB < 67.0) |

## Summary

- **Input:** 4 groups
- **Output:** 4 groups
- **Duplicates removed:** 0

## Terminal Output

```
2025-12-29 00:32:40,007 [INFO] Number of groups before deduplication: 4
2025-12-29 00:32:40,007 [INFO] Using full_scan=False: Only comparing adjacent images (sequential pairs)
2025-12-29 00:32:40,007 [INFO] [STEP] Pre-computing metrics for 4 middles…
2025-12-29 00:32:44,412 [WARNING] No metadata_dict provided, using empty dict for aerial detection
2025-12-29 00:32:44,412 [INFO] [STEP] Multi-metric dedup (weighted score, full_scan=False)
2025-12-29 00:32:50,600 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 009_Nancy Peppin - IMG_0003 : MTB=61.0  Edge=16.1  SSIM=9.1  CLIP=95.8  PDQ=102  SIFT=1982  SCORE=0.56 [REGULAR]
2025-12-29 00:32:50,600 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-29 00:32:50,600 [INFO]      With:      photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-29 00:32:55,871 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 050_Scott Wall - DSC_0098 : MTB=47.0  Edge=12.8  SSIM=4.0  CLIP=72.0  PDQ=136  SIFT=225  SCORE=0.43 [REGULAR]
2025-12-29 00:32:55,871 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-29 00:32:55,871 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-29 00:32:59,197 [INFO]   • 050_Scott Wall - DSC_0098 ↔ 053_Scott Wall - DSC_0143 : MTB=57.7  Edge=5.5  SSIM=11.4  CLIP=98.2  PDQ=136  SIFT=3128  SCORE=0.53 [REGULAR]
2025-12-29 00:32:59,197 [INFO]      Comparing: photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-29 00:32:59,197 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-29 00:32:59,197 [INFO] [RESULT] stacks: 4 → 4
2025-12-29 00:32:59,197 [INFO] Number of groups after deduplication: 4
```
