# Deduplication Experiment Logs

## Experiment 1: Baseline (CLIP Disabled)

**Date:** 2025-12-25  
**Branch:** CLIPenabled (but CLIP disabled for this run)

### Configuration

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

### Test Images

| # | Image Path |
|---|------------|
| 1 | photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg |
| 2 | photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg |
| 3 | photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg |
| 4 | photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg |

### Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|-------|----------|
| Nancy IMG_0009 | Nancy IMG_0003 | 61.0 | 16.1 | 9.1 | 0.0 | 102 | 0.39 | No (MTB < 67) |
| Nancy IMG_0009 | Scott DSC_0098 | 46.8 | 11.1 | 6.2 | 0.0 | 144 | 0.26 | No |
| Nancy IMG_0009 | Scott DSC_0143 | 46.8 | 9.9 | 5.9 | 0.0 | 140 | 0.26 | No |
| Nancy IMG_0003 | Scott DSC_0098 | 47.0 | 12.8 | 4.0 | 0.0 | 136 | 0.26 | No |
| Nancy IMG_0003 | Scott DSC_0143 | 47.1 | 13.5 | 3.8 | 0.0 | 128 | 0.26 | No |
| Scott DSC_0098 | Scott DSC_0143 | 57.7 | 5.5 | 11.4 | 0.0 | 136 | 0.32 | No |

### Summary

- **Input:** 4 groups
- **Output:** 4 groups
- **Duplicates removed:** 0

### Analysis

- Nancy pair (IMG_0009 ↔ IMG_0003): SCORE=0.39 exceeds threshold (0.35), but MTB=61.0% fails the MTB floor (67%)
- Scott pair (DSC_0098 ↔ DSC_0143): SCORE=0.32 below threshold (0.35)
- Cross-property pairs (Nancy ↔ Scott): Low scores (0.26), correctly identified as different

### Terminal Output

```
2025-12-25 04:20:21,457 [INFO] Number of groups before deduplication: 4
2025-12-25 04:20:21,457 [INFO] [STEP] Pre-computing metrics for 4 middles…
2025-12-25 04:20:23,079 [WARNING] No metadata_dict provided, using empty dict for aerial detection
2025-12-25 04:20:23,079 [INFO] [STEP] Multi-metric dedup (weighted score, full_scan=True)
2025-12-25 04:20:23,086 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 009_Nancy Peppin - IMG_0003 : MTB=61.0  Edge=16.1  SSIM=9.1  CLIP=0.0  PDQ=102  SCORE=0.39 [REGULAR]
2025-12-25 04:20:23,086 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:20:23,086 [INFO]      With:      photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:20:23,094 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 050_Scott Wall - DSC_0098 : MTB=46.8  Edge=11.1  SSIM=6.2  CLIP=0.0  PDQ=144  SCORE=0.26 [REGULAR]
2025-12-25 04:20:23,094 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:20:23,094 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:20:23,100 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 053_Scott Wall - DSC_0143 : MTB=46.8  Edge=9.9  SSIM=5.9  CLIP=0.0  PDQ=140  SCORE=0.26 [REGULAR]
2025-12-25 04:20:23,100 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:20:23,100 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:20:23,100 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 050_Scott Wall - DSC_0098 : MTB=47.0  Edge=12.8  SSIM=4.0  CLIP=0.0  PDQ=136  SCORE=0.26 [REGULAR]
2025-12-25 04:20:23,100 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:20:23,100 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:20:23,115 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 053_Scott Wall - DSC_0143 : MTB=47.1  Edge=13.5  SSIM=3.8  CLIP=0.0  PDQ=128  SCORE=0.26 [REGULAR]
2025-12-25 04:20:23,115 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:20:23,115 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:20:23,122 [INFO]   • 050_Scott Wall - DSC_0098 ↔ 053_Scott Wall - DSC_0143 : MTB=57.7  Edge=5.5  SSIM=11.4  CLIP=0.0  PDQ=136  SCORE=0.32 [REGULAR]
2025-12-25 04:20:23,122 [INFO]      Comparing: photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:20:23,122 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:20:23,122 [INFO] [RESULT] stacks: 4 → 4
2025-12-25 04:20:23,122 [INFO] Number of groups after deduplication: 4
```

---

## Experiment 2: CLIP Enabled

**Date:** 2025-12-25  
**Branch:** CLIPenabled

### Configuration

| Parameter | Value |
|-----------|-------|
| USE_CLIP | True |
| WEIGHT_MTB | 0.40 |
| WEIGHT_SSIM | 0.0 |
| WEIGHT_CLIP | 0.25 |
| WEIGHT_PDQ | 0.35 |
| COMPOSITE_DUP_THRESHOLD | 0.35 |
| MTB_HARD_FLOOR | 67.0 |
| PDQ_HD_CEIL | 115 |

### Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|-------|----------|
| Nancy IMG_0009 | Nancy IMG_0003 | 61.0 | 16.1 | 9.1 | 95.8 | 102 | 0.52 | No (MTB < 67) |
| Nancy IMG_0009 | Scott DSC_0098 | 46.8 | 11.1 | 6.2 | 72.9 | 144 | 0.37 | No (MTB < 67) |
| Nancy IMG_0009 | Scott DSC_0143 | 46.8 | 9.9 | 5.9 | 73.1 | 140 | 0.37 | No (MTB < 67) |
| Nancy IMG_0003 | Scott DSC_0098 | 47.0 | 12.8 | 4.0 | 72.0 | 136 | 0.37 | No (MTB < 67) |
| Nancy IMG_0003 | Scott DSC_0143 | 47.1 | 13.5 | 3.8 | 72.4 | 128 | 0.37 | No (MTB < 67) |
| Scott DSC_0098 | Scott DSC_0143 | 57.7 | 5.5 | 11.4 | 98.2 | 136 | 0.48 | No (MTB < 67) |

