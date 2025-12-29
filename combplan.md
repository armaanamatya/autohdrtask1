# Plan: Combinatorial Weight Testing for Deduplication Metrics

## User Request
Test different weight combinations for deduplication metrics (MTB, SSIM, CLIP, PDQ, SIFT) with:
- All metrics enabled (CLIP, SIFT, etc.)
- Weights varied by 5% increments
- Combinatorial testing (all valid combinations where weights sum to 1.0)
- No SIFT override
- Proper logging for graphing/visualization

## Initial Analysis
- 5 metrics in composite score: MTB, SSIM, CLIP, PDQ, SIFT (EDGE is computed but not used in scoring)
- 5% increments: 0.0, 0.05, 0.10, 0.15, ..., 0.95, 1.0
- Constraint: weights must sum to 1.0
- Estimated combinations: ~10,626 (using stars and bars: C(24,4))

## Phase 1: Understanding Current Setup ✅

**Findings from exploration:**
1. **ExperimentLogger class** captures all metrics per comparison and writes structured markdown files
2. **Metrics logged per pair:** MTB%, Edge%, SSIM%, CLIP%, PDQ_HD, SIFT matches, composite SCORE, drop decision
3. **Current test data:** 4 image groups = 3 sequential pair comparisons
4. **Performance:** ~20-30 seconds per experiment (SIFT is bottleneck at ~3-6s per pair)
5. **Metrics used in score:** 5 metrics (MTB, SSIM, CLIP, PDQ, SIFT) - Edge is computed but NOT used in scoring

## Critical Questions for User

### 1. Combinatorial Explosion
**5 metrics with 5% increments (0.0 to 1.0) where weights sum to 1.0:**
- Total valid combinations: **~10,626 experiments**
- Estimated runtime: **~60-90 hours** (assuming 20-30s per experiment)
- Storage: ~100-200 MB of log files

**Question:** This is computationally expensive. Would you like to:
- A) Run all 10,626 combinations (recommended: overnight batch job)
- B) Add constraints (e.g., each metric must have weight ≥ 0.05 or ≥ 0.10 to reduce combinations)
- C) Use coarser increments (10% instead of 5%, reducing to ~126 combinations)
- D) Focus on specific metric ranges based on current findings

### 2. Output Format for Visualization
**Question:** For graphing/visualization, which format(s) do you want?
- A) Individual markdown files per experiment (current format, good for detailed review)
- B) **Single CSV summary** with one row per experiment (optimal for graphing/analysis)
- C) Both markdown AND CSV summary
- D) JSON format for programmatic analysis

Recommended: **Both (C)** - CSV for easy visualization, markdown for detailed debugging

### 3. Optimization Strategy
**Question:** Should we optimize metric computation?
- A) **Cache Phase 1 metrics** (MTB, SSIM, CLIP, PDQ) across all experiments - these don't change with weights
- B) Run experiments independently (slower but simpler, easier to parallelize later)

Recommended: **Cache (A)** - saves ~5s per experiment = ~15 hours total

## User Decisions ✅

1. **Scope:** 10% increments → **1,001 combinations** (not 126 - that was my error)
   - Runtime estimate: ~5-8 hours
   - Storage: ~10-20 MB
2. **Output:** Both CSV summary + individual markdown files
3. **Optimization:** Cache Phase 1 metrics across all experiments

## Detailed Implementation Plan

### Component 1: Weight Combination Generator
**File to create:** `generate_weight_combinations.py`

**Purpose:** Generate all valid weight combinations for 5 metrics with 10% increments

**Algorithm:**
```python
# Generate all combinations where:
# w_mtb + w_ssim + w_clip + w_pdq + w_sift = 1.0
# Each weight in {0.0, 0.1, 0.2, ..., 1.0}

def generate_weights():
    """Generate all weight combinations using nested loops"""
    combinations = []
    for w_mtb in range(0, 11):      # 0.0 to 1.0 in 0.1 steps
        for w_ssim in range(0, 11-w_mtb):
            for w_clip in range(0, 11-w_mtb-w_ssim):
                for w_pdq in range(0, 11-w_mtb-w_ssim-w_clip):
                    w_sift = 10 - w_mtb - w_ssim - w_clip - w_pdq
                    if w_sift >= 0:  # Valid combination
                        combinations.append({
                            'mtb': w_mtb / 10.0,
                            'ssim': w_ssim / 10.0,
                            'clip': w_clip / 10.0,
                            'pdq': w_pdq / 10.0,
                            'sift': w_sift / 10.0
                        })
    return combinations
```

**Output:** List of 1,001 weight dictionaries

---

### Component 2: Batch Experiment Runner
**File to create:** `run_batch_experiments.py`

**Purpose:** Run all weight combinations with optimized metric caching

**Architecture:**

