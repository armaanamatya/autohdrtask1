# Folder 2 Deduplication Report: 2

**Generated:** 2026-01-03 19:56:55

## Summary

| Metric | Value |
|--------|-------|
| **Input Images** | 11 |
| **Output Images** | 5 |
| **Duplicates Removed** | 6 |
| **Removal Rate** | 54.5% |
| **Comparisons Made** | 10 |
| **Status** | ✅ Success |

## Configuration

| Parameter | Value |
|-----------|-------|
| USE_CLIP | True |
| WEIGHT_MTB | 0.4 |
| WEIGHT_SSIM | 0.1 |
| WEIGHT_CLIP | 0.2 |
| WEIGHT_PDQ | 0.15 |
| WEIGHT_SIFT | 0.15 |
| COMPOSITE_DUP_THRESHOLD | 0.55 |
| MTB_HARD_FLOOR | 58.0 |
| PDQ_HD_CEIL | 140 |
| SIFT_MIN_MATCHES | 150 |

## Statistics

### All Comparisons

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| MTB % | 59.43 | 57.72 | 46.56 | 71.95 | 7.83 |
| Edge % | 6.49 | 6.81 | 4.92 | 7.48 | 0.88 |
| SSIM % | 19.40 | 15.85 | 8.13 | 31.10 | 8.66 |
| CLIP % | 91.78 | 90.83 | 87.36 | 96.81 | 2.91 |
| PDQ HD | 132.20 | 132.00 | 118 | 148 | 8.92 |
| SIFT Matches | 332.90 | 308.00 | 138 | 583 | 128.02 |
| Composite Score | 0.600 | 0.593 | 0.520 | 0.671 | 0.047 |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 6 | 60.0% |
| **Kept (Unique)** | 4 | 40.0% |

## Dropped Images (6)

These images were identified as duplicates and removed:

### DSC00206.jpg

![DSC00206.jpg](thumbnails/2_DSC00206_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00206.jpg`

### DSC00211.jpg

![DSC00211.jpg](thumbnails/2_DSC00211_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00211.jpg`

### DSC00226.jpg

![DSC00226.jpg](thumbnails/2_DSC00226_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00226.jpg`

### DSC00236.jpg

![DSC00236.jpg](thumbnails/2_DSC00236_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00236.jpg`

### DSC00241.jpg

![DSC00241.jpg](thumbnails/2_DSC00241_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00241.jpg`

### DSC00251.jpg

![DSC00251.jpg](thumbnails/2_DSC00251_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00251.jpg`


## Kept Images (5)

These images were kept as unique:

### DSC00201.jpg

![DSC00201.jpg](thumbnails/2_DSC00201_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00201.jpg`

### DSC00216.jpg

![DSC00216.jpg](thumbnails/2_DSC00216_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00216.jpg`

### DSC00221.jpg

![DSC00221.jpg](thumbnails/2_DSC00221_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00221.jpg`

### DSC00231.jpg

![DSC00231.jpg](thumbnails/2_DSC00231_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00231.jpg`

### DSC00246.jpg

![DSC00246.jpg](thumbnails/2_DSC00246_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00246.jpg`


## Comparison Details (10 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| DSC00201 | DSC00206 | 55.0 | 7.4 | 13.4 | 94.7 | 132 | 489 | 0.58 | ✅ Yes | duplicate |
| DSC00201 | DSC00211 | 56.1 | 7.1 | 14.1 | 96.8 | 132 | 583 | 0.59 | ✅ Yes | duplicate |
| DSC00201 | DSC00216 | 46.6 | 5.8 | 8.6 | 87.4 | 144 | 293 | 0.52 | ❌ No | MTB < 58.0 |
| DSC00216 | DSC00221 | 50.3 | 5.7 | 8.1 | 91.5 | 148 | 138 | 0.54 | ❌ No | MTB < 58.0 |
| DSC00221 | DSC00226 | 58.7 | 7.5 | 15.8 | 89.6 | 126 | 203 | 0.59 | ✅ Yes | duplicate |
| DSC00221 | DSC00231 | 56.7 | 7.3 | 15.9 | 90.2 | 132 | 229 | 0.58 | ❌ No | MTB < 58.0 |
| DSC00231 | DSC00236 | 69.5 | 7.1 | 31.1 | 96.1 | 124 | 356 | 0.67 | ✅ Yes | duplicate |
| DSC00231 | DSC00241 | 71.9 | 6.5 | 30.1 | 89.9 | 118 | 306 | 0.67 | ✅ Yes | duplicate |
| DSC00231 | DSC00246 | 67.2 | 5.5 | 29.6 | 90.6 | 140 | 422 | 0.63 | ❌ No | PDQ >= 140 |
| DSC00246 | DSC00251 | 62.4 | 4.9 | 27.2 | 91.0 | 126 | 310 | 0.62 | ✅ Yes | duplicate |

