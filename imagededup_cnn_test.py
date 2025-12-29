#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Deduplication using imagededup library with CNN method
"""

from imagededup.methods import CNN
from imagededup.utils import plot_duplicates
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import json
from pathlib import Path
from typing import List, Set
import cv2

plt.rcParams['figure.figsize'] = (15, 10)

def find_duplicates_cnn(image_dir, threshold=0.9, recursive=False):
    """
    Find duplicate images using CNN-based encoding method

    Args:
        image_dir: Directory containing images to check
        threshold: Similarity threshold (0-1). Higher = more similar required
        recursive: Whether to search subdirectories

    Returns:
        Dictionary mapping image names to lists of duplicates
    """
    print(f"\n{'='*60}")
    print(f"Finding duplicates in: {image_dir}")
    print(f"Threshold: {threshold}")
    print(f"Recursive: {recursive}")
    print(f"{'='*60}\n")

    # Initialize CNN method
    cnn = CNN()

    # Generate encodings for all images
    print("Generating CNN encodings for images...")
    encodings = cnn.encode_images(image_dir=image_dir, recursive=recursive)
    print(f"[OK] Generated encodings for {len(encodings)} images\n")

    # Find duplicates
    print(f"Finding duplicates with threshold >= {threshold}...")
    duplicates = cnn.find_duplicates(
        encoding_map=encodings,
        min_similarity_threshold=threshold,
        scores=True  # Return similarity scores
    )

    return duplicates, encodings


def analyze_results(duplicates):
    """
    Analyze and print statistics about found duplicates
    """
    print(f"\n{'='*60}")
    print("DUPLICATE DETECTION RESULTS")
    print(f"{'='*60}\n")

    total_images = len(duplicates)
    images_with_dupes = sum(1 for v in duplicates.values() if v)
    total_duplicate_pairs = sum(len(v) for v in duplicates.values())

    print(f"Total images analyzed: {total_images}")
    print(f"Images with duplicates: {images_with_dupes}")
    print(f"Total duplicate connections: {total_duplicate_pairs}")
    print(f"Percentage with duplicates: {images_with_dupes/total_images*100:.1f}%\n")

    if images_with_dupes > 0:
        print("Images with duplicates:")
        print("-" * 60)
        for img, dupes in duplicates.items():
            if dupes:
                print(f"\n{img}:")
                for dup_img, score in dupes:
                    print(f"  -> {dup_img} (similarity: {score:.4f})")
    else:
        print("No duplicates found!")

    return {
        'total_images': total_images,
        'images_with_duplicates': images_with_dupes,
        'total_duplicate_pairs': total_duplicate_pairs
    }


def save_results(duplicates, stats, output_file='duplicate_results.json'):
    """
    Save results to JSON file
    """
    results = {
        'statistics': stats,
        'duplicates': {
            img: [(dup, float(score)) for dup, score in dupes]
            for img, dupes in duplicates.items()
            if dupes
        }
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[OK] Results saved to: {output_file}")


def visualize_duplicates(duplicates, image_dir, num_examples=3):
    """
    Visualize some duplicate examples
    """
    # Get images with duplicates
    examples = [(img, dupes) for img, dupes in duplicates.items() if dupes]

    if not examples:
        print("\nNo duplicates to visualize!")
        return

    print(f"\nVisualizing first {min(num_examples, len(examples))} duplicate groups...")

    for i, (img, dupes) in enumerate(examples[:num_examples]):
        try:
            plot_duplicates(
                image_dir=image_dir,
                duplicate_map=duplicates,
                filename=img
            )
            plt.savefig(f'duplicate_visualization_{i}.png', bbox_inches='tight', dpi=150)
            plt.close()
            print(f"  [OK] Saved duplicate_visualization_{i}.png")
        except Exception as e:
            print(f"  [ERROR] Error visualizing {img}: {e}")


def _get_image_quality_score(img_path: str) -> tuple:
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


def _find_duplicate_clusters(
    images: List[str],
    encodings: dict,
    threshold: float
) -> List[Set[str]]:
    """
    Find clusters of duplicate images based on CNN similarity.

    Returns: List of sets, each set contains duplicate image paths
    """
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Filter images with valid encodings
    valid_images = [img for img in images if encodings[img] is not None]

    if len(valid_images) <= 1:
        return [{img} for img in valid_images]

    # Build similarity matrix
    n = len(valid_images)
    clusters = []
    assigned = set()

    for i in range(n):
        if valid_images[i] in assigned:
            continue

        cluster = {valid_images[i]}
        assigned.add(valid_images[i])

        # Find all images similar to this one
        enc_i = encodings[valid_images[i]].reshape(1, -1)

        for j in range(i + 1, n):
            if valid_images[j] in assigned:
                continue

            enc_j = encodings[valid_images[j]].reshape(1, -1)
            similarity = cosine_similarity(enc_i, enc_j)[0, 0]

            if similarity >= threshold:
                cluster.add(valid_images[j])
                assigned.add(valid_images[j])

        clusters.append(cluster)

    return clusters


def remove_near_duplicates_cnn(
    groups: List[List[str]],
    threshold: float = 0.9,
    deduplication_flag: int = 0
) -> List[List[str]]:
    """
    Remove duplicate images WITHIN each group, keeping highest quality image.

    Args:
        groups: List of image groups (each group = one folder's images)
        threshold: CNN cosine similarity threshold (0-1)
        deduplication_flag: If not 1, returns groups unchanged

    Returns:
        List of deduplicated groups
    """
    # Early exit
    if deduplication_flag != 1:
        return groups

    print(f"\n{'='*60}")
    print(f"CNN Within-Group Deduplication")
    print(f"Processing {len(groups)} groups")
    print(f"Threshold: {threshold}")
    print(f"{'='*60}\n")

    # Initialize CNN encoder
    cnn = CNN()

    deduplicated_groups = []

    # Process each group independently
    for group_idx, group in enumerate(groups):
        if not group:
            deduplicated_groups.append([])
            continue

        print(f"\n[Group {group_idx + 1}/{len(groups)}] Processing {len(group)} images...")

        # Generate CNN encodings for all images in this group
        encodings = {}
        for img_path in group:
            try:
                enc = cnn.encode_image(image_file=img_path)
                encodings[img_path] = enc.squeeze()
            except Exception as e:
                print(f"  [WARN] Failed to encode {Path(img_path).name}: {e}")
                encodings[img_path] = None

        # Find duplicate clusters within this group
        duplicate_clusters = _find_duplicate_clusters(group, encodings, threshold)

        # For each cluster, keep only the highest quality image
        images_to_keep = set()
        images_to_drop = set()

        for cluster in duplicate_clusters:
            if len(cluster) <= 1:
                images_to_keep.update(cluster)
                continue

            # Find highest quality image in cluster
            best_img = max(cluster, key=lambda img: _get_image_quality_score(img))
            images_to_keep.add(best_img)

            dropped = cluster - {best_img}
            images_to_drop.update(dropped)

            print(f"  [CLUSTER] {len(cluster)} duplicates found:")
            print(f"    KEEP: {Path(best_img).name}")
            for img in dropped:
                print(f"    DROP: {Path(img).name}")

        # Add non-duplicate images
        for img in group:
            if img not in images_to_drop and encodings[img] is not None:
                images_to_keep.add(img)

        deduplicated_group = sorted(list(images_to_keep))
        deduplicated_groups.append(deduplicated_group)

        print(f"  [RESULT] {len(group)} -> {len(deduplicated_group)} images")

    total_before = sum(len(g) for g in groups)
    total_after = sum(len(g) for g in deduplicated_groups)
    print(f"\n{'='*60}")
    print(f"Total images: {total_before} -> {total_after}")
    print(f"Removed {total_before - total_after} duplicates")
    print(f"{'='*60}\n")

    return deduplicated_groups


def main():
    # Configuration for within-group deduplication
    FOLDERS = [
        'photos-706-winchester-blvd--los-gatos--ca-9',
        'photos-75-knollview-way--san-francisco--ca'
    ]
    THRESHOLD = 0.9

    print("="*60)
    print("CNN WITHIN-GROUP DEDUPLICATION TEST")
    print("="*60)

    # Create groups from folders
    groups = []
    for folder in FOLDERS:
        if Path(folder).exists():
            folder_images = sorted([str(img) for img in Path(folder).glob("*.jpg")])
            if folder_images:
                groups.append(folder_images)
                print(f"\nLoaded {folder}:")
                print(f"  {len(folder_images)} images")
                for img in folder_images:
                    print(f"    - {Path(img).name}")
            else:
                print(f"\n{folder}: No images found")
        else:
            print(f"\nFolder not found: {folder}")

    if not groups:
        print("\nNo folders with images found!")
        print("\nAlternative: Testing with 'combined' directory...")

        # Fallback to original single-directory mode
        IMAGE_DIR = 'combined'
        if os.path.exists(IMAGE_DIR):
            duplicates, encodings = find_duplicates_cnn(
                image_dir=IMAGE_DIR,
                threshold=THRESHOLD,
                recursive=False
            )
            stats = analyze_results(duplicates)
            save_results(duplicates, stats, output_file='cnn_duplicates.json')
        return

    # Apply within-group deduplication
    print(f"\n{'='*60}")
    print("Starting deduplication process...")
    print(f"{'='*60}")

    filtered = remove_near_duplicates_cnn(
        groups=groups,
        threshold=THRESHOLD,
        deduplication_flag=1
    )

    # Show results
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    for i, (original, filtered_group) in enumerate(zip(groups, filtered)):
        folder_name = FOLDERS[i] if i < len(FOLDERS) else f"Group {i}"
        print(f"\n{folder_name}:")
        print(f"  Before: {len(original)} images")
        print(f"  After:  {len(filtered_group)} images")
        print(f"  Removed: {len(original) - len(filtered_group)} duplicates")
        if filtered_group:
            print(f"  Kept images:")
            for img in filtered_group:
                print(f"    - {Path(img).name}")

    print(f"\n{'='*60}")
    print("DONE!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
