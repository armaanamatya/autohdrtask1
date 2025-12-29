#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_weight_combinations.py

Generates all valid weight combinations for 5 metrics (MTB, SSIM, CLIP, PDQ, SIFT)
with 10% increments where weights sum to 1.0.

Total combinations: 1,001 (using stars and bars: C(14, 4))
"""

def generate_weights():
    """
    Generate all weight combinations using nested loops.

    Returns:
        List[dict]: List of 1,001 weight dictionaries with keys:
                    'mtb', 'ssim', 'clip', 'pdq', 'sift'

    Example:
        >>> weights = generate_weights()
        >>> len(weights)
        1001
        >>> weights[0]
        {'mtb': 0.0, 'ssim': 0.0, 'clip': 0.0, 'pdq': 0.0, 'sift': 1.0}
        >>> weights[-1]
        {'mtb': 1.0, 'ssim': 0.0, 'clip': 0.0, 'pdq': 0.0, 'sift': 0.0}
    """
    combinations = []

    # Generate all combinations where:
    # w_mtb + w_ssim + w_clip + w_pdq + w_sift = 1.0
    # Each weight in {0.0, 0.1, 0.2, ..., 1.0}

    for w_mtb in range(0, 11):      # 0.0 to 1.0 in 0.1 steps
        for w_ssim in range(0, 11 - w_mtb):
            for w_clip in range(0, 11 - w_mtb - w_ssim):
                for w_pdq in range(0, 11 - w_mtb - w_ssim - w_clip):
                    w_sift = 10 - w_mtb - w_ssim - w_clip - w_pdq
                    if w_sift >= 0:  # Valid combination
                        combinations.append({
                            'mtb': w_mtb / 10.0,
                            'ssim': w_ssim / 10.0,
                            'clip': w_clip / 10.0,
                            'pdq': w_pdq / 10.0,
                            'sift': w_sift / 10.0
                        })

    return combinations


def validate_weights(weights):
    """
    Validate that all weight combinations sum to 1.0.

    Args:
        weights: List of weight dictionaries

    Returns:
        bool: True if all valid, raises AssertionError otherwise
    """
    for i, w in enumerate(weights):
        total = w['mtb'] + w['ssim'] + w['clip'] + w['pdq'] + w['sift']
        assert abs(total - 1.0) < 1e-9, f"Weights at index {i} sum to {total}, not 1.0: {w}"

    print(f"[OK] All {len(weights)} weight combinations are valid (sum to 1.0)")
    return True


if __name__ == "__main__":
    # Generate and validate
    print("Generating weight combinations...")
    weights = generate_weights()

    print(f"Generated {len(weights)} combinations")
    print(f"\nFirst 5 combinations:")
    for i, w in enumerate(weights[:5]):
        print(f"  {i+1}. MTB={w['mtb']:.1f}, SSIM={w['ssim']:.1f}, CLIP={w['clip']:.1f}, PDQ={w['pdq']:.1f}, SIFT={w['sift']:.1f}")

    print(f"\nLast 5 combinations:")
    for i, w in enumerate(weights[-5:], len(weights)-4):
        print(f"  {i}. MTB={w['mtb']:.1f}, SSIM={w['ssim']:.1f}, CLIP={w['clip']:.1f}, PDQ={w['pdq']:.1f}, SIFT={w['sift']:.1f}")

    # Validate
    print(f"\nValidating...")
    validate_weights(weights)
