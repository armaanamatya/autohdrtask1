# Deduplication Method Comparison Report

**Generated:** 2025-12-29 18:21:36

**Base Directory:** C:\Users\Armaan\Desktop\autohdrtask1\images

## Executive Summary

- **Total Folders Processed:** 5
- **Total Images:** 26
- **MTB Method:** Would drop 18 images
- **CNN Method:** Would drop 7 images
- **Agreement:** 3 folders (both methods agree)

## Configuration

### MTB Multi-Metric Method

| Parameter | Value |
|-----------|-------|
| WEIGHT_MTB | 0.3 |
| WEIGHT_SSIM | 0.1 |
| WEIGHT_CLIP | 0.25 |
| WEIGHT_PDQ | 0.25 |
| WEIGHT_SIFT | 0.1 |
| COMPOSITE_DUP_THRESHOLD | 0.35 |
| MTB_HARD_FLOOR | 67.0 |
| PDQ_HD_CEIL | 115 |
| SIFT_MIN_MATCHES | 50 |
| SIFT Override | Conditional (SIFT >= 50 AND CLIP >= 85%) |

### CNN Method

| Parameter | Value |
|-----------|-------|
| Threshold | 0.9 |
| Method | Cosine similarity on CNN embeddings |

---

## Per-Folder Detailed Results

### 1. Folder: `0004eefe-1b3a-4771-8fd4-fa3fd2db321d`

**Total Images:** 1

#### MTB Multi-Metric Method

*No comparisons possible (≤1 image)*

#### CNN Method

*No comparisons possible (≤1 image)*

#### Comparison

*Both methods agree: no duplicates*

---

### 2. Folder: `000fc774-cb56-4052-a33a-9974c58a00d6`

**Total Images:** 20

#### MTB Multi-Metric Method

**Would Drop:** 16 images

