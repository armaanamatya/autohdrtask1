# Deduplication Test Evaluation Report

**Generated:** 2026-01-03 20:11:23

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Folders Processed** | 5 |
| **Total Input Images** | 97 |
| **Total Output Images** | 50 |
| **Total Duplicates Removed** | 47 |
| **Removal Rate** | 48.5% |
| **Total Comparisons** | 92 |

## Configuration

### Regular Photos
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

### Aerial Photos
| Parameter | Value |
|-----------|-------|
| AERIAL_WEIGHT_MTB | 0.4 |
| AERIAL_WEIGHT_SSIM | 0.1 |
| AERIAL_WEIGHT_CLIP | 0.25 |
| AERIAL_WEIGHT_PDQ | 0.15 |
| AERIAL_WEIGHT_SIFT | 0.1 |
| AERIAL_COMPOSITE_DUP_THRESHOLD | 0.38 |
| AERIAL_MTB_HARD_FLOOR | 55.0 |
| AERIAL_PDQ_HD_CEIL | 130 |
| AERIAL_SIFT_MIN_MATCHES | 100 |

## Aggregate Statistics

### All Comparisons

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| MTB % | 57.17 | 56.40 | 43.82 | 71.95 | 6.47 |
| Edge % | 6.03 | 5.87 | 0.11 | 40.52 | 5.17 |
| SSIM % | 26.52 | 26.58 | 3.37 | 73.59 | 13.99 |
| CLIP % | 88.14 | 89.33 | 69.37 | 97.31 | 6.72 |
| PDQ HD | 127.96 | 127.00 | 82 | 156 | 10.12 |
| SIFT Matches | 286.05 | 226.50 | 5 | 1742 | 256.77 |
| Composite Score | 0.579 | 0.580 | 0.420 | 0.760 | 0.055 |

### Dropped vs Kept Comparisons

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 47 | 51.1% |
| **Kept (Unique)** | 45 | 48.9% |

#### Dropped Comparisons Statistics
| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| MTB % | 60.92 | 60.11 | 50.56 | 71.95 |
| CLIP % | 91.18 | 92.23 | 80.51 | 96.89 |
| Composite Score | 0.616 | 0.618 | 0.562 | 0.760 |

#### Kept Comparisons Statistics
| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| MTB % | 53.26 | 52.10 | 43.82 | 67.15 |
| CLIP % | 84.98 | 86.77 | 69.37 | 97.31 |
| Composite Score | 0.541 | 0.544 | 0.420 | 0.630 |

## Per-Folder Results

### Folder 1: 1

| Metric | Value |
|--------|-------|
| **Input Images** | 20 |
| **Output Images** | 13 |
| **Duplicates Removed** | 7 |
| **Removal Rate** | 35.0% |
| **Comparisons Made** | 19 |
| **Status** | ✅ Success |

#### Dropped Images (7)

- `IMG_3726.jpg`
- `IMG_3737.jpg`
- `IMG_3754.jpg`
- `IMG_3757.jpg`
- `IMG_3768.jpg`
- `IMG_3771.jpg`
- `IMG_3773.jpg`

#### Comparison Details (19 comparisons)

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

#### Kept Images (13)

- `IMG_3722.jpg`
- `IMG_3725.jpg`
- `IMG_3731.jpg`
- `IMG_3734.jpg`
- `IMG_3740.jpg`
- `IMG_3743.jpg`
- `IMG_3746.jpg`
- `IMG_3751.jpg`
- `IMG_3760.jpg`
- `IMG_3766.jpg`
- `IMG_3772.jpg`
- `IMG_3774.jpg`
- `IMG_3775.jpg`

### Folder 2: 2

| Metric | Value |
|--------|-------|
| **Input Images** | 11 |
| **Output Images** | 5 |
| **Duplicates Removed** | 6 |
| **Removal Rate** | 54.5% |
| **Comparisons Made** | 10 |
| **Status** | ✅ Success |

#### Dropped Images (6)

- `DSC00206.jpg`
- `DSC00211.jpg`
- `DSC00226.jpg`
- `DSC00236.jpg`
- `DSC00241.jpg`
- `DSC00251.jpg`

#### Comparison Details (10 comparisons)

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

#### Kept Images (5)

- `DSC00201.jpg`
- `DSC00216.jpg`
- `DSC00221.jpg`
- `DSC00231.jpg`
- `DSC00246.jpg`

### Folder 3: 3

