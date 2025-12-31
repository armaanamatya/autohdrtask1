#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deduplicationcluster.py – Clustering-based deduplication
Uses connected components to group duplicates, then keeps the BEST image from each cluster.

Key differences from deduplication.py:
1. Computes ALL pairwise similarities FIRST (no early stopping)
2. Builds clusters of duplicate images (connected components)
3. Picks highest quality image from each cluster
4. Global decision instead of sequential elimination
"""

from pathlib import Path
import sys
import logging
import cv2
import numpy as np
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Any, Union

# Import the metric computation from original deduplication
from deduplication import (
    _metric_worker,
    _pair_sim,
    _metric_store,
    _is_aerial,
    logger,
    ExperimentLogger,
    # Configuration
    WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT,
    COMPOSITE_DUP_THRESHOLD, MTB_HARD_FLOOR, PDQ_HD_CEIL, SIFT_MIN_MATCHES,
    AERIAL_WEIGHT_MTB, AERIAL_WEIGHT_SSIM, AERIAL_WEIGHT_CLIP,
    AERIAL_WEIGHT_PDQ, AERIAL_WEIGHT_SIFT,
    AERIAL_COMPOSITE_DUP_THRESHOLD, AERIAL_MTB_HARD_FLOOR, AERIAL_PDQ_HD_CEIL,
    AERIAL_SIFT_MIN_MATCHES,
    USE_CLIP
)
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

# ─── Quality Scoring ──────────────────────────────────────────────────────────
def compute_quality_score(image_path: str) -> float:
    """
    Compute a quality score for an image based on:
    - Resolution (width × height)
    - File size
    - Sharpness (Laplacian variance)

    Higher score = better quality
    """
    try:
        path = Path(image_path)

        # File size (bytes)
        file_size = path.stat().st_size

        # Image resolution
        img = cv2.imread(str(path))
        if img is None:
            return 0.0
        height, width = img.shape[:2]
        resolution = width * height

        # Sharpness (Laplacian variance)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()

        # Weighted quality score
        # Normalize components to similar scales
        quality = (
            resolution / 1_000_000 +      # Resolution in megapixels
            file_size / 1_000_000 +       # File size in MB
            sharpness / 100               # Sharpness (normalized)
        )

        return quality
    except Exception as e:
        logger.warning(f"Failed to compute quality for {image_path}: {e}")
        return 0.0


# ─── Connected Components (Union-Find) ────────────────────────────────────────
class UnionFind:
    """Union-Find data structure for building connected components"""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Find root of x with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """Union by rank"""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

    def get_components(self) -> Dict[int, List[int]]:
        """Get all connected components as dict of {root: [members]}"""
        components = defaultdict(list)
        for i in range(len(self.parent)):
            root = self.find(i)
            components[root].append(i)
        return dict(components)


# ─── Markdown Report Generation ──────────────────────────────────────────────
def generate_markdown_report(stats: Dict[str, Any], output_path: Path) -> None:
    """Generate a detailed markdown report of the clustering deduplication"""
    from datetime import datetime
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Clustering Deduplication Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Full Scan:** {stats['full_scan']}\n\n")
        
        # Summary Statistics
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total Images:** {stats['total_images']}\n")
        f.write(f"- **Total Comparisons:** {stats['total_comparisons']:,}\n")
        f.write(f"- **Duplicate Pairs Found:** {len(stats['duplicate_pairs'])}\n")
        f.write(f"- **Clusters Formed:** {len(stats['clusters'])}\n")
        f.write(f"- **Final Images:** {stats['final_count']}\n")
        f.write(f"- **Images Removed:** {stats['removed_count']}\n")
        f.write(f"- **Retention Rate:** {100.0 * stats['final_count'] / stats['total_images']:.1f}%\n\n")
        
        # Timing
        f.write("## Timing\n\n")
        timing = stats['timing']
        f.write(f"- **Metric Computation:** {timing.get('metric_computation', 0):.2f}s\n")
        f.write(f"- **Pairwise Comparisons:** {timing.get('comparison', 0):.2f}s\n")
        f.write(f"- **Clustering:** {timing.get('clustering', 0):.2f}s\n")
        f.write(f"- **Quality Scoring:** {timing.get('quality_scoring', 0):.2f}s\n")
        f.write(f"- **Total Time:** {timing.get('total', 0):.2f}s\n\n")
        
        # Configuration
        f.write("## Configuration\n\n")
        config = stats['config']
        f.write("### Regular Photos\n")
        f.write(f"- **Weights:** MTB={config['WEIGHT_MTB']}, SSIM={config['WEIGHT_SSIM']}, ")
        f.write(f"CLIP={config['WEIGHT_CLIP']}, PDQ={config['WEIGHT_PDQ']}, SIFT={config['WEIGHT_SIFT']}\n")
        f.write(f"- **Composite Threshold:** {config['COMPOSITE_DUP_THRESHOLD']}\n")
        f.write(f"- **MTB Floor:** {config['MTB_HARD_FLOOR']}\n")
        f.write(f"- **PDQ Ceiling:** {config['PDQ_HD_CEIL']}\n")
        f.write(f"- **SIFT Minimum:** {config['SIFT_MIN_MATCHES']}\n")
        f.write(f"- **USE_CLIP:** {config['USE_CLIP']}\n\n")
        
        f.write("### Aerial Photos\n")
        f.write(f"- **Weights:** MTB={AERIAL_WEIGHT_MTB}, SSIM={AERIAL_WEIGHT_SSIM}, ")
        f.write(f"CLIP={AERIAL_WEIGHT_CLIP}, PDQ={AERIAL_WEIGHT_PDQ}, SIFT={AERIAL_WEIGHT_SIFT}\n")
        f.write(f"- **Composite Threshold:** {config['AERIAL_COMPOSITE_DUP_THRESHOLD']}\n")
        f.write(f"- **MTB Floor:** {config['AERIAL_MTB_HARD_FLOOR']}\n")
        f.write(f"- **PDQ Ceiling:** {config['AERIAL_PDQ_HD_CEIL']}\n")
        f.write(f"- **SIFT Minimum:** {config['AERIAL_SIFT_MIN_MATCHES']}\n\n")
        
        # Duplicate Pairs
        f.write("## Duplicate Pairs\n\n")
        f.write(f"Found {len(stats['duplicate_pairs'])} duplicate pairs:\n\n")
        f.write("| Image A | Image B | Score | MTB | SSIM | CLIP | PDQ HD | SIFT | Override | Aerial |\n")
        f.write("|---------|---------|-------|-----|------|------|--------|------|----------|--------|\n")
        
        for pair in stats['duplicate_pairs']:
            override_str = "✓" if pair['sift_override'] else "✗"
            aerial_str = "✓" if pair['is_aerial'] else "✗"
            f.write(f"| {pair['img_i']} | {pair['img_j']} | {pair['score']:.3f} | ")
            f.write(f"{pair['mtb']:.1f} | {pair['ssim']:.1f} | {pair['clip']:.1f} | ")
            f.write(f"{pair['pdq_hd']} | {pair['sift_matches']} | {override_str} | {aerial_str} |\n")
        f.write("\n")
        
        # Clusters
        f.write("## Clusters\n\n")
        for cluster in sorted(stats['clusters'], key=lambda x: x['cluster_id']):
            f.write(f"### Cluster {cluster['cluster_id']} ({cluster['size']} images)\n\n")
            
            f.write("**Selected:** ")
            selected = cluster['selected']
            f.write(f"`{selected['name']}` (quality: {selected['quality']:.2f})\n\n")
            
            if cluster['dropped']:
                f.write("**Dropped:**\n")
                for dropped in sorted(cluster['dropped'], key=lambda x: x['quality'], reverse=True):
                    f.write(f"- `{dropped['name']}` (quality: {dropped['quality']:.2f})\n")
                f.write("\n")
            else:
                f.write("**Note:** Single image cluster (no duplicates found)\n\n")
        
        # Dropped Images Summary
        f.write("## Dropped Images Summary\n\n")
        f.write(f"Total images dropped: {len(stats['dropped_images'])}\n\n")
        f.write("| Image | Quality | Cluster | Selected Instead |\n")
        f.write("|-------|---------|---------|------------------|\n")
        
        for dropped in sorted(stats['dropped_images'], key=lambda x: x['quality'], reverse=True):
            f.write(f"| `{dropped['name']}` | {dropped['quality']:.2f} | ")
            f.write(f"{dropped['cluster_id']} | `{dropped['selected_instead']}` |\n")
        f.write("\n")
        
        # Representatives Summary
        f.write("## Selected Representatives\n\n")
        f.write(f"Total images kept: {len(stats['representatives'])}\n\n")
        for i, rep in enumerate(stats['representatives'], 1):
            f.write(f"{i}. `{rep}`\n")
        f.write("\n")
        
        # Override Statistics
        override_count = sum(1 for p in stats['duplicate_pairs'] if p['sift_override'])
        f.write("## Override Statistics\n\n")
        f.write(f"- **Pairs with SIFT Override:** {override_count} / {len(stats['duplicate_pairs'])}\n")
        f.write(f"- **Override Rate:** {100.0 * override_count / len(stats['duplicate_pairs']) if stats['duplicate_pairs'] else 0:.1f}%\n\n")
        
        if override_count > 0:
            f.write("### Pairs with Override\n\n")
            f.write("| Image A | Image B | SIFT | CLIP | Reason |\n")
            f.write("|---------|---------|------|------|--------|\n")
            for pair in stats['duplicate_pairs']:
                if pair['sift_override']:
                    reason = "SIFT ≥ 1.5×min" if pair['sift_matches'] >= pair['sift_min'] * 1.5 else "SIFT ≥ min + CLIP ≥ 85"
                    f.write(f"| {pair['img_i']} | {pair['img_j']} | {pair['sift_matches']} | ")
                    f.write(f"{pair['clip']:.1f} | {reason} |\n")
            f.write("\n")


# ─── Clustering Deduplication ─────────────────────────────────────────────────
def remove_near_duplicates_clustering(
    groups: List[List[str]],
    deduplication_flag: int = 0,
    metadata_dict: Dict[str, Dict[str, Any]] = None,
    full_scan: bool = True,  # Always use full scan for clustering
    return_stats: bool = False  # Return detailed statistics
) -> Union[List[List[str]], Tuple[List[List[str]], Dict[str, Any]]]:
    """
    Remove near-duplicates using clustering approach.

    Algorithm:
    1. Compute ALL pairwise similarities (no early stopping)
    2. Build clusters using connected components
    3. Pick best quality image from each cluster

    Returns: 
        - List of groups (one per cluster representative)
        - Statistics dict (if return_stats=True)
    """
    import time
    start_time = time.time()
    
    stats = {
        'full_scan': full_scan,
        'total_images': len(groups),
        'total_comparisons': 0,
        'duplicate_pairs': [],
        'clusters': [],
        'representatives': [],
        'dropped_images': [],
        'timing': {},
        'config': {}
    }
    
    if deduplication_flag != 1 or len(groups) < 2:
        if return_stats:
            stats['final_count'] = len(groups)
            stats['removed_count'] = 0
            stats['timing']['total'] = time.time() - start_time
            return groups, stats
        return groups

    mids = [g[len(g)//2] for g in groups]
    n = len(mids)
    stats['total_images'] = n

    # Pre-compute metrics for all images
    metric_start = time.time()
    logger.info("[STEP 1/4] Pre-computing metrics for %d images...", n)
    with ThreadPoolExecutor(max_workers=16) as pool:
        for fut in as_completed(pool.submit(_metric_worker, p) for p in mids):
            m = fut.result()
            _metric_store[m["path"]] = m
    stats['timing']['metric_computation'] = time.time() - metric_start

    if metadata_dict is None:
        metadata_dict = {}

    # Build comparison pairs (always full scan for clustering)
    pairs = [(i, j) for i in range(n-1) for j in range(i+1, n)]
    stats['total_comparisons'] = len(pairs)
    logger.info("[STEP 2/4] Computing %d pairwise similarities...", len(pairs))

    # Store all similarities and duplicate relationships
    similarities = []
    duplicate_pairs = []
    comparison_start = time.time()

    for i, j in pairs:
        mtb, edge, hd, ssim, clip, sift_matches = _pair_sim(mids[i], mids[j])

        if hd == 999:
            continue  # unusable comparison

        # Determine if aerial
        is_aerial_i = _is_aerial(mids[i], metadata_dict)
        is_aerial_j = _is_aerial(mids[j], metadata_dict)
        is_aerial_pair = is_aerial_i or is_aerial_j

        # Select weights
        if is_aerial_pair:
            w_mtb, w_ssim, w_clip, w_pdq, w_sift = (
                AERIAL_WEIGHT_MTB, AERIAL_WEIGHT_SSIM, AERIAL_WEIGHT_CLIP,
                AERIAL_WEIGHT_PDQ, AERIAL_WEIGHT_SIFT
            )
            dup_threshold = AERIAL_COMPOSITE_DUP_THRESHOLD
            mtb_floor = AERIAL_MTB_HARD_FLOOR
            pdq_ceil = AERIAL_PDQ_HD_CEIL
            sift_min = AERIAL_SIFT_MIN_MATCHES
        else:
            w_mtb, w_ssim, w_clip, w_pdq, w_sift = (
                WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT
            )
            dup_threshold = COMPOSITE_DUP_THRESHOLD
            mtb_floor = MTB_HARD_FLOOR
            pdq_ceil = PDQ_HD_CEIL
            sift_min = SIFT_MIN_MATCHES

        # Normalize SIFT
        sift_score = min(sift_matches / 100.0, 1.0) if sift_matches > 0 else 0.0

        # Compute composite score
        score = (
            w_mtb  * (mtb  / 100.0) +
            w_ssim * (ssim / 100.0) +
            w_clip * (clip / 100.0) +
            w_pdq  * (0.0 if hd >= pdq_ceil else 1.0 - hd / pdq_ceil) +
            w_sift * sift_score
        )

        similarities.append({
            'i': i, 'j': j,
            'mtb': mtb, 'edge': edge, 'ssim': ssim, 'clip': clip,
            'pdq_hd': hd, 'sift': sift_matches, 'score': score,
            'is_aerial': is_aerial_pair
        })

        # Check if duplicate using same logic as original
        sift_override = (sift_matches >= sift_min * 1.5) or (
            (sift_matches >= sift_min) and (clip >= 85.0)
        )

        # Decision logic
        mtb_failed = mtb < mtb_floor and not sift_override
        pdq_failed = hd >= pdq_ceil and not sift_override
        
        if mtb_failed:
            continue
        if pdq_failed:
            continue

        dup = (score >= dup_threshold) and (
            (mtb >= mtb_floor) or sift_override
        ) and (
            (hd < pdq_ceil) or sift_override
        )

        if dup:
            pair_info = {
                'i': i, 'j': j, 'score': score,
                'img_i': Path(mids[i]).name, 'img_j': Path(mids[j]).name,
                'mtb': mtb, 'ssim': ssim, 'clip': clip, 'pdq_hd': hd,
                'sift_matches': sift_matches, 'sift_override': sift_override,
                'is_aerial': is_aerial_pair,
                'threshold': dup_threshold, 'mtb_floor': mtb_floor,
                'pdq_ceil': pdq_ceil, 'sift_min': sift_min
            }
            duplicate_pairs.append((i, j, score, pair_info))
            stats['duplicate_pairs'].append(pair_info)

    stats['timing']['comparison'] = time.time() - comparison_start
    logger.info("[STEP 3/4] Found %d duplicate pairs", len(duplicate_pairs))

    # Build connected components (clusters)
    cluster_start = time.time()
    uf = UnionFind(n)
    for pair_data in duplicate_pairs:
        i, j = pair_data[0], pair_data[1]
        uf.union(i, j)

    components = uf.get_components()
    stats['timing']['clustering'] = time.time() - cluster_start
    logger.info("[STEP 4/4] Built %d clusters from %d images", len(components), n)

    # For each cluster, pick the best quality image
    quality_start = time.time()
    representatives = []
    quality_scores = {}
    cluster_details = []

    for cluster_id, members in components.items():
        logger.info(f"Cluster {cluster_id}: {len(members)} images")
        
        cluster_info = {
            'cluster_id': cluster_id,
            'size': len(members),
            'members': [],
            'selected': None,
            'dropped': []
        }

        # Compute quality for each member
        member_qualities = []
        for idx in members:
            if mids[idx] not in quality_scores:
                quality_scores[mids[idx]] = compute_quality_score(mids[idx])
            quality = quality_scores[mids[idx]]
            member_qualities.append((idx, quality))
            cluster_info['members'].append({
                'idx': idx,
                'path': mids[idx],
                'name': Path(mids[idx]).name,
                'quality': quality
            })
            logger.info(f"  - {Path(mids[idx]).name}: quality={quality:.2f}")

        # Pick best quality
        best_idx, best_quality = max(member_qualities, key=lambda x: x[1])
        representatives.append(best_idx)
        cluster_info['selected'] = {
            'idx': best_idx,
            'path': mids[best_idx],
            'name': Path(mids[best_idx]).name,
            'quality': best_quality
        }
        
        # Track dropped images
        for idx, quality in member_qualities:
            if idx != best_idx:
                cluster_info['dropped'].append({
                    'idx': idx,
                    'path': mids[idx],
                    'name': Path(mids[idx]).name,
                    'quality': quality
                })
                stats['dropped_images'].append({
                    'path': mids[idx],
                    'name': Path(mids[idx]).name,
                    'quality': quality,
                    'cluster_id': cluster_id,
                    'selected_instead': Path(mids[best_idx]).name
                })
        
        cluster_details.append(cluster_info)
        stats['clusters'] = cluster_details
        logger.info(f"  → Selected {Path(mids[best_idx]).name} (quality={best_quality:.2f})")
    
    stats['timing']['quality_scoring'] = time.time() - quality_start

    # Build final result
    final_groups = [groups[idx] for idx in sorted(representatives)]
    
    stats['representatives'] = [Path(mids[idx]).name for idx in sorted(representatives)]
    stats['final_count'] = len(final_groups)
    stats['removed_count'] = n - len(final_groups)
    stats['timing']['total'] = time.time() - start_time
    
    # Store configuration
    stats['config'] = {
        'USE_CLIP': USE_CLIP,
        'WEIGHT_MTB': WEIGHT_MTB,
        'WEIGHT_SSIM': WEIGHT_SSIM,
        'WEIGHT_CLIP': WEIGHT_CLIP,
        'WEIGHT_PDQ': WEIGHT_PDQ,
        'WEIGHT_SIFT': WEIGHT_SIFT,
        'COMPOSITE_DUP_THRESHOLD': COMPOSITE_DUP_THRESHOLD,
        'MTB_HARD_FLOOR': MTB_HARD_FLOOR,
        'PDQ_HD_CEIL': PDQ_HD_CEIL,
        'SIFT_MIN_MATCHES': SIFT_MIN_MATCHES,
        'AERIAL_COMPOSITE_DUP_THRESHOLD': AERIAL_COMPOSITE_DUP_THRESHOLD,
        'AERIAL_MTB_HARD_FLOOR': AERIAL_MTB_HARD_FLOOR,
        'AERIAL_PDQ_HD_CEIL': AERIAL_PDQ_HD_CEIL,
        'AERIAL_SIFT_MIN_MATCHES': AERIAL_SIFT_MIN_MATCHES
    }

    logger.info("[RESULT] Clusters: %d → Representatives: %d", len(components), len(final_groups))
    logger.info("[RESULT] Images: %d → %d (removed %d)", n, len(final_groups), n - len(final_groups))

    if return_stats:
        return final_groups, stats
    return final_groups


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Clustering-based near-duplicate image remover"
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
        default="cluster_experiment_logs.md",
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
                folder_images = sorted(folder_path.glob("*.jpg"))
                logger.info(f"  → {folder}: {len(folder_images)} images")
                for img in folder_images:
                    groups.append([str(img)])
            else:
                logger.warning(f"  → {folder}: NOT FOUND, skipping")
    else:
        # Default test folder
        logger.info("No folders specified, using default test folder...")
        default_folder = r"c:\Users\Armaan\Desktop\autohdrtask1\00a959b5-1b0b-4670-9c07-5df8b7636cfe\processed"

        folder_path = Path(default_folder)
        if folder_path.exists():
            folder_images = sorted(folder_path.glob("*.jpg"))
            logger.info(f"  → {default_folder}: {len(folder_images)} images")
            for img in folder_images:
                groups.append([str(img)])

    if not groups:
        logger.error("No images found! Exiting.")
        sys.exit(1)

    n = len(groups)
    num_comparisons = (n * (n - 1)) // 2

    logger.info("=" * 70)
    logger.info("CLUSTERING MODE - Connected Components")
    logger.info("=" * 70)
    logger.info(f"Total images: {n}")
    logger.info(f"Total comparisons: {num_comparisons:,} pairs")
    logger.info("")
    logger.info("Configuration:")
    logger.info(f"  USE_CLIP: {USE_CLIP}")
    logger.info(f"  Weights: MTB={WEIGHT_MTB}, SSIM={WEIGHT_SSIM}, CLIP={WEIGHT_CLIP}, PDQ={WEIGHT_PDQ}, SIFT={WEIGHT_SIFT}")
    logger.info(f"  Threshold: {COMPOSITE_DUP_THRESHOLD}")
    logger.info(f"  Safety: MTB_floor={MTB_HARD_FLOOR}, PDQ_ceil={PDQ_HD_CEIL}, SIFT_min={SIFT_MIN_MATCHES}")
    logger.info("=" * 70)

    # Run clustering deduplication
    logger.info("Starting clustering-based deduplication...")
    filtered, stats = remove_near_duplicates_clustering(
        groups,
        deduplication_flag=1,
        metadata_dict={},
        full_scan=True,
        return_stats=True
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

    logger.info("\n✓ Done!")
    
    # Generate markdown report
    if args.folders:
        # Extract parent folder name if path contains 'processed' or similar
        folder_path = Path(args.folders[0])
        if folder_path.name == "processed" and folder_path.parent.exists():
            folder_name = folder_path.parent.name
        else:
            folder_name = folder_path.name
        # Save report in the folder's parent directory
        report_dir = folder_path.parent if folder_path.name == "processed" else folder_path
        report_path = report_dir / f"{folder_name}_cluster_report.md"
    else:
        folder_name = "00a959b5-1b0b-4670-9c07-5df8b7636cfe"
        report_path = Path(f"{folder_name}_cluster_report.md")
    
    generate_markdown_report(stats, report_path)
    logger.info(f"\n📊 Detailed report saved to: {report_path}")
