import fiftyone as fo
import os

# Define the directory containing images
image_dir = r"c:\Users\Armaan\Desktop\autohdrtask1\000fc774-cb56-4052-a33a-9974c58a00d6\processed"

# Create a dataset
dataset_name = "processed_images"

# Delete existing dataset if it exists
if dataset_name in fo.list_datasets():
    fo.delete_dataset(dataset_name)

# Create a new dataset from the directory
dataset = fo.Dataset.from_dir(
    dataset_dir=image_dir,
    dataset_type=fo.types.ImageDirectory,
    name=dataset_name
)

print(f"Created dataset '{dataset_name}' with {len(dataset)} samples")
print(f"Dataset info:\n{dataset}")

# Launch the FiftyOne App
session = fo.launch_app(dataset)

# Keep the session open
session.wait()
