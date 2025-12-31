#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compare MTB multi-metric vs CNN deduplication methods across all folders
"""

import logging
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

import cv2
import numpy as np

# Import from existing modules
from deduplication import (
    _metric_worker, _pair_sim, _metric_store,
    WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT,
    COMPOSITE_DUP_THRESHOLD, MTB_HARD_FLOOR, PDQ_HD_CEIL, SIFT_MIN_MATCHES
)

from imagededup.methods import CNN
from sklearn.metrics.pairwise import cosine_similarity

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class PairComparison:
    """Results from comparing two images with MTB method"""
    img_a: str
    img_b: str
    mtb: float
    edge: float
    ssim: float
    clip: float
    pdq_hd: int
    sift_matches: int
    score: float
    would_drop: bool
    drop_reason: str


@dataclass
class MTBResults:
    """Results from MTB multi-metric deduplication on a folder"""
    folder_name: str
    images: List[str]
    comparisons: List[PairComparison] = field(default_factory=list)
    dropped_images: Set[str] = field(default_factory=set)


@dataclass
class DuplicateCluster:
    """A cluster of duplicate images found by CNN method"""
    images: List[str]
    kept_image: str
    similarities: Dict[Tuple[str, str], float] = field(default_factory=dict)
    dropped_images: List[str] = field(default_factory=list)


@dataclass
class CNNResults:
    """Results from CNN deduplication on a folder"""
    folder_name: str
    images: List[str]
    clusters: List[DuplicateCluster] = field(default_factory=list)
    dropped_images: Set[str] = field(default_factory=set)


# ─── Helper Functions ─────────────────────────────────────────────────────────

def _get_image_quality_score(img_path: str) -> Tuple[int, int]:
    """
    Get quality score for an image based on resolution and file size.
    Returns: (width * height, file_size_bytes) for comparison
    """
    try:
        img = cv2.imread(img_path)
        if img is None:
            return (0, 0)

        height, width = img.shape[:2]
        file_size = os.path.getsize(img_path)

        return (width * height, file_size)
    except Exception:
        return (0, 0)


# ─── Main Comparison Class ────────────────────────────────────────────────────

class DedupComparison:
    """Compares MTB and CNN deduplication methods"""

    def __init__(self, images_base_dir: str, output_md_file: str):
        self.images_base_dir = images_base_dir
        self.output_md_file = output_md_file

    def discover_folders(self) -> List[Dict[str, Any]]:
        """
        Discover all UUID folders with processed subdirectories.

        Returns:
            List of folder info dicts sorted by name
        """
        base = Path(self.images_base_dir)
        folders = []

        logger.info(f"Discovering folders in {base}")

        for folder in sorted(base.iterdir()):
            if not folder.is_dir():
                continue

            processed_dir = folder / "processed"
            if processed_dir.exists():
                # Count images
                images = sorted([str(img) for img in processed_dir.glob("*.jpg")])
                if len(images) > 0:
                    folders.append({
                        'path': folder,
                        'uuid': folder.name,
                        'processed_dir': processed_dir,
                        'image_count': len(images),
                        'images': images
                    })

        logger.info(f"Discovered {len(folders)} folders with images")
        return folders

    def process_folder_mtb(self, folder_info: Dict[str, Any]) -> MTBResults:
        """
        Run MTB multi-metric deduplication logic WITHOUT deleting.

        This creates a "dry-run" version of deduplication.py's logic.
        """
        images = folder_info['images']
        folder_name = folder_info['uuid']

        # Skip folders with 0 or 1 images
        if len(images) <= 1:
            return MTBResults(
                folder_name=folder_name,
                images=[Path(img).name for img in images],
                comparisons=[],
                dropped_images=set()
            )

        logger.info(f"[MTB] Processing {folder_name}: {len(images)} images")

        # Compute metrics for all images
        with ThreadPoolExecutor(max_workers=16) as pool:
            for fut in as_completed(pool.submit(_metric_worker, img) for img in images):
                m = fut.result()
                _metric_store[m["path"]] = m

        # Compare all pairs (full scan within folder)
        comparisons = []
        dropped_images = set()

        for i in range(len(images)):
            for j in range(i + 1, len(images)):
                img_a, img_b = images[i], images[j]

                mtb, edge, hd, ssim, clip, sift_matches = _pair_sim(img_a, img_b)

                if hd == 999:  # Invalid comparison
                    continue

                # Calculate score
                sift_score = min(sift_matches / 100.0, 1.0) if sift_matches > 0 else 0.0
                score = (
                    WEIGHT_MTB * (mtb / 100.0) +
                    WEIGHT_SSIM * (ssim / 100.0) +
                    WEIGHT_CLIP * (clip / 100.0) +
                    WEIGHT_PDQ * (0.0 if hd >= PDQ_HD_CEIL else 1.0 - hd / PDQ_HD_CEIL) +
                    WEIGHT_SIFT * sift_score
                )

                # SIFT override (FIXED VERSION)
                sift_override = (sift_matches >= SIFT_MIN_MATCHES) and (clip >= 85.0)

                # Decision logic
                would_drop = False
                drop_reason = ""

                if score >= COMPOSITE_DUP_THRESHOLD:
                    if mtb < MTB_HARD_FLOOR and not sift_override:
                        drop_reason = f"MTB < {MTB_HARD_FLOOR}"
                    elif hd >= PDQ_HD_CEIL and not sift_override:
                        drop_reason = f"PDQ_HD >= {PDQ_HD_CEIL}"
                    else:
                        # Would drop img_a (first image in pair)
                        would_drop = True
                        dropped_images.add(img_a)
                        drop_reason = "duplicate"
                else:
                    drop_reason = f"SCORE < {COMPOSITE_DUP_THRESHOLD}"

                comparisons.append(PairComparison(
                    img_a=Path(img_a).name,
                    img_b=Path(img_b).name,
                    mtb=mtb, edge=edge, ssim=ssim, clip=clip,
                    pdq_hd=hd, sift_matches=sift_matches,
                    score=score,
                    would_drop=would_drop,
                    drop_reason=drop_reason
                ))

        # Clear metric store to free memory
        for img in images:
            _metric_store.pop(img, None)

        return MTBResults(
            folder_name=folder_name,
            images=[Path(img).name for img in images],
            comparisons=comparisons,
            dropped_images={Path(img).name for img in dropped_images}
        )

    def process_folder_cnn(self, folder_info: Dict[str, Any]) -> CNNResults:
        """
        Run CNN deduplication logic WITHOUT deleting.

        Uses imagededup CNN method to find duplicates.
        """
        images = folder_info['images']
        folder_name = folder_info['uuid']

        # Skip folders with 0 or 1 images
        if len(images) <= 1:
            return CNNResults(
                folder_name=folder_name,
                images=[Path(img).name for img in images],
                clusters=[],
                dropped_images=set()
            )

        logger.info(f"[CNN] Processing {folder_name}: {len(images)} images")

        # Initialize CNN
        cnn = CNN()
        threshold = 0.9  # Default threshold from imagededup_cnn_test.py

        # Generate encodings
        encodings = {}
        for img_path in images:
            try:
                enc = cnn.encode_image(image_file=img_path)
                encodings[img_path] = enc.squeeze()
            except Exception as e:
                logger.warning(f"Failed to encode {Path(img_path).name}: {e}")
                encodings[img_path] = None

        # Find duplicate clusters
        clusters = []
        assigned = set()
        dropped_images = set()

        valid_images = [img for img in images if encodings[img] is not None]

        for i, img_i in enumerate(valid_images):
            if img_i in assigned:
                continue

            cluster_images = [img_i]
            similarities = {}
            assigned.add(img_i)

            enc_i = encodings[img_i].reshape(1, -1)

            for j in range(i + 1, len(valid_images)):
                img_j = valid_images[j]
                if img_j in assigned:
                    continue

                enc_j = encodings[img_j].reshape(1, -1)
                similarity = cosine_similarity(enc_i, enc_j)[0, 0]

                if similarity >= threshold:
                    cluster_images.append(img_j)
                    similarities[(img_i, img_j)] = similarity
                    assigned.add(img_j)

            if len(cluster_images) > 1:
                # Find highest quality image
                best_img = max(cluster_images, key=lambda img: _get_image_quality_score(img))
                dropped = [img for img in cluster_images if img != best_img]

                clusters.append(DuplicateCluster(
                    images=[Path(img).name for img in cluster_images],
                    kept_image=Path(best_img).name,
                    similarities={(Path(a).name, Path(b).name): s for (a, b), s in similarities.items()},
                    dropped_images=[Path(img).name for img in dropped]
                ))

                dropped_images.update(dropped)

        return CNNResults(
            folder_name=folder_name,
            images=[Path(img).name for img in images],
            clusters=clusters,
            dropped_images={Path(img).name for img in dropped_images}
        )

    def generate_markdown_report(self, all_results: List[Dict[str, Any]]):
        """
        Generate comprehensive markdown report.

        Structure:
        - Executive Summary
        - Per-Folder Detailed Breakdown
        - Analysis & Insights
        """

        report = []

        # Header
        report.append("# Deduplication Method Comparison Report\n\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        report.append(f"**Base Directory:** {self.images_base_dir}\n\n")

        # Executive Summary
        report.append("## Executive Summary\n\n")

        total_folders = len(all_results)
        total_images = sum(r['image_count'] for r in all_results)

        mtb_total_dropped = sum(len(r['mtb_results'].dropped_images) for r in all_results)
        cnn_total_dropped = sum(len(r['cnn_results'].dropped_images) for r in all_results)

        # Count agreement (folders where both methods drop the same images)
        agreement_count = sum(1 for r in all_results
                             if r['mtb_results'].dropped_images == r['cnn_results'].dropped_images)

        report.append(f"- **Total Folders Processed:** {total_folders}\n")
        report.append(f"- **Total Images:** {total_images}\n")
        report.append(f"- **MTB Method:** Would drop {mtb_total_dropped} images\n")
        report.append(f"- **CNN Method:** Would drop {cnn_total_dropped} images\n")
        report.append(f"- **Agreement:** {agreement_count} folders (both methods agree)\n\n")

        # Configuration
        report.append("## Configuration\n\n")
        report.append("### MTB Multi-Metric Method\n\n")
        report.append("| Parameter | Value |\n")
        report.append("|-----------|-------|\n")
        report.append(f"| WEIGHT_MTB | {WEIGHT_MTB} |\n")
        report.append(f"| WEIGHT_SSIM | {WEIGHT_SSIM} |\n")
        report.append(f"| WEIGHT_CLIP | {WEIGHT_CLIP} |\n")
        report.append(f"| WEIGHT_PDQ | {WEIGHT_PDQ} |\n")
        report.append(f"| WEIGHT_SIFT | {WEIGHT_SIFT} |\n")
        report.append(f"| COMPOSITE_DUP_THRESHOLD | {COMPOSITE_DUP_THRESHOLD} |\n")
        report.append(f"| MTB_HARD_FLOOR | {MTB_HARD_FLOOR} |\n")
        report.append(f"| PDQ_HD_CEIL | {PDQ_HD_CEIL} |\n")
        report.append(f"| SIFT_MIN_MATCHES | {SIFT_MIN_MATCHES} |\n")
        report.append(f"| SIFT Override | Conditional (SIFT >= 50 AND CLIP >= 85%) |\n\n")

        report.append("### CNN Method\n\n")
        report.append("| Parameter | Value |\n")
        report.append("|-----------|-------|\n")
        report.append("| Threshold | 0.9 |\n")
        report.append("| Method | Cosine similarity on CNN embeddings |\n\n")

        # Per-Folder Breakdown
        report.append("---\n\n")
        report.append("## Per-Folder Detailed Results\n\n")

        for idx, result in enumerate(all_results, 1):
            folder_name = result['folder_name']
            image_count = result['image_count']
            mtb = result['mtb_results']
            cnn = result['cnn_results']

            report.append(f"### {idx}. Folder: `{folder_name}`\n\n")
            report.append(f"**Total Images:** {image_count}\n\n")

            # MTB Results
            report.append("#### MTB Multi-Metric Method\n\n")

            if len(mtb.dropped_images) == 0 and len(mtb.comparisons) == 0:
                report.append("*No comparisons possible (≤1 image)*\n\n")
            elif len(mtb.dropped_images) == 0:
                report.append("*No duplicates detected*\n\n")
            else:
                report.append(f"**Would Drop:** {len(mtb.dropped_images)} images\n\n")

            # Show all comparisons if any
            if len(mtb.comparisons) > 0:
                report.append("<details>\n")
                report.append("<summary>View All Comparisons</summary>\n\n")
                report.append("| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | Score | Drop? | Reason |\n")
                report.append("|---------|---------|-------|--------|--------|--------|--------|------|-------|-------|--------|\n")

                for comp in mtb.comparisons:
                    drop_str = "Yes" if comp.would_drop else "No"
                    report.append(f"| {comp.img_a} | {comp.img_b} | {comp.mtb:.1f} | {comp.edge:.1f} | {comp.ssim:.1f} | {comp.clip:.1f} | {comp.pdq_hd} | {comp.sift_matches} | {comp.score:.3f} | {drop_str} | {comp.drop_reason} |\n")

                report.append("\n</details>\n\n")

            # Summary of dropped images
            if len(mtb.dropped_images) > 0:
                report.append("**Dropped Images:**\n")
                for img in sorted(mtb.dropped_images):
                    report.append(f"- {img}\n")
                report.append("\n")

            # CNN Results
            report.append("#### CNN Method\n\n")

            if len(cnn.dropped_images) == 0 and len(cnn.clusters) == 0:
                report.append("*No comparisons possible (≤1 image)*\n\n")
            elif len(cnn.dropped_images) == 0:
                report.append("*No duplicates detected*\n\n")
            else:
                report.append(f"**Would Drop:** {len(cnn.dropped_images)} images\n\n")

            # Show clusters if any
            if len(cnn.clusters) > 0:
                report.append("<details>\n")
                report.append("<summary>View Duplicate Clusters</summary>\n\n")

                for cluster_idx, cluster in enumerate(cnn.clusters, 1):
                    report.append(f"**Cluster {cluster_idx}:** {len(cluster.images)} images\n\n")
                    report.append(f"- **KEEP:** {cluster.kept_image}\n")
                    for img in cluster.dropped_images:
                        report.append(f"- **DROP:** {img}\n")

                    # Show similarities
                    if cluster.similarities:
                        report.append("\nSimilarities:\n")
                        for (img_a, img_b), sim in cluster.similarities.items():
                            report.append(f"  - {img_a} ↔ {img_b}: {sim:.4f}\n")
                    report.append("\n")

                report.append("</details>\n\n")

            # Summary of dropped images
            if len(cnn.dropped_images) > 0:
                report.append("**Dropped Images:**\n")
                for img in sorted(cnn.dropped_images):
                    report.append(f"- {img}\n")
                report.append("\n")

            # Comparison
            report.append("#### Comparison\n\n")

            mtb_only = mtb.dropped_images - cnn.dropped_images
            cnn_only = cnn.dropped_images - mtb.dropped_images
            both = mtb.dropped_images & cnn.dropped_images

            if mtb_only or cnn_only:
                report.append("**Differences:**\n")
                if mtb_only:
                    report.append(f"- MTB only would drop: {', '.join(sorted(mtb_only))}\n")
                if cnn_only:
                    report.append(f"- CNN only would drop: {', '.join(sorted(cnn_only))}\n")
                if both:
                    report.append(f"- Both agree on: {', '.join(sorted(both))}\n")
            else:
                if len(mtb.dropped_images) == 0 and len(cnn.dropped_images) == 0:
                    report.append("*Both methods agree: no duplicates*\n")
                else:
                    report.append("*Both methods agree on all duplicates*\n")

            report.append("\n---\n\n")

        # Write to file
        with open(self.output_md_file, 'w', encoding='utf-8') as f:
            f.writelines(report)

        logger.info(f"Report written to {self.output_md_file}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Compare deduplication methods")
    parser.add_argument("--images-dir", type=str,
                        default=r"C:\Users\Armaan\Desktop\autohdrtask1\images",
                        help="Base directory containing UUID folders")
    parser.add_argument("--output", type=str,
                        default="deduplication_comparison_report.md",
                        help="Output markdown file")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit processing to first N folders (for testing)")

    args = parser.parse_args()

    logger.info("="*60)
    logger.info("DEDUPLICATION METHOD COMPARISON")
    logger.info("="*60)

    # Create comparison runner
    comparison = DedupComparison(
        images_base_dir=args.images_dir,
        output_md_file=args.output
    )

    # Discover folders
    folders = comparison.discover_folders()
    logger.info(f"Discovered {len(folders)} folders with images")

    if args.limit:
        folders = folders[:args.limit]
        logger.info(f"Processing first {args.limit} folders only")

    # Process each folder
    all_results = []

    for idx, folder_info in enumerate(folders, 1):
        logger.info(f"\n[{idx}/{len(folders)}] Processing {folder_info['uuid']}")

        # Process with MTB method
        mtb_results = comparison.process_folder_mtb(folder_info)

        # Process with CNN method
        cnn_results = comparison.process_folder_cnn(folder_info)

        all_results.append({
            'folder_name': folder_info['uuid'],
            'image_count': folder_info['image_count'],
            'mtb_results': mtb_results,
            'cnn_results': cnn_results
        })

    # Generate markdown report
    comparison.generate_markdown_report(all_results)

    logger.info("\n" + "="*60)
    logger.info("COMPARISON COMPLETE")
    logger.info(f"Results written to: {args.output}")
    logger.info("="*60)


if __name__ == "__main__":
    main()