### Summary

- **Input:** 4 groups
- **Output:** 4 groups
- **Duplicates removed:** 0

### Analysis

- CLIP significantly boosted scores for semantically similar images
- Nancy pair: CLIP=95.8% shows high semantic similarity → SCORE increased from 0.39 to 0.52
- Scott pair: CLIP=98.2% shows very high semantic similarity → SCORE increased from 0.32 to 0.48
- Cross-property pairs: CLIP=72-73% (indoor real estate photos share semantic features)
- **Key finding:** MTB hard floor (67%) prevented all drops despite high CLIP/SCORE values
- **Consideration:** May need to lower MTB_HARD_FLOOR if CLIP-based semantic similarity should override pixel-level differences


---

## Experiment 3: Baseline Rerun

**Date:** 2025-12-25 04:23:52

### Configuration

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

### Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|-------|----------|
| 008_Nancy Peppin - IMG_0009 | 009_Nancy Peppin - IMG_0003 | 61.0 | 16.1 | 9.1 | 0.0 | 102 | 0.39 | No (MTB < 67.0) |
| 008_Nancy Peppin - IMG_0009 | 050_Scott Wall - DSC_0098 | 46.8 | 11.1 | 6.2 | 0.0 | 144 | 0.26 | No (MTB < 67.0) |
| 008_Nancy Peppin - IMG_0009 | 053_Scott Wall - DSC_0143 | 46.8 | 9.9 | 5.9 | 0.0 | 140 | 0.26 | No (MTB < 67.0) |
| 009_Nancy Peppin - IMG_0003 | 050_Scott Wall - DSC_0098 | 47.0 | 12.8 | 4.0 | 0.0 | 136 | 0.26 | No (MTB < 67.0) |
| 009_Nancy Peppin - IMG_0003 | 053_Scott Wall - DSC_0143 | 47.1 | 13.5 | 3.8 | 0.0 | 128 | 0.26 | No (MTB < 67.0) |
| 050_Scott Wall - DSC_0098 | 053_Scott Wall - DSC_0143 | 57.7 | 5.5 | 11.4 | 0.0 | 136 | 0.32 | No (MTB < 67.0) |

### Summary

- **Input:** 4 groups
- **Output:** 4 groups
- **Duplicates removed:** 0

### Terminal Output

```
2025-12-25 04:23:50,597 [INFO] Number of groups before deduplication: 4
2025-12-25 04:23:50,597 [INFO] [STEP] Pre-computing metrics for 4 middles…
2025-12-25 04:23:52,251 [WARNING] No metadata_dict provided, using empty dict for aerial detection
2025-12-25 04:23:52,253 [INFO] [STEP] Multi-metric dedup (weighted score, full_scan=True)
2025-12-25 04:23:52,260 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 009_Nancy Peppin - IMG_0003 : MTB=61.0  Edge=16.1  SSIM=9.1  CLIP=0.0  PDQ=102  SCORE=0.39 [REGULAR]
2025-12-25 04:23:52,260 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:23:52,260 [INFO]      With:      photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:23:52,267 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 050_Scott Wall - DSC_0098 : MTB=46.8  Edge=11.1  SSIM=6.2  CLIP=0.0  PDQ=144  SCORE=0.26 [REGULAR]
2025-12-25 04:23:52,268 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:23:52,268 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:23:52,276 [INFO]   • 008_Nancy Peppin - IMG_0009 ↔ 053_Scott Wall - DSC_0143 : MTB=46.8  Edge=9.9  SSIM=5.9  CLIP=0.0  PDQ=140  SCORE=0.26 [REGULAR]
2025-12-25 04:23:52,276 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\008_Nancy Peppin - IMG_0009.jpg
2025-12-25 04:23:52,276 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:23:52,282 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 050_Scott Wall - DSC_0098 : MTB=47.0  Edge=12.8  SSIM=4.0  CLIP=0.0  PDQ=136  SCORE=0.26 [REGULAR]
2025-12-25 04:23:52,282 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:23:52,282 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:23:52,289 [INFO]   • 009_Nancy Peppin - IMG_0003 ↔ 053_Scott Wall - DSC_0143 : MTB=47.1  Edge=13.5  SSIM=3.8  CLIP=0.0  PDQ=128  SCORE=0.26 [REGULAR]
2025-12-25 04:23:52,289 [INFO]      Comparing: photos-706-winchester-blvd--los-gatos--ca-9\009_Nancy Peppin - IMG_0003.jpg
2025-12-25 04:23:52,289 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:23:52,295 [INFO]   • 050_Scott Wall - DSC_0098 ↔ 053_Scott Wall - DSC_0143 : MTB=57.7  Edge=5.5  SSIM=11.4  CLIP=0.0  PDQ=136  SCORE=0.32 [REGULAR]
2025-12-25 04:23:52,295 [INFO]      Comparing: photos-75-knollview-way--san-francisco--ca\050_Scott Wall - DSC_0098.jpg
2025-12-25 04:23:52,296 [INFO]      With:      photos-75-knollview-way--san-francisco--ca\053_Scott Wall - DSC_0143.jpg
2025-12-25 04:23:52,296 [INFO] [RESULT] stacks: 4 → 4
2025-12-25 04:23:52,296 [INFO] Number of groups after deduplication: 4
```
