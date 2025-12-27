#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedupe_mtb_multi.py  – 17 Jul 2025  (weighted-score edition + full logging)
Near-duplicate remover that now uses

    • MTB   (Median-Threshold Bitmaps)
    • SSIM  (thumbnail structural similarity)
    • CLIP  (optional cosine similarity)
    • PDQ   (optional Hamming distance)

All metrics feed a **weighted composite score** so "almost-high-enough"
combinations can still count as duplicates.  
⚠️ Logging restored to original verbosity (pair details, Δ-stats,
'Triggered by', etc.).

------------------------------------------------------------
Dependencies
------------------------------------------------------------
    pip install opencv-python-headless numpy pillow
    pip install scikit-image           # <-- for SSIM
    pip install pdqhash-lite           # <-- optional PDQ
    pip install open_clip_torch torch  # <-- only if you enable CLIP
"""

from __future__ import annotations

import logging
import os
import io
import sys
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
except ImportError:           # PDQ is optional
    pdqhash = None

try:
    from skimage.metrics import structural_similarity as _ssim
except ImportError:
    _ssim = None              # SSIM gate disabled if missing

try:
    from PIL import Image
    _pil_available = True
except ImportError:
    _pil_available = False

USE_CLIP = True               # flip to True if you have open_clip-torch installed
if USE_CLIP:
    try:
        import torch, open_clip
        _clip_model = _clip_pre = _clip_device = None
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
                       ssim: float, clip: float, pdq_hd: int, sift_matches: int,
                       score: float, dropped: bool, drop_reason: str) -> None:
        self.comparison_results.append({
            "img_a": Path(img_a).stem,
            "img_b": Path(img_b).stem,
            "mtb": mtb,
            "edge": edge,
            "ssim": ssim,
            "clip": clip,
            "pdq_hd": pdq_hd,
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
| WEIGHT_SIFT | {WEIGHT_SIFT} |
| COMPOSITE_DUP_THRESHOLD | {COMPOSITE_DUP_THRESHOLD} |
| MTB_HARD_FLOOR | {MTB_HARD_FLOOR} |
| PDQ_HD_CEIL | {PDQ_HD_CEIL} |
| SIFT_MIN_MATCHES | {SIFT_MIN_MATCHES} |

## Results

| Image A | Image B | MTB % | Edge % | SSIM % | CLIP % | PDQ HD | SIFT | SCORE | Dropped? |
|---------|---------|-------|--------|--------|--------|--------|------|-------|----------|
"""
        for r in self.comparison_results:
            dropped_str = f"Yes ({r['drop_reason']})" if r["dropped"] else "No"
            if not r["dropped"] and r["drop_reason"]:
                dropped_str = f"No ({r['drop_reason']})"
            entry += f"| {r['img_a']} | {r['img_b']} | {r['mtb']:.1f} | {r['edge']:.1f} | {r['ssim']:.1f} | {r['clip']:.1f} | {r['pdq_hd']} | {r['sift_matches']} | {r['score']:.2f} | {dropped_str} |\n"
        
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
MTB_HARD_FLOOR = 67.0     # never drop if below this MTB %
PDQ_HD_CEIL    = 115      # HD ≥ this ⇒ totally different



# weighted-score config for REGULAR photos (weights must sum to 1.0)
WEIGHT_MTB  = 0.30
WEIGHT_SSIM = 0.0
WEIGHT_CLIP = 0.30
WEIGHT_PDQ  = 0.30
WEIGHT_SIFT = 0.10
COMPOSITE_DUP_THRESHOLD = 0.4    # 0–1 scale
SIFT_MIN_MATCHES = 50            # Minimum SIFT matches to consider as duplicate


# safety guardrails for AERIAL photos
AERIAL_MTB_HARD_FLOOR = 62.0     # never drop if below this MTB %
AERIAL_PDQ_HD_CEIL    = 130      # HD ≥ this ⇒ totally different

# weighted-score config for AERIAL photos (weights must sum to 1.0)
AERIAL_WEIGHT_MTB  = 0.30
AERIAL_WEIGHT_SSIM = 0.0
AERIAL_WEIGHT_CLIP = 0.30
AERIAL_WEIGHT_PDQ  = 0.30
AERIAL_WEIGHT_SIFT = 0.10
AERIAL_COMPOSITE_DUP_THRESHOLD = 0.32    # 0–1 scale
AERIAL_SIFT_MIN_MATCHES = 50              # Minimum SIFT matches for aerial photos