<details>
<summary>View All Comparisons</summary>

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | Score | Drop? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|-------|--------|
| IMG_3722.jpg | IMG_3725.jpg | 49.3 | 1.0 | 39.3 | 75.0 | 116 | 5 | 0.380 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3726.jpg | 50.6 | 1.0 | 41.9 | 87.2 | 134 | 11 | 0.423 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3731.jpg | 48.4 | 2.3 | 38.5 | 82.6 | 136 | 7 | 0.397 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3734.jpg | 54.5 | 0.4 | 49.5 | 83.3 | 126 | 10 | 0.431 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3737.jpg | 59.5 | 0.3 | 44.1 | 77.1 | 126 | 15 | 0.431 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3740.jpg | 54.2 | 1.8 | 45.0 | 78.8 | 126 | 17 | 0.421 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3743.jpg | 44.1 | 0.5 | 37.2 | 76.6 | 136 | 3 | 0.364 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3746.jpg | 48.8 | 2.9 | 29.3 | 72.7 | 130 | 8 | 0.365 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3751.jpg | 49.4 | 0.4 | 36.6 | 77.4 | 114 | 18 | 0.398 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3754.jpg | 52.7 | 2.4 | 41.1 | 84.4 | 126 | 8 | 0.418 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3757.jpg | 55.6 | 0.6 | 44.4 | 81.5 | 138 | 29 | 0.444 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3760.jpg | 53.9 | 1.2 | 36.7 | 75.9 | 120 | 26 | 0.414 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3766.jpg | 44.7 | 1.5 | 33.9 | 78.9 | 142 | 11 | 0.376 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3768.jpg | 49.2 | 2.2 | 37.0 | 79.5 | 130 | 20 | 0.403 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3771.jpg | 49.3 | 0.0 | 47.1 | 85.0 | 134 | 12 | 0.419 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3772.jpg | 50.2 | 11.4 | 9.3 | 69.7 | 136 | 9 | 0.343 | No | SCORE < 0.35 |
| IMG_3722.jpg | IMG_3773.jpg | 53.1 | 14.5 | 11.6 | 67.3 | 122 | 4 | 0.343 | No | SCORE < 0.35 |
| IMG_3722.jpg | IMG_3774.jpg | 57.1 | 3.8 | 16.6 | 68.8 | 122 | 10 | 0.370 | No | MTB < 67.0 |
| IMG_3722.jpg | IMG_3775.jpg | 51.7 | 9.1 | 12.3 | 69.9 | 144 | 8 | 0.350 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3726.jpg | 60.0 | 1.7 | 41.5 | 87.5 | 128 | 94 | 0.534 | Yes | duplicate |
| IMG_3725.jpg | IMG_3731.jpg | 51.1 | 2.5 | 37.9 | 81.7 | 146 | 87 | 0.482 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3734.jpg | 58.6 | 2.1 | 44.4 | 88.8 | 126 | 93 | 0.535 | Yes | duplicate |
| IMG_3725.jpg | IMG_3737.jpg | 58.3 | 2.2 | 40.9 | 90.4 | 128 | 62 | 0.504 | Yes | duplicate |
| IMG_3725.jpg | IMG_3740.jpg | 57.5 | 1.1 | 38.5 | 91.5 | 122 | 77 | 0.517 | Yes | duplicate |
| IMG_3725.jpg | IMG_3743.jpg | 56.3 | 3.8 | 35.0 | 90.6 | 120 | 97 | 0.527 | Yes | duplicate |
| IMG_3725.jpg | IMG_3746.jpg | 53.2 | 1.1 | 27.4 | 79.4 | 132 | 87 | 0.472 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3751.jpg | 59.4 | 5.7 | 38.5 | 89.3 | 126 | 125 | 0.540 | Yes | duplicate |
| IMG_3725.jpg | IMG_3754.jpg | 56.4 | 2.1 | 39.0 | 81.0 | 130 | 128 | 0.511 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3757.jpg | 59.3 | 3.8 | 43.5 | 86.6 | 124 | 156 | 0.538 | Yes | duplicate |
| IMG_3725.jpg | IMG_3760.jpg | 48.4 | 0.7 | 30.5 | 75.8 | 144 | 73 | 0.438 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3766.jpg | 51.1 | 1.3 | 37.0 | 77.2 | 138 | 73 | 0.456 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3768.jpg | 49.7 | 2.1 | 39.5 | 76.2 | 122 | 142 | 0.479 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3771.jpg | 62.9 | 3.3 | 44.1 | 84.9 | 128 | 151 | 0.545 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3772.jpg | 52.6 | 14.6 | 11.4 | 77.6 | 126 | 55 | 0.418 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3773.jpg | 46.1 | 12.6 | 11.1 | 73.8 | 128 | 59 | 0.393 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3774.jpg | 52.2 | 9.7 | 15.3 | 76.7 | 112 | 93 | 0.463 | No | MTB < 67.0 |
| IMG_3725.jpg | IMG_3775.jpg | 52.9 | 14.7 | 12.1 | 75.4 | 132 | 54 | 0.413 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3731.jpg | 49.7 | 4.8 | 44.0 | 91.2 | 130 | 90 | 0.511 | Yes | duplicate |
| IMG_3726.jpg | IMG_3734.jpg | 68.3 | 1.4 | 51.9 | 91.2 | 112 | 65 | 0.556 | Yes | duplicate |
| IMG_3726.jpg | IMG_3737.jpg | 73.2 | 4.1 | 52.1 | 83.3 | 126 | 104 | 0.580 | No | PDQ_HD >= 115 |
| IMG_3726.jpg | IMG_3740.jpg | 61.5 | 4.6 | 46.8 | 83.4 | 142 | 71 | 0.511 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3743.jpg | 56.6 | 1.7 | 37.5 | 81.3 | 128 | 27 | 0.438 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3746.jpg | 60.2 | 2.5 | 34.1 | 81.3 | 126 | 59 | 0.477 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3751.jpg | 59.0 | 3.8 | 42.6 | 82.7 | 124 | 156 | 0.526 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3754.jpg | 69.9 | 3.0 | 45.4 | 87.1 | 122 | 86 | 0.559 | Yes | duplicate |
| IMG_3726.jpg | IMG_3757.jpg | 68.3 | 3.2 | 53.3 | 87.6 | 120 | 111 | 0.577 | Yes | duplicate |
| IMG_3726.jpg | IMG_3760.jpg | 55.9 | 1.1 | 41.0 | 80.6 | 124 | 96 | 0.506 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3766.jpg | 59.2 | 4.7 | 44.2 | 85.0 | 140 | 50 | 0.484 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3768.jpg | 59.5 | 3.2 | 47.1 | 84.4 | 136 | 88 | 0.525 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3771.jpg | 70.8 | 2.0 | 53.4 | 90.3 | 132 | 125 | 0.592 | Yes | duplicate |
| IMG_3726.jpg | IMG_3772.jpg | 52.3 | 13.5 | 11.2 | 75.7 | 126 | 55 | 0.412 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3773.jpg | 49.2 | 14.4 | 11.1 | 72.8 | 130 | 36 | 0.377 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3774.jpg | 51.5 | 11.8 | 16.8 | 74.6 | 132 | 61 | 0.419 | No | MTB < 67.0 |
| IMG_3726.jpg | IMG_3775.jpg | 49.4 | 10.4 | 14.3 | 75.0 | 122 | 42 | 0.392 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3734.jpg | 54.3 | 2.1 | 47.4 | 87.3 | 126 | 82 | 0.511 | Yes | duplicate |
| IMG_3731.jpg | IMG_3737.jpg | 52.3 | 3.8 | 46.7 | 80.6 | 108 | 101 | 0.520 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3740.jpg | 49.8 | 2.3 | 41.9 | 81.3 | 126 | 59 | 0.454 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3743.jpg | 53.6 | 2.8 | 37.1 | 80.1 | 124 | 77 | 0.475 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3746.jpg | 53.4 | 3.6 | 30.7 | 84.5 | 128 | 76 | 0.478 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3751.jpg | 52.7 | 5.5 | 39.2 | 80.5 | 136 | 67 | 0.466 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3754.jpg | 50.9 | 3.4 | 42.8 | 85.2 | 134 | 106 | 0.509 | Yes | duplicate |
| IMG_3731.jpg | IMG_3757.jpg | 52.0 | 2.4 | 48.2 | 86.2 | 134 | 137 | 0.520 | Yes | duplicate |
| IMG_3731.jpg | IMG_3760.jpg | 58.1 | 1.2 | 37.1 | 84.7 | 112 | 207 | 0.530 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3766.jpg | 63.8 | 1.7 | 44.8 | 86.5 | 124 | 76 | 0.528 | Yes | duplicate |
| IMG_3731.jpg | IMG_3768.jpg | 56.0 | 2.5 | 42.6 | 86.2 | 132 | 123 | 0.526 | Yes | duplicate |
| IMG_3731.jpg | IMG_3771.jpg | 52.3 | 2.9 | 50.4 | 86.9 | 134 | 93 | 0.518 | Yes | duplicate |
| IMG_3731.jpg | IMG_3772.jpg | 47.2 | 12.1 | 8.6 | 73.8 | 136 | 58 | 0.393 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3773.jpg | 45.5 | 12.8 | 10.3 | 71.7 | 130 | 48 | 0.374 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3774.jpg | 51.8 | 10.5 | 14.7 | 73.2 | 138 | 60 | 0.413 | No | MTB < 67.0 |
| IMG_3731.jpg | IMG_3775.jpg | 50.2 | 10.2 | 13.3 | 73.6 | 116 | 47 | 0.395 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3737.jpg | 66.5 | 8.2 | 55.4 | 92.5 | 124 | 49 | 0.535 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3740.jpg | 65.1 | 2.7 | 52.0 | 89.6 | 156 | 45 | 0.516 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3743.jpg | 54.9 | 1.5 | 41.3 | 84.6 | 126 | 57 | 0.475 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3746.jpg | 55.4 | 1.6 | 36.6 | 81.8 | 132 | 87 | 0.494 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3751.jpg | 57.8 | 4.0 | 42.5 | 87.8 | 128 | 56 | 0.491 | Yes | duplicate |
| IMG_3734.jpg | IMG_3754.jpg | 63.6 | 3.7 | 49.3 | 88.5 | 124 | 45 | 0.506 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3757.jpg | 64.0 | 3.0 | 54.9 | 94.2 | 116 | 107 | 0.582 | Yes | duplicate |
| IMG_3734.jpg | IMG_3760.jpg | 56.6 | 0.8 | 42.4 | 80.3 | 136 | 108 | 0.513 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3766.jpg | 54.9 | 3.4 | 44.4 | 83.2 | 136 | 53 | 0.470 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3768.jpg | 48.1 | 3.5 | 45.1 | 84.3 | 148 | 94 | 0.494 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3771.jpg | 66.5 | 0.1 | 54.8 | 96.8 | 132 | 102 | 0.596 | Yes | duplicate |
| IMG_3734.jpg | IMG_3772.jpg | 50.4 | 15.7 | 10.6 | 77.9 | 128 | 44 | 0.401 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3773.jpg | 48.4 | 13.3 | 12.0 | 73.6 | 120 | 35 | 0.376 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3774.jpg | 55.9 | 10.8 | 17.7 | 76.5 | 138 | 38 | 0.415 | No | MTB < 67.0 |
| IMG_3734.jpg | IMG_3775.jpg | 51.0 | 10.7 | 13.2 | 77.2 | 132 | 32 | 0.391 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3740.jpg | 69.9 | 3.4 | 51.2 | 97.0 | 126 | 163 | 0.604 | Yes | duplicate |
| IMG_3737.jpg | IMG_3743.jpg | 50.9 | 2.2 | 36.7 | 92.6 | 134 | 86 | 0.507 | Yes | duplicate |
| IMG_3737.jpg | IMG_3746.jpg | 50.9 | 2.9 | 33.7 | 79.0 | 128 | 82 | 0.466 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3751.jpg | 54.8 | 5.8 | 44.4 | 95.2 | 132 | 92 | 0.539 | Yes | duplicate |
| IMG_3737.jpg | IMG_3754.jpg | 64.7 | 2.8 | 47.4 | 88.2 | 144 | 139 | 0.562 | Yes | duplicate |
| IMG_3737.jpg | IMG_3757.jpg | 68.6 | 3.2 | 52.6 | 93.4 | 132 | 139 | 0.592 | Yes | duplicate |
| IMG_3737.jpg | IMG_3760.jpg | 55.7 | 1.2 | 40.5 | 79.1 | 132 | 124 | 0.505 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3766.jpg | 57.3 | 3.1 | 44.6 | 79.0 | 130 | 117 | 0.514 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3768.jpg | 58.5 | 3.3 | 45.5 | 78.8 | 124 | 119 | 0.518 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3771.jpg | 66.1 | 1.8 | 51.5 | 90.7 | 140 | 152 | 0.577 | Yes | duplicate |
| IMG_3737.jpg | IMG_3772.jpg | 50.3 | 11.4 | 11.9 | 80.7 | 142 | 184 | 0.465 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3773.jpg | 44.6 | 12.6 | 12.3 | 75.9 | 124 | 152 | 0.436 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3774.jpg | 54.8 | 14.3 | 19.5 | 77.0 | 114 | 70 | 0.449 | No | MTB < 67.0 |
| IMG_3737.jpg | IMG_3775.jpg | 46.8 | 10.8 | 15.5 | 77.8 | 138 | 97 | 0.447 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3743.jpg | 50.3 | 2.4 | 38.3 | 95.5 | 140 | 139 | 0.528 | Yes | duplicate |
| IMG_3740.jpg | IMG_3746.jpg | 52.8 | 2.2 | 32.6 | 78.7 | 138 | 94 | 0.482 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3751.jpg | 49.6 | 4.2 | 38.2 | 96.9 | 118 | 198 | 0.529 | Yes | duplicate |
| IMG_3740.jpg | IMG_3754.jpg | 57.0 | 2.8 | 46.3 | 87.9 | 130 | 166 | 0.537 | Yes | duplicate |
| IMG_3740.jpg | IMG_3757.jpg | 60.9 | 1.3 | 48.0 | 93.1 | 136 | 162 | 0.564 | Yes | duplicate |
| IMG_3740.jpg | IMG_3760.jpg | 50.9 | 2.4 | 37.5 | 79.6 | 124 | 102 | 0.489 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3766.jpg | 54.8 | 1.9 | 41.0 | 79.7 | 120 | 112 | 0.505 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3768.jpg | 55.3 | 1.8 | 42.2 | 79.1 | 110 | 129 | 0.517 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3771.jpg | 61.4 | 1.6 | 49.8 | 87.9 | 120 | 194 | 0.554 | Yes | duplicate |
| IMG_3740.jpg | IMG_3772.jpg | 46.6 | 11.1 | 10.0 | 81.0 | 130 | 121 | 0.452 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3773.jpg | 46.7 | 13.7 | 12.6 | 76.6 | 128 | 96 | 0.440 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3774.jpg | 53.7 | 12.9 | 16.9 | 79.4 | 120 | 88 | 0.465 | No | MTB < 67.0 |
| IMG_3740.jpg | IMG_3775.jpg | 48.2 | 10.3 | 13.9 | 77.8 | 120 | 92 | 0.445 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3746.jpg | 48.7 | 1.8 | 27.1 | 78.0 | 138 | 96 | 0.464 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3751.jpg | 59.9 | 1.5 | 38.4 | 96.2 | 144 | 267 | 0.558 | Yes | duplicate |
| IMG_3743.jpg | IMG_3754.jpg | 55.7 | 3.2 | 32.7 | 83.9 | 140 | 184 | 0.509 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3757.jpg | 60.9 | 6.7 | 44.8 | 87.2 | 126 | 214 | 0.545 | Yes | duplicate |
| IMG_3743.jpg | IMG_3760.jpg | 56.0 | 1.2 | 34.5 | 78.7 | 136 | 81 | 0.480 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3766.jpg | 56.2 | 2.1 | 36.9 | 78.6 | 116 | 135 | 0.502 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3768.jpg | 49.3 | 2.0 | 37.8 | 76.9 | 132 | 158 | 0.478 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3771.jpg | 64.2 | 2.4 | 45.2 | 82.4 | 150 | 276 | 0.544 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3772.jpg | 46.3 | 10.8 | 6.8 | 78.5 | 120 | 94 | 0.436 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3773.jpg | 47.0 | 10.1 | 8.6 | 75.2 | 120 | 98 | 0.436 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3774.jpg | 48.2 | 7.8 | 15.8 | 77.8 | 128 | 246 | 0.455 | No | MTB < 67.0 |
| IMG_3743.jpg | IMG_3775.jpg | 47.6 | 10.5 | 11.0 | 75.5 | 122 | 83 | 0.426 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3751.jpg | 52.0 | 2.0 | 26.9 | 77.5 | 122 | 45 | 0.422 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3754.jpg | 62.7 | 2.2 | 33.0 | 78.6 | 126 | 68 | 0.486 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3757.jpg | 55.5 | 1.3 | 35.5 | 81.8 | 144 | 93 | 0.500 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3760.jpg | 63.1 | 3.3 | 35.4 | 96.8 | 104 | 60 | 0.551 | Yes | duplicate |
| IMG_3746.jpg | IMG_3766.jpg | 52.8 | 1.9 | 30.6 | 95.8 | 136 | 48 | 0.476 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3768.jpg | 52.9 | 3.7 | 31.9 | 93.2 | 126 | 55 | 0.479 | Yes | duplicate |
| IMG_3746.jpg | IMG_3771.jpg | 53.7 | 5.7 | 35.6 | 79.1 | 132 | 126 | 0.494 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3772.jpg | 50.3 | 8.5 | 8.4 | 75.4 | 124 | 37 | 0.385 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3773.jpg | 48.8 | 9.7 | 6.2 | 71.5 | 134 | 39 | 0.370 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3774.jpg | 48.7 | 9.1 | 10.8 | 72.4 | 120 | 32 | 0.370 | No | MTB < 67.0 |
| IMG_3746.jpg | IMG_3775.jpg | 52.8 | 9.7 | 9.0 | 74.1 | 128 | 26 | 0.379 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3754.jpg | 59.6 | 4.2 | 39.8 | 89.2 | 116 | 206 | 0.542 | Yes | duplicate |
| IMG_3751.jpg | IMG_3757.jpg | 60.3 | 2.9 | 44.8 | 92.3 | 128 | 105 | 0.556 | Yes | duplicate |
| IMG_3751.jpg | IMG_3760.jpg | 52.1 | 6.2 | 34.4 | 77.7 | 126 | 46 | 0.431 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3766.jpg | 54.8 | 2.0 | 38.2 | 79.2 | 148 | 82 | 0.483 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3768.jpg | 47.6 | 2.5 | 39.6 | 78.1 | 128 | 96 | 0.474 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3771.jpg | 62.0 | 2.5 | 46.7 | 86.2 | 116 | 113 | 0.548 | Yes | duplicate |
| IMG_3751.jpg | IMG_3772.jpg | 50.5 | 12.4 | 9.2 | 82.2 | 126 | 73 | 0.439 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3773.jpg | 48.3 | 13.2 | 10.9 | 77.7 | 130 | 65 | 0.415 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3774.jpg | 48.4 | 14.0 | 16.6 | 80.4 | 126 | 124 | 0.463 | No | MTB < 67.0 |
| IMG_3751.jpg | IMG_3775.jpg | 53.3 | 14.6 | 13.4 | 79.0 | 126 | 52 | 0.423 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3757.jpg | 62.4 | 3.0 | 48.5 | 90.4 | 122 | 101 | 0.562 | Yes | duplicate |
| IMG_3754.jpg | IMG_3760.jpg | 56.0 | 1.9 | 36.4 | 79.8 | 128 | 41 | 0.445 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3766.jpg | 59.5 | 1.6 | 38.6 | 83.0 | 122 | 84 | 0.509 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3768.jpg | 55.2 | 2.2 | 39.0 | 82.6 | 118 | 88 | 0.499 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3771.jpg | 64.5 | 4.2 | 47.4 | 88.8 | 122 | 101 | 0.563 | Yes | duplicate |
| IMG_3754.jpg | IMG_3772.jpg | 48.3 | 14.8 | 10.5 | 79.4 | 132 | 84 | 0.438 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3773.jpg | 46.4 | 10.9 | 11.8 | 74.3 | 134 | 77 | 0.414 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3774.jpg | 48.8 | 11.5 | 14.5 | 74.8 | 122 | 42 | 0.390 | No | MTB < 67.0 |
| IMG_3754.jpg | IMG_3775.jpg | 46.8 | 11.0 | 14.1 | 77.7 | 122 | 60 | 0.409 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3760.jpg | 54.8 | 1.0 | 41.6 | 81.2 | 134 | 45 | 0.454 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3766.jpg | 54.6 | 1.2 | 47.5 | 84.0 | 120 | 30 | 0.451 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3768.jpg | 50.1 | 1.7 | 48.1 | 83.9 | 140 | 52 | 0.460 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3771.jpg | 68.0 | 1.8 | 58.5 | 93.0 | 120 | 58 | 0.553 | Yes | duplicate |
| IMG_3757.jpg | IMG_3772.jpg | 50.1 | 10.4 | 9.8 | 78.3 | 126 | 40 | 0.396 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3773.jpg | 49.8 | 15.2 | 13.3 | 73.3 | 142 | 46 | 0.392 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3774.jpg | 54.2 | 10.1 | 17.8 | 75.2 | 138 | 39 | 0.407 | No | MTB < 67.0 |
| IMG_3757.jpg | IMG_3775.jpg | 51.4 | 10.4 | 13.6 | 76.4 | 132 | 33 | 0.392 | No | MTB < 67.0 |
| IMG_3760.jpg | IMG_3766.jpg | 55.0 | 1.7 | 38.0 | 96.0 | 138 | 50 | 0.493 | Yes | duplicate |
| IMG_3760.jpg | IMG_3768.jpg | 51.4 | 1.2 | 39.0 | 93.6 | 108 | 102 | 0.542 | Yes | duplicate |
| IMG_3760.jpg | IMG_3771.jpg | 55.6 | 1.8 | 44.9 | 79.7 | 128 | 161 | 0.511 | No | MTB < 67.0 |
| IMG_3760.jpg | IMG_3772.jpg | 48.8 | 8.9 | 8.3 | 73.5 | 124 | 54 | 0.392 | No | MTB < 67.0 |
| IMG_3760.jpg | IMG_3773.jpg | 48.3 | 10.6 | 8.7 | 70.4 | 130 | 35 | 0.365 | No | MTB < 67.0 |
| IMG_3760.jpg | IMG_3774.jpg | 50.9 | 7.0 | 13.3 | 70.6 | 150 | 38 | 0.381 | No | MTB < 67.0 |
| IMG_3760.jpg | IMG_3775.jpg | 48.0 | 10.5 | 10.4 | 72.1 | 120 | 32 | 0.367 | No | MTB < 67.0 |
| IMG_3766.jpg | IMG_3768.jpg | 70.1 | 40.5 | 73.6 | 96.9 | 82 | 155 | 0.698 | Yes | duplicate |
| IMG_3766.jpg | IMG_3771.jpg | 60.1 | 1.2 | 49.1 | 82.0 | 126 | 141 | 0.534 | No | MTB < 67.0 |
| IMG_3766.jpg | IMG_3772.jpg | 50.1 | 8.8 | 8.5 | 75.1 | 130 | 50 | 0.396 | No | MTB < 67.0 |
| IMG_3766.jpg | IMG_3773.jpg | 47.7 | 9.6 | 10.2 | 72.0 | 126 | 30 | 0.363 | No | MTB < 67.0 |
| IMG_3766.jpg | IMG_3774.jpg | 53.4 | 7.6 | 14.9 | 72.2 | 138 | 35 | 0.390 | No | MTB < 67.0 |
| IMG_3766.jpg | IMG_3775.jpg | 46.1 | 11.1 | 11.7 | 73.9 | 130 | 41 | 0.376 | No | MTB < 67.0 |
| IMG_3768.jpg | IMG_3771.jpg | 53.6 | 2.0 | 49.4 | 82.7 | 120 | 39 | 0.456 | No | MTB < 67.0 |
| IMG_3768.jpg | IMG_3772.jpg | 50.0 | 9.1 | 8.2 | 75.4 | 128 | 12 | 0.359 | No | MTB < 67.0 |
| IMG_3768.jpg | IMG_3773.jpg | 52.6 | 10.9 | 12.6 | 72.3 | 112 | 20 | 0.378 | No | MTB < 67.0 |
| IMG_3768.jpg | IMG_3774.jpg | 54.0 | 8.3 | 16.2 | 73.3 | 112 | 19 | 0.387 | No | MTB < 67.0 |
| IMG_3768.jpg | IMG_3775.jpg | 47.8 | 9.4 | 11.7 | 74.8 | 134 | 19 | 0.361 | No | MTB < 67.0 |
| IMG_3771.jpg | IMG_3772.jpg | 51.2 | 14.1 | 9.5 | 73.9 | 136 | 27 | 0.375 | No | MTB < 67.0 |
| IMG_3771.jpg | IMG_3773.jpg | 47.6 | 11.2 | 10.8 | 70.0 | 136 | 28 | 0.357 | No | MTB < 67.0 |
| IMG_3771.jpg | IMG_3774.jpg | 53.1 | 9.3 | 18.4 | 72.4 | 122 | 22 | 0.381 | No | MTB < 67.0 |
| IMG_3771.jpg | IMG_3775.jpg | 50.5 | 15.5 | 13.6 | 73.8 | 118 | 25 | 0.374 | No | MTB < 67.0 |
| IMG_3772.jpg | IMG_3773.jpg | 50.6 | 11.4 | 4.5 | 93.7 | 122 | 1731 | 0.490 | Yes | duplicate |
| IMG_3772.jpg | IMG_3774.jpg | 51.2 | 11.5 | 5.3 | 91.6 | 128 | 312 | 0.488 | Yes | duplicate |
| IMG_3772.jpg | IMG_3775.jpg | 51.5 | 11.5 | 4.4 | 96.0 | 122 | 1397 | 0.499 | Yes | duplicate |
| IMG_3773.jpg | IMG_3774.jpg | 54.0 | 11.1 | 7.6 | 93.5 | 104 | 490 | 0.527 | Yes | duplicate |
| IMG_3773.jpg | IMG_3775.jpg | 48.3 | 11.7 | 6.3 | 95.2 | 134 | 2571 | 0.489 | Yes | duplicate |
| IMG_3774.jpg | IMG_3775.jpg | 47.1 | 10.1 | 3.6 | 93.2 | 140 | 392 | 0.478 | Yes | duplicate |

