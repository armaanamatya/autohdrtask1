#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedupwphash.py  – Image Deduplication with pHash Integration

Near-duplicate remover that uses:
    • MTB   (Median-Threshold Bitmaps)
    • SSIM  (thumbnail structural similarity)
    • CLIP  (cosine similarity)
    • PDQ   (Hamming distance)
    • SIFT  (geometric feature matching)
    • pHash (Perceptual Hash) ✨ NEW

pHash provides complementary perceptual hashing using DCT-based approach,
different from PDQ's algorithm. This adds diversity to duplicate detection.

------------------------------------------------------------
Dependencies
------------------------------------------------------------
    pip install opencv-python-headless numpy pillow
    pip install scikit-image           # <-- for SSIM
    pip install pdqhash-lite           # <-- for PDQ
    pip install open_clip_torch torch  # <-- for CLIP
    pip install imagehash              # <-- for pHash ✨ NEW
"""

from __future__ import annotations

import logging
import os
import io
import sys
import threading
from datetime import datetime
from pathlib import Path
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Any, Optional

import cv2
import numpy as np

# ─── optional deps ────────────────────────────────────────────────────────────
try:
    import pdqhash
except ImportError:
    pdqhash = None

try:
    from skimage.metrics import structural_similarity as _ssim
except ImportError:
    _ssim = None

try:
    from PIL import Image
    _pil_available = True
except ImportError:
    _pil_available = False

try:
    import imagehash
    _phash_available = True
except ImportError:
    _phash_available = False
    logging.warning("imagehash not available - pHash will be disabled. Install with: pip install imagehash")

USE_CLIP = True
if USE_CLIP:
    try:
        import torch, open_clip
        _clip_model = _clip_pre = _clip_device = None
        _clip_lock = threading.Lock()
    except ImportError:
        USE_CLIP = False

# ─── logging ──────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# ─── experiment logging ───────────────────────────────────────────────────────
EXPERIMENT_LOG_FILE = "experiment_logs.md"

class ExperimentLogger:
    """Captures log output and writes experiment results to markdown"""

    def __init__(self):
        self.log_capture = io.StringIO()
        self.handler: Optional[logging.Handler] = None
        self.comparison_results: List[Dict[str, Any]] = []
        self.input_count = 0
        self.output_count = 0

    def start_capture(self) -> None:
        self.handler = logging.StreamHandler(self.log_capture)
        self.handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(self.handler)

    def stop_capture(self) -> str:
        if self.handler:
            logger.removeHandler(self.handler)
        return self.log_capture.getvalue()

    def add_comparison(self, img_a: str, img_b: str, mtb: float, edge: float,
                       ssim: float, clip: float, pdq_hd: int, phash_hd: int,
                       sift_matches: int, score: float, dropped: bool, drop_reason: str) -> None:
        self.comparison_results.append({
            "img_a": Path(img_a).stem,
            "img_b": Path(img_b).stem,
            "mtb": mtb,
            "edge": edge,
            "ssim": ssim,
            "clip": clip,
            "pdq_hd": pdq_hd,
            "phash_hd": phash_hd,
            "sift_matches": sift_matches,
            "score": score,
            "dropped": dropped,
            "drop_reason": drop_reason
        })

    def write_experiment_log(self, experiment_name: str, terminal_output: str, log_file: str) -> None:
        log_path = Path(log_file)

        # Build the complete markdown file
        entry = f"""# {experiment_name}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration

| Parameter | Value |
|-----------|-------|
| USE_CLIP | {USE_CLIP} |
| WEIGHT_MTB | {WEIGHT_MTB} |
| WEIGHT_SSIM | {WEIGHT_SSIM} |
| WEIGHT_CLIP | {WEIGHT_CLIP} |
| WEIGHT_PDQ | {WEIGHT_PDQ} |
| WEIGHT_PHASH | {WEIGHT_PHASH} ✨ |
| WEIGHT_SIFT | {WEIGHT_SIFT} |
| COMPOSITE_DUP_THRESHOLD | {COMPOSITE_DUP_THRESHOLD} |
| MTB_HARD_FLOOR | {MTB_HARD_FLOOR} |
| PDQ_HD_CEIL | {PDQ_HD_CEIL} |
| PHASH_HD_CEIL | {PHASH_HD_CEIL} ✨ |
| SIFT_MIN_MATCHES | {SIFT_MIN_MATCHES} |

## Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | pHash HD | SIFT | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|----------|------|-------|----------|
"""
        for r in self.comparison_results:
            dropped_str = f"Yes ({r['drop_reason']})" if r["dropped"] else "No"
            if not r["dropped"] and r["drop_reason"]:
                dropped_str = f"No ({r['drop_reason']})"
            entry += f"| {r['img_a']} | {r['img_b']} | {r['mtb']:.1f} | {r['edge']:.1f} | {r['ssim']:.1f} | {r['clip']:.1f} | {r['pdq_hd']} | {r['phash_hd']} | {r['sift_matches']} | {r['score']:.2f} | {dropped_str} |\n"

        entry += f"""
## Summary

- **Input:** {self.input_count} groups
- **Output:** {self.output_count} groups
- **Duplicates removed:** {self.input_count - self.output_count}

## Terminal Output

