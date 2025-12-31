#!/usr/bin/env python3
"""
Run FiftyOne plugin's approximate duplicate detection and save results to markdown
"""
import fiftyone as fo
import fiftyone.brain as fob
from pathlib import Path
import sys
from datetime import datetime

# Add the plugin directory to path
sys.path.insert(0, r"c:\Users\Armaan\Desktop\autohdrtask1\image-deduplication-plugin-main")
from approx_dups import find_approximate_duplicates, get_approximate_duplicate_groups

# Configuration
image_dir = r"c:\Users\Armaan\Desktop\autohdrtask1\000fc774-cb56-4052-a33a-9974c58a00d6\processed"
output_md = r"c:\Users\Armaan\Desktop\autohdrtask1\000fc774-cb56-4052-a33a-9974c58a00d6\fiftyoneresults.md"
dataset_name = "fiftyone_approx_test"

print(f"[INFO] Loading images from {image_dir}")

# Delete existing dataset if it exists
if dataset_name in fo.list_datasets():
    fo.delete_dataset(dataset_name)

# Create dataset from directory
dataset = fo.Dataset.from_dir(
    dataset_dir=image_dir,
    dataset_type=fo.types.ImageDirectory,
    name=dataset_name
)

print(f"[INFO] Created dataset with {len(dataset)} samples")

# Compute similarity index using CLIP embeddings
print("[INFO] Computing CLIP embeddings (this may take a moment)...")
brain_key = "img_sim"

try:
    fob.compute_similarity(
        dataset,
        brain_key=brain_key,
        model="clip-vit-base32-torch"
    )
    print(f"[INFO] Computed similarity index: {brain_key}")
except Exception as e:
    print(f"[ERROR] Failed to compute embeddings: {e}")
    print("[INFO] Trying alternative embedding model...")
    try:
        fob.compute_similarity(
            dataset,
            brain_key=brain_key,
        )
    except Exception as e2:
        print(f"[ERROR] Failed with default model too: {e2}")
        sys.exit(1)

# Find approximate duplicates using different thresholds
print("[INFO] Finding approximate duplicates...")

results = []
thresholds = [0.95, 0.90, 0.85, 0.80]

for threshold in thresholds:
    print(f"[INFO] Testing threshold: {threshold}")
    try:
        result = find_approximate_duplicates(
            dataset,
            brain_key=brain_key,
            threshold=threshold
        )
        results.append({
            'threshold': threshold,
            'num_images_with_dups': result['num_images_with_approx_dups'],
            'num_dups': result['num_dups']
        })
        print(f"  → Found {result['num_dups']} duplicates (out of {result['num_images_with_approx_dups']} images)")
    except Exception as e:
        print(f"[ERROR] Failed at threshold {threshold}: {e}")
        results.append({
            'threshold': threshold,
            'error': str(e)
        })

# Get the duplicate groups from the last threshold
print("[INFO] Getting duplicate groups...")
try:
    dup_groups = get_approximate_duplicate_groups(dataset)
    group_info = []

    for group in dup_groups:
        group_samples = list(group)
        filenames = [Path(s.filepath).name for s in group_samples]
        group_info.append({
            'count': len(group_samples),
            'files': filenames
        })
except Exception as e:
    print(f"[ERROR] Failed to get groups: {e}")
    group_info = []

# Write results to markdown
print(f"[INFO] Writing results to {output_md}")

md_content = f"""# FiftyOne Plugin Approximate Duplicate Detection Results

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Dataset:** `{image_dir}`

**Total Images:** {len(dataset)}

**Method:** FiftyOne plugin `approx_dups.py` with CLIP embeddings

---

## Results by Threshold

| Threshold | Images with Duplicates | Duplicates Removed | Total Remaining |
|-----------|----------------------|-------------------|----------------|
"""

for r in results:
    if 'error' in r:
        md_content += f"| {r['threshold']:.2f} | ERROR | {r['error']} | - |\n"
    else:
        remaining = len(dataset) - r['num_dups']
        md_content += f"| {r['threshold']:.2f} | {r['num_images_with_dups']} | {r['num_dups']} | {remaining} |\n"

md_content += f"""

---

## Duplicate Groups (at threshold {thresholds[-1]})

"""

if group_info:
    for idx, group in enumerate(group_info, 1):
        md_content += f"\n### Group {idx} ({group['count']} images)\n\n"
        for filename in group['files']:
            md_content += f"- `{filename}`\n"
else:
    md_content += "\nNo duplicate groups found or error retrieving groups.\n"

md_content += f"""

---

## Method Details

### FiftyOne Plugin Approach

The FiftyOne plugin's `approx_dups.py` uses:

1. **CLIP Embeddings**: Converts images to semantic embeddings using CLIP model
2. **Similarity Index**: Builds a nearest-neighbor index for fast comparison
3. **Threshold-Based Matching**: Images with similarity score > threshold are marked as duplicates
4. **Single Metric**: Uses only semantic similarity (CLIP cosine similarity)

### Comparison with Custom deduplication.py

| Aspect | FiftyOne Plugin | Custom deduplication.py |
|--------|----------------|------------------------|
| Metrics | 1 (CLIP only) | 5 (MTB, SSIM, CLIP, PDQ, SIFT) |
| Scoring | Single threshold | Weighted composite |
| Safety checks | None | MTB floor, PDQ ceiling |
| Photo awareness | No | Yes (aerial vs regular) |
| Explainability | Low | High (logs all metrics) |

---

## Notes

- Higher thresholds (0.95) are more conservative (fewer duplicates detected)
- Lower thresholds (0.80) are more aggressive (more duplicates detected)
- The plugin uses only semantic similarity, so it may miss visually similar images with different content
- The plugin may flag semantically similar but visually different images as duplicates

"""

with open(output_md, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"[SUCCESS] Results written to {output_md}")

# Cleanup
print("[INFO] Cleaning up dataset...")
fo.delete_dataset(dataset_name)
print("[DONE]")