</details>

**Dropped Images:**
- IMG_3725.jpg
- IMG_3726.jpg
- IMG_3731.jpg
- IMG_3734.jpg
- IMG_3737.jpg
- IMG_3740.jpg
- IMG_3743.jpg
- IMG_3746.jpg
- IMG_3751.jpg
- IMG_3754.jpg
- IMG_3757.jpg
- IMG_3760.jpg
- IMG_3766.jpg
- IMG_3772.jpg
- IMG_3773.jpg
- IMG_3774.jpg

#### CNN Method

**Would Drop:** 5 images

<details>
<summary>View Duplicate Clusters</summary>

**Cluster 1:** 2 images

- **KEEP:** IMG_3734.jpg
- **DROP:** IMG_3771.jpg

Similarities:
  - IMG_3734.jpg ↔ IMG_3771.jpg: 0.9169

**Cluster 2:** 2 images

- **KEEP:** IMG_3737.jpg
- **DROP:** IMG_3740.jpg

Similarities:
  - IMG_3737.jpg ↔ IMG_3740.jpg: 0.9014

**Cluster 3:** 2 images

- **KEEP:** IMG_3751.jpg
- **DROP:** IMG_3743.jpg

Similarities:
  - IMG_3743.jpg ↔ IMG_3751.jpg: 0.9056

