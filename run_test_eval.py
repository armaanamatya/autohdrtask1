#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test evaluation script for deduplication.py
Runs deduplication on folders 1-10 and generates comprehensive markdown report.
"""

from __future__ import annotations

import logging
import io
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict

import numpy as np

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Import deduplication module
import deduplicationwnew as dedupe
from deduplicationwnew import (
    remove_near_duplicates,
    ExperimentLogger,
    WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT,
    COMPOSITE_DUP_THRESHOLD, MTB_HARD_FLOOR, PDQ_HD_CEIL, SIFT_MIN_MATCHES,
    AERIAL_WEIGHT_MTB, AERIAL_WEIGHT_SSIM, AERIAL_WEIGHT_CLIP, AERIAL_WEIGHT_PDQ, AERIAL_WEIGHT_SIFT,
    AERIAL_COMPOSITE_DUP_THRESHOLD, AERIAL_MTB_HARD_FLOOR, AERIAL_PDQ_HD_CEIL, AERIAL_SIFT_MIN_MATCHES,
    USE_CLIP
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def find_images_in_folder(folder_path: Path) -> List[Path]:
    """
    Find all JPG images in a folder's 'processed' subdirectory only.
    
    Args:
        folder_path: Path to the folder to search
        
    Returns:
        List of image paths found
    """
    images = []
    
    # Only check processed subfolder
    processed_path = folder_path / 'processed'
    if processed_path.exists() and processed_path.is_dir():
        for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
            images.extend(processed_path.glob(ext))
    else:
        logger.warning(f"Processed directory not found: {processed_path}")
    
    return sorted(images)


def process_folder(folder_num: int, folder_path: Path, full_scan: bool = False) -> Dict[str, Any]:
    """
    Process a single folder through deduplication.
    
    Args:
        folder_num: Folder number (1-10)
        folder_path: Path to the folder
        full_scan: Whether to do full scan (all pairs) or just adjacent pairs
        
    Returns:
        Dictionary with results and statistics
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"Processing Folder {folder_num}: {folder_path}")
    logger.info(f"{'='*70}")
    
    # Find images
    images = find_images_in_folder(folder_path)
    
    if not images:
        logger.warning(f"No images found in folder {folder_num}")
        return {
            'folder_num': folder_num,
            'folder_path': str(folder_path),
            'input_count': 0,
            'output_count': 0,
            'duplicates_removed': 0,
            'comparisons': [],
            'dropped_images': [],
            'kept_images': [],
            'error': 'No images found'
        }
    
    # Deduplicate by absolute path (in case same file appears multiple times)
    seen_paths = set()
    unique_images = []
    for img in images:
        abs_path = str(img.resolve())
        if abs_path not in seen_paths:
            seen_paths.add(abs_path)
            unique_images.append(img)
    
    if len(unique_images) < len(images):
        logger.info(f"Removed {len(images) - len(unique_images)} duplicate paths from {len(images)} images")
    
    logger.info(f"Found {len(unique_images)} unique images")
    
    # Create groups (one image per group) - use absolute paths
    groups = [[str(img.resolve())] for img in unique_images]
    
    # Setup experiment logger
    exp_logger = ExperimentLogger()
    exp_logger.start_capture()
    exp_logger.input_count = len(groups)
    
    # Set global experiment logger in deduplication module
    dedupe._experiment_logger = exp_logger
    
    # Run deduplication
    try:
        filtered_groups = remove_near_duplicates(
            groups,
            deduplication_flag=1,
            metadata_dict={},
            full_scan=full_scan
        )
        
        exp_logger.output_count = len(filtered_groups)
        terminal_output = exp_logger.stop_capture()
        
        # Extract results
        input_images = [img[0] for img in groups]
        output_images = [img[0] for img in filtered_groups]
        dropped_images = [img for img in input_images if img not in output_images]
        
        return {
            'folder_num': folder_num,
            'folder_path': str(folder_path),
            'input_count': len(groups),
            'output_count': len(filtered_groups),
            'duplicates_removed': len(dropped_images),
            'comparisons': exp_logger.comparison_results,
            'dropped_images': dropped_images,
            'kept_images': output_images,
            'terminal_output': terminal_output,
            'error': None
        }
    except Exception as e:
        logger.error(f"Error processing folder {folder_num}: {e}", exc_info=True)
        return {
            'folder_num': folder_num,
            'folder_path': str(folder_path),
            'input_count': len(groups),
            'output_count': 0,
            'duplicates_removed': 0,
            'comparisons': [],
            'dropped_images': [],
            'kept_images': [],
            'error': str(e)
        }
    finally:
        dedupe._experiment_logger = None


