#!/usr/bin/env python3
"""
Find similar images using CLIP embeddings
Similar to Towhee notebook but using CLIP which is already set up
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import torch
import open_clip
from typing import List, Tuple, Dict

# CLIP model setup (same as deduplication.py)
_clip_model = None
_clip_pre = None
_clip_device = None

def load_clip_model():
    """Load CLIP model"""
    global _clip_model, _clip_pre, _clip_device

    if _clip_model is None:
        print("Loading CLIP model (ViT-B-32)...")
        _clip_device = "cpu"  # Force CPU to avoid GPU compatibility issues
        _clip_model, _clip_pre, _ = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="openai", device=_clip_device
        )
        _clip_model.eval()
        print(f"CLIP model loaded on {_clip_device}")

def get_clip_embedding(img_path: str) -> np.ndarray:
    """Get CLIP embedding for an image"""
    try:
        img = Image.open(img_path).convert("RGB")
        t = _clip_pre(img).unsqueeze(0).to(_clip_device)

        with torch.no_grad():
            emb = _clip_model.encode_image(t).cpu().squeeze()

        # L2 normalize
        emb = emb / (emb.norm() + 1e-8)
        return emb.numpy()

    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return None

def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings"""
    return float(np.dot(emb1, emb2))

def find_similar_images(folder_path: str, threshold: float = 0.9) -> List[Tuple[str, str, float]]:
    """
    Find all pairs of similar images above threshold

    Returns: List of (image1, image2, similarity_score) tuples
    """
    folder = Path(folder_path)

    # Find the processed folder or use root
    processed_folder = folder / "processed" if (folder / "processed").exists() else folder

    # Get all images
    images = sorted(processed_folder.glob("*.jpg"))

    if not images:
        print(f"No images found in {processed_folder}")
        return []

    print(f"Found {len(images)} images")
    print("Computing CLIP embeddings...")

    # Load CLIP model
    load_clip_model()

    # Compute embeddings
    embeddings = {}
    for idx, img_path in enumerate(images, 1):
        print(f"  [{idx}/{len(images)}] Processing {img_path.name}")
        emb = get_clip_embedding(str(img_path))
        if emb is not None:
            embeddings[str(img_path)] = emb

    print(f"\nComputed embeddings for {len(embeddings)} images")
    print(f"Finding pairs with similarity >= {threshold}...")

    # Find similar pairs
    similar_pairs = []
    image_paths = list(embeddings.keys())

    for i in range(len(image_paths)):
        for j in range(i + 1, len(image_paths)):
            img1 = image_paths[i]
            img2 = image_paths[j]

            similarity = cosine_similarity(embeddings[img1], embeddings[img2])

            if similarity >= threshold:
                similar_pairs.append((img1, img2, similarity))

    # Sort by similarity (highest first)
    similar_pairs.sort(key=lambda x: x[2], reverse=True)

    return similar_pairs