| Metric | Value |
|--------|-------|
| **Input Images** | 25 |
| **Output Images** | 17 |
| **Duplicates Removed** | 8 |
| **Removal Rate** | 32.0% |
| **Comparisons Made** | 24 |
| **Status** | ✅ Success |

#### Dropped Images (8)

- `IMG_5506.jpg`
- `IMG_5509.jpg`
- `IMG_5548.jpg`
- `IMG_5560.jpg`
- `IMG_5563.jpg`
- `IMG_5566.jpg`
- `IMG_5572.jpg`
- `IMG_5602.jpg`

#### Comparison Details (24 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| IMG_5503 | IMG_5506 | 64.6 | 8.8 | 16.6 | 96.5 | 118 | 814 | 0.64 | ✅ Yes | duplicate |
| IMG_5503 | IMG_5509 | 52.8 | 9.4 | 12.6 | 95.3 | 126 | 676 | 0.58 | ✅ Yes | duplicate |
| IMG_5503 | IMG_5512 | 46.2 | 6.7 | 16.0 | 71.6 | 128 | 400 | 0.51 | ❌ No | MTB < 58.0 |
| IMG_5512 | IMG_5515 | 57.6 | 1.2 | 31.2 | 92.4 | 136 | 72 | 0.56 | ❌ No | MTB < 58.0 |
| IMG_5515 | IMG_5521 | 49.6 | 1.2 | 41.3 | 79.7 | 120 | 99 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_5521 | IMG_5527 | 60.7 | 0.1 | 59.9 | 75.1 | 118 | 38 | 0.53 | ❌ No | SCORE < 0.55 |
| IMG_5527 | IMG_5530 | 61.2 | 0.5 | 54.6 | 83.2 | 114 | 7 | 0.50 | ❌ No | SCORE < 0.55 |
| IMG_5530 | IMG_5539 | 59.4 | 1.3 | 41.4 | 77.7 | 132 | 58 | 0.53 | ❌ No | SCORE < 0.55 |
| IMG_5539 | IMG_5542 | 54.1 | 2.9 | 35.3 | 97.3 | 150 | 118 | 0.60 | ❌ No | MTB < 58.0 |
| IMG_5542 | IMG_5545 | 55.8 | 2.6 | 33.4 | 97.1 | 132 | 100 | 0.61 | ❌ No | MTB < 58.0 |
| IMG_5545 | IMG_5548 | 64.4 | 2.9 | 32.8 | 95.8 | 120 | 138 | 0.65 | ✅ Yes | duplicate |
| IMG_5545 | IMG_5560 | 62.6 | 3.8 | 39.2 | 86.9 | 130 | 152 | 0.62 | ✅ Yes | duplicate |
| IMG_5545 | IMG_5563 | 59.4 | 2.2 | 33.7 | 91.8 | 124 | 141 | 0.62 | ✅ Yes | duplicate |
| IMG_5545 | IMG_5566 | 62.7 | 5.3 | 36.3 | 91.6 | 124 | 185 | 0.64 | ✅ Yes | duplicate |
| IMG_5545 | IMG_5572 | 63.2 | 2.1 | 39.3 | 87.2 | 126 | 148 | 0.63 | ✅ Yes | duplicate |
| IMG_5545 | IMG_5575 | 56.8 | 1.4 | 37.1 | 87.2 | 136 | 194 | 0.59 | ❌ No | MTB < 58.0 |
| IMG_5575 | IMG_5581 | 43.8 | 0.7 | 33.4 | 89.3 | 136 | 68 | 0.49 | ❌ No | MTB < 58.0 |
| IMG_5581 | IMG_5584 | 53.5 | 4.0 | 26.3 | 91.5 | 138 | 132 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_5584 | IMG_5587 | 49.8 | 2.5 | 32.2 | 87.1 | 126 | 152 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_5587 | IMG_5590 | 53.3 | 1.0 | 39.0 | 87.9 | 122 | 71 | 0.55 | ❌ No | MTB < 58.0 |
| IMG_5590 | IMG_5599 | 66.4 | 0.7 | 43.0 | 92.8 | 148 | 39 | 0.55 | ❌ No | PDQ >= 140 |
| IMG_5599 | IMG_5602 | 59.6 | 0.2 | 45.3 | 92.5 | 126 | 117 | 0.63 | ✅ Yes | duplicate |
| IMG_5599 | IMG_5608 | 48.6 | 1.3 | 31.4 | 86.5 | 118 | 67 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_5608 | IMG_5611 | 57.1 | 2.2 | 34.7 | 84.6 | 124 | 46 | 0.52 | ❌ No | MTB < 58.0 |

#### Kept Images (17)

