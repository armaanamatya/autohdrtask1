# FiftyOne Plugin vs Custom Deduplication Comparison

## Overview

This document compares the image deduplication approaches used in the FiftyOne plugin (`image-deduplication-plugin-main`) with the custom `deduplication.py` implementation.

---

## exact_dups.py (FiftyOne Plugin)

### What it does:
- Computes file hashes using `fou.compute_filehash()` (likely MD5/SHA)
- Groups images by hash to find **exact** duplicates
- Integrates with FiftyOne's UI for visualization
- Simple hash-based approach: binary match or no match

### Key function:
`find_exact_duplicates()` - Computes hashes, counts duplicates, saves views

### Implementation:
```python
def find_exact_duplicates(sample_collection):
    if _need_to_compute_filehashes(sample_collection):
        compute_filehashes(sample_collection)

    filehash_counts = Counter(sample.filehash for sample in sample_collection)
    dup_filehashes = [k for k, v in filehash_counts.items() if v > 1]

    exact_dup_view = sample_collection.match(
        F("filehash").is_in(dup_filehashes)
    ).sort_by("filehash")
```

---

## approx_dups.py (FiftyOne Plugin)

### What it does:
- Uses FiftyOne's **brain/similarity index** system (embeddings-based)
- Requires pre-computed embeddings (CLIP or similar)
- Finds **approximate** duplicates using distance threshold or fraction
- Groups similar images and provides UI views

### Key function:
`find_approximate_duplicates()` - Uses pre-computed index to find neighbors

### Implementation:
```python
def find_approximate_duplicates(
    sample_collection, brain_key, threshold=None, fraction=None
):
    dataset = sample_collection._dataset
    index = dataset.load_brain_results(brain_key)

    if threshold is not None:
        index.find_duplicates(thresh=threshold)
    else:
        index.find_duplicates(fraction=fraction)

    approx_dup_view = index.duplicates_view()
```

---

## deduplication.py (Custom Implementation)

### What it does:
- **Multi-metric composite scoring** system with 5+ algorithms:
  - **MTB**: Median-Threshold Bitmaps (custom binary edge comparison)
  - **SSIM**: Structural Similarity Index (perceptual quality)
  - **CLIP**: Semantic similarity (what objects are in the image)
  - **PDQ**: Facebook's perceptual hash (Hamming distance)
  - **SIFT**: Scale-Invariant Feature Transform (keypoint matching)

- **Weighted scoring formula**:
  - Regular photos: `0.30×MTB + 0.10×SSIM + 0.25×CLIP + 0.25×PDQ + 0.10×SIFT`
  - Aerial photos: Separate weight configuration

- **Adaptive thresholds** for different photo types (regular vs aerial)
- **Safety guardrails**:
  - MTB hard floor (67%) - never drop if below this
  - PDQ HD ceiling (115) - definitely different if above this
  - SIFT override - high SIFT matches can override other restrictions

- **Detailed logging** with experiment tracking and markdown reports

### Key function:
`remove_near_duplicates()` - Multi-metric weighted comparison with safety checks

### Implementation highlights:
```python
# Composite score calculation
score = (
    w_mtb  * (mtb  / 100.0) +
    w_ssim * (ssim / 100.0) +
    w_clip * (clip / 100.0) +
    w_pdq  * (0.0 if hd >= pdq_ceil else 1.0 - hd / pdq_ceil) +
    w_sift * sift_score
)

# Safety checks
if mtb < mtb_floor and not sift_override:
    continue  # Don't drop - too different
if hd >= pdq_ceil and not sift_override:
    continue  # Don't drop - PDQ says too different

# Final decision
dup = (score >= dup_threshold) and
      ((mtb >= mtb_floor) or sift_override) and
      ((hd < pdq_ceil) or sift_override)
```

---

## Feature Comparison Matrix

| Feature | Plugin (exact/approx) | Custom deduplication.py |
|---------|---------------------|----------------------|
| **Exact duplicates** | ✅ Hash-based (simple, fast) | ❌ Not the focus |
| **Approximate duplicates** | ✅ Embedding-based (single metric) | ✅ **Multi-metric weighted** |
| **Precision** | Medium (single metric) | **High** (composite scoring) |
| **Recall** | Good for similar images | **Excellent** (catches subtle matches) |
| **False positives** | Higher risk | **Lower** (safety guardrails) |
| **Customization** | Limited | **Very flexible** (weights, thresholds) |
| **Integration** | FiftyOne UI only | **Standalone** or integrate anywhere |
| **Photo type awareness** | No | **Yes** (aerial vs regular) |
| **Explainability** | Low | **High** (logs which metrics triggered) |
| **Performance** | Fast (leverages indexes) | Slower (multiple algorithms) |
| **Dependencies** | FiftyOne required | OpenCV, scikit-image, CLIP, etc. |
| **UI Integration** | ✅ Built-in views | ❌ Command-line only |

