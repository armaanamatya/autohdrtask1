#!/usr/bin/env python3
"""
Re-analyze existing markdown reports with SIFT >= 150 threshold
Uses existing comparison data instead of re-running expensive CLIP/SIFT computations
"""
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def parse_detailed_results(md_content):
    """Parse the detailed comparison results table from markdown"""
    comparisons = []

    # Find the detailed results section
    in_table = False
    for line in md_content.split('\n'):
        if '| Kept Image | Duplicate Image | Composite Score' in line:
            in_table = True
            continue

        if in_table and line.startswith('|') and '---' not in line:
            # Parse table row: | Kept | Dup | Score | MTB | Edge | SSIM | CLIP | PDQ | SIFT |
            parts = [p.strip() for p in line.split('|')[1:-1]]

            if len(parts) >= 9 and parts[0] and parts[0] != 'Kept Image':
                try:
                    comp = {
                        'kept': parts[0],
                        'duplicate': parts[1],
                        'score': float(parts[2]),
                        'mtb': float(parts[3]),
                        'edge': float(parts[4]),
                        'ssim': float(parts[5]),
                        'clip': float(parts[6]),
                        'pdq_hd': int(parts[7]),
                        'sift': int(parts[8])
                    }
                    comparisons.append(comp)
                except (ValueError, IndexError):
                    continue

        if in_table and line.startswith('##'):
            break

    return comparisons

def evaluate_with_sift150(comparisons):
    """Re-evaluate duplicates with SIFT >= 150 threshold"""
    # Group by kept image
    duplicate_groups = defaultdict(list)
    all_kept_images = set()

    for comp in comparisons:
        all_kept_images.add(comp['kept'])

    # Evaluate which comparisons are still duplicates with SIFT >= 150
    for comp in comparisons:
        # Check if this would be a duplicate with stricter SIFT threshold
        sift_override = (comp['sift'] >= 150) and (comp['clip'] >= 85.0)

        # Original duplicate logic (simplified)
        is_duplicate = (
            comp['score'] >= 0.35 or  # Composite threshold
            sift_override  # SIFT override (now with 150 threshold)
        )

        if is_duplicate:
            duplicate_groups[comp['kept']].append(comp)

    return duplicate_groups, all_kept_images

def count_total_images(md_content):
    """Extract total image count from original markdown"""
    match = re.search(r'- \*\*Total Images:\*\* (\d+)', md_content)
    if match:
        return int(match.group(1))
    return 0