```python
import sys
from pathlib import Path
from deduplication import (
    _load_gray, _apply_clahe, _compute_mtb, _compute_edges,
    _compute_ssim, _pdq_bits, _safe_clip_embed, _compute_sift_matches,
    _pair_sim, remove_near_duplicates
)
from generate_weight_combinations import generate_weights
import csv
from datetime import datetime

class BatchExperimentRunner:
    def __init__(self, output_dir='batch_results'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.csv_path = self.output_dir / 'weight_experiments_summary.csv'
        self.cached_metrics = {}  # Cache Phase 1 metrics

    def precompute_metrics(self, image_paths):
        """Cache MTB, SSIM, CLIP, PDQ for all images"""
        # Similar to _metric_worker but stores globally
        # Compute once, reuse across all 1001 experiments

    def run_single_experiment(self, exp_id, weights):
        """Run one experiment with given weights"""
        # Set global weight variables
        # Run remove_near_duplicates with cached metrics
        # Return results dict

    def run_all_experiments(self):
        """Main batch loop"""
        weights_list = generate_weights()

        # Initialize CSV
        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[...])
            writer.writeheader()

        for i, weights in enumerate(weights_list, 1):
            print(f"[{i}/1001] Testing weights: {weights}")
            result = self.run_single_experiment(i, weights)

            # Write to CSV
            self.append_to_csv(result)

            # Optionally write markdown (every Nth experiment or on request)
            if self.should_write_markdown(i, result):
                self.write_markdown(i, weights, result)
```

**Key Features:**
1. **Metric Caching:** Precompute MTB, CLIP, PDQ, SSIM once before loop
2. **CSV Writing:** Append row after each experiment (survives interruptions)
3. **Progress Tracking:** Print progress, estimated time remaining
4. **Selective Markdown:** Write detailed logs only for interesting cases

---

### Component 3: CSV Output Schema
**File:** `batch_results/weight_experiments_summary.csv`

**Columns:**
```csv
exp_id, w_mtb, w_ssim, w_clip, w_pdq, w_sift,
pair1_mtb, pair1_ssim, pair1_clip, pair1_pdq, pair1_sift, pair1_score, pair1_dropped,
pair2_mtb, pair2_ssim, pair2_clip, pair2_pdq, pair2_sift, pair2_score, pair2_dropped,
pair3_mtb, pair3_ssim, pair3_clip, pair3_pdq, pair3_sift, pair3_score, pair3_dropped,
duplicates_removed, accuracy
```

**Rationale:**
- One row per experiment
- Weights in first 6 columns (easy to filter/group)
- Raw metrics for each pair (should be constant across experiments - good validation)
- Scores vary based on weights
- Summary stats: duplicates_removed, accuracy (2/2 = 100%, 0/2 = 0%, 1/2 = 50%)

---

### Component 4: Markdown Output (Selective)
**Directory:** `batch_results/experiments/`

**Strategy:** Only write markdown for:
- First 10 experiments (validation)
- Last 10 experiments (completion check)
- Experiments with interesting results (e.g., accuracy changes, edge cases)
- Every 100th experiment (sampling)

**Naming:** `exp_weights_{exp_id:04d}.md` (e.g., `exp_weights_0001.md`)

---

### Component 5: Modified deduplication.py
**Changes needed:**

1. **Disable SIFT Override (line 535):**
   ```python
   sift_override = False  # Already done
   ```

2. **Make weights configurable (new function):**
   ```python
   def set_weights(mtb, ssim, clip, pdq, sift):
       """Set global weight variables for batch testing"""
       global WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT
       WEIGHT_MTB = mtb
       WEIGHT_SSIM = ssim
       WEIGHT_CLIP = clip
       WEIGHT_PDQ = pdq
       WEIGHT_SIFT = sift
   ```

3. **Export metric computation functions (already done - they're module-level)**

---

## Implementation Steps

### Step 1: Create Weight Generator
- Create `generate_weight_combinations.py`
- Test: Verify 1,001 combinations generated
- Test: Verify all sum to 1.0

### Step 2: Create Batch Runner Skeleton
- Create `run_batch_experiments.py`
- Implement CSV writing structure
- Implement progress tracking

### Step 3: Integrate with deduplication.py
- Add `set_weights()` function
- Test: Run single experiment programmatically
- Verify: SIFT override is disabled

### Step 4: Implement Metric Caching
- Precompute Phase 1 metrics before batch loop
- Modify batch runner to reuse cached metrics
- Test: Verify metrics identical across experiments

### Step 5: Full Integration
- Connect all components
- Test: Run first 10 experiments
- Validate: CSV format, markdown output, metrics consistency

### Step 6: Production Run
- Run full 1,001 experiments
- Monitor progress
- Generate final CSV summary

---

## Critical Files

**New files to create:**
1. `C:\Users\Armaan\Desktop\autohdrtask1\generate_weight_combinations.py`
2. `C:\Users\Armaan\Desktop\autohdrtask1\run_batch_experiments.py`
3. `C:\Users\Armaan\Desktop\autohdrtask1\batch_results\weight_experiments_summary.csv` (output)
4. `C:\Users\Armaan\Desktop\autohdrtask1\batch_results\experiments\*.md` (output)

**Files to modify:**
1. `C:\Users\Armaan\Desktop\autohdrtask1\deduplication.py` (add `set_weights()`, already has SIFT override disabled)

---

## Expected Results

After completion:
- **CSV file** with 1,001 rows for easy visualization in pandas/Excel
- **~50-100 markdown files** for detailed review of interesting cases
- **Analysis ready:** Can plot accuracy vs weights, find optimal combinations
- **Validation:** Raw metrics (MTB, SSIM, CLIP, PDQ, SIFT) should be identical across all experiments

---

## Next Steps After Planning

1. Create `generate_weight_combinations.py`
2. Create `run_batch_experiments.py`
3. Modify `deduplication.py` to add `set_weights()`
4. Test with first 10 combinations
5. Run full batch (1,001 experiments)
6. Analyze results and visualize optimal weight combinations