**Cluster 4:** 2 images

- **KEEP:** IMG_3768.jpg
- **DROP:** IMG_3766.jpg

Similarities:
  - IMG_3766.jpg ↔ IMG_3768.jpg: 0.9499

**Cluster 5:** 2 images

- **KEEP:** IMG_3773.jpg
- **DROP:** IMG_3775.jpg

Similarities:
  - IMG_3773.jpg ↔ IMG_3775.jpg: 0.9061

</details>

**Dropped Images:**
- IMG_3740.jpg
- IMG_3743.jpg
- IMG_3766.jpg
- IMG_3771.jpg
- IMG_3775.jpg

#### Comparison

**Differences:**
- MTB only would drop: IMG_3725.jpg, IMG_3726.jpg, IMG_3731.jpg, IMG_3734.jpg, IMG_3737.jpg, IMG_3746.jpg, IMG_3751.jpg, IMG_3754.jpg, IMG_3757.jpg, IMG_3760.jpg, IMG_3772.jpg, IMG_3773.jpg, IMG_3774.jpg
- CNN only would drop: IMG_3771.jpg, IMG_3775.jpg
- Both agree on: IMG_3740.jpg, IMG_3743.jpg, IMG_3766.jpg

---

### 3. Folder: `001422f9-aff7-433c-aca9-daf331fa786d`

