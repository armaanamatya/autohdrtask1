# Folder 2 Deduplication Report: 2

**Generated:** 2026-01-03 01:36:11

## Summary

| Metric | Value |
|--------|-------|
| **Input Images** | 11 |
| **Output Images** | 1 |
| **Duplicates Removed** | 10 |
| **Removal Rate** | 90.9% |
| **Comparisons Made** | 10 |
| **Status** | ✅ Success |

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

## Statistics

### All Comparisons

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| MTB % | 61.05 | 60.53 | 48.71 | 72.18 | 8.68 |
| Edge % | 6.70 | 6.80 | 4.92 | 8.44 | 1.03 |
| SSIM % | 21.22 | 21.48 | 8.13 | 32.97 | 9.27 |
| CLIP % | 92.19 | 91.24 | 88.07 | 96.08 | 2.76 |
| PDQ HD | 128.80 | 127.00 | 118 | 148 | 7.96 |
| SIFT Matches | 385.20 | 328.00 | 138 | 742 | 196.56 |
| Composite Score | 0.535 | 0.529 | 0.484 | 0.580 | 0.035 |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 10 | 100.0% |
| **Kept (Unique)** | 0 | 0.0% |

## Dropped Images (10)

These images were identified as duplicates and removed:

### DSC00201.jpg

![DSC00201.jpg](thumbnails/2_DSC00201_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00201.jpg`

### DSC00206.jpg

![DSC00206.jpg](thumbnails/2_DSC00206_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00206.jpg`

### DSC00211.jpg

![DSC00211.jpg](thumbnails/2_DSC00211_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00211.jpg`

### DSC00216.jpg

![DSC00216.jpg](thumbnails/2_DSC00216_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00216.jpg`

### DSC00221.jpg

![DSC00221.jpg](thumbnails/2_DSC00221_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00221.jpg`

### DSC00226.jpg

![DSC00226.jpg](thumbnails/2_DSC00226_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00226.jpg`

### DSC00231.jpg

![DSC00231.jpg](thumbnails/2_DSC00231_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00231.jpg`

### DSC00236.jpg

![DSC00236.jpg](thumbnails/2_DSC00236_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00236.jpg`

### DSC00241.jpg

![DSC00241.jpg](thumbnails/2_DSC00241_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00241.jpg`

### DSC00246.jpg

![DSC00246.jpg](thumbnails/2_DSC00246_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00246.jpg`


## Kept Images (1)

These images were kept as unique:

### DSC00251.jpg

![DSC00251.jpg](thumbnails/2_DSC00251_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\2\processed\DSC00251.jpg`


## Comparison Details (10 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| DSC00201 | DSC00206 | 55.0 | 7.4 | 13.4 | 94.7 | 132 | 489 | 0.52 | ✅ Yes | duplicate |
| DSC00206 | DSC00211 | 52.8 | 6.5 | 12.0 | 95.7 | 128 | 264 | 0.51 | ✅ Yes | duplicate |
| DSC00211 | DSC00216 | 48.7 | 5.9 | 11.8 | 90.3 | 136 | 274 | 0.48 | ✅ Yes | duplicate |
| DSC00216 | DSC00221 | 50.3 | 5.7 | 8.1 | 91.5 | 148 | 138 | 0.49 | ✅ Yes | duplicate |
| DSC00221 | DSC00226 | 58.7 | 7.5 | 15.8 | 89.6 | 126 | 203 | 0.52 | ✅ Yes | duplicate |
| DSC00226 | DSC00231 | 69.9 | 6.0 | 30.8 | 95.1 | 118 | 742 | 0.58 | ✅ Yes | duplicate |
| DSC00231 | DSC00236 | 69.5 | 7.1 | 31.1 | 96.1 | 124 | 356 | 0.58 | ✅ Yes | duplicate |
| DSC00236 | DSC00241 | 72.2 | 8.4 | 29.0 | 88.1 | 128 | 346 | 0.57 | ✅ Yes | duplicate |
| DSC00241 | DSC00246 | 71.1 | 7.5 | 33.0 | 89.9 | 122 | 730 | 0.57 | ✅ Yes | duplicate |
| DSC00246 | DSC00251 | 62.4 | 4.9 | 27.2 | 91.0 | 126 | 310 | 0.54 | ✅ Yes | duplicate |