def create_image_thumbnail(img_path: str, output_dir: Path, size: int = 200) -> Optional[str]:
    """
    Create a thumbnail of an image and return the path to the thumbnail.
    
    Args:
        img_path: Path to the image file
        output_dir: Directory to save thumbnails in
        size: Thumbnail size in pixels
        
    Returns:
        Path to thumbnail file, or None if creation failed
    """
    if not PIL_AVAILABLE:
        return None
    
    try:
        img = Image.open(img_path)
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Create thumbnails directory in output_dir
        thumbs_dir = output_dir / "thumbnails"
        thumbs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique thumbnail filename using folder and image name
        img_path_obj = Path(img_path)
        # Get folder name (e.g., "1" from "1/processed/IMG_3722.jpg")
        folder_name = img_path_obj.parent.parent.name if img_path_obj.parent.name == "processed" else img_path_obj.parent.name
        # Create unique filename: folder_image_thumb.jpg
        thumb_filename = f"{folder_name}_{img_path_obj.stem}_thumb{img_path_obj.suffix}"
        thumb_path = thumbs_dir / thumb_filename
        
        img.save(thumb_path, quality=85)
        return str(thumb_path)
    except Exception as e:
        logger.debug(f"Failed to create thumbnail for {img_path}: {e}")
        return None


