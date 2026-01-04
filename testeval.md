# Deduplication Test Evaluation Report

**Generated:** 2026-01-03 18:52:15

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Folders Processed** | 5 |
| **Total Input Images** | 97 |
| **Total Output Images** | 45 |
| **Total Duplicates Removed** | 52 |
| **Removal Rate** | 53.6% |
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
| MTB % | 57.89 | 56.40 | 43.82 | 75.82 | 7.34 |
| Edge % | 6.19 | 5.62 | 0.09 | 40.52 | 5.42 |
| SSIM % | 27.58 | 27.16 | 3.56 | 73.59 | 14.83 |
| CLIP % | 89.17 | 90.73 | 69.37 | 97.31 | 6.72 |
| PDQ HD | 126.50 | 126.00 | 82 | 150 | 9.84 |
| SIFT Matches | 284.67 | 180.00 | 5 | 1742 | 269.13 |
| Composite Score | 0.584 | 0.580 | 0.399 | 0.760 | 0.061 |

### Dropped vs Kept Comparisons

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | 52 | 56.5% |
| **Kept (Unique)** | 40 | 43.5% |

#### Dropped Comparisons Statistics
| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| MTB % | 62.00 | 62.46 | 50.56 | 75.82 |
| CLIP % | 92.55 | 93.56 | 86.49 | 97.15 |
| Composite Score | 0.622 | 0.625 | 0.552 | 0.760 |

#### Kept Comparisons Statistics
| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| MTB % | 52.53 | 51.82 | 43.82 | 66.39 |
| CLIP % | 84.78 | 85.63 | 69.37 | 97.31 |
| Composite Score | 0.534 | 0.539 | 0.399 | 0.609 |

## Per-Folder Results

### Folder 1: 1

| Metric | Value |
|--------|-------|
| **Input Images** | 20 |
| **Output Images** | 12 |
| **Duplicates Removed** | 8 |
| **Removal Rate** | 40.0% |
| **Comparisons Made** | 19 |
| **Status** | ✅ Success |

#### Dropped Images (8)

- `IMG_3725.jpg`
- `IMG_3734.jpg`
- `IMG_3737.jpg`
- `IMG_3751.jpg`
- `IMG_3754.jpg`
- `IMG_3766.jpg`
- `IMG_3772.jpg`
- `IMG_3773.jpg`

#### Comparison Details (19 comparisons)

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

#### Kept Images (12)

- `IMG_3722.jpg`
- `IMG_3726.jpg`
- `IMG_3731.jpg`
- `IMG_3740.jpg`
- `IMG_3743.jpg`
- `IMG_3746.jpg`
- `IMG_3757.jpg`
- `IMG_3760.jpg`
- `IMG_3768.jpg`
- `IMG_3771.jpg`
- `IMG_3774.jpg`
- `IMG_3775.jpg`

### Folder 2: 2

| Metric | Value |
|--------|-------|
| **Input Images** | 11 |
| **Output Images** | 3 |
| **Duplicates Removed** | 8 |
| **Removal Rate** | 72.7% |
| **Comparisons Made** | 10 |
| **Status** | ✅ Success |

#### Dropped Images (8)

- `DSC00201.jpg`
- `DSC00206.jpg`
- `DSC00221.jpg`
- `DSC00226.jpg`
- `DSC00231.jpg`
- `DSC00236.jpg`
- `DSC00241.jpg`
- `DSC00246.jpg`

#### Comparison Details (10 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| DSC00201 | DSC00206 | 55.0 | 7.4 | 13.4 | 94.7 | 132 | 489 | 0.58 | ✅ Yes | duplicate |
| DSC00206 | DSC00211 | 52.8 | 6.5 | 12.0 | 95.7 | 128 | 264 | 0.58 | ✅ Yes | duplicate |
| DSC00211 | DSC00216 | 48.7 | 5.9 | 11.8 | 90.3 | 136 | 274 | 0.54 | ❌ No | MTB < 58.0 |
| DSC00216 | DSC00221 | 50.3 | 5.7 | 8.1 | 91.5 | 148 | 138 | 0.54 | ❌ No | MTB < 58.0 |
| DSC00221 | DSC00226 | 58.7 | 7.5 | 15.8 | 89.6 | 126 | 203 | 0.59 | ✅ Yes | duplicate |
| DSC00226 | DSC00231 | 69.9 | 6.0 | 30.8 | 95.1 | 118 | 742 | 0.67 | ✅ Yes | duplicate |
| DSC00231 | DSC00236 | 69.5 | 7.1 | 31.1 | 96.1 | 124 | 356 | 0.67 | ✅ Yes | duplicate |
| DSC00236 | DSC00241 | 72.2 | 8.4 | 29.0 | 88.1 | 128 | 346 | 0.66 | ✅ Yes | duplicate |
| DSC00241 | DSC00246 | 71.1 | 7.5 | 33.0 | 89.9 | 122 | 730 | 0.67 | ✅ Yes | duplicate |
| DSC00246 | DSC00251 | 62.4 | 4.9 | 27.2 | 91.0 | 126 | 310 | 0.62 | ✅ Yes | duplicate |

