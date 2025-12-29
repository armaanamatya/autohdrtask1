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


def main():
    # Configuration
    IMAGE_DIR = 'combined'  # Change this to your image directory
    THRESHOLD = 0.9  # Adjust threshold (0.85-0.95 typical range)
    RECURSIVE = False  # Set to True to include subdirectories

    # Check if directory exists
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: Directory '{IMAGE_DIR}' not found!")
        print("\nAvailable directories:")
        for item in os.listdir('.'):
            if os.path.isdir(item) and not item.startswith('.'):
                print(f"  - {item}")
        return

    # Find duplicates
    duplicates, encodings = find_duplicates_cnn(
        image_dir=IMAGE_DIR,
        threshold=THRESHOLD,
        recursive=RECURSIVE
    )

    # Analyze results
    stats = analyze_results(duplicates)

    # Save results
    save_results(duplicates, stats, output_file='cnn_duplicates.json')

    # Optional: Visualize some examples (set to False for non-interactive mode)
    VISUALIZE = False  # Set to True to generate visualization images
    if stats['images_with_duplicates'] > 0 and VISUALIZE:
        visualize_duplicates(duplicates, IMAGE_DIR, num_examples=3)

    print(f"\n{'='*60}")
    print("DONE!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