def generate_folder_markdown(result: Dict[str, Any], output_dir: Path) -> str:
    """
    Generate a markdown report for a single folder with visualizations.
    
    Args:
        result: Result dictionary from process_folder
        output_dir: Directory to save the markdown file
        
    Returns:
        Path to the generated markdown file
    """
    folder_num = result['folder_num']
    folder_name = Path(result['folder_path']).name
    
    # Create output filename
    output_file = output_dir / f"folder_{folder_num}_report_optimized.md"
    
    # Calculate statistics for this folder
    comparisons = result['comparisons']
    dropped_images = result['dropped_images']
    kept_images = result['kept_images']
    
    if comparisons:
        mtb_values = [c['mtb'] for c in comparisons]
        edge_values = [c['edge'] for c in comparisons]
        ssim_values = [c['ssim'] for c in comparisons]
        clip_values = [c['clip'] for c in comparisons]
        pdq_values = [c['pdq_hd'] for c in comparisons if c['pdq_hd'] < 999]
        sift_values = [c['sift_matches'] for c in comparisons]
        score_values = [c['score'] for c in comparisons]
        
        dropped_comps = [c for c in comparisons if c['dropped']]
        kept_comps = [c for c in comparisons if not c['dropped']]
    else:
        mtb_values = edge_values = ssim_values = clip_values = pdq_values = sift_values = score_values = []
        dropped_comps = kept_comps = []
    
    # Build markdown content
    md_content = f"""# Folder {folder_num} Deduplication Report: {folder_name}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

| Metric | Value |
|--------|-------|
| **Input Images** | {result['input_count']} |
| **Output Images** | {result['output_count']} |
| **Duplicates Removed** | {result['duplicates_removed']} |
| **Removal Rate** | {(result['duplicates_removed']/result['input_count']*100) if result['input_count'] > 0 else 0:.1f}% |
| **Comparisons Made** | {len(comparisons)} |
| **Status** | {'✅ Success' if result['error'] is None else f'❌ Error: {result["error"]}'} |

## Configuration

| Parameter | Value |
|-----------|-------|
| USE_CLIP | {USE_CLIP} |
| WEIGHT_MTB | {WEIGHT_MTB} |
| WEIGHT_SSIM | {WEIGHT_SSIM} |
| WEIGHT_CLIP | {WEIGHT_CLIP} |
| WEIGHT_PDQ | {WEIGHT_PDQ} |
| WEIGHT_SIFT | {WEIGHT_SIFT} |
| COMPOSITE_DUP_THRESHOLD | {COMPOSITE_DUP_THRESHOLD} |
| MTB_HARD_FLOOR | {MTB_HARD_FLOOR} |
| PDQ_HD_CEIL | {PDQ_HD_CEIL} |
| SIFT_MIN_MATCHES | {SIFT_MIN_MATCHES} |

"""
    
    if result['error']:
        md_content += f"**Error:** {result['error']}\n\n"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return str(output_file)
    
    # Statistics section
    if comparisons:
        md_content += f"""## Statistics

### All Comparisons

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| MTB % | {np.mean(mtb_values):.2f} | {np.median(mtb_values):.2f} | {np.min(mtb_values):.2f} | {np.max(mtb_values):.2f} | {np.std(mtb_values):.2f} |
| Edge % | {np.mean(edge_values):.2f} | {np.median(edge_values):.2f} | {np.min(edge_values):.2f} | {np.max(edge_values):.2f} | {np.std(edge_values):.2f} |
| SSIM % | {np.mean(ssim_values):.2f} | {np.median(ssim_values):.2f} | {np.min(ssim_values):.2f} | {np.max(ssim_values):.2f} | {np.std(ssim_values):.2f} |
| CLIP % | {np.mean(clip_values):.2f} | {np.median(clip_values):.2f} | {np.min(clip_values):.2f} | {np.max(clip_values):.2f} | {np.std(clip_values):.2f} |
| PDQ HD | {np.mean(pdq_values):.2f} | {np.median(pdq_values):.2f} | {np.min(pdq_values):.0f} | {np.max(pdq_values):.0f} | {np.std(pdq_values):.2f} |
| SIFT Matches | {np.mean(sift_values):.2f} | {np.median(sift_values):.2f} | {np.min(sift_values):.0f} | {np.max(sift_values):.0f} | {np.std(sift_values):.2f} |
| Composite Score | {np.mean(score_values):.3f} | {np.median(score_values):.3f} | {np.min(score_values):.3f} | {np.max(score_values):.3f} | {np.std(score_values):.3f} |

### Dropped vs Kept

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | {len(dropped_comps)} | {(len(dropped_comps)/len(comparisons)*100) if comparisons else 0:.1f}% |
| **Kept (Unique)** | {len(kept_comps)} | {(len(kept_comps)/len(comparisons)*100) if comparisons else 0:.1f}% |

"""
    
    # Dropped images section with thumbnails
    if dropped_images:
        md_content += f"""## Dropped Images ({len(dropped_images)})

These images were identified as duplicates and removed:

"""
        for img_path in dropped_images:
            img_name = Path(img_path).name
            # Try to create thumbnail
            thumb_path = create_image_thumbnail(img_path, output_dir, size=200)
            if thumb_path and Path(thumb_path).exists():
                # Compute relative path from output_dir (where markdown is) to thumbnail
                try:
                    thumb_path_obj = Path(thumb_path).resolve()
                    output_dir_resolved = Path(output_dir).resolve()
                    # Use os.path.relpath for cross-platform compatibility
                    import os
                    thumb_rel = os.path.relpath(str(thumb_path_obj), str(output_dir_resolved))
                    # Convert backslashes to forward slashes for markdown
                    thumb_rel = thumb_rel.replace('\\', '/')
                except (ValueError, OSError):
                    # Fallback to just filename if relative path calculation fails
                    thumb_rel = Path(thumb_path).name
                md_content += f"### {img_name}\n\n"
                md_content += f"![{img_name}]({thumb_rel})\n\n"
                md_content += f"**Path:** `{img_path}`\n\n"
            else:
                md_content += f"- `{img_name}`\n"
                md_content += f"  - Path: `{img_path}`\n"
        md_content += "\n"
    
    # Kept images section with thumbnails
    if kept_images:
        md_content += f"""## Kept Images ({len(kept_images)})

These images were kept as unique:

"""
        # Show all kept images with thumbnails (limit to first 50 for readability)
        shown_images = kept_images[:50]
        for img_path in shown_images:
            img_name = Path(img_path).name
            thumb_path = create_image_thumbnail(img_path, output_dir, size=200)
            if thumb_path and Path(thumb_path).exists():
                # Compute relative path from output_dir (where markdown is) to thumbnail
                try:
                    import os
                    thumb_path_obj = Path(thumb_path).resolve()
                    output_dir_resolved = Path(output_dir).resolve()
                    # Use os.path.relpath for cross-platform compatibility
                    thumb_rel = os.path.relpath(str(thumb_path_obj), str(output_dir_resolved))
                    # Convert backslashes to forward slashes for markdown
                    thumb_rel = thumb_rel.replace('\\', '/')
                except (ValueError, OSError):
                    # Fallback to just filename if relative path calculation fails
                    thumb_rel = Path(thumb_path).name
                md_content += f"### {img_name}\n\n"
                md_content += f"![{img_name}]({thumb_rel})\n\n"
                md_content += f"**Path:** `{img_path}`\n\n"
            else:
                md_content += f"- `{img_name}`\n"
        if len(kept_images) > 50:
            md_content += f"\n*... and {len(kept_images) - 50} more kept images*\n"
        md_content += "\n"
    
    # Comparison details
    if comparisons:
        md_content += f"""## Comparison Details ({len(comparisons)} comparisons)

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|
"""
        for comp in comparisons:
            dropped_str = "✅ Yes" if comp['dropped'] else "❌ No"
            reason = comp.get('drop_reason', '')
            if not reason and comp['dropped']:
                reason = "duplicate"
            elif not reason:
                reason = "-"
            
            md_content += f"| {comp['img_a']} | {comp['img_b']} | {comp['mtb']:.1f} | {comp['edge']:.1f} | {comp['ssim']:.1f} | {comp['clip']:.1f} | {comp['pdq_hd']} | {comp['sift_matches']} | {comp['score']:.2f} | {dropped_str} | {reason} |\n"
        
        md_content += "\n"
    
    # Write to file immediately
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
        f.flush()  # Ensure data is written to disk immediately
        os.fsync(f.fileno())  # Force write to disk (Unix/Windows compatible)
    
    logger.info(f"✅ Folder {folder_num} report saved immediately: {output_file}")
    return str(output_file)