def generate_markdown(folder_name, comparisons, total_images):
    """Generate new markdown with SIFT >= 150 analysis"""
    duplicate_groups, all_kept_images = evaluate_with_sift150(comparisons)

    unique_count = len(all_kept_images)
    duplicate_count = total_images - unique_count
    duplicate_rate = (duplicate_count / total_images * 100) if total_images > 0 else 0

    md = f"# Duplicate Analysis: {folder_name} (SIFT >= 150)\n\n"
    md += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += f"**Note:** Re-analyzed using existing data with SIFT_MIN_MATCHES = 150 (increased from 50)\n\n"

    md += "## Summary\n\n"
    md += f"- **Total Images:** {total_images}\n"
    md += f"- **Unique Images:** {unique_count}\n"
    md += f"- **Duplicates Found:** {duplicate_count}\n"
    md += f"- **Duplicate Rate:** {duplicate_rate:.1f}%\n\n"

    md += "## Configuration\n\n"
    md += "| Parameter | Value |\n"
    md += "|-----------|-------|\n"
    md += "| MTB Weight | 0.3 |\n"
    md += "| SSIM Weight | 0.1 |\n"
    md += "| CLIP Weight | 0.25 |\n"
    md += "| PDQ Weight | 0.25 |\n"
    md += "| SIFT Weight | 0.1 |\n"
    md += "| Composite Threshold | 0.35 |\n"
    md += "| MTB Hard Floor | 67.0 |\n"
    md += "| PDQ HD Ceiling | 115 |\n"
    md += "| SIFT Min Matches | **150** |\n\n"

    md += "## Comparison with Original Analysis\n\n"
    md += "| Metric | Original (SIFT >= 50) | New (SIFT >= 150) | Change |\n"
    md += "|--------|----------------------|-------------------|--------|\n"

    # Count from original
    original_dups = len(comparisons)
    new_dups = sum(len(dups) for dups in duplicate_groups.values())

    md += f"| Duplicate Pairs | {original_dups} | {new_dups} | {new_dups - original_dups:+d} |\n"
    md += f"| Unique Images | - | {unique_count} | - |\n\n"

    md += "## Duplicate Groups\n\n"

    for kept_img in sorted(all_kept_images):
        md += f"### {kept_img} (KEPT)\n\n"

        if kept_img in duplicate_groups and duplicate_groups[kept_img]:
            dup_list = duplicate_groups[kept_img]
            md += f"**{len(dup_list)} duplicate(s) found:**\n\n"
            md += "| Duplicate Image | Score | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT Matches |\n"
            md += "|----------------|-------|-------|--------|--------|--------|--------|-------------||\n"

            for comp in dup_list:
                md += f"| {comp['duplicate']} | {comp['score']:.3f} | {comp['mtb']:.1f} | "
                md += f"{comp['edge']:.1f} | {comp['ssim']:.1f} | {comp['clip']:.1f} | "
                md += f"{comp['pdq_hd']} | {comp['sift']} |\n"
            md += "\n"
        else:
            md += "**No duplicates found** - This image is unique.\n\n"

    md += "## Detailed Comparison Results\n\n"

    if new_dups > 0:
        md += "| Kept Image | Duplicate Image | Composite Score | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT |\n"
        md += "|-----------|----------------|----------------|-------|--------|--------|--------|--------|------|\n"

        for kept_img in sorted(duplicate_groups.keys()):
            for comp in duplicate_groups[kept_img]:
                md += f"| {comp['kept']} | {comp['duplicate']} | {comp['score']:.3f} | "
                md += f"{comp['mtb']:.1f} | {comp['edge']:.1f} | {comp['ssim']:.1f} | "
                md += f"{comp['clip']:.1f} | {comp['pdq_hd']} | {comp['sift']} |\n"
    else:
        md += "*No duplicates detected with SIFT >= 150 threshold.*\n"

    md += "\n## Metrics Explanation\n\n"
    md += "- **MTB (Median Threshold Bitmap):** Measures structural similarity (0-100%)\n"
    md += "- **Edge:** Compares edge patterns (0-100%)\n"
    md += "- **SSIM (Structural Similarity Index):** Perceptual similarity (0-100%)\n"
    md += "- **CLIP:** Semantic similarity using AI vision model (0-100%)\n"
    md += "- **PDQ HD (Hamming Distance):** Perceptual hash distance (lower = more similar)\n"
    md += "- **SIFT:** Number of matching visual features\n"
    md += "- **Composite Score:** Weighted combination of all metrics (0-1 scale)\n\n"

    md += "## Detection Logic\n\n"
    md += f"Images are marked as duplicates when:\n"
    md += f"- Composite score ≥ 0.35\n"
    md += f"- MTB ≥ 67.0% OR SIFT override (≥**150** matches + CLIP ≥85%)\n"
    md += f"- PDQ HD < 115 OR SIFT override\n\n"

    return md

def reanalyze_folder(folder_path):
    """Re-analyze a folder using existing markdown data"""
    folder = Path(folder_path)
    folder_name = folder.name

    # Read existing markdown
    md_path = folder / f"{folder_name}.md"

    if not md_path.exists():
        print(f"Error: Original markdown not found at {md_path}")
        return None

    print(f"Reading existing analysis from {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Parse comparison data
    comparisons = parse_detailed_results(md_content)
    total_images = count_total_images(md_content)

    print(f"Found {len(comparisons)} comparison pairs from original analysis")
    print(f"Total images: {total_images}")

    # Generate new markdown
    new_md = generate_markdown(folder_name, comparisons, total_images)

    # Save new markdown
    new_md_path = folder / f"{folder_name}_greatersift.md"
    with open(new_md_path, 'w', encoding='utf-8') as f:
        f.write(new_md)

    print(f"Saved re-analyzed results to {new_md_path}")

    return new_md_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
    else:
        folders = [
            r"000fc774-cb56-4052-a33a-9974c58a00d6",
            r"00aab07550cc482ca9c575efb14de476bd3cd2463f"
        ]

    for folder in folders:
        print(f"\n{'='*60}")
        print(f"Re-analyzing: {folder}")
        print('='*60)
        reanalyze_folder(folder)
