# Folder Deduplication Report (with pHash): 2

**Generated:** 2026-01-03 19:08:02

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
| WEIGHT_MTB | 0.38 |
| WEIGHT_SSIM | 0.1 |
| WEIGHT_CLIP | 0.2 |
| WEIGHT_PDQ | 0.14 |
| WEIGHT_PHASH | 0.05 ✨ |
| WEIGHT_SIFT | 0.13 |
| COMPOSITE_DUP_THRESHOLD | 0.55 |
| MTB_HARD_FLOOR | 58.0 |
| PDQ_HD_CEIL | 140 |
| PHASH_HD_CEIL | 20 ✨ |
| SIFT_MIN_MATCHES | 150 |

## Statistics

### All Comparisons

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------||
| MTB % | 61.05 | 60.53 | 48.71 | 72.18 | 8.68 |
| Edge % | 6.70 | 6.80 | 4.92 | 8.44 | 1.03 |
| SSIM % | 21.22 | 21.48 | 8.13 | 32.97 | 9.27 |
| CLIP % | 92.19 | 91.24 | 88.07 | 96.08 | 2.76 |
| PDQ HD | 128.80 | 127.00 | 118 | 148 | 7.96 |
| pHash HD ✨ | 30.20 | 30.00 | 28 | 34 | 1.89 |
| SIFT Matches | 385.20 | 328.00 | 138 | 742 | 196.56 |
| Composite Score | 0.580 | 0.576 | 0.511 | 0.638 | 0.047 |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 6 | 60.0% |
| **Kept (Unique)** | 5 | 50.0% |

## Dropped Images (6)

These images were identified as duplicates and removed:

### DSC00241.jpg

![DSC00241.jpg](thumbnails/2_DSC00241_thumb.jpg)

**Path:** `2\processed\DSC00241.jpg`

### DSC00231.jpg

![DSC00231.jpg](thumbnails/2_DSC00231_thumb.jpg)

**Path:** `2\processed\DSC00231.jpg`

### DSC00226.jpg

![DSC00226.jpg](thumbnails/2_DSC00226_thumb.jpg)

**Path:** `2\processed\DSC00226.jpg`

### DSC00246.jpg

![DSC00246.jpg](thumbnails/2_DSC00246_thumb.jpg)

**Path:** `2\processed\DSC00246.jpg`

### DSC00221.jpg

![DSC00221.jpg](thumbnails/2_DSC00221_thumb.jpg)

**Path:** `2\processed\DSC00221.jpg`

### DSC00236.jpg

![DSC00236.jpg](thumbnails/2_DSC00236_thumb.jpg)

**Path:** `2\processed\DSC00236.jpg`

## Kept Images (5)

These images were kept as unique:

### DSC00201.jpg

![DSC00201.jpg](thumbnails/2_DSC00201_thumb.jpg)

**Path:** `2\processed\DSC00201.jpg`

### DSC00206.jpg

![DSC00206.jpg](thumbnails/2_DSC00206_thumb.jpg)

**Path:** `2\processed\DSC00206.jpg`

### DSC00211.jpg

![DSC00211.jpg](thumbnails/2_DSC00211_thumb.jpg)

**Path:** `2\processed\DSC00211.jpg`

### DSC00216.jpg

![DSC00216.jpg](thumbnails/2_DSC00216_thumb.jpg)

**Path:** `2\processed\DSC00216.jpg`

### DSC00251.jpg

![DSC00251.jpg](thumbnails/2_DSC00251_thumb.jpg)

**Path:** `2\processed\DSC00251.jpg`