```
{terminal_output.strip()}
```
"""
        # Write to file (overwrite)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(entry)

        logger.info(f"Experiment logged to {log_path}")

_experiment_logger: Optional[ExperimentLogger] = None

# ─── tuning knobs ─────────────────────────────────────────────────────────────
MTB_SIZE, EDGE_SIZE, SSIM_SIZE = 640, 640, 320
BLUR_SIZE, CANNY1, CANNY2 = 5, 50, 150
USE_AUTO_CANNY, SIGMA, USE_CLAHE = True, 0.33, True

# safety guardrails
MTB_HARD_FLOOR = 58.0     # never drop if below this MTB %
PDQ_HD_CEIL    = 140      # HD ≥ this ⇒ totally different
PHASH_HD_CEIL  = 20       # ✨ NEW: pHash Hamming distance ceiling (max 64 bits)

# weighted-score config for REGULAR photos (weights must sum to 1.0)
WEIGHT_MTB   = 0.38   # Slightly reduced to make room for pHash
WEIGHT_SSIM  = 0.10   # ENABLED - Testing with SSIM
WEIGHT_CLIP  = 0.20   # Slightly reduced
WEIGHT_PDQ   = 0.14   # Reduced to make room for pHash
WEIGHT_PHASH = 0.05   # ✨ NEW: pHash weight (5% - complementary to PDQ)
WEIGHT_SIFT  = 0.13   # Adjusted to keep sum = 1.0
COMPOSITE_DUP_THRESHOLD = 0.55   # 0–1 scale
SIFT_MIN_MATCHES = 150            # Minimum SIFT matches

# safety guardrails for AERIAL photos
AERIAL_MTB_HARD_FLOOR = 55.0
AERIAL_PDQ_HD_CEIL    = 130
AERIAL_PHASH_HD_CEIL  = 18       # ✨ NEW: Slightly lower for aerial

# weighted-score config for AERIAL photos (weights must sum to 1.0)
AERIAL_WEIGHT_MTB   = 0.38   # Adjusted
AERIAL_WEIGHT_SSIM  = 0.10
AERIAL_WEIGHT_CLIP  = 0.25   # Higher for aerial - semantic more reliable
AERIAL_WEIGHT_PDQ   = 0.13   # Reduced to make room for pHash
AERIAL_WEIGHT_PHASH = 0.04   # ✨ NEW: Slightly lower weight for aerial
AERIAL_WEIGHT_SIFT  = 0.10
AERIAL_COMPOSITE_DUP_THRESHOLD = 0.38
AERIAL_SIFT_MIN_MATCHES = 100

MAX_WORKERS = 16

# ─── weight configuration helper ──────────────────────────────────────────────
def set_weights(mtb=None, ssim=None, clip=None, pdq=None, phash=None, sift=None,
                aerial_mtb=None, aerial_ssim=None, aerial_clip=None,
                aerial_pdq=None, aerial_phash=None, aerial_sift=None):
    """
    Set global weight variables for batch testing.

    Args:
        mtb, ssim, clip, pdq, phash, sift: Weights for regular photos (0.0-1.0)
        aerial_*: Weights for aerial photos (0.0-1.0)

    Note: Weights should sum to 1.0. This function does NOT validate the sum.
    """
    global WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_PHASH, WEIGHT_SIFT
    global AERIAL_WEIGHT_MTB, AERIAL_WEIGHT_SSIM, AERIAL_WEIGHT_CLIP
    global AERIAL_WEIGHT_PDQ, AERIAL_WEIGHT_PHASH, AERIAL_WEIGHT_SIFT

    # Set regular photo weights
    if mtb is not None:
        WEIGHT_MTB = mtb
    if ssim is not None:
        WEIGHT_SSIM = ssim
    if clip is not None:
        WEIGHT_CLIP = clip
    if pdq is not None:
        WEIGHT_PDQ = pdq
    if phash is not None:
        WEIGHT_PHASH = phash
    if sift is not None:
        WEIGHT_SIFT = sift

    # Set aerial photo weights (if provided)
    if aerial_mtb is not None:
        AERIAL_WEIGHT_MTB = aerial_mtb
    if aerial_ssim is not None:
        AERIAL_WEIGHT_SSIM = aerial_ssim
    if aerial_clip is not None:
        AERIAL_WEIGHT_CLIP = aerial_clip
    if aerial_pdq is not None:
        AERIAL_WEIGHT_PDQ = aerial_pdq
    if aerial_phash is not None:
        AERIAL_WEIGHT_PHASH = aerial_phash
    if aerial_sift is not None:
        AERIAL_WEIGHT_SIFT = aerial_sift


def get_weights():
    """
    Get current weight configuration.

    Returns:
        dict: Dictionary with 'regular' and 'aerial' weight configurations
    """
    return {
        'regular': {
            'mtb': WEIGHT_MTB,
            'ssim': WEIGHT_SSIM,
            'clip': WEIGHT_CLIP,
            'pdq': WEIGHT_PDQ,
            'phash': WEIGHT_PHASH,
            'sift': WEIGHT_SIFT
        },
        'aerial': {
            'mtb': AERIAL_WEIGHT_MTB,
            'ssim': AERIAL_WEIGHT_SSIM,
            'clip': AERIAL_WEIGHT_CLIP,
            'pdq': AERIAL_WEIGHT_PDQ,
            'phash': AERIAL_WEIGHT_PHASH,
            'sift': AERIAL_WEIGHT_SIFT
        }
    }

# ─── helpers: I/O / resize / CLAHE / metadata ─────────────────────────────────
@lru_cache(maxsize=512)
def _load_gray(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise IOError(f"Failed to read {path}")
    return img

def _resize_keep_aspect(img: np.ndarray, target: int) -> np.ndarray:
    h, w = img.shape[:2]
    if max(h, w) <= target:
        return img
    scale = target / max(h, w)
    new_w, new_h = int(w*scale), int(h*scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def _resize_to_exact_size(img: np.ndarray, target_size: int) -> np.ndarray:
    """Resize image to exact target size by cropping to square, no padding"""
    h, w = img.shape[:2]
    if h == target_size and w == target_size:
        return img

    # Calculate scale to fit the longer dimension to target_size
    scale = target_size / max(h, w)
    new_h, new_w = int(h * scale), int(w * scale)

    # Resize image
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # If not square, crop to center square
    if new_h != new_w:
        min_dim = min(new_h, new_w)
        start_h = (new_h - min_dim) // 2
        start_w = (new_w - min_dim) // 2
        resized = resized[start_h:start_h+min_dim, start_w:start_w+min_dim]

    # Final resize to exact target size if needed
    if resized.shape[0] != target_size or resized.shape[1] != target_size:
        resized = cv2.resize(resized, (target_size, target_size), interpolation=cv2.INTER_AREA)

    return resized

def _apply_clahe(img: np.ndarray) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(img)

# ─── metadata extraction ──────────────────────────────────────────────────────
def _is_aerial(path: str, metadata_dict: Dict[str, Dict[str, Any]]) -> bool:
    """Check if photo is aerial (drone/aircraft) based on filename and metadata"""
    filename = os.path.basename(path).upper()
    make = metadata_dict.get(path, {}).get('make', '')
    model = metadata_dict.get(path, {}).get('model', '')
    if 'DJI' in filename or (make and ('DJI' in make.upper() or ('HASSELBLAD' in make.upper() and model and 'X1D' not in model.upper()) or 'AUTEL ROBOTICS' in make.upper())):
        return True
    return False

# ─── bitmap / edge / SSIM ─────────────────────────────────────────────────────
def _compute_mtb(gray: np.ndarray) -> np.ndarray:
    return gray > np.median(gray)

def _compute_edges(gray: np.ndarray) -> np.ndarray:
    if BLUR_SIZE > 0:
        gray = cv2.medianBlur(gray, BLUR_SIZE)
    c1, c2 = CANNY1, CANNY2
    if USE_AUTO_CANNY:
        v = np.median(gray)
        c1 = int(max(0, (1.0 - SIGMA) * v))
        c2 = int(min(255, (1.0 + SIGMA) * v))
    return (cv2.Canny(gray, c1, c2) > 0)

def overlap_percent(a: np.ndarray, b: np.ndarray) -> float:
    if a.sum() == 0 or b.sum() == 0:
        return 0.0
    return 100.0 * np.logical_and(a, b).sum() / min(a.sum(), b.sum())

def _compute_ssim(gA: np.ndarray, gB: np.ndarray) -> float:
    """Return SSIM in 0–100 (%). 0 if skimage unavailable."""
    if _ssim is None:
        return 0.0
    H, W = max(gA.shape[0], gB.shape[0]), max(gA.shape[1], gB.shape[1])
    padA = np.pad(gA, ((0, H-gA.shape[0]), (0, W-gA.shape[1])), constant_values=0)
    padB = np.pad(gB, ((0, H-gB.shape[0]), (0, W-gB.shape[1])), constant_values=0)
    return 100.0 * float(_ssim(padA, padB, data_range=255))

# ─── PDQ helpers ──────────────────────────────────────────────────────────────
def _pdq_bits(path: str) -> Optional[np.ndarray]:
    if pdqhash is None:
        return None
    try:
        from PIL import Image
        bits, _ = pdqhash.compute(np.asarray(Image.open(path).convert("RGB")))
        return np.array(bits, np.uint8)
    except Exception:
        return None

def _pdq_hd(a: np.ndarray, b: np.ndarray) -> int:
    if a is None or b is None or a.shape != b.shape:
        return 999
    return int(np.count_nonzero(a ^ b))

# ─── pHash helpers ✨ NEW ─────────────────────────────────────────────────────
def _phash_hash(path: str) -> Optional[imagehash.ImageHash]:
    """Compute pHash (Perceptual Hash) using DCT-based algorithm"""
    if not _phash_available:
        return None
    try:
        from PIL import Image
        img = Image.open(path)
        # Using hash_size=8 gives 64-bit hash (8x8 DCT)
        return imagehash.phash(img, hash_size=8)
    except Exception as e:
        logger.debug(f"pHash computation failed for {path}: {e}")
        return None

def _phash_hd(a: Optional[imagehash.ImageHash], b: Optional[imagehash.ImageHash]) -> int:
    """Calculate Hamming distance between two pHash hashes"""
    if a is None or b is None:
        return 999
    try:
        return int(a - b)  # imagehash overloads '-' operator for Hamming distance
    except Exception:
        return 999

# ─── CLIP helpers ─────────────────────────────────────────────────────────────
_clip_failed = False

def _safe_clip_embed(path: str) -> Optional[np.ndarray]:
    if not USE_CLIP:
        return None
    global _clip_model, _clip_pre, _clip_device, _clip_failed

    if _clip_failed:
        return None

    try:
        import PIL.Image as Image
        if _clip_model is None:
            with _clip_lock:
                if _clip_model is None:
                    if torch.cuda.is_available():
                        try:
                            _clip_device = "cuda"
                            _clip_model, _clip_pre, _ = open_clip.create_model_and_transforms(
                                "ViT-B-32", pretrained="openai", device=_clip_device)
                            _clip_model.eval()

                            test_tensor = torch.randn(1, 3, 224, 224).to(_clip_device)
                            with torch.no_grad():
                                test_emb = _clip_model.encode_image(test_tensor)

                            logger.info(f"CLIP model loaded on CUDA successfully")
                        except Exception as cuda_err:
                            logger.warning(f"CLIP CUDA failed ({cuda_err}), falling back to CPU")
                            _clip_device = "cpu"
                            _clip_model, _clip_pre, _ = open_clip.create_model_and_transforms(
                                "ViT-B-32", pretrained="openai", device=_clip_device)
                            _clip_model.eval()
                            logger.info(f"CLIP model loaded on CPU successfully")
                    else:
                        _clip_device = "cpu"
                        _clip_model, _clip_pre, _ = open_clip.create_model_and_transforms(
                            "ViT-B-32", pretrained="openai", device=_clip_device)
                        _clip_model.eval()
                        logger.info(f"CLIP model loaded on CPU (CUDA not available)")

        img = Image.open(path).convert("RGB")
        t = _clip_pre(img).unsqueeze(0).to(_clip_device)
        with torch.no_grad():
            emb = _clip_model.encode_image(t).cpu().squeeze()

        if emb is None or emb.numel() == 0 or torch.isnan(emb).any():
            logger.error(f"CLIP produced invalid embedding for {path}")
            return None

        return (emb / (emb.norm() + 1e-8)).numpy()
    except Exception as e:
        logger.error(f"CLIP embedding failed for {path}: {e}")
        if "CUDA" in str(e) or "device" in str(e).lower():
            logger.error("CLIP appears to have device issues, disabling for this session")
            _clip_failed = True
        return None

def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    if a is None or b is None:
        return 0.0
    return float(np.dot(a, b))

# ─── SIFT helpers ─────────────────────────────────────────────────────────────
def _compute_sift_matches(path_a: str, path_b: str, min_matches: int = 50) -> int:
    """
    Compute SIFT feature matches between two images.
    Returns the number of good matches after Lowe's ratio test.
    """
    try:
        img1 = cv2.imread(path_a, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(path_b, cv2.IMREAD_GRAYSCALE)

        if img1 is None or img2 is None:
            return 0

        sift = cv2.SIFT_create()

        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        if des1 is None or des2 is None or len(des1) < 2 or len(des2) < 2:
            return 0

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)

        return len(good_matches)
    except Exception as e:
        logger.debug(f"SIFT computation failed for {path_a} vs {path_b}: {e}")
        return 0

# ─── metric worker & cache ────────────────────────────────────────────────────
def _metric_worker(path: str) -> Dict[str, Any]:
    gray = _load_gray(path)
    if USE_CLAHE:
        gray = _apply_clahe(gray)

    return dict(
        path=path,
        filename=Path(path).name,
        mtb=_compute_mtb(_resize_to_exact_size(gray, MTB_SIZE)),
        edges=_compute_edges(_resize_to_exact_size(gray, EDGE_SIZE)),
        gray_ssim=_resize_keep_aspect(gray, SSIM_SIZE),
        pdq=_pdq_bits(path),
        phash=_phash_hash(path),  # ✨ NEW
        clip=_safe_clip_embed(path)
    )

_metric_store: Dict[str, Dict[str, Any]] = {}

@lru_cache(maxsize=4096)
def _pair_sim(path_a: str, path_b: str) -> Tuple[float, float, int, float, float, int, int]:
    """Return (mtb %, edge %, PDQ-HD, SSIM %, CLIP %, pHash-HD, SIFT matches)"""
    mA, mB = _metric_store[path_a], _metric_store[path_b]

    if mA["mtb"].shape != mB["mtb"].shape:
        logger.warning("MTB shape mismatch: %s vs %s - this shouldn't happen anymore",
                       mA["mtb"].shape, mB["mtb"].shape)
        return 0.0, 0.0, 999, 0.0, 0.0, 999, 0
    if mA["edges"].shape != mB["edges"].shape:
        logger.warning("Edge shape mismatch: %s vs %s - this shouldn't happen anymore",
                       mA["edges"].shape, mB["edges"].shape)
        return 0.0, 0.0, 999, 0.0, 0.0, 999, 0

    mtb  = overlap_percent(mA["mtb"],   mB["mtb"])
    edge = overlap_percent(mA["edges"], mB["edges"])
    hd   = _pdq_hd(mA["pdq"],           mB["pdq"])
    phash_hd = _phash_hd(mA["phash"],   mB["phash"])  # ✨ NEW
    ssim = _compute_ssim(mA["gray_ssim"], mB["gray_ssim"])
    clip = 100.0 * _cosine(mA["clip"],     mB["clip"])
    sift_matches = _compute_sift_matches(path_a, path_b, SIFT_MIN_MATCHES)
    return mtb, edge, hd, ssim, clip, phash_hd, sift_matches

# ─── main deduper ─────────────────────────────────────────────────────────────
def remove_near_duplicates(
    groups: List[List[str]],
    deduplication_flag: int = 0,
    metadata_dict: Dict[str, Dict[str, Any]] = None,
    threshold: float = 0.0,
    full_scan: bool = False
) -> List[List[str]]:
    if deduplication_flag != 1 or len(groups) < 2:
        return groups

    mids = [g[len(g)//2] for g in groups]
    logger.info("[STEP] Pre-computing metrics for %d middles (including pHash)…", len(mids))
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for fut in as_completed(pool.submit(_metric_worker, p) for p in mids):
            m = fut.result()
            _metric_store[m["path"]] = m

    if metadata_dict is None:
        logger.warning("No metadata_dict provided, using empty dict for aerial detection")
        metadata_dict = {}

    logger.info("[STEP] Multi-metric dedup (6 metrics: MTB+SSIM+CLIP+PDQ+pHash+SIFT, full_scan=%s)", full_scan)
    keep = [True] * len(groups)
    stats = {"mtb": [], "edge": [], "hd": [], "phash_hd": [], "ssim": [], "clip": [], "sift": [], "score": []}

    def _log_pair(i: int, j: int, mtb: float, edge: float, hd: int, phash_hd: int,
                  ssim: float, clip: float, sift_matches: int, score: float, is_aerial_pair: bool):
        weight_type = "AERIAL" if is_aerial_pair else "REGULAR"
        logger.info(
            "  • %s ↔ %s : MTB=%.1f  Edge=%.1f  SSIM=%.1f  CLIP=%.1f  PDQ=%d  pHash=%d  SIFT=%d  SCORE=%.2f [%s]",
            Path(mids[i]).stem, Path(mids[j]).stem,
            mtb, edge, ssim, clip, hd, phash_hd, sift_matches, score, weight_type
        )
        logger.info("     Comparing: %s", mids[i])
        logger.info("     With:      %s", mids[j])

    def _drop(idx: int, mtb: float, edge: float, hd: int, phash_hd: int,
              ssim: float, clip: float, score: float,
              trigger_metrics: List[str], is_aerial_img: bool):
        mean = {k: (np.mean(v) if v else 0.0) for k, v in stats.items()}

        uuid = next((p for p in Path(mids[idx]).parts
                     if len(p) == 36 and p.count('-') == 4), "unknown")

        weight_type = "AERIAL" if is_aerial_img else "REGULAR"
        logger.info(
            "       → DROPPING stack %s (UUID: %s) [%s]   ΔMTB=%.1f  ΔEdge=%.1f  ΔSSIM=%.1f  "
            "ΔCLIP=%.1f  ΔPDQ_HD=%+.0f  ΔpHash_HD=%+.0f  ΔSCORE=%.2f  "
            "(means MTB=%.1f Edge=%.1f SSIM=%.1f CLIP=%.1f PDQ_HD=%.0f pHash_HD=%.0f SCORE=%.2f)",
            Path(mids[idx]).stem, uuid, weight_type,
            mtb - mean["mtb"], edge - mean["edge"],
            ssim - mean["ssim"], clip - mean["clip"], hd - mean["hd"],
            phash_hd - mean["phash_hd"], score - mean["score"],
            mean["mtb"], mean["edge"], mean["ssim"], mean["clip"],
            mean["hd"], mean["phash_hd"], mean["score"]
        )
        logger.info("       → Triggered by: %s", ", ".join(trigger_metrics))
        logger.info("       → Dropped image: %s", mids[idx])
        keep[idx] = False

    # comparison schedule
    idx_pairs = ([(i, j) for i in range(len(groups)-1)
                           for j in range(i+1, len(groups))]
                 if full_scan else [(i, i+1) for i in range(len(groups)-1)])

    for i, j in idx_pairs:
        if not keep[i] or not keep[j]:
            continue

        if mids[i] == mids[j]:
            logger.debug("Skipping self-comparison: %s", mids[i])
            continue

        mtb, edge, hd, ssim, clip, phash_hd, sift_matches = _pair_sim(mids[i], mids[j])
        if hd == 999:
            continue

        # Check if either image is aerial
        is_aerial_i = _is_aerial(mids[i], metadata_dict)
        is_aerial_j = _is_aerial(mids[j], metadata_dict)
        is_aerial_pair = is_aerial_i or is_aerial_j

        # Select appropriate weights and threshold
        if is_aerial_pair:
            w_mtb, w_ssim, w_clip, w_pdq, w_phash, w_sift = (
                AERIAL_WEIGHT_MTB, AERIAL_WEIGHT_SSIM, AERIAL_WEIGHT_CLIP,
                AERIAL_WEIGHT_PDQ, AERIAL_WEIGHT_PHASH, AERIAL_WEIGHT_SIFT
            )
            dup_threshold = AERIAL_COMPOSITE_DUP_THRESHOLD
            mtb_floor = AERIAL_MTB_HARD_FLOOR
            pdq_ceil = AERIAL_PDQ_HD_CEIL
            phash_ceil = AERIAL_PHASH_HD_CEIL
            sift_min = AERIAL_SIFT_MIN_MATCHES
        else:
            w_mtb, w_ssim, w_clip, w_pdq, w_phash, w_sift = (
                WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP,
                WEIGHT_PDQ, WEIGHT_PHASH, WEIGHT_SIFT
            )
            dup_threshold = COMPOSITE_DUP_THRESHOLD
            mtb_floor = MTB_HARD_FLOOR
            pdq_ceil = PDQ_HD_CEIL
            phash_ceil = PHASH_HD_CEIL
            sift_min = SIFT_MIN_MATCHES

        # Normalize SIFT matches to 0-1 scale (cap at 100 matches = 1.0)
        sift_score = min(sift_matches / 100.0, 1.0) if sift_matches > 0 else 0.0

        # composite score with selected weights (including pHash ✨)
        score = (
            w_mtb    * (mtb  / 100.0) +
            w_ssim   * (ssim / 100.0) +
            w_clip   * (clip / 100.0) +
            w_pdq    * (0.0 if hd >= pdq_ceil else 1.0 - hd / pdq_ceil) +
            w_phash  * (0.0 if phash_hd >= phash_ceil else 1.0 - phash_hd / phash_ceil) +  # ✨ NEW
            w_sift   * sift_score
        )

        # stats + logging
        for k, v in zip(("mtb", "edge", "hd", "phash_hd", "ssim", "clip", "sift", "score"),
                        (mtb, edge, hd, phash_hd, ssim, clip, sift_matches, score)):
            stats[k].append(v)
        _log_pair(i, j, mtb, edge, hd, phash_hd, ssim, clip, sift_matches, score, is_aerial_pair)

        # decision logic
        trigger_metrics = []
        drop_reason = ""
        if score >= dup_threshold:
            trigger_metrics.append(f"SCORE({score:.2f}≥{dup_threshold})")

        # SIFT override
        sift_override = (sift_matches >= sift_min * 3.0) or ((sift_matches >= sift_min) and (clip >= 92.0))

        if mtb < mtb_floor and not sift_override:
            trigger_metrics.append(f"MTB_FLOOR_FAIL({mtb:.1f}<{mtb_floor})")
            drop_reason = f"MTB < {mtb_floor}"
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, phash_hd, sift_matches, score,
                    dropped=False, drop_reason=drop_reason
                )
            continue
        if hd >= pdq_ceil and not sift_override:
            trigger_metrics.append(f"PDQ_HD({hd:.0f}≥{pdq_ceil})")
            drop_reason = f"PDQ >= {pdq_ceil}"
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, phash_hd, sift_matches, score,
                    dropped=False, drop_reason=drop_reason
                )
            continue

        # Allow duplicate if: (score high AND (MTB floor passed OR SIFT override)) AND (PDQ ceiling passed OR SIFT override)
        dup = (score >= dup_threshold) and ((mtb >= mtb_floor) or sift_override) and ((hd < pdq_ceil) or sift_override)

        if sift_override:
            if sift_matches >= sift_min * 3.0:
                trigger_metrics.append(f"SIFT_OVERRIDE(HIGH: {sift_matches}≥{sift_min * 3.0:.0f})")
            else:
                trigger_metrics.append(f"SIFT_OVERRIDE(COMBO: SIFT={sift_matches}≥{sift_min}, CLIP={clip:.1f}≥92.0)")

        if dup:
            _drop(i, mtb, edge, hd, phash_hd, ssim, clip, score, trigger_metrics, is_aerial_i)
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, phash_hd, sift_matches, score,
                    dropped=True, drop_reason="duplicate"
                )
        else:
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, phash_hd, sift_matches, score,
                    dropped=False, drop_reason=f"SCORE < {dup_threshold}" if score < dup_threshold else ""
                )

    final_groups = [g for g, k in zip(groups, keep) if k]
    logger.info("[RESULT] stacks: %d → %d", len(groups), len(final_groups))
    return final_groups



def generate_thumbnail(img_path: str, output_path: str, size: int = 200) -> bool:
    """Generate thumbnail for an image"""
    try:
        from PIL import Image
        img = Image.open(img_path)
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        img.save(output_path, "JPEG", quality=85)
        return True
    except Exception as e:
        logger.error(f"Failed to generate thumbnail for {img_path}: {e}")
        return False


def generate_folder_report(folder_name: str, output_dir: str, groups_before: List[List[str]],
                          groups_after: List[List[str]], comparisons: List[Dict[str, Any]],
                          dropped_images: List[str]) -> None:
    """Generate markdown report with visualizations and statistics for a folder"""

    # Create thumbnails directory
    thumb_dir = Path(output_dir) / "thumbnails"
    thumb_dir.mkdir(parents=True, exist_ok=True)

    # Calculate statistics
    n_input = len(groups_before)
    n_output = len(groups_after)
    n_dropped = n_input - n_output
    removal_rate = (n_dropped / n_input * 100) if n_input > 0 else 0.0

    # Statistics from comparisons
    if comparisons:
        mtb_vals = [c['mtb'] for c in comparisons]
        edge_vals = [c['edge'] for c in comparisons]
        ssim_vals = [c['ssim'] for c in comparisons]
        clip_vals = [c['clip'] for c in comparisons]
        pdq_vals = [c['pdq_hd'] for c in comparisons]
        phash_vals = [c['phash_hd'] for c in comparisons]
        sift_vals = [c['sift_matches'] for c in comparisons]
        score_vals = [c['score'] for c in comparisons]

        def stats(vals):
            return {
                'mean': np.mean(vals),
                'median': np.median(vals),
                'min': np.min(vals),
                'max': np.max(vals),
                'std': np.std(vals)
            }
    else:
        mtb_vals = edge_vals = ssim_vals = clip_vals = pdq_vals = phash_vals = sift_vals = score_vals = []

    # Generate report
    report_path = Path(output_dir) / f"{folder_name}_report_phash.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Folder Deduplication Report (with pHash): {folder_name}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Summary
        f.write("## Summary\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| **Input Images** | {n_input} |\n")
        f.write(f"| **Output Images** | {n_output} |\n")
        f.write(f"| **Duplicates Removed** | {n_dropped} |\n")
        f.write(f"| **Removal Rate** | {removal_rate:.1f}% |\n")
        f.write(f"| **Comparisons Made** | {len(comparisons)} |\n")
        f.write(f"| **Status** | ✅ Success |\n\n")

        # Configuration
        f.write("## Configuration\n\n")
        f.write("| Parameter | Value |\n")
        f.write("|-----------|-------|\n")
        f.write(f"| USE_CLIP | {USE_CLIP} |\n")
        f.write(f"| WEIGHT_MTB | {WEIGHT_MTB} |\n")
        f.write(f"| WEIGHT_SSIM | {WEIGHT_SSIM} |\n")
        f.write(f"| WEIGHT_CLIP | {WEIGHT_CLIP} |\n")
        f.write(f"| WEIGHT_PDQ | {WEIGHT_PDQ} |\n")
        f.write(f"| WEIGHT_PHASH | {WEIGHT_PHASH} ✨ |\n")
        f.write(f"| WEIGHT_SIFT | {WEIGHT_SIFT} |\n")
        f.write(f"| COMPOSITE_DUP_THRESHOLD | {COMPOSITE_DUP_THRESHOLD} |\n")
        f.write(f"| MTB_HARD_FLOOR | {MTB_HARD_FLOOR} |\n")
        f.write(f"| PDQ_HD_CEIL | {PDQ_HD_CEIL} |\n")
        f.write(f"| PHASH_HD_CEIL | {PHASH_HD_CEIL} ✨ |\n")
        f.write(f"| SIFT_MIN_MATCHES | {SIFT_MIN_MATCHES} |\n\n")

        # Statistics
        if comparisons:
            f.write("## Statistics\n\n")
            f.write("### All Comparisons\n\n")
            f.write("| Metric | Mean | Median | Min | Max | Std Dev |\n")
            f.write("|--------|------|--------|-----|-----|---------||\n")

            for name, vals, fmt in [
                ("MTB %", mtb_vals, ".2f"),
                ("Edge %", edge_vals, ".2f"),
                ("SSIM %", ssim_vals, ".2f"),
                ("CLIP %", clip_vals, ".2f"),
                ("PDQ HD", pdq_vals, "d"),
                ("pHash HD ✨", phash_vals, "d"),
                ("SIFT Matches", sift_vals, "d"),
                ("Composite Score", score_vals, ".3f")
            ]:
                s = stats(vals)
                if 'd' in fmt:
                    f.write(f"| {name} | {s['mean']:.2f} | {s['median']:.2f} | {int(s['min'])} | {int(s['max'])} | {s['std']:.2f} |\n")
                else:
                    f.write(f"| {name} | {s['mean']:{fmt}} | {s['median']:{fmt}} | {s['min']:{fmt}} | {s['max']:{fmt}} | {s['std']:{fmt}} |\n")

            f.write("\n### Dropped vs Kept\n\n")
            f.write("| Category | Count | Percentage |\n")
            f.write("|----------|-------|------------|\n")
            f.write(f"| **Dropped (Duplicates)** | {n_dropped} | {(n_dropped/len(comparisons)*100):.1f}% |\n")
            f.write(f"| **Kept (Unique)** | {len(comparisons)-n_dropped+1} | {((len(comparisons)-n_dropped+1)/len(comparisons)*100):.1f}% |\n\n")

        # Dropped images
        if dropped_images:
            f.write(f"## Dropped Images ({len(dropped_images)})\n\n")
            f.write("These images were identified as duplicates and removed:\n\n")

            for img_path in dropped_images:
                img_name = Path(img_path).name
                thumb_name = f"{folder_name}_{Path(img_path).stem}_thumb.jpg"
                thumb_path = thumb_dir / thumb_name

                # Generate thumbnail
                generate_thumbnail(img_path, str(thumb_path))

                f.write(f"### {img_name}\n\n")
                f.write(f"![{img_name}](thumbnails/{thumb_name})\n\n")
                f.write(f"**Path:** `{img_path}`\n\n")

        # Kept images
        kept_images = [g[0] for g in groups_after]
        if kept_images:
            f.write(f"## Kept Images ({len(kept_images)})\n\n")
            f.write("These images were kept as unique:\n\n")

            for img_path in kept_images:
                img_name = Path(img_path).name
                thumb_name = f"{folder_name}_{Path(img_path).stem}_thumb.jpg"
                thumb_path = thumb_dir / thumb_name

                # Generate thumbnail
                generate_thumbnail(img_path, str(thumb_path))

                f.write(f"### {img_name}\n\n")
                f.write(f"![{img_name}](thumbnails/{thumb_name})\n\n")
                f.write(f"**Path:** `{img_path}`\n\n")

    logger.info(f"Report generated: {report_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Near-duplicate image remover with pHash")
    parser.add_argument("--folders", nargs="+", default=None,
                        help="Folder names/numbers to process (e.g., 1 2 3 4)")
    parser.add_argument("--per-folder", action="store_true",
                        help="Process each folder separately and generate individual reports")
    parser.add_argument("--output-dir", type=str, default=".",
                        help="Directory to save reports and thumbnails")
    parser.add_argument("--log-experiment", type=str, default=None,
                        help="Name for this experiment")
    parser.add_argument("--log-file", type=str, default="experiment_phash_logs.md",
                        help="File to log experiment results to")
    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.folders and args.per_folder:
        # Process each folder separately
        for folder_name in args.folders:
            # Try multiple path options
            possible_paths = [
                Path(folder_name),
                Path(folder_name) / "processed",
            ]

            folder_path = None
            groups = []

            # Find the first path that has images
            for path in possible_paths:
                if path.exists():
                    image_files = sorted(path.glob("*.jpg")) + sorted(path.glob("*.png"))
                    if image_files:
                        folder_path = path
                        for img in image_files:
                            groups.append([str(img)])
                        break

            if not folder_path or not groups:
                logger.warning(f"No images found in {folder_name} or {folder_name}/processed, skipping...")
                continue

            logger.info(f"\n{'='*60}")
            logger.info(f"Processing folder: {folder_name}")
            logger.info(f"Path: {folder_path}")
            logger.info(f"{'='*60}\n")

            logger.info(f"Found {len(groups)} images in {folder_name}")

            # Track comparisons and dropped images
            groups_before = groups.copy()

            # Enable experiment logger to track comparisons
            _experiment_logger = ExperimentLogger()
            _experiment_logger.start_capture()
            _experiment_logger.input_count = len(groups)

            # Run deduplication
            logger.info(f"Running deduplication on {folder_name}...")
            filtered = remove_near_duplicates(groups, deduplication_flag=1, full_scan=False)

            _experiment_logger.output_count = len(filtered)
            _experiment_logger.stop_capture()

            # Identify dropped images
            before_paths = {g[0] for g in groups_before}
            after_paths = {g[0] for g in filtered}
            dropped_image_paths = list(before_paths - after_paths)

            logger.info(f"Results: {len(groups_before)} → {len(filtered)} ({len(dropped_image_paths)} removed)")

            # Generate report with comparison data
            generate_folder_report(
                folder_name=folder_name,
                output_dir=str(output_dir),
                groups_before=groups_before,
                groups_after=filtered,
                comparisons=_experiment_logger.comparison_results,
                dropped_images=dropped_image_paths
            )

            # Clear metric store for next folder
            _metric_store.clear()
            _pair_sim.cache_clear()
            _load_gray.cache_clear()

    else:
        # Original behavior - single run
        # Test folders
        folders = [
            "photos-706-winchester-blvd--los-gatos--ca-9",
            "photos-75-knollview-way--san-francisco--ca"
        ]
        groups = []
        for folder in folders:
            if Path(folder).exists():
                folder_images = sorted(Path(folder).glob("*.jpg"))
                for img in folder_images:
                    groups.append([str(img)])

        # Fallback: Hardcoded paths
        if not groups:
            groups = [
                [r"combined\008_Nancy Peppin - IMG_0009.jpg"],
                [r"combined\009_Nancy Peppin - IMG_0003.jpg"],
                [r"combined\050_Scott Wall - DSC_0098.jpg"],
                [r"combined\053_Scott Wall - DSC_0143.jpg"],
            ]

        # Setup experiment logging if requested
        if args.log_experiment:
            _experiment_logger = ExperimentLogger()
            _experiment_logger.start_capture()
            _experiment_logger.input_count = len(groups)

        logger.info(f"Number of groups before deduplication: {len(groups)}")
        logger.info(f"Using 6 metrics: MTB + SSIM + CLIP + PDQ + pHash ✨ + SIFT")
        logger.info(f"Using full_scan=False: Only comparing adjacent images (sequential pairs)")
        filtered = remove_near_duplicates(groups, deduplication_flag=1, full_scan=False)
        logger.info(f"Number of groups after deduplication: {len(filtered)}")

        # Write experiment log if requested
        if args.log_experiment and _experiment_logger:
            _experiment_logger.output_count = len(filtered)
            terminal_output = _experiment_logger.stop_capture()
            _experiment_logger.write_experiment_log(args.log_experiment, terminal_output, args.log_file)
