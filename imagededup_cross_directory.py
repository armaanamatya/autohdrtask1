#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Directory Image Deduplication using imagededup CNN method
Finds duplicates across multiple directories
"""

from imagededup.methods import CNN
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
from pathlib import Path
import shutil

plt.rcParams['figure.figsize'] = (15, 10)


def find_duplicates_across_directories(directories, threshold=0.9):
    """
    Find duplicate images across multiple directories using CNN encoding

    Args:
        directories: List of directories to search
        threshold: Similarity threshold (0-1). Higher = more similar required

    Returns:
        Dictionary mapping image names to lists of duplicates with scores
    """
    print(f"\n{'='*60}")
    print("CROSS-DIRECTORY DUPLICATE DETECTION")
    print(f"{'='*60}")
    print(f"Directories to analyze: {directories}")
    print(f"Threshold: {threshold}")
    print(f"{'='*60}\n")

    # Create a temporary directory with all images
    temp_dir = Path("temp_all_images")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Copy all images to temp directory with source path in name
    image_mapping = {}  # Maps temp filename to original path

    print("Collecting images from all directories...")
    for dir_path in directories:
        if not os.path.exists(dir_path):
            print(f"  [WARNING] Directory not found: {dir_path}")
            continue

        dir_name = Path(dir_path).name
        image_files = list(Path(dir_path).glob("*.jpg")) + \
                     list(Path(dir_path).glob("*.jpeg")) + \
                     list(Path(dir_path).glob("*.png")) + \
                     list(Path(dir_path).glob("*.JPG")) + \
                     list(Path(dir_path).glob("*.JPEG")) + \
                     list(Path(dir_path).glob("*.PNG"))

        print(f"  {dir_path}: {len(image_files)} images")

        for img_path in image_files:
            # Create unique name with directory prefix
            temp_name = f"{dir_name}___{img_path.name}"
            temp_path = temp_dir / temp_name
            shutil.copy2(img_path, temp_path)
            image_mapping[temp_name] = str(img_path)

    print(f"\n[OK] Collected {len(image_mapping)} total images\n")

    # Initialize CNN method
    cnn = CNN()

    # Generate encodings for all images
    print("Generating CNN encodings...")
    encodings = cnn.encode_images(image_dir=str(temp_dir))
    print(f"[OK] Generated encodings for {len(encodings)} images\n")

    # Find duplicates
    print(f"Finding duplicates with threshold >= {threshold}...")
    duplicates_temp = cnn.find_duplicates(
        encoding_map=encodings,
        min_similarity_threshold=threshold,
        scores=True
    )

    # Clean up temp directory
    shutil.rmtree(temp_dir)

    # Remap results back to original filenames and paths
    duplicates = {}
    for temp_name, dupes in duplicates_temp.items():
        original_path = image_mapping.get(temp_name, temp_name)
        duplicates[original_path] = []

        for dup_temp_name, score in dupes:
            dup_original_path = image_mapping.get(dup_temp_name, dup_temp_name)
            # Only include if they're from different directories or different files
            if dup_original_path != original_path:
                duplicates[original_path].append((dup_original_path, score))

    return duplicates


def analyze_cross_directory_results(duplicates):
    """
    Analyze and print statistics about found duplicates
    """
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}\n")

    total_images = len(duplicates)
    images_with_dupes = sum(1 for v in duplicates.values() if v)

    # Count unique pairs (avoid counting both A->B and B->A)
    unique_pairs = set()
    for img, dupes in duplicates.items():
        for dup_img, score in dupes:
            pair = tuple(sorted([img, dup_img]))
            unique_pairs.add(pair)

    print(f"Total images analyzed: {total_images}")
    print(f"Images with duplicates: {images_with_dupes}")
    print(f"Unique duplicate pairs: {len(unique_pairs)}")
    print(f"Percentage with duplicates: {images_with_dupes/total_images*100:.1f}%\n")

    if unique_pairs:
        print("Duplicate pairs found:")
        print("-" * 60)
        for i, (img1, img2) in enumerate(sorted(unique_pairs), 1):
            # Find the score
            score = None
            if img1 in duplicates:
                for dup, s in duplicates[img1]:
                    if dup == img2:
                        score = s
                        break

            print(f"\n{i}. Match (similarity: {score:.4f})")
            print(f"   File A: {img1}")
            print(f"   File B: {img2}")
    else:
        print("No duplicates found!")

    return {
        'total_images': total_images,
        'images_with_duplicates': images_with_dupes,
        'unique_pairs': len(unique_pairs),
        'pairs': list(unique_pairs)
    }


def save_results(duplicates, stats, output_file='cross_directory_duplicates.json'):
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


def main():
    # Configuration - List all directories to check
    DIRECTORIES = [
        'combined',
        'photos-75-knollview-way--san-francisco--ca',
        'photos-706-winchester-blvd--los-gatos--ca-9'
    ]

    THRESHOLD = 0.9  # Adjust threshold (0.85-0.95 typical range)

    # Find duplicates across all directories
    duplicates = find_duplicates_across_directories(
        directories=DIRECTORIES,
        threshold=THRESHOLD
    )

    # Analyze results
    stats = analyze_cross_directory_results(duplicates)

    # Save results
    save_results(duplicates, stats, output_file='cross_directory_duplicates.json')

    print(f"\n{'='*60}")
    print("DONE!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