MAX_WORKERS = 16

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

# ─── CLIP helpers ─────────────────────────────────────────────────────────────
def _safe_clip_embed(path: str) -> Optional[np.ndarray]:
    if not USE_CLIP:
        return None
    global _clip_model, _clip_pre, _clip_device
    try:
        import PIL.Image as Image
        if _clip_model is None:
            _clip_device = "cuda" if torch.cuda.is_available() else "cpu"
            _clip_model, _clip_pre, _ = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="openai", device=_clip_device)
            _clip_model.eval()
        img = Image.open(path).convert("RGB")
        t = _clip_pre(img).unsqueeze(0).to(_clip_device)
        with torch.no_grad():
            emb = _clip_model.encode_image(t).cpu().squeeze()
        return (emb / (emb.norm() + 1e-8)).numpy()
    except Exception:
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
        
        # Create SIFT detector
        sift = cv2.SIFT_create()
        
        # Detect keypoints and descriptors
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        
        if des1 is None or des2 is None or len(des1) < 2 or len(des2) < 2:
            return 0
        
        # FLANN-based matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Match descriptors
        matches = flann.knnMatch(des1, des2, k=2)
        
        # Apply Lowe's ratio test
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
        clip=_safe_clip_embed(path)
    )

_metric_store: Dict[str, Dict[str, Any]] = {}

@lru_cache(maxsize=4096)
def _pair_sim(path_a: str, path_b: str) -> Tuple[float, float, int, float, float, int]:
    """Return (mtb %, edge %, PDQ-HD, SSIM %, CLIP %, SIFT matches)"""
    mA, mB = _metric_store[path_a], _metric_store[path_b]

    # Shapes should now be consistent due to _resize_to_exact_size
    # But keep the safety check just in case
    if mA["mtb"].shape != mB["mtb"].shape:
        logger.warning("MTB shape mismatch: %s vs %s - this shouldn't happen anymore",
                       mA["mtb"].shape, mB["mtb"].shape)
        return 0.0, 0.0, 999, 0.0, 0.0, 0
    if mA["edges"].shape != mB["edges"].shape:
        logger.warning("Edge shape mismatch: %s vs %s - this shouldn't happen anymore",
                       mA["edges"].shape, mB["edges"].shape)
        return 0.0, 0.0, 999, 0.0, 0.0, 0

    mtb  = overlap_percent(mA["mtb"],   mB["mtb"])
    edge = overlap_percent(mA["edges"], mB["edges"])
    hd   = _pdq_hd(mA["pdq"],           mB["pdq"])
    ssim = _compute_ssim(mA["gray_ssim"], mB["gray_ssim"])
    clip = 100.0 * _cosine(mA["clip"],     mB["clip"])
    sift_matches = _compute_sift_matches(path_a, path_b, SIFT_MIN_MATCHES)
    return mtb, edge, hd, ssim, clip, sift_matches

