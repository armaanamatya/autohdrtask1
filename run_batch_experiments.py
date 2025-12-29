#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_batch_experiments.py

Batch runner for testing all weight combinations (1,001 total) with metric caching.
Generates CSV summary + selective markdown files for analysis.
"""

import sys
import csv
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Import from deduplication module
import deduplication as dedupe
from generate_weight_combinations import generate_weights


class BatchExperimentRunner:
    """Run batch experiments with different weight combinations"""

    def __init__(self, output_dir='batch_results', test_limit=None):
        """
        Initialize batch runner.

        Args:
            output_dir: Directory for output files
            test_limit: If set, only run first N experiments (for testing)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.experiments_dir = self.output_dir / 'experiments'
        self.experiments_dir.mkdir(exist_ok=True)

        self.csv_path = self.output_dir / 'weight_experiments_summary.csv'
        self.test_limit = test_limit

        # Image paths (hardcoded from deduplication.py)
        self.image_groups = []

        # Cached metrics (computed once, reused for all experiments)
        self.cached_metrics = {}

        # CSV fieldnames
        self.csv_fieldnames = [
            'exp_id', 'w_mtb', 'w_ssim', 'w_clip', 'w_pdq', 'w_sift',
            'pair1_mtb', 'pair1_ssim', 'pair1_clip', 'pair1_pdq', 'pair1_pdq_hd',
            'pair1_sift', 'pair1_score', 'pair1_dropped',
            'pair2_mtb', 'pair2_ssim', 'pair2_clip', 'pair2_pdq', 'pair2_pdq_hd',
            'pair2_sift', 'pair2_score', 'pair2_dropped',
            'pair3_mtb', 'pair3_ssim', 'pair3_clip', 'pair3_pdq', 'pair3_pdq_hd',
            'pair3_sift', 'pair3_score', 'pair3_dropped',
            'duplicates_removed', 'accuracy_pct'
        ]

    def load_images(self):
        """Load image groups (same as in deduplication.py __main__)"""
        folders = [
            "photos-706-winchester-blvd--los-gatos--ca-9",
            "photos-75-knollview-way--san-francisco--ca"
        ]

        self.image_groups = []
        for folder in folders:
            folder_path = Path(folder)
            if folder_path.exists():
                folder_images = sorted(folder_path.glob("*.jpg"))
                for img in folder_images:
                    self.image_groups.append([str(img)])

        # Fallback: Hardcoded paths
        if not self.image_groups:
            self.image_groups = [
                [r"combined\008_Nancy Peppin - IMG_0009.jpg"],
                [r"combined\009_Nancy Peppin - IMG_0003.jpg"],
                [r"combined\050_Scott Wall - DSC_0098.jpg"],
                [r"combined\053_Scott Wall - DSC_0143.jpg"],
            ]

        print(f"Loaded {len(self.image_groups)} image groups")

    def precompute_metrics(self):
        """Precompute Phase 1 metrics (MTB, SSIM, CLIP, PDQ) for all images"""
        print("\n[PRECOMPUTE] Computing metrics for all images...")
        mids = [g[len(g)//2] for g in self.image_groups]

        # Use deduplication module's _metric_worker
        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=dedupe.MAX_WORKERS) as pool:
            futures = [pool.submit(dedupe._metric_worker, p) for p in mids]
            for fut in as_completed(futures):
                m = fut.result()
                self.cached_metrics[m["path"]] = m
                dedupe._metric_store[m["path"]] = m  # Also populate global store
                print(f"  - Cached metrics for {Path(m['path']).name}")

        print(f"[PRECOMPUTE] Cached metrics for {len(self.cached_metrics)} images\n")

    def run_single_experiment(self, exp_id: int, weights: Dict[str, float]) -> Dict[str, Any]:
        """
        Run one experiment with given weights.

        Args:
            exp_id: Experiment ID (1-indexed)
            weights: Dict with keys 'mtb', 'ssim', 'clip', 'pdq', 'sift'

        Returns:
            Dict with experiment results
        """
        # Set weights globally
        dedupe.set_weights(
            mtb=weights['mtb'],
            ssim=weights['ssim'],
            clip=weights['clip'],
            pdq=weights['pdq'],
            sift=weights['sift']
        )

        # Run deduplication (metrics already cached in _metric_store)
        # Note: We're not using ExperimentLogger here to avoid overhead
        # We'll manually collect results

        mids = [g[len(g)//2] for g in self.image_groups]

        # Compute pair similarities (SIFT is computed on-demand)
        pairs_results = []

        # Pairs: (0,1), (1,2), (2,3) - sequential pairs
        pair_indices = [(i, i+1) for i in range(len(self.image_groups)-1)]

        for i, j in pair_indices:
            mtb, edge, hd, ssim, clip, sift_matches = dedupe._pair_sim(mids[i], mids[j])

            # Compute score using current weights
            w_mtb = dedupe.WEIGHT_MTB
            w_ssim = dedupe.WEIGHT_SSIM
            w_clip = dedupe.WEIGHT_CLIP
            w_pdq = dedupe.WEIGHT_PDQ
            w_sift = dedupe.WEIGHT_SIFT

            mtb_floor = dedupe.MTB_HARD_FLOOR
            pdq_ceil = dedupe.PDQ_HD_CEIL

            sift_score = min(sift_matches / 100.0, 1.0) if sift_matches > 0 else 0.0

            score = (
                w_mtb  * (mtb  / 100.0) +
                w_ssim * (ssim / 100.0) +
                w_clip * (clip / 100.0) +
                w_pdq  * (0.0 if hd >= pdq_ceil else 1.0 - hd / pdq_ceil) +
                w_sift * sift_score
            )

            # Decision logic (no SIFT override since it's disabled)
            dup_threshold = dedupe.COMPOSITE_DUP_THRESHOLD

            dropped = False
            if score >= dup_threshold and mtb >= mtb_floor and hd < pdq_ceil:
                dropped = True

            pairs_results.append({
                'mtb': mtb,
                'ssim': ssim,
                'clip': clip,
                'pdq': hd,  # Store Hamming distance
                'sift': sift_matches,
                'score': score,
                'dropped': dropped
            })

        # Calculate summary stats
        duplicates_removed = sum(1 for p in pairs_results if p['dropped'])

        # Accuracy: We know pairs 0 and 2 are duplicates (2 total)
        # 100% = 2/2, 50% = 1/2, 0% = 0/2
        # Pair 0 (index 0,1) and Pair 2 (index 2,3) should be dropped
        correct_drops = 0
        if len(pairs_results) >= 1 and pairs_results[0]['dropped']:  # Pair 1 (Nancy Peppin)
            correct_drops += 1
        if len(pairs_results) >= 3 and pairs_results[2]['dropped']:  # Pair 3 (Scott Wall)
            correct_drops += 1

        accuracy_pct = (correct_drops / 2.0) * 100.0

        # Build result dict
        result = {
            'exp_id': exp_id,
            'w_mtb': weights['mtb'],
            'w_ssim': weights['ssim'],
            'w_clip': weights['clip'],
            'w_pdq': weights['pdq'],
            'w_sift': weights['sift'],
            'duplicates_removed': duplicates_removed,
            'accuracy_pct': accuracy_pct
        }

        # Add pair-specific results
        for i, p in enumerate(pairs_results, 1):
            result[f'pair{i}_mtb'] = p['mtb']
            result[f'pair{i}_ssim'] = p['ssim']
            result[f'pair{i}_clip'] = p['clip']
            result[f'pair{i}_pdq'] = p['pdq']  # Store as pdq for CSV
            result[f'pair{i}_pdq_hd'] = p['pdq']  # Also store with _hd suffix
            result[f'pair{i}_sift'] = p['sift']
            result[f'pair{i}_score'] = p['score']
            result[f'pair{i}_dropped'] = p['dropped']

        return result

    def write_csv_header(self):
        """Initialize CSV file with header"""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_fieldnames)
            writer.writeheader()

    def append_to_csv(self, result: Dict[str, Any]):
        """Append one result row to CSV"""
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_fieldnames)
            writer.writerow(result)

    def should_write_markdown(self, exp_id: int, result: Dict[str, Any]) -> bool:
        """Decide whether to write detailed markdown for this experiment"""
        # Write markdown for:
        # - First 10 experiments
        # - Last 10 experiments
        # - Every 100th experiment
        # - Experiments with interesting accuracy (50% or 100%)

        total_experiments = self.test_limit or 1001

        if exp_id <= 10:
            return True
        if exp_id > total_experiments - 10:
            return True
        if exp_id % 100 == 0:
            return True
        if result['accuracy_pct'] in [50.0, 100.0]:
            return True

        return False

    def write_markdown(self, exp_id: int, weights: Dict[str, float], result: Dict[str, Any]):
        """Write detailed markdown file for one experiment"""
        md_path = self.experiments_dir / f"exp_weights_{exp_id:04d}.md"

        content = f"""# Experiment {exp_id}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration

| Parameter | Value |
|-----------|-------|
| WEIGHT_MTB | {weights['mtb']} |
| WEIGHT_SSIM | {weights['ssim']} |
| WEIGHT_CLIP | {weights['clip']} |
| WEIGHT_PDQ | {weights['pdq']} |
| WEIGHT_SIFT | {weights['sift']} |
| COMPOSITE_DUP_THRESHOLD | {dedupe.COMPOSITE_DUP_THRESHOLD} |
| MTB_HARD_FLOOR | {dedupe.MTB_HARD_FLOOR} |
| PDQ_HD_CEIL | {dedupe.PDQ_HD_CEIL} |
| SIFT_MIN_MATCHES | {dedupe.SIFT_MIN_MATCHES} |
| SIFT_OVERRIDE | False (disabled) |

## Results

| Pair | MTB % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? |
|------|-------|--------|--------|--------|------|-------|----------|
| Pair 1 | {result['pair1_mtb']:.1f} | {result['pair1_ssim']:.1f} | {result['pair1_clip']:.1f} | {result['pair1_pdq_hd']} | {result['pair1_sift']} | {result['pair1_score']:.3f} | {'Yes' if result['pair1_dropped'] else 'No'} |
| Pair 2 | {result['pair2_mtb']:.1f} | {result['pair2_ssim']:.1f} | {result['pair2_clip']:.1f} | {result['pair2_pdq_hd']} | {result['pair2_sift']} | {result['pair2_score']:.3f} | {'Yes' if result['pair2_dropped'] else 'No'} |
| Pair 3 | {result['pair3_mtb']:.1f} | {result['pair3_ssim']:.1f} | {result['pair3_clip']:.1f} | {result['pair3_pdq_hd']} | {result['pair3_sift']} | {result['pair3_score']:.3f} | {'Yes' if result['pair3_dropped'] else 'No'} |

## Summary

- **Duplicates removed:** {result['duplicates_removed']}
- **Accuracy:** {result['accuracy_pct']:.0f}% (correct duplicates: {int(result['accuracy_pct']/50)}/2)

## Notes

- Pair 1 (Nancy Peppin photos) and Pair 3 (Scott Wall photos) are known duplicates
- Pair 2 (cross-property) is NOT a duplicate
- Accuracy = (correct drops / 2) * 100%
"""

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def run_all_experiments(self):
        """Main batch loop"""
        weights_list = generate_weights()

        if self.test_limit:
            weights_list = weights_list[:self.test_limit]
            print(f"[TEST MODE] Running first {self.test_limit} experiments only\n")

        total = len(weights_list)

        # Initialize CSV
        self.write_csv_header()
        print(f"[CSV] Initialized {self.csv_path}\n")

        # Track timing
        start_time = time.time()

        # Main loop
        for i, weights in enumerate(weights_list, 1):
            exp_start = time.time()

            print(f"\n[{i}/{total}] Experiment {i}")
            print(f"  Weights: MTB={weights['mtb']:.1f}, SSIM={weights['ssim']:.1f}, "
                  f"CLIP={weights['clip']:.1f}, PDQ={weights['pdq']:.1f}, SIFT={weights['sift']:.1f}")

            # Run experiment
            result = self.run_single_experiment(i, weights)

            # Write to CSV
            self.append_to_csv(result)

            # Optionally write markdown
            if self.should_write_markdown(i, result):
                self.write_markdown(i, weights, result)
                print(f"  [MD] Written to exp_weights_{i:04d}.md")

            exp_elapsed = time.time() - exp_start
            total_elapsed = time.time() - start_time

            # Progress update
            avg_time = total_elapsed / i
            remaining = (total - i) * avg_time
            print(f"  Result: {result['duplicates_removed']} duplicates, "
                  f"{result['accuracy_pct']:.0f}% accuracy")
            print(f"  Time: {exp_elapsed:.1f}s (avg: {avg_time:.1f}s, est. remaining: {remaining/60:.1f}min)")

        # Final summary
        total_elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"[COMPLETE] All {total} experiments finished in {total_elapsed/60:.1f} minutes")
        print(f"[CSV] Results saved to: {self.csv_path}")
        print(f"[MD]  Markdown files in: {self.experiments_dir}/")
        print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Run batch weight experiments")
    parser.add_argument("--test", type=int, default=None,
                        help="Test mode: only run first N experiments (e.g., --test 10)")
    parser.add_argument("--output-dir", type=str, default="batch_results",
                        help="Output directory for results")

    args = parser.parse_args()

    print("="*60)
    print("BATCH WEIGHT EXPERIMENT RUNNER")
    print("="*60)

    # Create runner
    runner = BatchExperimentRunner(output_dir=args.output_dir, test_limit=args.test)

    # Load images
    runner.load_images()

    # Precompute metrics (Phase 1 - done once)
    runner.precompute_metrics()

    # Run all experiments
    runner.run_all_experiments()


if __name__ == "__main__":
    main()
