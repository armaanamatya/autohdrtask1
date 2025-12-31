#!/usr/bin/env python3
"""
Run ASIFT deduplication on a folder and generate report
"""
import sys
from pathlib import Path
from deduplication_asift import remove_near_duplicates

if __name__ == "__main__":
    # Default folder or use command line argument
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = "00a959b5-1b0b-4670-9c07-5df8b7636cfe"
    
    folder = Path(folder_path)
    
    # Find images in processed subfolder or main folder
    processed_folder = folder / "processed" if (folder / "processed").exists() else folder
    images = sorted(processed_folder.glob("*.jpg"))
    
    if not images:
        print(f"No images found in {processed_folder}")
        sys.exit(1)
    
    print(f"Found {len(images)} images in {processed_folder}")
    
    # Create groups (one image per group)
    groups = [[str(img)] for img in images]
    
    # Run deduplication with full_scan=True (compare all pairs)
    print(f"\nRunning ASIFT deduplication with full_scan=True...")
    print("This will compare ALL image pairs (n*(n-1)/2 comparisons)")
    
    filtered = remove_near_duplicates(
        groups, 
        deduplication_flag=1, 
        full_scan=True  # Compare all pairs, not just adjacent
    )
    
    print(f"\nResults: {len(groups)} images -> {len(filtered)} unique")
    print(f"Duplicates found: {len(groups) - len(filtered)}")
    
    # Show which images were kept
    kept_paths = {g[0] for g in filtered}
    print("\nKept images:")
    for img_path in images:
        if str(img_path) in kept_paths:
            print(f"  ✓ {img_path.name}")
        else:
            print(f"  ✗ {img_path.name} (duplicate)")

