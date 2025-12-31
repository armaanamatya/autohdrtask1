#!/usr/bin/env python3
"""Test CLIP CPU fallback and improved error logging"""

import logging
from pathlib import Path

# Setup logging to see all messages
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from deduplication import _safe_clip_embed

# Test on a single image
test_image = r"c:\Users\Armaan\Desktop\autohdrtask1\00a959b5-1b0b-4670-9c07-5df8b7636cfe\processed\DSC00201.jpg"

if Path(test_image).exists():
    print(f"Testing CLIP on: {test_image}")
    print("=" * 70)

    embedding = _safe_clip_embed(test_image)

    print("=" * 70)
    if embedding is not None:
        print(f"SUCCESS: CLIP embedding generated")
        print(f"  Shape: {embedding.shape}")
        print(f"  First 5 values: {embedding[:5]}")
        print(f"\nCLIP is now working on CPU!")
    else:
        print(f"FAILED: CLIP returned None")
else:
    print(f"Test image not found: {test_image}")