---

## Detailed Algorithm Comparison

### Plugin Approach (approx_dups.py)
- **Single metric**: Uses one similarity index (typically CLIP embeddings)
- **Simple threshold**: Distance < threshold → duplicate
- **No context awareness**: Same rules for all photo types
- **Quick**: Pre-computed embeddings make comparison fast

### Custom Approach (deduplication.py)
- **Five complementary metrics**:
  1. **MTB**: Catches images with similar brightness patterns
  2. **SSIM**: Catches images with similar structure/quality
  3. **CLIP**: Catches images with similar semantic content
  4. **PDQ**: Catches perceptually similar images (robust to crops/edits)
  5. **SIFT**: Catches images with matching keypoints

- **Weighted composite scoring**: Weak signal in one metric can be compensated by strong signals in others
- **Context-aware**: Different weights for aerial vs ground photos
- **Safety mechanisms**: Multiple guardrails prevent false positives
- **Explainable**: Logs show exactly which metrics triggered the duplicate decision

---

## Performance Characteristics

### FiftyOne Plugin
- **Speed**: ⚡ Fast (uses pre-computed indexes)
- **Memory**: Low (stores only embeddings)
- **Setup**: Requires FiftyOne ecosystem
- **Scalability**: Excellent (designed for large datasets)

### Custom deduplication.py
- **Speed**: 🐢 Slower (computes 5+ metrics per pair)
- **Memory**: High (loads models: CLIP, SIFT detectors)
- **Setup**: Complex (multiple dependencies)
- **Scalability**: Moderate (uses threading, but compute-heavy)

---

## Use Case Recommendations

### Use FiftyOne Plugin When:
- You need exact duplicate detection (hash-based)
- You want a simple, fast approximate duplicate finder
- You're already using FiftyOne for dataset management
- You need UI-based duplicate review and removal
- Performance is critical

### Use Custom deduplication.py When:
- You need **high precision** near-duplicate detection
- False positives are unacceptable
- You're working with diverse photo types (aerial, ground, indoor, outdoor)
- You need explainable results (why was this marked as duplicate?)
- You want fine-grained control over thresholds and weights
- You're building a production pipeline for real estate/photography

---

## Recommendation

**The custom `deduplication.py` is significantly more sophisticated** for near-duplicate detection because:

1. **Multi-metric approach** catches duplicates that single metrics miss
2. **Adaptive thresholds** handle different photo types (aerial vs ground)
3. **Safety guardrails** prevent false positives
4. **Explainable results** - you can see WHY images were marked as duplicates
5. **Production-ready** for distinguishing subtle near-duplicates

### Should you implement the plugin's approach in your pipeline?

**No, keep your current approach.** The plugin's methods are:
- **exact_dups.py**: Too simple - just hash matching (though you could add this as a pre-filter)
- **approx_dups.py**: Less sophisticated than your weighted composite scoring

### However, you could:

1. **Add hash-based pre-filter** from `exact_dups.py` to catch identical files before running expensive multi-metric checks
2. **Use FiftyOne's UI** to visualize your deduplication results (integrate your code with FiftyOne datasets)
3. **Export your results** to FiftyOne format for manual review

---

## Potential Hybrid Approach

```python
# Step 1: Fast exact duplicate removal (hash-based)
exact_dups = find_exact_duplicates_via_hash(images)
remove_exact_duplicates(exact_dups)

# Step 2: Multi-metric near-duplicate detection (your approach)
remaining_images = [img for img in images if img not in exact_dups]
near_dups = remove_near_duplicates(remaining_images,
                                   deduplication_flag=1,
                                   full_scan=False)

# Step 3: Visualize results in FiftyOne UI
dataset = export_to_fiftyone(near_dups)
fo.launch_app(dataset)
```

This combines the best of both worlds: fast exact matching + sophisticated near-duplicate detection + visualization.

---

## Conclusion

**Your `deduplication.py` is the winner** for production near-duplicate detection. The FiftyOne plugin is simpler and faster, but your multi-metric weighted approach with safety guardrails is far more robust and explainable. The plugin's main value is in exact duplicate detection and UI visualization, which could complement your existing pipeline.