#### Kept Images (3)

- `DSC00211.jpg`
- `DSC00216.jpg`
- `DSC00251.jpg`

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

- `IMG_5503.jpg`
- `IMG_5545.jpg`
- `IMG_5548.jpg`
- `IMG_5560.jpg`
- `IMG_5563.jpg`
- `IMG_5566.jpg`
- `IMG_5572.jpg`
- `IMG_5599.jpg`

#### Comparison Details (24 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| IMG_5503 | IMG_5506 | 64.6 | 8.8 | 16.6 | 96.5 | 118 | 814 | 0.64 | ✅ Yes | duplicate |
| IMG_5506 | IMG_5509 | 48.7 | 10.3 | 15.2 | 92.6 | 140 | 465 | 0.54 | ❌ No | SCORE < 0.55 |
| IMG_5509 | IMG_5512 | 47.3 | 6.8 | 16.0 | 74.5 | 134 | 401 | 0.51 | ❌ No | MTB < 58.0 |
| IMG_5512 | IMG_5515 | 57.6 | 1.2 | 31.2 | 92.4 | 136 | 72 | 0.56 | ❌ No | MTB < 58.0 |
| IMG_5515 | IMG_5521 | 49.6 | 1.2 | 41.3 | 79.7 | 120 | 99 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_5521 | IMG_5527 | 60.7 | 0.1 | 59.9 | 75.1 | 118 | 38 | 0.53 | ❌ No | SCORE < 0.55 |
| IMG_5527 | IMG_5530 | 61.2 | 0.5 | 54.6 | 83.2 | 114 | 7 | 0.50 | ❌ No | SCORE < 0.55 |
| IMG_5530 | IMG_5539 | 59.4 | 1.3 | 41.4 | 77.7 | 132 | 58 | 0.53 | ❌ No | SCORE < 0.55 |
| IMG_5539 | IMG_5542 | 54.1 | 2.9 | 35.3 | 97.3 | 150 | 118 | 0.60 | ❌ No | MTB < 58.0 |
| IMG_5542 | IMG_5545 | 55.8 | 2.6 | 33.4 | 97.1 | 132 | 100 | 0.61 | ❌ No | MTB < 58.0 |
| IMG_5545 | IMG_5548 | 64.4 | 2.9 | 32.8 | 95.8 | 120 | 138 | 0.65 | ✅ Yes | duplicate |
| IMG_5548 | IMG_5560 | 70.4 | 3.0 | 40.2 | 87.3 | 134 | 148 | 0.65 | ✅ Yes | duplicate |
| IMG_5560 | IMG_5563 | 62.6 | 0.1 | 43.7 | 95.1 | 114 | 60 | 0.60 | ✅ Yes | duplicate |
| IMG_5563 | IMG_5566 | 69.9 | 0.5 | 40.0 | 97.1 | 126 | 90 | 0.66 | ✅ Yes | duplicate |
| IMG_5566 | IMG_5572 | 67.8 | 1.7 | 44.6 | 90.2 | 126 | 67 | 0.61 | ✅ Yes | duplicate |
| IMG_5572 | IMG_5575 | 75.8 | 2.5 | 59.1 | 94.4 | 116 | 49 | 0.65 | ✅ Yes | duplicate |
| IMG_5575 | IMG_5581 | 43.8 | 0.7 | 33.4 | 89.3 | 136 | 68 | 0.49 | ❌ No | MTB < 58.0 |
| IMG_5581 | IMG_5584 | 53.5 | 4.0 | 26.3 | 91.5 | 138 | 132 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_5584 | IMG_5587 | 49.8 | 2.5 | 32.2 | 87.1 | 126 | 152 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_5587 | IMG_5590 | 53.3 | 1.0 | 39.0 | 87.9 | 122 | 71 | 0.55 | ❌ No | MTB < 58.0 |
| IMG_5590 | IMG_5599 | 66.4 | 0.7 | 43.0 | 92.8 | 148 | 39 | 0.55 | ❌ No | PDQ >= 140 |
| IMG_5599 | IMG_5602 | 59.6 | 0.2 | 45.3 | 92.5 | 126 | 117 | 0.63 | ✅ Yes | duplicate |
| IMG_5602 | IMG_5608 | 50.9 | 4.8 | 41.7 | 82.2 | 120 | 40 | 0.49 | ❌ No | MTB < 58.0 |
| IMG_5608 | IMG_5611 | 57.1 | 2.2 | 34.7 | 84.6 | 124 | 46 | 0.52 | ❌ No | MTB < 58.0 |