- `IMG_5503.jpg`
- `IMG_5512.jpg`
- `IMG_5515.jpg`
- `IMG_5521.jpg`
- `IMG_5527.jpg`
- `IMG_5530.jpg`
- `IMG_5539.jpg`
- `IMG_5542.jpg`
- `IMG_5545.jpg`
- `IMG_5575.jpg`
- `IMG_5581.jpg`
- `IMG_5584.jpg`
- `IMG_5587.jpg`
- `IMG_5590.jpg`
- `IMG_5599.jpg`
- `IMG_5608.jpg`
- `IMG_5611.jpg`

### Folder 4: 4

| Metric | Value |
|--------|-------|
| **Input Images** | 40 |
| **Output Images** | 14 |
| **Duplicates Removed** | 26 |
| **Removal Rate** | 65.0% |
| **Comparisons Made** | 39 |
| **Status** | ✅ Success |

#### Dropped Images (26)

- `IMG_0307.jpg`
- `IMG_0312.jpg`
- `IMG_0317.jpg`
- `IMG_0332.jpg`
- `IMG_0337.jpg`
- `IMG_0347.jpg`
- `IMG_0352.jpg`
- `IMG_0367.jpg`
- `IMG_0382.jpg`
- `IMG_0407.jpg`
- `IMG_0412.jpg`
- `IMG_0417.jpg`
- `IMG_0422.jpg`
- `IMG_0433.jpg`
- `IMG_0437.jpg`
- `IMG_0447.jpg`
- `IMG_0453.jpg`
- `IMG_0457.jpg`
- `IMG_0467.jpg`
- `IMG_0692.jpg`
- `IMG_0697.jpg`
- `IMG_0702.jpg`
- `IMG_0707.jpg`
- `IMG_0712.jpg`
- `IMG_0717.jpg`
- `IMG_0722.jpg`