# ─── main deduper ─────────────────────────────────────────────────────────────
def remove_near_duplicates(
    groups: List[List[str]],
    deduplication_flag: int = 0,
    metadata_dict: Dict[str, Dict[str, Any]] = None,
    threshold: float = 0.0,          # kept for API compat (unused)
    full_scan: bool = False
) -> List[List[str]]:
    if deduplication_flag != 1 or len(groups) < 2:
        return groups

    mids = [g[len(g)//2] for g in groups]
    logger.info("[STEP] Pre-computing metrics for %d middles…", len(mids))
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for fut in as_completed(pool.submit(_metric_worker, p) for p in mids):
            m = fut.result()
            _metric_store[m["path"]] = m

    # Use the passed-in metadata_dict instead of extracting new metadata
    if metadata_dict is None:
        logger.warning("No metadata_dict provided, using empty dict for aerial detection")
        metadata_dict = {}

    logger.info("[STEP] Multi-metric dedup (weighted score, full_scan=%s)", full_scan)
    keep = [True] * len(groups)
    stats = {"mtb": [], "edge": [], "hd": [], "ssim": [], "clip": [], "sift": [], "score": []}

    def _log_pair(i: int, j: int, mtb: float, edge: float, hd: int,
                  ssim: float, clip: float, sift_matches: int, score: float, is_aerial_pair: bool):
        weight_type = "AERIAL" if is_aerial_pair else "REGULAR"
        logger.info(
            "  • %s ↔ %s : MTB=%.1f  Edge=%.1f  SSIM=%.1f  CLIP=%.1f  PDQ=%d  SIFT=%d  SCORE=%.2f [%s]",
            Path(mids[i]).stem, Path(mids[j]).stem,
            mtb, edge, ssim, clip, hd, sift_matches, score, weight_type
        )
        logger.info("     Comparing: %s", mids[i])
        logger.info("     With:      %s", mids[j])

    def _drop(idx: int, mtb: float, edge: float, hd: int,
              ssim: float, clip: float, score: float,
              trigger_metrics: List[str], is_aerial_img: bool):
        mean = {k: (np.mean(v) if v else 0.0) for k, v in stats.items()}

        # attempt to pull UUID from any 36-char segment in path
        uuid = next((p for p in Path(mids[idx]).parts
                     if len(p) == 36 and p.count('-') == 4), "unknown")

        weight_type = "AERIAL" if is_aerial_img else "REGULAR"
        logger.info(
            "       → DROPPING stack %s (UUID: %s) [%s]   ΔMTB=%.1f  ΔEdge=%.1f  ΔSSIM=%.1f  "
            "ΔCLIP=%.1f  ΔPDQ_HD=%+.0f  ΔSCORE=%.2f  "
            "(means MTB=%.1f Edge=%.1f SSIM=%.1f CLIP=%.1f PDQ_HD=%.0f SCORE=%.2f)",
            Path(mids[idx]).stem, uuid, weight_type,
            mtb - mean["mtb"], edge - mean["edge"],
            ssim - mean["ssim"], clip - mean["clip"], hd - mean["hd"],
            score - mean["score"],
            mean["mtb"], mean["edge"], mean["ssim"], mean["clip"],
            mean["hd"], mean["score"]
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

        mtb, edge, hd, ssim, clip, sift_matches = _pair_sim(mids[i], mids[j])
        if hd == 999:
            continue  # unusable comparison

        # Check if either image is aerial to determine which weights to use
        is_aerial_i = _is_aerial(mids[i], metadata_dict)
        is_aerial_j = _is_aerial(mids[j], metadata_dict)
        is_aerial_pair = is_aerial_i or is_aerial_j  # Use aerial weights if either is aerial

        # Select appropriate weights and threshold
        if is_aerial_pair:
            w_mtb, w_ssim, w_clip, w_pdq, w_sift = AERIAL_WEIGHT_MTB, AERIAL_WEIGHT_SSIM, AERIAL_WEIGHT_CLIP, AERIAL_WEIGHT_PDQ, AERIAL_WEIGHT_SIFT
            dup_threshold = AERIAL_COMPOSITE_DUP_THRESHOLD
            mtb_floor = AERIAL_MTB_HARD_FLOOR
            pdq_ceil = AERIAL_PDQ_HD_CEIL
            sift_min = AERIAL_SIFT_MIN_MATCHES
        else:
            w_mtb, w_ssim, w_clip, w_pdq, w_sift = WEIGHT_MTB, WEIGHT_SSIM, WEIGHT_CLIP, WEIGHT_PDQ, WEIGHT_SIFT
            dup_threshold = COMPOSITE_DUP_THRESHOLD
            mtb_floor = MTB_HARD_FLOOR
            pdq_ceil = PDQ_HD_CEIL
            sift_min = SIFT_MIN_MATCHES

        # Normalize SIFT matches to 0-1 scale (cap at 100 matches = 1.0)
        sift_score = min(sift_matches / 100.0, 1.0) if sift_matches > 0 else 0.0

        # composite score with selected weights
        score = (
            w_mtb  * (mtb  / 100.0) +
            w_ssim * (ssim / 100.0) +
            w_clip * (clip / 100.0) +
            w_pdq  * (0.0 if hd >= pdq_ceil else 1.0 - hd / pdq_ceil) +
            w_sift * sift_score
        )

        # stats + logging
        for k, v in zip(("mtb", "edge", "hd", "ssim", "clip", "sift", "score"),
                        (mtb, edge, hd, ssim, clip, sift_matches, score)):
            stats[k].append(v)
        _log_pair(i, j, mtb, edge, hd, ssim, clip, sift_matches, score, is_aerial_pair)

        # decision logic
        trigger_metrics = []
        drop_reason = ""
        if score >= dup_threshold:
            trigger_metrics.append(f"SCORE({score:.2f}≥{dup_threshold})")
        
        # SIFT override: If SIFT matches are high and CLIP is high, allow override of MTB floor AND PDQ ceiling
        sift_override = (sift_matches >= sift_min) and (clip >= 85.0)
        
        if mtb < mtb_floor and not sift_override:
            trigger_metrics.append(f"MTB_FLOOR_FAIL({mtb:.1f}<{mtb_floor})")
            drop_reason = f"MTB < {mtb_floor}"
            # Log comparison even if not dropped
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, sift_matches, score,
                    dropped=False, drop_reason=drop_reason
                )
            continue
        if hd >= pdq_ceil and not sift_override:
            trigger_metrics.append(f"PDQ_HD({hd:.0f}≥{pdq_ceil})")
            drop_reason = f"PDQ >= {pdq_ceil}"
            # Log comparison even if not dropped
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, sift_matches, score,
                    dropped=False, drop_reason=drop_reason
                )
            continue

        # Allow duplicate if: (score high AND (MTB floor passed OR SIFT override)) AND (PDQ ceiling passed OR SIFT override)
        dup = (score >= dup_threshold) and ((mtb >= mtb_floor) or sift_override) and ((hd < pdq_ceil) or sift_override)
        
        if sift_override:
            trigger_metrics.append(f"SIFT_OVERRIDE({sift_matches}≥{sift_min}, CLIP={clip:.1f}≥85.0)")

        if dup:
            _drop(i, mtb, edge, hd, ssim, clip, score, trigger_metrics, is_aerial_i)
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, sift_matches, score,
                    dropped=True, drop_reason="duplicate"
                )
        else:
            if _experiment_logger:
                _experiment_logger.add_comparison(
                    mids[i], mids[j], mtb, edge, ssim, clip, hd, sift_matches, score,
                    dropped=False, drop_reason=f"SCORE < {dup_threshold}" if score < dup_threshold else ""
                )

    final_groups = [g for g, k in zip(groups, keep) if k]
    logger.info("[RESULT] stacks: %d → %d", len(groups), len(final_groups))
    return final_groups



