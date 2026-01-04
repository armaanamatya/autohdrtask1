# Folder 1 Deduplication Report: 1

**Generated:** 2026-01-03 18:34:47

## Summary

| Metric | Value |
|--------|-------|
| **Input Images** | 20 |
| **Output Images** | 12 |
| **Duplicates Removed** | 8 |
| **Removal Rate** | 40.0% |
| **Comparisons Made** | 19 |
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
| MTB % | 55.75 | 54.03 | 47.08 | 70.14 | 6.90 |
| Edge % | 6.66 | 2.96 | 1.00 | 40.52 | 8.92 |
| SSIM % | 36.17 | 39.76 | 3.56 | 73.59 | 18.30 |
| CLIP % | 88.00 | 90.45 | 73.94 | 97.03 | 7.47 |
| PDQ HD | 124.42 | 126.00 | 82 | 140 | 13.62 |
| SIFT Matches | 211.63 | 93.00 | 5 | 1742 | 381.08 |
| Composite Score | 0.563 | 0.573 | 0.399 | 0.760 | 0.085 |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 8 | 42.1% |
| **Kept (Unique)** | 11 | 57.9% |

## Dropped Images (8)

These images were identified as duplicates and removed:

### IMG_3725.jpg

![IMG_3725.jpg](thumbnails/1_IMG_3725_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3725.jpg`

### IMG_3734.jpg

![IMG_3734.jpg](thumbnails/1_IMG_3734_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3734.jpg`

### IMG_3737.jpg

![IMG_3737.jpg](thumbnails/1_IMG_3737_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3737.jpg`

### IMG_3751.jpg

![IMG_3751.jpg](thumbnails/1_IMG_3751_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3751.jpg`

### IMG_3754.jpg

![IMG_3754.jpg](thumbnails/1_IMG_3754_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3754.jpg`

### IMG_3766.jpg

![IMG_3766.jpg](thumbnails/1_IMG_3766_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3766.jpg`

### IMG_3772.jpg

![IMG_3772.jpg](thumbnails/1_IMG_3772_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3772.jpg`

### IMG_3773.jpg

![IMG_3773.jpg](thumbnails/1_IMG_3773_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3773.jpg`


## Kept Images (12)

These images were kept as unique:

### IMG_3722.jpg

![IMG_3722.jpg](thumbnails/1_IMG_3722_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3722.jpg`

### IMG_3726.jpg

![IMG_3726.jpg](thumbnails/1_IMG_3726_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3726.jpg`

### IMG_3731.jpg

![IMG_3731.jpg](thumbnails/1_IMG_3731_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3731.jpg`

### IMG_3740.jpg

![IMG_3740.jpg](thumbnails/1_IMG_3740_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3740.jpg`

### IMG_3743.jpg

![IMG_3743.jpg](thumbnails/1_IMG_3743_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3743.jpg`

### IMG_3746.jpg

![IMG_3746.jpg](thumbnails/1_IMG_3746_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3746.jpg`

### IMG_3757.jpg

![IMG_3757.jpg](thumbnails/1_IMG_3757_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3757.jpg`

### IMG_3760.jpg

![IMG_3760.jpg](thumbnails/1_IMG_3760_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3760.jpg`

### IMG_3768.jpg

![IMG_3768.jpg](thumbnails/1_IMG_3768_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3768.jpg`

### IMG_3771.jpg

![IMG_3771.jpg](thumbnails/1_IMG_3771_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3771.jpg`

### IMG_3774.jpg

![IMG_3774.jpg](thumbnails/1_IMG_3774_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3774.jpg`

### IMG_3775.jpg

![IMG_3775.jpg](thumbnails/1_IMG_3775_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3775.jpg`


## Comparison Details (19 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| IMG_3722 | IMG_3725 | 49.3 | 1.0 | 39.3 | 75.0 | 116 | 5 | 0.42 | ❌ No | MTB < 58.0 |
| IMG_3725 | IMG_3726 | 60.0 | 1.7 | 41.5 | 87.5 | 128 | 89 | 0.60 | ✅ Yes | duplicate |
| IMG_3726 | IMG_3731 | 49.7 | 4.8 | 44.0 | 91.2 | 130 | 93 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_3731 | IMG_3734 | 54.3 | 2.1 | 47.4 | 87.3 | 126 | 79 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_3734 | IMG_3737 | 66.5 | 8.2 | 55.4 | 92.5 | 124 | 49 | 0.60 | ✅ Yes | duplicate |
| IMG_3737 | IMG_3740 | 69.9 | 3.4 | 51.2 | 97.0 | 126 | 168 | 0.69 | ✅ Yes | duplicate |
| IMG_3740 | IMG_3743 | 50.3 | 2.4 | 38.3 | 95.5 | 140 | 145 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_3743 | IMG_3746 | 48.7 | 1.8 | 27.1 | 78.0 | 138 | 94 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_3746 | IMG_3751 | 52.0 | 2.0 | 26.9 | 77.5 | 122 | 45 | 0.48 | ❌ No | MTB < 58.0 |
| IMG_3751 | IMG_3754 | 59.6 | 4.2 | 39.8 | 89.2 | 116 | 203 | 0.63 | ✅ Yes | duplicate |
| IMG_3754 | IMG_3757 | 62.4 | 3.0 | 48.5 | 90.4 | 122 | 104 | 0.65 | ✅ Yes | duplicate |
| IMG_3757 | IMG_3760 | 54.8 | 1.0 | 41.6 | 81.2 | 134 | 45 | 0.50 | ❌ No | MTB < 58.0 |
| IMG_3760 | IMG_3766 | 55.0 | 1.7 | 38.0 | 96.0 | 138 | 48 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_3766 | IMG_3768 | 70.1 | 40.5 | 73.6 | 96.9 | 82 | 154 | 0.76 | ✅ Yes | duplicate |
| IMG_3768 | IMG_3771 | 53.6 | 2.0 | 49.4 | 82.7 | 120 | 40 | 0.51 | ❌ No | MTB < 58.0 |
| IMG_3771 | IMG_3772 | 51.2 | 14.1 | 9.5 | 73.9 | 136 | 22 | 0.40 | ❌ No | MTB < 58.0 |
| IMG_3772 | IMG_3773 | 50.6 | 11.4 | 4.5 | 93.7 | 122 | 1742 | 0.56 | ✅ Yes | duplicate |
| IMG_3773 | IMG_3774 | 54.0 | 11.1 | 7.6 | 93.5 | 104 | 506 | 0.60 | ✅ Yes | duplicate |
| IMG_3774 | IMG_3775 | 47.1 | 10.1 | 3.6 | 93.2 | 140 | 390 | 0.53 | ❌ No | SCORE < 0.55 |