#### Comparison Details (39 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| IMG_0302 | IMG_0307 | 68.5 | 5.9 | 31.2 | 91.3 | 128 | 432 | 0.65 | ✅ Yes | duplicate |
| IMG_0302 | IMG_0312 | 64.0 | 6.4 | 28.4 | 94.7 | 124 | 317 | 0.64 | ✅ Yes | duplicate |
| IMG_0302 | IMG_0317 | 70.0 | 8.1 | 30.3 | 94.6 | 108 | 247 | 0.68 | ✅ Yes | duplicate |
| IMG_0302 | IMG_0322 | 47.8 | 3.3 | 21.5 | 76.6 | 118 | 305 | 0.54 | ❌ No | MTB < 58.0 |
| IMG_0322 | IMG_0327 | 45.4 | 5.3 | 18.3 | 74.6 | 130 | 59 | 0.45 | ❌ No | MTB < 58.0 |
| IMG_0327 | IMG_0332 | 67.2 | 12.6 | 25.2 | 95.7 | 124 | 451 | 0.65 | ✅ Yes | duplicate |
| IMG_0327 | IMG_0337 | 56.9 | 6.9 | 17.1 | 92.2 | 124 | 715 | 0.60 | ✅ Yes | duplicate |
| IMG_0327 | IMG_0342 | 55.5 | 6.9 | 15.4 | 84.2 | 118 | 411 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_0342 | IMG_0347 | 58.0 | 7.4 | 9.2 | 95.0 | 124 | 384 | 0.60 | ✅ Yes | duplicate |
| IMG_0342 | IMG_0352 | 52.8 | 6.7 | 9.7 | 94.5 | 128 | 224 | 0.57 | ✅ Yes | duplicate |
| IMG_0342 | IMG_0357 | 53.0 | 6.8 | 15.1 | 87.4 | 126 | 232 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_0357 | IMG_0367 | 55.7 | 6.2 | 12.8 | 93.7 | 140 | 242 | 0.57 | ✅ Yes | duplicate |
| IMG_0357 | IMG_0372 | 50.8 | 3.2 | 15.5 | 86.7 | 138 | 229 | 0.54 | ❌ No | MTB < 58.0 |
| IMG_0372 | IMG_0377 | 53.4 | 2.2 | 19.8 | 86.8 | 132 | 164 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_0377 | IMG_0382 | 63.3 | 1.4 | 31.3 | 96.1 | 136 | 184 | 0.63 | ✅ Yes | duplicate |
| IMG_0377 | IMG_0387 | 55.1 | 0.9 | 30.5 | 95.6 | 134 | 123 | 0.60 | ❌ No | MTB < 58.0 |
| IMG_0387 | IMG_0392 | 51.6 | 8.8 | 18.6 | 79.0 | 138 | 82 | 0.51 | ❌ No | MTB < 58.0 |
| IMG_0392 | IMG_0397 | 51.5 | 4.6 | 16.0 | 69.4 | 124 | 301 | 0.53 | ❌ No | MTB < 58.0 |
| IMG_0397 | IMG_0402 | 53.3 | 4.8 | 21.5 | 81.0 | 132 | 115 | 0.56 | ❌ No | MTB < 58.0 |
| IMG_0402 | IMG_0407 | 68.0 | 8.3 | 27.4 | 93.4 | 132 | 372 | 0.64 | ✅ Yes | duplicate |
| IMG_0402 | IMG_0412 | 62.3 | 6.8 | 22.8 | 89.8 | 138 | 254 | 0.60 | ✅ Yes | duplicate |
| IMG_0402 | IMG_0417 | 64.9 | 6.5 | 24.5 | 88.3 | 124 | 268 | 0.63 | ✅ Yes | duplicate |
| IMG_0402 | IMG_0422 | 66.5 | 5.8 | 27.0 | 88.9 | 128 | 336 | 0.63 | ✅ Yes | duplicate |
| IMG_0402 | IMG_0427 | 51.8 | 13.6 | 7.6 | 72.2 | 130 | 253 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_0427 | IMG_0433 | 52.5 | 14.5 | 5.8 | 86.5 | 112 | 865 | 0.57 | ✅ Yes | duplicate |
| IMG_0427 | IMG_0437 | 55.0 | 15.5 | 7.6 | 85.5 | 122 | 773 | 0.57 | ✅ Yes | duplicate |
| IMG_0427 | IMG_0442 | 50.6 | 12.4 | 3.4 | 88.0 | 128 | 801 | 0.54 | ❌ No | SCORE < 0.55 |
| IMG_0442 | IMG_0447 | 54.5 | 8.0 | 10.5 | 89.4 | 136 | 524 | 0.56 | ✅ Yes | duplicate |
| IMG_0442 | IMG_0453 | 62.9 | 10.9 | 22.5 | 81.8 | 136 | 448 | 0.59 | ✅ Yes | duplicate |
| IMG_0442 | IMG_0457 | 57.4 | 9.3 | 18.5 | 80.5 | 120 | 504 | 0.58 | ✅ Yes | duplicate |
| IMG_0442 | IMG_0462 | 55.9 | 8.5 | 17.3 | 83.8 | 124 | 448 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_0462 | IMG_0467 | 63.7 | 8.2 | 25.1 | 95.9 | 114 | 504 | 0.65 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0692 | 54.8 | 6.8 | 16.5 | 87.9 | 122 | 519 | 0.58 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0697 | 58.9 | 10.9 | 15.4 | 85.1 | 120 | 516 | 0.59 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0702 | 53.3 | 14.4 | 10.0 | 88.2 | 114 | 491 | 0.58 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0707 | 59.1 | 7.3 | 20.0 | 93.0 | 130 | 526 | 0.60 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0712 | 63.8 | 8.6 | 26.3 | 87.9 | 122 | 526 | 0.63 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0717 | 59.8 | 8.9 | 13.8 | 92.4 | 132 | 521 | 0.60 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0722 | 59.3 | 8.1 | 22.9 | 93.2 | 136 | 482 | 0.60 | ✅ Yes | duplicate |

#### Kept Images (14)

- `IMG_0302.jpg`
- `IMG_0322.jpg`
- `IMG_0327.jpg`
- `IMG_0342.jpg`
- `IMG_0357.jpg`
- `IMG_0372.jpg`
- `IMG_0377.jpg`
- `IMG_0387.jpg`
- `IMG_0392.jpg`
- `IMG_0397.jpg`
- `IMG_0402.jpg`
- `IMG_0427.jpg`
- `IMG_0442.jpg`
- `IMG_0462.jpg`

### Folder 5: 5

| Metric | Value |
|--------|-------|
| **Input Images** | 1 |
| **Output Images** | 1 |
| **Duplicates Removed** | 0 |
| **Removal Rate** | 0.0% |
| **Comparisons Made** | 0 |
| **Status** | ✅ Success |

#### Kept Images (1)

- `0F7A0421.jpg`

## Drop Reason Analysis

| Reason | Count |
|--------|-------|
| duplicate | 47 |
| Not dropped: MTB < 58.0 | 37 |
| Not dropped: SCORE < 0.55 | 5 |
| Not dropped: PDQ >= 140 | 3 |

