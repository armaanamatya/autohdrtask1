#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fullscandeduplication.py – Full-scan version of deduplication
Uses full_scan=True to compare ALL image pairs (O(N²) complexity)

This mode is more thorough but significantly slower than the default sequential mode.
Use this when:
- Images are not pre-sorted/grouped
- You want to catch ALL possible duplicates regardless of ordering
- Dataset size is small-medium (< 100 images)

For large datasets (> 100 images), consider pre-sorting images before using sequential mode.
"""

from pathlib import Path
import sys
import logging

# Import the deduplication module
from deduplication import (
    remove_near_duplicates,
    logger,
    ExperimentLogger,
    _experiment_logger,
    WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT,
    COMPOSITE_DUP_THRESHOLD, MTB_HARD_FLOOR, PDQ_HD_CEIL, SIFT_MIN_MATCHES,
    USE_CLIP
)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Full-scan near-duplicate image remover (compares all pairs)"
    )
    parser.add_argument(
        "--folders",
        nargs="+",
        help="Folders containing images to deduplicate"
    )
    parser.add_argument(
        "--log-experiment",
        type=str,
        default=None,
        help="Name for this experiment"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="fullscan_experiment_logs.md",
        help="File to log experiment results to"
    )
    args = parser.parse_args()

    # Load images from specified folders
    groups = []

    if args.folders:
        logger.info(f"Loading images from {len(args.folders)} folders...")
        for folder in args.folders:
            folder_path = Path(folder)
            if folder_path.exists():
                # Sort images within each folder for consistent ordering
                folder_images = sorted(folder_path.glob("*.jpg"))
                logger.info(f"  → {folder}: {len(folder_images)} images")
                for img in folder_images:
                    groups.append([str(img)])
            else:
                logger.warning(f"  → {folder}: NOT FOUND, skipping")
    else:
        # Default test folders
        logger.info("No folders specified, using default test folders...")
        default_folders = [
            r"c:\Users\Armaan\Desktop\autohdrtask1\000fc774-cb56-4052-a33a-9974c58a00d6\processed",
        ]

        for folder in default_folders:
            folder_path = Path(folder)
            if folder_path.exists():
                folder_images = sorted(folder_path.glob("*.jpg"))
                logger.info(f"  → {folder}: {len(folder_images)} images")
                for img in folder_images:
                    groups.append([str(img)])

    if not groups:
        logger.error("No images found! Exiting.")
        sys.exit(1)

    # Calculate number of comparisons
    n = len(groups)
    num_comparisons = (n * (n - 1)) // 2

    logger.info("=" * 70)
    logger.info("FULL SCAN MODE - All-to-All Comparison")
    logger.info("=" * 70)
    logger.info(f"Total images: {n}")
    logger.info(f"Total comparisons: {num_comparisons:,} pairs")
    logger.info(f"Complexity: O(N²)")
    logger.info("")
    logger.info("Configuration:")
    logger.info(f"  USE_CLIP: {USE_CLIP}")
    logger.info(f"  Weights: MTB={WEIGHT_MTB}, SSIM={WEIGHT_SSIM}, CLIP={WEIGHT_CLIP}, PDQ={WEIGHT_PDQ}, SIFT={WEIGHT_SIFT}")
    logger.info(f"  Threshold: {COMPOSITE_DUP_THRESHOLD}")
    logger.info(f"  Safety: MTB_floor={MTB_HARD_FLOOR}, PDQ_ceil={PDQ_HD_CEIL}, SIFT_min={SIFT_MIN_MATCHES}")
    logger.info("=" * 70)

    # Setup experiment logging if requested
    if args.log_experiment:
        import deduplication
        deduplication._experiment_logger = ExperimentLogger()
        deduplication._experiment_logger.start_capture()
        deduplication._experiment_logger.input_count = len(groups)

    # Run deduplication with full_scan=True
    logger.info("Starting full-scan deduplication...")
    filtered = remove_near_duplicates(
        groups,
        deduplication_flag=1,
        metadata_dict={},  # Could extract metadata if needed
        full_scan=True     # ⚠️ KEY DIFFERENCE: Compare ALL pairs
    )

    logger.info("=" * 70)
    logger.info("RESULTS")
    logger.info("=" * 70)
    logger.info(f"Input images:  {len(groups)}")
    logger.info(f"Output images: {len(filtered)}")
    logger.info(f"Duplicates removed: {len(groups) - len(filtered)}")
    logger.info(f"Retention rate: {100.0 * len(filtered) / len(groups):.1f}%")
    logger.info("=" * 70)

    # Print remaining images
    logger.info("\nRemaining images:")
    for idx, group in enumerate(filtered, 1):
        logger.info(f"  {idx}. {Path(group[0]).name}")

    # Write experiment log if requested
    if args.log_experiment and deduplication._experiment_logger:
        deduplication._experiment_logger.output_count = len(filtered)
        terminal_output = deduplication._experiment_logger.stop_capture()
        deduplication._experiment_logger.write_experiment_log(
            args.log_experiment,
            terminal_output,
            args.log_file
        )

    logger.info("\n✓ Done!")
