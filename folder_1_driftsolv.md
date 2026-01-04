# Folder 1 Deduplication Report: 1

**Generated:** 2026-01-03 19:55:31

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
| MTB % | 55.45 | 52.10 | 47.08 | 70.14 | 6.53 |
| Edge % | 6.47 | 2.69 | 1.00 | 40.52 | 8.76 |
| SSIM % | 35.12 | 38.28 | 3.56 | 73.59 | 18.32 |
| CLIP % | 86.95 | 89.17 | 74.97 | 96.89 | 7.34 |
| PDQ HD | 128.00 | 128.00 | 82 | 156 | 14.70 |
| SIFT Matches | 200.42 | 90.00 | 5 | 1742 | 375.12 |
| Composite Score | 0.558 | 0.558 | 0.420 | 0.760 | 0.076 |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 7 | 36.8% |
| **Kept (Unique)** | 12 | 63.2% |

## Dropped Images (7)

These images were identified as duplicates and removed:

### IMG_3726.jpg

![IMG_3726.jpg](thumbnails/1_IMG_3726_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3726.jpg`

### IMG_3737.jpg

![IMG_3737.jpg](thumbnails/1_IMG_3737_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3737.jpg`

### IMG_3754.jpg

![IMG_3754.jpg](thumbnails/1_IMG_3754_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3754.jpg`

### IMG_3757.jpg

![IMG_3757.jpg](thumbnails/1_IMG_3757_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3757.jpg`

### IMG_3768.jpg

![IMG_3768.jpg](thumbnails/1_IMG_3768_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3768.jpg`

### IMG_3771.jpg

![IMG_3771.jpg](thumbnails/1_IMG_3771_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3771.jpg`

### IMG_3773.jpg

![IMG_3773.jpg](thumbnails/1_IMG_3773_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3773.jpg`


## Kept Images (13)

These images were kept as unique:

### IMG_3722.jpg

![IMG_3722.jpg](thumbnails/1_IMG_3722_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3722.jpg`

### IMG_3725.jpg

![IMG_3725.jpg](thumbnails/1_IMG_3725_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3725.jpg`

### IMG_3731.jpg

![IMG_3731.jpg](thumbnails/1_IMG_3731_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3731.jpg`

### IMG_3734.jpg

![IMG_3734.jpg](thumbnails/1_IMG_3734_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3734.jpg`

### IMG_3740.jpg

![IMG_3740.jpg](thumbnails/1_IMG_3740_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3740.jpg`

### IMG_3743.jpg

![IMG_3743.jpg](thumbnails/1_IMG_3743_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3743.jpg`

### IMG_3746.jpg

![IMG_3746.jpg](thumbnails/1_IMG_3746_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3746.jpg`

### IMG_3751.jpg

![IMG_3751.jpg](thumbnails/1_IMG_3751_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3751.jpg`

### IMG_3760.jpg

![IMG_3760.jpg](thumbnails/1_IMG_3760_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3760.jpg`

### IMG_3766.jpg

![IMG_3766.jpg](thumbnails/1_IMG_3766_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3766.jpg`

### IMG_3772.jpg

![IMG_3772.jpg](thumbnails/1_IMG_3772_thumb.jpg)

**Path:** `C:\Users\Armaan\Desktop\autohdrtask1\1\processed\IMG_3772.jpg`

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
| IMG_3725 | IMG_3731 | 51.1 | 2.5 | 37.9 | 81.7 | 146 | 90 | 0.54 | ❌ No | MTB < 58.0 |
| IMG_3731 | IMG_3734 | 54.3 | 2.1 | 47.4 | 87.3 | 126 | 79 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_3734 | IMG_3737 | 66.5 | 8.2 | 55.4 | 92.5 | 124 | 49 | 0.60 | ✅ Yes | duplicate |
| IMG_3734 | IMG_3740 | 65.1 | 2.7 | 52.0 | 89.6 | 156 | 44 | 0.56 | ❌ No | PDQ >= 140 |
| IMG_3740 | IMG_3743 | 50.3 | 2.4 | 38.3 | 95.5 | 140 | 145 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_3743 | IMG_3746 | 48.7 | 1.8 | 27.1 | 78.0 | 138 | 94 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_3746 | IMG_3751 | 52.0 | 2.0 | 26.9 | 77.5 | 122 | 45 | 0.48 | ❌ No | MTB < 58.0 |
| IMG_3751 | IMG_3754 | 59.6 | 4.2 | 39.8 | 89.2 | 116 | 203 | 0.63 | ✅ Yes | duplicate |
| IMG_3751 | IMG_3757 | 60.3 | 2.9 | 44.8 | 92.3 | 128 | 106 | 0.63 | ✅ Yes | duplicate |
| IMG_3751 | IMG_3760 | 52.1 | 6.2 | 34.4 | 77.7 | 126 | 47 | 0.48 | ❌ No | MTB < 58.0 |
| IMG_3760 | IMG_3766 | 55.0 | 1.7 | 38.0 | 96.0 | 138 | 48 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_3766 | IMG_3768 | 70.1 | 40.5 | 73.6 | 96.9 | 82 | 154 | 0.76 | ✅ Yes | duplicate |
| IMG_3766 | IMG_3771 | 60.1 | 1.2 | 49.1 | 82.0 | 126 | 131 | 0.62 | ✅ Yes | duplicate |
| IMG_3766 | IMG_3772 | 50.1 | 8.8 | 8.5 | 75.1 | 130 | 44 | 0.44 | ❌ No | MTB < 58.0 |
| IMG_3772 | IMG_3773 | 50.6 | 11.4 | 4.5 | 93.7 | 122 | 1742 | 0.56 | ✅ Yes | duplicate |
| IMG_3772 | IMG_3774 | 51.2 | 11.5 | 5.3 | 91.6 | 128 | 303 | 0.56 | ❌ No | MTB < 58.0 |
| IMG_3774 | IMG_3775 | 47.1 | 10.1 | 3.6 | 93.2 | 140 | 390 | 0.53 | ❌ No | SCORE < 0.55 |