def generate_markdown_report(results: List[Dict[str, Any]], output_file: str = "testeval.md", per_folder: bool = False) -> None:
    """
    Generate comprehensive markdown report with visualizations.
    
    Args:
        results: List of results from processing each folder
        output_file: Output markdown file path
    """
    logger.info(f"\nGenerating markdown report: {output_file}")
    
    # Calculate aggregate statistics
    total_input = sum(r['input_count'] for r in results)
    total_output = sum(r['output_count'] for r in results)
    total_dropped = sum(r['duplicates_removed'] for r in results)
    total_comparisons = sum(len(r['comparisons']) for r in results)
    
    all_comparisons = []
    for r in results:
        all_comparisons.extend(r['comparisons'])
    
    # Calculate metric statistics
    if all_comparisons:
        mtb_values = [c['mtb'] for c in all_comparisons]
        edge_values = [c['edge'] for c in all_comparisons]
        ssim_values = [c['ssim'] for c in all_comparisons]
        clip_values = [c['clip'] for c in all_comparisons]
        pdq_values = [c['pdq_hd'] for c in all_comparisons if c['pdq_hd'] < 999]
        sift_values = [c['sift_matches'] for c in all_comparisons]
        score_values = [c['score'] for c in all_comparisons]
        
        dropped_comparisons = [c for c in all_comparisons if c['dropped']]
        kept_comparisons = [c for c in all_comparisons if not c['dropped']]
    else:
        mtb_values = edge_values = ssim_values = clip_values = pdq_values = sift_values = score_values = []
        dropped_comparisons = kept_comparisons = []
    
    # Build markdown content
    md_content = f"""# Deduplication Test Evaluation Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Folders Processed** | {len(results)} |
| **Total Input Images** | {total_input} |
| **Total Output Images** | {total_output} |
| **Total Duplicates Removed** | {total_dropped} |
| **Removal Rate** | {(total_dropped/total_input*100) if total_input > 0 else 0:.1f}% |
| **Total Comparisons** | {total_comparisons} |

## Configuration

### Regular Photos
| Parameter | Value |
|-----------|-------|
| USE_CLIP | {USE_CLIP} |
| WEIGHT_MTB | {WEIGHT_MTB} |
| WEIGHT_SSIM | {WEIGHT_SSIM} |
| WEIGHT_CLIP | {WEIGHT_CLIP} |
| WEIGHT_PDQ | {WEIGHT_PDQ} |
| WEIGHT_SIFT | {WEIGHT_SIFT} |
| COMPOSITE_DUP_THRESHOLD | {COMPOSITE_DUP_THRESHOLD} |
| MTB_HARD_FLOOR | {MTB_HARD_FLOOR} |
| PDQ_HD_CEIL | {PDQ_HD_CEIL} |
| SIFT_MIN_MATCHES | {SIFT_MIN_MATCHES} |

### Aerial Photos
| Parameter | Value |
|-----------|-------|
| AERIAL_WEIGHT_MTB | {AERIAL_WEIGHT_MTB} |
| AERIAL_WEIGHT_SSIM | {AERIAL_WEIGHT_SSIM} |
| AERIAL_WEIGHT_CLIP | {AERIAL_WEIGHT_CLIP} |
| AERIAL_WEIGHT_PDQ | {AERIAL_WEIGHT_PDQ} |
| AERIAL_WEIGHT_SIFT | {AERIAL_WEIGHT_SIFT} |
| AERIAL_COMPOSITE_DUP_THRESHOLD | {AERIAL_COMPOSITE_DUP_THRESHOLD} |
| AERIAL_MTB_HARD_FLOOR | {AERIAL_MTB_HARD_FLOOR} |
| AERIAL_PDQ_HD_CEIL | {AERIAL_PDQ_HD_CEIL} |
| AERIAL_SIFT_MIN_MATCHES | {AERIAL_SIFT_MIN_MATCHES} |

## Aggregate Statistics

### All Comparisons
"""
    
    if all_comparisons:
        md_content += f"""
| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| MTB % | {np.mean(mtb_values):.2f} | {np.median(mtb_values):.2f} | {np.min(mtb_values):.2f} | {np.max(mtb_values):.2f} | {np.std(mtb_values):.2f} |
| Edge % | {np.mean(edge_values):.2f} | {np.median(edge_values):.2f} | {np.min(edge_values):.2f} | {np.max(edge_values):.2f} | {np.std(edge_values):.2f} |
| SSIM % | {np.mean(ssim_values):.2f} | {np.median(ssim_values):.2f} | {np.min(ssim_values):.2f} | {np.max(ssim_values):.2f} | {np.std(ssim_values):.2f} |
| CLIP % | {np.mean(clip_values):.2f} | {np.median(clip_values):.2f} | {np.min(clip_values):.2f} | {np.max(clip_values):.2f} | {np.std(clip_values):.2f} |
| PDQ HD | {np.mean(pdq_values):.2f} | {np.median(pdq_values):.2f} | {np.min(pdq_values):.0f} | {np.max(pdq_values):.0f} | {np.std(pdq_values):.2f} |
| SIFT Matches | {np.mean(sift_values):.2f} | {np.median(sift_values):.2f} | {np.min(sift_values):.0f} | {np.max(sift_values):.0f} | {np.std(sift_values):.2f} |
| Composite Score | {np.mean(score_values):.3f} | {np.median(score_values):.3f} | {np.min(score_values):.3f} | {np.max(score_values):.3f} | {np.std(score_values):.3f} |
"""
    else:
        md_content += "\n*No comparisons performed*\n"
    
    md_content += f"""
### Dropped vs Kept Comparisons

| Category | Count | Percentage |
|----------|-------|------------|
| **Dropped (Duplicates)** | {len(dropped_comparisons)} | {(len(dropped_comparisons)/len(all_comparisons)*100) if all_comparisons else 0:.1f}% |
| **Kept (Unique)** | {len(kept_comparisons)} | {(len(kept_comparisons)/len(all_comparisons)*100) if all_comparisons else 0:.1f}% |
"""
    
    if dropped_comparisons:
        dropped_mtb = [c['mtb'] for c in dropped_comparisons]
        dropped_clip = [c['clip'] for c in dropped_comparisons]
        dropped_score = [c['score'] for c in dropped_comparisons]
        md_content += f"""
#### Dropped Comparisons Statistics
| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| MTB % | {np.mean(dropped_mtb):.2f} | {np.median(dropped_mtb):.2f} | {np.min(dropped_mtb):.2f} | {np.max(dropped_mtb):.2f} |
| CLIP % | {np.mean(dropped_clip):.2f} | {np.median(dropped_clip):.2f} | {np.min(dropped_clip):.2f} | {np.max(dropped_clip):.2f} |
| Composite Score | {np.mean(dropped_score):.3f} | {np.median(dropped_score):.3f} | {np.min(dropped_score):.3f} | {np.max(dropped_score):.3f} |
"""
    
    if kept_comparisons:
        kept_mtb = [c['mtb'] for c in kept_comparisons]
        kept_clip = [c['clip'] for c in kept_comparisons]
        kept_score = [c['score'] for c in kept_comparisons]
        md_content += f"""
#### Kept Comparisons Statistics
| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| MTB % | {np.mean(kept_mtb):.2f} | {np.median(kept_mtb):.2f} | {np.min(kept_mtb):.2f} | {np.max(kept_mtb):.2f} |
| CLIP % | {np.mean(kept_clip):.2f} | {np.median(kept_clip):.2f} | {np.min(kept_clip):.2f} | {np.max(kept_clip):.2f} |
| Composite Score | {np.mean(kept_score):.3f} | {np.median(kept_score):.3f} | {np.min(kept_score):.3f} | {np.max(kept_score):.3f} |
"""
    
    # Per-folder results
    md_content += "\n## Per-Folder Results\n\n"
    
    for result in results:
        folder_num = result['folder_num']
        md_content += f"""### Folder {folder_num}: {Path(result['folder_path']).name}

| Metric | Value |
|--------|-------|
| **Input Images** | {result['input_count']} |
| **Output Images** | {result['output_count']} |
| **Duplicates Removed** | {result['duplicates_removed']} |
| **Removal Rate** | {(result['duplicates_removed']/result['input_count']*100) if result['input_count'] > 0 else 0:.1f}% |
| **Comparisons Made** | {len(result['comparisons'])} |
| **Status** | {'✅ Success' if result['error'] is None else f'❌ Error: {result["error"]}'} |

"""
        
        if result['error']:
            md_content += f"**Error:** {result['error']}\n\n"
            continue
        
        if result['dropped_images']:
            md_content += f"#### Dropped Images ({len(result['dropped_images'])})\n\n"
            for img in result['dropped_images']:
                img_name = Path(img).name
                md_content += f"- `{img_name}`\n"
            md_content += "\n"
        
        if result['comparisons']:
            md_content += f"#### Comparison Details ({len(result['comparisons'])} comparisons)\n\n"
            md_content += "| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? | Reason |\n"
            md_content += "|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|--------|\n"
            
            for comp in result['comparisons']:
                dropped_str = "✅ Yes" if comp['dropped'] else "❌ No"
                reason = comp.get('drop_reason', '')
                if not reason and comp['dropped']:
                    reason = "duplicate"
                elif not reason:
                    reason = "-"
                
                md_content += f"| {comp['img_a']} | {comp['img_b']} | {comp['mtb']:.1f} | {comp['edge']:.1f} | {comp['ssim']:.1f} | {comp['clip']:.1f} | {comp['pdq_hd']} | {comp['sift_matches']} | {comp['score']:.2f} | {dropped_str} | {reason} |\n"
            
            md_content += "\n"
        
        if result['kept_images']:
            md_content += f"#### Kept Images ({len(result['kept_images'])})\n\n"
            # Show first 20 kept images to avoid huge lists
            shown_images = result['kept_images'][:20]
            for img in shown_images:
                img_name = Path(img).name
                md_content += f"- `{img_name}`\n"
            if len(result['kept_images']) > 20:
                md_content += f"\n*... and {len(result['kept_images']) - 20} more*\n"
            md_content += "\n"
    
    # Drop reasons analysis
    if all_comparisons:
        drop_reasons = defaultdict(int)
        for comp in all_comparisons:
            if comp['dropped']:
                reason = comp.get('drop_reason', 'duplicate')
                drop_reasons[reason] += 1
            else:
                reason = comp.get('drop_reason', '')
                if reason:
                    drop_reasons[f"Not dropped: {reason}"] += 1
        
        if drop_reasons:
            md_content += "## Drop Reason Analysis\n\n"
            md_content += "| Reason | Count |\n"
            md_content += "|--------|-------|\n"
            for reason, count in sorted(drop_reasons.items(), key=lambda x: x[1], reverse=True):
                md_content += f"| {reason} | {count} |\n"
            md_content += "\n"
    
    # Write to file
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    logger.info(f"Report written to {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run deduplication test evaluation on folders 1-10")
    parser.add_argument("--folders", nargs="+", type=int, default=list(range(1, 11)),
                        help="Folder numbers to process (default: 1-10)")
    parser.add_argument("--output", type=str, default="testeval.md",
                        help="Output markdown file (default: testeval.md)")
    parser.add_argument("--output-dir", type=str, default=".",
                        help="Directory to save per-folder reports (default: current directory)")
    parser.add_argument("--per-folder", action="store_true",
                        help="Generate separate markdown file for each folder")
    parser.add_argument("--full-scan", action="store_true",
                        help="Use full scan mode (compare all pairs, not just adjacent)")
    args = parser.parse_args()
    
    # Get current directory
    base_dir = Path.cwd()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each folder
    results = []
    for folder_num in args.folders:
        folder_path = base_dir / str(folder_num)
        
        if not folder_path.exists():
            logger.warning(f"Folder {folder_num} does not exist, skipping")
            results.append({
                'folder_num': folder_num,
                'folder_path': str(folder_path),
                'input_count': 0,
                'output_count': 0,
                'duplicates_removed': 0,
                'comparisons': [],
                'dropped_images': [],
                'kept_images': [],
                'error': 'Folder does not exist'
            })
            continue
        
        result = process_folder(folder_num, folder_path, full_scan=args.full_scan)
        results.append(result)
        
        # Generate and save per-folder report immediately if requested
        if args.per_folder:
            report_path = generate_folder_markdown(result, output_dir)
            logger.info(f"✅ Folder {folder_num} report saved immediately: {report_path}")
    
    # Generate aggregate report
    if not args.per_folder or len(results) > 1:
        generate_markdown_report(results, output_file=args.output)
    
    logger.info(f"\n{'='*70}")
    logger.info("Test evaluation complete!")
    if args.per_folder:
        logger.info(f"Per-folder reports saved to: {output_dir}")
    logger.info(f"Aggregate report saved to: {args.output}")
    logger.info(f"{'='*70}\n")


if __name__ == "__main__":
    main()

