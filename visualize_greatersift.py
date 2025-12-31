#!/usr/bin/env python3
"""
Create visualizations for SIFT >= 150 analysis results
"""
import sys
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

def parse_duplicate_groups(md_content):
    """Parse duplicate groups from markdown"""
    groups = {}
    current_kept = None

    lines = md_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Look for kept image header: ### IMG_3771.jpg (KEPT)
        if line.startswith('### ') and '(KEPT)' in line:
            # Extract filename
            match = re.search(r'### (.+?) \(KEPT\)', line)
            if match:
                current_kept = match.group(1)
                groups[current_kept] = []

        # Look for duplicate table rows
        elif current_kept and line.startswith('| ') and '.jpg' in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 1 and parts[0] and parts[0].endswith('.jpg'):
                groups[current_kept].append(parts[0])

        i += 1

    return groups

def create_visualization(folder_path, duplicate_groups, output_filename):
    """Create visualization showing duplicate groups"""
    folder = Path(folder_path)

    # Find the processed folder or use root
    processed_folder = folder / "processed" if (folder / "processed").exists() else folder

    print(f"Looking for images in: {processed_folder}")

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

    for group_idx, (kept_img, dup_list) in enumerate(sorted(duplicate_groups.items())):
        x_offset = padding

        # Draw kept image
        img_path = processed_folder / kept_img

        if not img_path.exists():
            print(f"Warning: Image not found: {img_path}")
            y_offset += thumb_size + text_height + padding
            continue

        img = Image.open(img_path)
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
        for dup_img in dup_list:
            dup_path = processed_folder / dup_img

            if not dup_path.exists():
                print(f"Warning: Image not found: {dup_path}")
                continue

            img = Image.open(dup_path)
            img.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)

            thumb = Image.new('RGB', (thumb_size, thumb_size), 'white')
            paste_x = (thumb_size - img.width) // 2
            paste_y = (thumb_size - img.height) // 2
            thumb.paste(img, (paste_x, paste_y))

            draw_thumb = ImageDraw.Draw(thumb)
            for i in range(3):
                draw_thumb.rectangle([(i, i), (thumb_size-1-i, thumb_size-1-i)], outline='red')

            canvas.paste(thumb, (x_offset, y_offset))

            filename = Path(dup_img).stem
            label = f"[DUP] {filename}"
            text_bbox = draw.textbbox((0, 0), label, font=small_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = x_offset + (thumb_size - text_width) // 2
            text_y = y_offset + thumb_size + 5
            draw.text((text_x, text_y), label, fill='red', font=small_font)

            x_offset += thumb_size + padding

        y_offset += thumb_size + text_height + padding

    # Save visualization
    viz_path = folder / output_filename
    canvas.save(viz_path, quality=95)
    print(f"Visualization saved to: {viz_path}")

    return viz_path

def update_markdown_with_visualization(md_path, viz_filename):
    """Update markdown to include visualization"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where to insert visualization (after Configuration section)
    insertion_point = content.find('## Comparison with Original Analysis')

    if insertion_point == -1:
        print("Warning: Could not find insertion point for visualization")
        return

    # Insert visualization section
    viz_section = f"\n## Visualization\n\n![Duplicate Groups]({viz_filename})\n\n"

    updated_content = content[:insertion_point] + viz_section + content[insertion_point:]

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Updated markdown: {md_path}")

def process_folder(folder_path):
    """Process a folder: create visualization and update markdown"""
    folder = Path(folder_path)
    folder_name = folder.name

    md_path = folder / f"{folder_name}_greatersift.md"

    if not md_path.exists():
        print(f"Error: Markdown not found at {md_path}")
        return

    print(f"\nProcessing: {folder_name}")
    print("="*60)

    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Parse duplicate groups
    duplicate_groups = parse_duplicate_groups(md_content)

    print(f"Found {len(duplicate_groups)} duplicate groups")
    for kept, dups in duplicate_groups.items():
        print(f"  {kept}: {len(dups)} duplicates")

    # Create visualization
    viz_filename = f"{folder_name}_duplicates_sift150.jpg"
    viz_path = create_visualization(folder_path, duplicate_groups, viz_filename)

    # Update markdown
    update_markdown_with_visualization(md_path, viz_filename)

    print(f"[OK] Completed: {folder_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
    else:
        folders = [
            r"000fc774-cb56-4052-a33a-9974c58a00d6",
            r"00aab07550cc482ca9c575efb14de476bd3cd2463f"
        ]

    for folder in folders:
        process_folder(folder)