**Total Images:** 1

#### MTB Multi-Metric Method

*No comparisons possible (≤1 image)*

#### CNN Method

*No comparisons possible (≤1 image)*

#### Comparison

*Both methods agree: no duplicates*

---

### 4. Folder: `001ad590-d1ba-461c-b7f5-11df53670d02`

**Total Images:** 3

#### MTB Multi-Metric Method

**Would Drop:** 2 images

<details>
<summary>View All Comparisons</summary>

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | Score | Drop? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|-------|--------|
| 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg | 6T7A0540-HDR.jpg | 99.3 | 97.9 | 99.7 | 99.4 | 2 | 28350 | 0.992 | Yes | duplicate |
| 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg | 81413516-cac9-4ce2-aeeb-55a8fb5b89e1.jpg | 99.9 | 99.0 | 100.0 | 99.9 | 0 | 32439 | 1.000 | Yes | duplicate |
| 6T7A0540-HDR.jpg | 81413516-cac9-4ce2-aeeb-55a8fb5b89e1.jpg | 99.3 | 97.7 | 99.7 | 99.6 | 2 | 28574 | 0.992 | Yes | duplicate |

</details>

**Dropped Images:**
- 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg
- 6T7A0540-HDR.jpg

#### CNN Method

**Would Drop:** 2 images

