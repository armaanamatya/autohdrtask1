#!/usr/bin/env python3
"""
Visualize duplicate groups from deduplication analysis
"""
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from deduplication import remove_near_duplicates, _metric_store

def create_duplicate_visualization(folder_path, output_path="duplicate_groups.jpg"):
    """
    Create a visual grid showing images grouped with their duplicates
    """
    folder = Path(folder_path)
    images = sorted(folder.glob("*.jpg"))

    if not images:
        print(f"No images found in {folder_path}")
        return

    print(f"Found {len(images)} images")

    # Create groups (one image per group)
    groups = [[str(img)] for img in images]

    # Track which images are duplicates
    original_count = len(groups)
    print(f"\nRunning deduplication with full_scan=True to find all duplicates...")

    # Run with full_scan=True to compare all pairs
    filtered = remove_near_duplicates(groups, deduplication_flag=1, full_scan=True)

    print(f"\nResults: {original_count} images -> {len(filtered)} unique")
    print(f"Duplicates found: {original_count - len(filtered)}")

    # Identify which images were kept
    kept_paths = {g[0] for g in filtered}

    # Group duplicates together
    # Format: {kept_image: [duplicate1, duplicate2, ...]}
    duplicate_groups = {}
    all_images = [str(img) for img in images]

    for img_path in all_images:
        if img_path in kept_paths:
            duplicate_groups[img_path] = [img_path]  # Start with the kept image

    # Now we need to identify which dropped images are duplicates of which kept images
    # We'll re-run comparisons to build the groups
    print("\nBuilding duplicate groups...")

    from deduplication import _pair_sim, _is_aerial
    from deduplication import COMPOSITE_DUP_THRESHOLD, MTB_HARD_FLOOR, PDQ_HD_CEIL
    from deduplication import WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT
    from deduplication import SIFT_MIN_MATCHES

    # For each dropped image, find which kept image it's a duplicate of
    for img_path in all_images:
        if img_path not in kept_paths:
            # This image was dropped, find its match
            best_match = None
            best_score = 0

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

            if best_match and best_score >= COMPOSITE_DUP_THRESHOLD:
                duplicate_groups[best_match].append(img_path)
                print(f"  {Path(img_path).name} is duplicate of {Path(best_match).name} (score: {best_score:.2f})")

    # Create visualization
    print(f"\nCreating visualization with {len(duplicate_groups)} groups...")

    thumb_size = 300
    padding = 20
    text_height = 40

    # Calculate grid dimensions
    max_group_size = max(len(group) for group in duplicate_groups.values())
    num_groups = len(duplicate_groups)

    # Canvas dimensions
    canvas_width = max_group_size * (thumb_size + padding) + padding
    canvas_height = num_groups * (thumb_size + text_height + padding) + padding

    # Create white canvas
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)

    # Try to load a font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    y_offset = padding

    for group_idx, (kept_img, group_images) in enumerate(duplicate_groups.items()):
        x_offset = padding

        for img_idx, img_path in enumerate(group_images):
            # Load and resize image
            img = Image.open(img_path)
            img.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)

            # Create a new image with white background
            thumb = Image.new('RGB', (thumb_size, thumb_size), 'white')
            # Center the image
            paste_x = (thumb_size - img.width) // 2
            paste_y = (thumb_size - img.height) // 2
            thumb.paste(img, (paste_x, paste_y))

            # Draw border
            if img_idx == 0:
                # Green border for kept image
                border_color = 'green'
                border_width = 5
            else:
                # Red border for duplicates
                border_color = 'red'
                border_width = 3

            draw_thumb = ImageDraw.Draw(thumb)
            for i in range(border_width):
                draw_thumb.rectangle(
                    [(i, i), (thumb_size-1-i, thumb_size-1-i)],
                    outline=border_color
                )

            # Paste thumbnail on canvas
            canvas.paste(thumb, (x_offset, y_offset))

            # Add filename below
            filename = Path(img_path).stem
            label = f"{'[KEPT] ' if img_idx == 0 else '[DUP] '}{filename}"

            # Text position
            text_bbox = draw.textbbox((0, 0), label, font=small_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = x_offset + (thumb_size - text_width) // 2
            text_y = y_offset + thumb_size + 5

            text_color = 'green' if img_idx == 0 else 'red'
            draw.text((text_x, text_y), label, fill=text_color, font=small_font)

            x_offset += thumb_size + padding

        y_offset += thumb_size + text_height + padding

    # Save
    canvas.save(output_path, quality=95)
    print(f"\nVisualization saved to: {output_path}")
    print(f"Image size: {canvas_width}x{canvas_height}")

    # Print summary
    print("\n" + "="*60)
    print("DUPLICATE GROUPS SUMMARY")
    print("="*60)
    for kept_img, group_images in duplicate_groups.items():
        print(f"\n{Path(kept_img).name} [KEPT]")
        if len(group_images) > 1:
            for dup_img in group_images[1:]:
                print(f"  └─ {Path(dup_img).name} [DUPLICATE]")
        else:
            print(f"  └─ No duplicates")
    print("="*60)

if __name__ == "__main__":
    folder = r"00a959b5-1b0b-4670-9c07-5df8b7636cfe\processed"
    output = "duplicate_groups_visualization.jpg"

    create_duplicate_visualization(folder, output)
