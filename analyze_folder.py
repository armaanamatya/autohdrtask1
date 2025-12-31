#!/usr/bin/env python3
"""
Analyze a folder for duplicates and generate comprehensive markdown report
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from deduplication import remove_near_duplicates, _metric_store, _pair_sim
from deduplication import COMPOSITE_DUP_THRESHOLD, MTB_HARD_FLOOR, PDQ_HD_CEIL
from deduplication import WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT
from deduplication import SIFT_MIN_MATCHES

def analyze_folder_with_report(folder_path):
    """
    Analyze folder for duplicates and generate comprehensive report
    """
    folder = Path(folder_path)
    folder_name = folder.name

    # Find images
    processed_folder = folder / "processed" if (folder / "processed").exists() else folder
    images = sorted(processed_folder.glob("*.jpg"))

    if not images:
        print(f"No images found in {processed_folder}")
        return

    print(f"Found {len(images)} images in {processed_folder}")

    # Create groups (one image per group)
    groups = [[str(img)] for img in images]

    # Track comparison details
    comparison_details = []

    # Run deduplication
    original_count = len(groups)
    print(f"\nRunning deduplication with full_scan=True...")

    filtered = remove_near_duplicates(groups, deduplication_flag=1, full_scan=True)

    print(f"\nResults: {original_count} images -> {len(filtered)} unique")
    print(f"Duplicates found: {original_count - len(filtered)}")

    # Identify which images were kept
    kept_paths = {g[0] for g in filtered}

    # Group duplicates together
    duplicate_groups = {}
    all_images = [str(img) for img in images]

    for img_path in all_images:
        if img_path in kept_paths:
            duplicate_groups[img_path] = []

    # Build duplicate groups with detailed metrics
    print("\nBuilding duplicate groups with metrics...")

    for img_path in all_images:
        if img_path not in kept_paths:
            best_match = None
            best_score = 0
            best_metrics = None

            for kept_img in kept_paths:
                mtb, edge, hd, ssim, clip, sift_matches = _pair_sim(img_path, kept_img)

                sift_score = min(sift_matches / 100.0, 1.0) if sift_matches > 0 else 0.0
                score = (
                    WEIGHT_MTB * (mtb / 100.0) +
                    WEIGHT_SSIM * (ssim / 100.0) +
                    WEIGHT_CLIP * (clip / 100.0) +
                    WEIGHT_PDQ * (0.0 if hd >= PDQ_HD_CEIL else 1.0 - hd / PDQ_HD_CEIL) +
                    WEIGHT_SIFT * sift_score
                )

                if score > best_score:
                    best_score = score
                    best_match = kept_img
                    best_metrics = (mtb, edge, hd, ssim, clip, sift_matches)

            if best_match and best_score >= COMPOSITE_DUP_THRESHOLD:
                duplicate_groups[best_match].append({
                    'path': img_path,
                    'score': best_score,
                    'metrics': best_metrics
                })
                comparison_details.append({
                    'kept': Path(best_match).name,
                    'duplicate': Path(img_path).name,
                    'mtb': best_metrics[0],
                    'edge': best_metrics[1],
                    'pdq_hd': best_metrics[2],
                    'ssim': best_metrics[3],
                    'clip': best_metrics[4],
                    'sift': best_metrics[5],
                    'score': best_score
                })
                print(f"  {Path(img_path).name} is duplicate of {Path(best_match).name} (score: {best_score:.2f})")

    # Create visualization
    print(f"\nCreating visualization...")

    thumb_size = 300
    padding = 20
    text_height = 40

    # Calculate grid dimensions
    max_group_size = max(1 + len(group) for group in duplicate_groups.values())
    num_groups = len(duplicate_groups)

    canvas_width = max_group_size * (thumb_size + padding) + padding
    canvas_height = num_groups * (thumb_size + text_height + padding) + padding

    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    y_offset = padding

    for group_idx, (kept_img, dup_list) in enumerate(duplicate_groups.items()):
        x_offset = padding

        # Draw kept image
        img = Image.open(kept_img)
        img.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)

        thumb = Image.new('RGB', (thumb_size, thumb_size), 'white')
        paste_x = (thumb_size - img.width) // 2
        paste_y = (thumb_size - img.height) // 2
        thumb.paste(img, (paste_x, paste_y))

        draw_thumb = ImageDraw.Draw(thumb)
        for i in range(5):
            draw_thumb.rectangle([(i, i), (thumb_size-1-i, thumb_size-1-i)], outline='green')

        canvas.paste(thumb, (x_offset, y_offset))

        filename = Path(kept_img).stem
        label = f"[KEPT] {filename}"
        text_bbox = draw.textbbox((0, 0), label, font=small_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x_offset + (thumb_size - text_width) // 2
        text_y = y_offset + thumb_size + 5
        draw.text((text_x, text_y), label, fill='green', font=small_font)

        x_offset += thumb_size + padding

        # Draw duplicates
        for dup_info in dup_list:
            img = Image.open(dup_info['path'])
            img.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)

            thumb = Image.new('RGB', (thumb_size, thumb_size), 'white')
            paste_x = (thumb_size - img.width) // 2
            paste_y = (thumb_size - img.height) // 2
            thumb.paste(img, (paste_x, paste_y))

            draw_thumb = ImageDraw.Draw(thumb)
            for i in range(3):
                draw_thumb.rectangle([(i, i), (thumb_size-1-i, thumb_size-1-i)], outline='red')

            canvas.paste(thumb, (x_offset, y_offset))

            filename = Path(dup_info['path']).stem
            label = f"[DUP] {filename}"
            text_bbox = draw.textbbox((0, 0), label, font=small_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = x_offset + (thumb_size - text_width) // 2
            text_y = y_offset + thumb_size + 5
            draw.text((text_x, text_y), label, fill='red', font=small_font)

            x_offset += thumb_size + padding

        y_offset += thumb_size + text_height + padding

    # Save visualization in the target folder
    viz_path = folder / f"{folder_name}_duplicates.jpg"
    canvas.save(viz_path, quality=95)
    print(f"Visualization saved to: {viz_path}")

    # Generate markdown report
    md_path = folder / f"{folder_name}.md"

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Duplicate Analysis: {folder_name}\n\n")
        f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Total Images:** {original_count}\n")
        f.write(f"- **Unique Images:** {len(filtered)}\n")
        f.write(f"- **Duplicates Found:** {original_count - len(filtered)}\n")
        f.write(f"- **Duplicate Rate:** {((original_count - len(filtered)) / original_count * 100):.1f}%\n\n")

        f.write("## Configuration\n\n")
        f.write("| Parameter | Value |\n")
        f.write("|-----------|-------|\n")
        f.write(f"| MTB Weight | {WEIGHT_MTB} |\n")
        f.write(f"| SSIM Weight | {WEIGHT_SSIM} |\n")
        f.write(f"| CLIP Weight | {WEIGHT_CLIP} |\n")
        f.write(f"| PDQ Weight | {WEIGHT_PDQ} |\n")
        f.write(f"| SIFT Weight | {WEIGHT_SIFT} |\n")
        f.write(f"| Composite Threshold | {COMPOSITE_DUP_THRESHOLD} |\n")
        f.write(f"| MTB Hard Floor | {MTB_HARD_FLOOR} |\n")
        f.write(f"| PDQ HD Ceiling | {PDQ_HD_CEIL} |\n")
        f.write(f"| SIFT Min Matches | {SIFT_MIN_MATCHES} |\n\n")

        f.write("## Visualization\n\n")
        f.write(f"![Duplicate Groups]({folder_name}_duplicates.jpg)\n\n")

        f.write("## Duplicate Groups\n\n")

        for kept_img, dup_list in duplicate_groups.items():
            kept_name = Path(kept_img).name
            f.write(f"### {kept_name} (KEPT)\n\n")

            if dup_list:
                f.write(f"**{len(dup_list)} duplicate(s) found:**\n\n")
                f.write("| Duplicate Image | Score | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT Matches |\n")
                f.write("|----------------|-------|-------|--------|--------|--------|--------|-------------|\n")

                for dup_info in dup_list:
                    dup_name = Path(dup_info['path']).name
                    mtb, edge, hd, ssim, clip, sift = dup_info['metrics']
                    f.write(f"| {dup_name} | {dup_info['score']:.3f} | {mtb:.1f} | {edge:.1f} | {ssim:.1f} | {clip:.1f} | {hd} | {sift} |\n")
                f.write("\n")
            else:
                f.write("**No duplicates found** - This image is unique.\n\n")

        f.write("## Detailed Comparison Results\n\n")

        if comparison_details:
            f.write("| Kept Image | Duplicate Image | Composite Score | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT |\n")
            f.write("|-----------|----------------|----------------|-------|--------|--------|--------|--------|------|\n")

            for comp in comparison_details:
                f.write(f"| {comp['kept']} | {comp['duplicate']} | {comp['score']:.3f} | "
                       f"{comp['mtb']:.1f} | {comp['edge']:.1f} | {comp['ssim']:.1f} | "
                       f"{comp['clip']:.1f} | {comp['pdq_hd']} | {comp['sift']} |\n")
        else:
            f.write("*No duplicates detected in this folder.*\n")

        f.write("\n## Metrics Explanation\n\n")
        f.write("- **MTB (Median Threshold Bitmap):** Measures structural similarity (0-100%)\n")
        f.write("- **Edge:** Compares edge patterns (0-100%)\n")
        f.write("- **SSIM (Structural Similarity Index):** Perceptual similarity (0-100%)\n")
        f.write("- **CLIP:** Semantic similarity using AI vision model (0-100%)\n")
        f.write("- **PDQ HD (Hamming Distance):** Perceptual hash distance (lower = more similar)\n")
        f.write("- **SIFT:** Number of matching visual features\n")
        f.write("- **Composite Score:** Weighted combination of all metrics (0-1 scale)\n\n")

        f.write("## Detection Logic\n\n")
        f.write(f"Images are marked as duplicates when:\n")
        f.write(f"- Composite score ≥ {COMPOSITE_DUP_THRESHOLD}\n")
        f.write(f"- MTB ≥ {MTB_HARD_FLOOR}% OR SIFT override (≥{SIFT_MIN_MATCHES} matches + CLIP ≥85%)\n")
        f.write(f"- PDQ HD < {PDQ_HD_CEIL} OR SIFT override\n\n")

    print(f"\nMarkdown report saved to: {md_path}")

    return md_path, viz_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = r"00a959b5-1b0b-4670-9c07-5df8b7636cfe"
    analyze_folder_with_report(folder)