def create_similarity_visualization(similar_pairs: List[Tuple[str, str, float]],
                                   output_path: str,
                                   max_pairs: int = 20):
    """Create a visualization showing similar image pairs"""

    if not similar_pairs:
        print("No similar pairs to visualize")
        return

    # Limit to max_pairs
    pairs_to_show = similar_pairs[:max_pairs]

    thumb_size = 300
    padding = 20
    text_height = 60

    canvas_width = 2 * thumb_size + 3 * padding
    canvas_height = len(pairs_to_show) * (thumb_size + text_height + padding) + padding

    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    y_offset = padding

    for idx, (img1_path, img2_path, similarity) in enumerate(pairs_to_show, 1):
        x_offset = padding

        # Draw first image
        img1 = Image.open(img1_path)
        img1.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)

        thumb1 = Image.new('RGB', (thumb_size, thumb_size), 'white')
        paste_x = (thumb_size - img1.width) // 2
        paste_y = (thumb_size - img1.height) // 2
        thumb1.paste(img1, (paste_x, paste_y))

        # Blue border
        draw_thumb = ImageDraw.Draw(thumb1)
        for i in range(3):
            draw_thumb.rectangle([(i, i), (thumb_size-1-i, thumb_size-1-i)], outline='blue')

        canvas.paste(thumb1, (x_offset, y_offset))

        # Label for first image
        filename1 = Path(img1_path).stem
        draw.text((x_offset, y_offset + thumb_size + 5), filename1, fill='blue', font=small_font)

        x_offset += thumb_size + padding

        # Draw similarity score in the middle
        sim_text = f"{similarity:.1%}"
        text_bbox = draw.textbbox((0, 0), sim_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x_offset + (padding - text_width) // 2
        text_y = y_offset + thumb_size // 2
        draw.text((text_x, text_y), sim_text, fill='black', font=font)

        x_offset += padding

        # Draw second image
        img2 = Image.open(img2_path)
        img2.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)

        thumb2 = Image.new('RGB', (thumb_size, thumb_size), 'white')
        paste_x = (thumb_size - img2.width) // 2
        paste_y = (thumb_size - img2.height) // 2
        thumb2.paste(img2, (paste_x, paste_y))

        # Blue border
        draw_thumb = ImageDraw.Draw(thumb2)
        for i in range(3):
            draw_thumb.rectangle([(i, i), (thumb_size-1-i, thumb_size-1-i)], outline='blue')

        canvas.paste(thumb2, (x_offset, y_offset))

        # Label for second image
        filename2 = Path(img2_path).stem
        draw.text((x_offset, y_offset + thumb_size + 5), filename2, fill='blue', font=small_font)

        y_offset += thumb_size + text_height + padding

    # Save
    canvas.save(output_path, quality=95)
    print(f"Visualization saved to: {output_path}")

def generate_similarity_report(folder_path: str, similar_pairs: List[Tuple[str, str, float]],
                               output_path: str):
    """Generate markdown report of similar images"""

    folder_name = Path(folder_path).name

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Similar Images Report: {folder_name}\n\n")
        f.write(f"**Threshold:** 0.9 (90% similarity)\n")
        f.write(f"**Total Similar Pairs Found:** {len(similar_pairs)}\n\n")

        f.write("## Similarity Pairs\n\n")

        if similar_pairs:
            f.write("| Image 1 | Image 2 | Similarity |\n")
            f.write("|---------|---------|------------|\n")

            for img1, img2, sim in similar_pairs:
                name1 = Path(img1).name
                name2 = Path(img2).name
                f.write(f"| {name1} | {name2} | {sim:.2%} |\n")
        else:
            f.write("*No similar pairs found with similarity >= 0.9*\n")

        f.write("\n## Visualization\n\n")
        viz_filename = f"{folder_name}_similar_images.jpg"
        f.write(f"![Similar Image Pairs]({viz_filename})\n\n")

        f.write("## Interpretation\n\n")
        f.write("- **Similarity Score:** Cosine similarity between CLIP embeddings (0-100%)\n")
        f.write("- **CLIP Model:** ViT-B-32 pre-trained on 400M images\n")
        f.write("- **Threshold:** 90% - Only pairs with similarity >= 90% are shown\n")
        f.write("- **Use Case:** Find near-duplicate or very similar images\n")

    print(f"Report saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
    else:
        folder = r"000fc774-cb56-4052-a33a-9974c58a00d6"
        threshold = 0.9

    folder_path = Path(folder)
    folder_name = folder_path.name

    print(f"Finding similar images in: {folder}")
    print(f"Similarity threshold: {threshold:.1%}")
    print("="*60)

    # Find similar images
    similar_pairs = find_similar_images(folder, threshold)

    print(f"\nFound {len(similar_pairs)} similar pairs")

    if similar_pairs:
        print("\nTop 10 most similar pairs:")
        for i, (img1, img2, sim) in enumerate(similar_pairs[:10], 1):
            print(f"  {i}. {Path(img1).name} <-> {Path(img2).name}: {sim:.2%}")

    # Create visualization
    viz_path = folder_path / f"{folder_name}_similar_images.jpg"
    create_similarity_visualization(similar_pairs, str(viz_path), max_pairs=20)

    # Generate report
    report_path = folder_path / f"{folder_name}_similar_images.md"
    generate_similarity_report(folder, similar_pairs, str(report_path))

    print("\n" + "="*60)
    print("Analysis complete!")