if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Near-duplicate image remover")
    parser.add_argument("--log-experiment", type=str, default=None,
                        help="Name for this experiment")
    parser.add_argument("--log-file", type=str, default="experiment_logs.md",
                        help="File to log experiment results to")
    args = parser.parse_args()
    
    # Option 1: Load from a single folder (one group per image)
    # folder = "combined"
    # groups = [[str(img)] for img in Path(folder).glob("*.jpg")]
    
    # Option 2: Load from multiple folders
    # With full_scan=False: Only compares ADJACENT images
    # Images from same folder are grouped together, so they'll be compared
    folders = [
        "photos-706-winchester-blvd--los-gatos--ca-9",
        "photos-75-knollview-way--san-francisco--ca"
    ]
    groups = []
    for folder in folders:
        if Path(folder).exists():
            # Sort images within each folder for consistent ordering
            folder_images = sorted(Path(folder).glob("*.jpg"))
            for img in folder_images:
                groups.append([str(img)])
    
    # Option 3: Use combined folder if you want all images together
    # groups = [[str(img)] for img in Path("combined").glob("*.jpg")]
    
    # Fallback: Hardcoded paths (for testing)
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
    logger.info(f"Using full_scan=False: Only comparing adjacent images (sequential pairs)")
    filtered = remove_near_duplicates(groups, deduplication_flag=1, full_scan=False)
    logger.info(f"Number of groups after deduplication: {len(filtered)}")
    
    # Write experiment log if requested
    if args.log_experiment and _experiment_logger:
        _experiment_logger.output_count = len(filtered)
        terminal_output = _experiment_logger.stop_capture()
        _experiment_logger.write_experiment_log(args.log_experiment, terminal_output, args.log_file)