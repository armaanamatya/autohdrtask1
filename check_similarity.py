#!/usr/bin/env python3
"""Quick script to check CNN similarity between specific images"""

from imagededup.methods import CNN
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Images to compare
folder = 'photos-706-winchester-blvd--los-gatos--ca-9'
images = [
    f'{folder}/008_Nancy Peppin - IMG_0009.jpg',
    f'{folder}/009_Nancy Peppin - IMG_0003.jpg'
]

print("Calculating CNN similarity...\n")

# Initialize CNN
cnn = CNN()

# Generate encodings
encodings = {}
for img_path in images:
    enc = cnn.encode_image(image_file=img_path)
    encodings[img_path] = enc.squeeze()
    print(f"Encoded: {Path(img_path).name}")

# Calculate similarity
enc1 = encodings[images[0]].reshape(1, -1)
enc2 = encodings[images[1]].reshape(1, -1)
similarity = cosine_similarity(enc1, enc2)[0, 0]

print(f"\nSimilarity between:")
print(f"  {Path(images[0]).name}")
print(f"  {Path(images[1]).name}")
print(f"\nCNN Cosine Similarity: {similarity:.6f} ({similarity*100:.2f}%)")
print(f"Threshold: 0.9 (90%)")
print(f"Duplicates? {'YES' if similarity >= 0.9 else 'NO'}")