<details>
<summary>View Duplicate Clusters</summary>

**Cluster 1:** 3 images

- **KEEP:** 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg
- **DROP:** 6T7A0540-HDR.jpg
- **DROP:** 81413516-cac9-4ce2-aeeb-55a8fb5b89e1.jpg

Similarities:
  - 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg ↔ 6T7A0540-HDR.jpg: 0.9989
  - 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg ↔ 81413516-cac9-4ce2-aeeb-55a8fb5b89e1.jpg: 0.9993

</details>

**Dropped Images:**
- 6T7A0540-HDR.jpg
- 81413516-cac9-4ce2-aeeb-55a8fb5b89e1.jpg

#### Comparison

**Differences:**
- MTB only would drop: 1505bc3a-5baf-44a9-9d17-b80b5c2d9115.jpg
- CNN only would drop: 81413516-cac9-4ce2-aeeb-55a8fb5b89e1.jpg
- Both agree on: 6T7A0540-HDR.jpg

---

### 5. Folder: `0022311f-931f-4a9d-8e6d-6c86877340aa`

**Total Images:** 1

#### MTB Multi-Metric Method

*No comparisons possible (≤1 image)*

#### CNN Method

*No comparisons possible (≤1 image)*

#### Comparison

*Both methods agree: no duplicates*

---