#### Kept Images (17)

- `IMG_5506.jpg`
- `IMG_5509.jpg`
- `IMG_5512.jpg`
- `IMG_5515.jpg`
- `IMG_5521.jpg`
- `IMG_5527.jpg`
- `IMG_5530.jpg`
- `IMG_5539.jpg`
- `IMG_5542.jpg`
- `IMG_5575.jpg`
- `IMG_5581.jpg`
- `IMG_5584.jpg`
- `IMG_5587.jpg`
- `IMG_5590.jpg`
- `IMG_5602.jpg`
- `IMG_5608.jpg`
- `IMG_5611.jpg`

### Folder 4: 4

| Metric | Value |
|--------|-------|
| **Input Images** | 40 |
| **Output Images** | 12 |
| **Duplicates Removed** | 28 |
| **Removal Rate** | 70.0% |
| **Comparisons Made** | 39 |
| **Status** | ✅ Success |

#### Dropped Images (28)

- `IMG_0302.jpg`
- `IMG_0307.jpg`
- `IMG_0312.jpg`
- `IMG_0327.jpg`
- `IMG_0332.jpg`
- `IMG_0337.jpg`
- `IMG_0342.jpg`
- `IMG_0347.jpg`
- `IMG_0357.jpg`
- `IMG_0377.jpg`
- `IMG_0382.jpg`
- `IMG_0402.jpg`
- `IMG_0407.jpg`
- `IMG_0412.jpg`
- `IMG_0417.jpg`
- `IMG_0427.jpg`
- `IMG_0433.jpg`
- `IMG_0442.jpg`
- `IMG_0447.jpg`
- `IMG_0453.jpg`
- `IMG_0457.jpg`
- `IMG_0462.jpg`
- `IMG_0692.jpg`
- `IMG_0697.jpg`
- `IMG_0702.jpg`
- `IMG_0707.jpg`
- `IMG_0712.jpg`
- `IMG_0717.jpg`

