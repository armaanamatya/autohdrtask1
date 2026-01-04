# Folder Deduplication Report (with pHash): 1

**Generated:** 2026-01-03 19:06:20

## Summary

| Metric | Value |
|--------|-------|
| **Input Images** | 20 |
| **Output Images** | 13 |
| **Duplicates Removed** | 7 |
| **Removal Rate** | 35.0% |
| **Comparisons Made** | 19 |
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
| MTB % | 55.75 | 54.03 | 47.08 | 70.14 | 6.90 |
| Edge % | 6.66 | 2.96 | 1.00 | 40.52 | 8.92 |
| SSIM % | 36.17 | 39.76 | 3.56 | 73.59 | 18.30 |
| CLIP % | 88.00 | 90.45 | 73.94 | 97.03 | 7.47 |
| PDQ HD | 124.42 | 126.00 | 82 | 140 | 13.62 |
| pHash HD ✨ | 30.32 | 32.00 | 20 | 38 | 4.55 |
| SIFT Matches | 211.63 | 93.00 | 5 | 1742 | 381.08 |
| Composite Score | 0.536 | 0.545 | 0.385 | 0.722 | 0.079 |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 7 | 36.8% |
| **Kept (Unique)** | 13 | 68.4% |

## Dropped Images (7)

These images were identified as duplicates and removed:

### IMG_3754.jpg

![IMG_3754.jpg](thumbnails/1_IMG_3754_thumb.jpg)

**Path:** `1\processed\IMG_3754.jpg`

### IMG_3734.jpg

![IMG_3734.jpg](thumbnails/1_IMG_3734_thumb.jpg)

**Path:** `1\processed\IMG_3734.jpg`

### IMG_3766.jpg

![IMG_3766.jpg](thumbnails/1_IMG_3766_thumb.jpg)

**Path:** `1\processed\IMG_3766.jpg`

### IMG_3725.jpg

![IMG_3725.jpg](thumbnails/1_IMG_3725_thumb.jpg)

**Path:** `1\processed\IMG_3725.jpg`

### IMG_3737.jpg

![IMG_3737.jpg](thumbnails/1_IMG_3737_thumb.jpg)

**Path:** `1\processed\IMG_3737.jpg`

### IMG_3751.jpg

![IMG_3751.jpg](thumbnails/1_IMG_3751_thumb.jpg)

**Path:** `1\processed\IMG_3751.jpg`

### IMG_3773.jpg

![IMG_3773.jpg](thumbnails/1_IMG_3773_thumb.jpg)

**Path:** `1\processed\IMG_3773.jpg`

## Kept Images (13)

These images were kept as unique:

### IMG_3722.jpg

![IMG_3722.jpg](thumbnails/1_IMG_3722_thumb.jpg)

**Path:** `1\processed\IMG_3722.jpg`

### IMG_3726.jpg

![IMG_3726.jpg](thumbnails/1_IMG_3726_thumb.jpg)

**Path:** `1\processed\IMG_3726.jpg`

### IMG_3731.jpg

![IMG_3731.jpg](thumbnails/1_IMG_3731_thumb.jpg)

**Path:** `1\processed\IMG_3731.jpg`

### IMG_3740.jpg

![IMG_3740.jpg](thumbnails/1_IMG_3740_thumb.jpg)

**Path:** `1\processed\IMG_3740.jpg`

### IMG_3743.jpg

![IMG_3743.jpg](thumbnails/1_IMG_3743_thumb.jpg)

**Path:** `1\processed\IMG_3743.jpg`

### IMG_3746.jpg

![IMG_3746.jpg](thumbnails/1_IMG_3746_thumb.jpg)

**Path:** `1\processed\IMG_3746.jpg`

### IMG_3757.jpg

![IMG_3757.jpg](thumbnails/1_IMG_3757_thumb.jpg)

**Path:** `1\processed\IMG_3757.jpg`

### IMG_3760.jpg

![IMG_3760.jpg](thumbnails/1_IMG_3760_thumb.jpg)

**Path:** `1\processed\IMG_3760.jpg`

### IMG_3768.jpg

![IMG_3768.jpg](thumbnails/1_IMG_3768_thumb.jpg)

**Path:** `1\processed\IMG_3768.jpg`

### IMG_3771.jpg

![IMG_3771.jpg](thumbnails/1_IMG_3771_thumb.jpg)

**Path:** `1\processed\IMG_3771.jpg`

### IMG_3772.jpg

![IMG_3772.jpg](thumbnails/1_IMG_3772_thumb.jpg)

**Path:** `1\processed\IMG_3772.jpg`

### IMG_3774.jpg

![IMG_3774.jpg](thumbnails/1_IMG_3774_thumb.jpg)

**Path:** `1\processed\IMG_3774.jpg`

### IMG_3775.jpg

![IMG_3775.jpg](thumbnails/1_IMG_3775_thumb.jpg)

**Path:** `1\processed\IMG_3775.jpg`