#### Comparison Details (39 comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
| IMG_0302 | IMG_0307 | 68.5 | 5.9 | 31.2 | 91.3 | 128 | 432 | 0.65 | ✅ Yes | duplicate |
| IMG_0307 | IMG_0312 | 71.5 | 4.6 | 37.8 | 95.8 | 114 | 222 | 0.69 | ✅ Yes | duplicate |
| IMG_0312 | IMG_0317 | 66.3 | 4.5 | 31.4 | 93.7 | 126 | 115 | 0.65 | ✅ Yes | duplicate |
| IMG_0317 | IMG_0322 | 47.8 | 3.6 | 25.0 | 75.3 | 136 | 187 | 0.52 | ❌ No | MTB < 58.0 |
| IMG_0322 | IMG_0327 | 45.4 | 5.3 | 18.3 | 74.6 | 130 | 59 | 0.45 | ❌ No | MTB < 58.0 |
| IMG_0327 | IMG_0332 | 67.2 | 12.6 | 25.2 | 95.7 | 124 | 451 | 0.65 | ✅ Yes | duplicate |
| IMG_0332 | IMG_0337 | 55.5 | 6.8 | 19.0 | 92.9 | 132 | 468 | 0.59 | ✅ Yes | duplicate |
| IMG_0337 | IMG_0342 | 58.3 | 10.4 | 15.9 | 89.2 | 130 | 562 | 0.59 | ✅ Yes | duplicate |
| IMG_0342 | IMG_0347 | 58.0 | 7.4 | 9.2 | 95.0 | 124 | 384 | 0.60 | ✅ Yes | duplicate |
| IMG_0347 | IMG_0352 | 59.7 | 6.1 | 6.8 | 96.5 | 130 | 332 | 0.60 | ✅ Yes | duplicate |
| IMG_0352 | IMG_0357 | 50.3 | 6.6 | 9.7 | 89.9 | 114 | 176 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_0357 | IMG_0367 | 55.7 | 6.2 | 12.8 | 93.7 | 140 | 242 | 0.57 | ✅ Yes | duplicate |
| IMG_0367 | IMG_0372 | 56.6 | 5.6 | 14.2 | 84.2 | 120 | 343 | 0.58 | ❌ No | MTB < 58.0 |
| IMG_0372 | IMG_0377 | 53.4 | 2.2 | 19.8 | 86.8 | 132 | 164 | 0.57 | ❌ No | MTB < 58.0 |
| IMG_0377 | IMG_0382 | 63.3 | 1.4 | 31.3 | 96.1 | 136 | 184 | 0.63 | ✅ Yes | duplicate |
| IMG_0382 | IMG_0387 | 51.8 | 2.2 | 30.6 | 93.7 | 126 | 262 | 0.59 | ✅ Yes | duplicate |
| IMG_0387 | IMG_0392 | 51.6 | 8.8 | 18.6 | 79.0 | 138 | 82 | 0.51 | ❌ No | MTB < 58.0 |
| IMG_0392 | IMG_0397 | 51.5 | 4.6 | 16.0 | 69.4 | 124 | 301 | 0.53 | ❌ No | MTB < 58.0 |
| IMG_0397 | IMG_0402 | 53.3 | 4.8 | 21.5 | 81.0 | 132 | 115 | 0.56 | ❌ No | MTB < 58.0 |
| IMG_0402 | IMG_0407 | 68.0 | 8.3 | 27.4 | 93.4 | 132 | 372 | 0.64 | ✅ Yes | duplicate |
| IMG_0407 | IMG_0412 | 63.5 | 6.1 | 24.0 | 91.2 | 126 | 132 | 0.63 | ✅ Yes | duplicate |
| IMG_0412 | IMG_0417 | 57.3 | 6.4 | 23.2 | 95.0 | 126 | 477 | 0.61 | ✅ Yes | duplicate |
| IMG_0417 | IMG_0422 | 62.5 | 4.2 | 27.4 | 96.5 | 122 | 121 | 0.64 | ✅ Yes | duplicate |
| IMG_0422 | IMG_0427 | 53.0 | 15.8 | 7.0 | 77.4 | 106 | 129 | 0.56 | ❌ No | MTB < 58.0 |
| IMG_0427 | IMG_0433 | 52.5 | 14.5 | 5.8 | 86.5 | 112 | 865 | 0.57 | ✅ Yes | duplicate |
| IMG_0433 | IMG_0437 | 54.5 | 11.4 | 8.1 | 87.6 | 130 | 831 | 0.56 | ✅ Yes | duplicate |
| IMG_0437 | IMG_0442 | 46.9 | 9.7 | 7.7 | 86.7 | 124 | 618 | 0.54 | ❌ No | SCORE < 0.55 |
| IMG_0442 | IMG_0447 | 54.5 | 8.0 | 10.5 | 89.4 | 136 | 524 | 0.56 | ✅ Yes | duplicate |
| IMG_0447 | IMG_0453 | 62.1 | 9.4 | 16.9 | 87.1 | 116 | 654 | 0.62 | ✅ Yes | duplicate |
| IMG_0453 | IMG_0457 | 63.5 | 9.9 | 29.3 | 94.9 | 124 | 311 | 0.64 | ✅ Yes | duplicate |
| IMG_0457 | IMG_0462 | 64.4 | 9.1 | 25.0 | 95.5 | 120 | 388 | 0.64 | ✅ Yes | duplicate |
| IMG_0462 | IMG_0467 | 63.7 | 8.2 | 25.1 | 95.9 | 114 | 504 | 0.65 | ✅ Yes | duplicate |
| IMG_0467 | IMG_0692 | 57.1 | 7.3 | 19.1 | 88.9 | 124 | 421 | 0.59 | ❌ No | MTB < 58.0 |
| IMG_0692 | IMG_0697 | 56.2 | 14.3 | 15.0 | 86.5 | 132 | 603 | 0.57 | ✅ Yes | duplicate |
| IMG_0697 | IMG_0702 | 53.8 | 17.0 | 7.8 | 86.9 | 128 | 502 | 0.56 | ✅ Yes | duplicate |
| IMG_0702 | IMG_0707 | 53.4 | 15.8 | 9.1 | 86.6 | 134 | 586 | 0.55 | ✅ Yes | duplicate |
| IMG_0707 | IMG_0712 | 62.6 | 8.3 | 22.1 | 94.7 | 124 | 633 | 0.63 | ✅ Yes | duplicate |
| IMG_0712 | IMG_0717 | 62.3 | 9.9 | 16.8 | 90.2 | 126 | 468 | 0.61 | ✅ Yes | duplicate |
| IMG_0717 | IMG_0722 | 53.7 | 10.0 | 15.5 | 91.3 | 124 | 708 | 0.58 | ✅ Yes | duplicate |

#### Kept Images (12)

- `IMG_0317.jpg`
- `IMG_0322.jpg`
- `IMG_0352.jpg`
- `IMG_0367.jpg`
- `IMG_0372.jpg`
- `IMG_0387.jpg`
- `IMG_0392.jpg`
- `IMG_0397.jpg`
- `IMG_0422.jpg`
- `IMG_0437.jpg`
- `IMG_0467.jpg`
- `IMG_0722.jpg`

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
| duplicate | 52 |
| Not dropped: MTB < 58.0 | 33 |
| Not dropped: SCORE < 0.55 | 6 |
| Not dropped: PDQ >= 140 | 1 |

