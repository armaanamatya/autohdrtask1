#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_s3_images.py

Downloads processed images from AWS S3 bucket to local directory structure.
Each folder in S3 bucket is downloaded to images/{id}/processed/
"""

import subprocess
import sys
import shutil
import platform
import json
from pathlib import Path
from typing import List, Optional, Set


def find_aws_cli() -> str:
    """
    Find AWS CLI executable path.
    
    Returns:
        Path to AWS CLI executable
        
    Raises:
        RuntimeError: If AWS CLI is not found
    """
    # Try common AWS CLI names in PATH
    aws_names = ["aws", "aws.cmd"]
    
    for aws_name in aws_names:
        aws_path = shutil.which(aws_name)
        if aws_path:
            return aws_path
    
    # On Windows, check common installation locations
    if platform.system() == "Windows":
        import glob
        
        common_paths = [
            r"C:\Program Files\Amazon\AWSCLIV2\aws.exe",
            r"C:\Program Files (x86)\Amazon\AWSCLIV2\aws.exe",
        ]
        
        # Check Python installation paths (common for pip-installed AWS CLI)
        python_scripts_pattern = str(Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Python*" / "Scripts" / "aws.exe")
        python_matches = glob.glob(python_scripts_pattern)
        common_paths.extend(python_matches)
        
        for path_str in common_paths:
            path = Path(path_str)
            if path.exists():
                return str(path)
    
    raise RuntimeError(
        "AWS CLI not found. Please install AWS CLI:\n"
        "  https://aws.amazon.com/cli/\n"
        "Or ensure 'aws' is in your PATH."
    )


def run_aws_command(command: List[str]) -> tuple[int, str, str]:
    """
    Execute AWS CLI command and return result.
    
    Args:
        command: List of command arguments (first element should be 'aws')
        
    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    # Replace 'aws' with full path if needed
    if command[0] == "aws":
        try:
            aws_path = find_aws_cli()
            command[0] = aws_path
        except RuntimeError as e:
            raise RuntimeError(str(e))
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        raise RuntimeError(
            f"AWS CLI executable not found: {command[0]}\n"
            f"Please install AWS CLI: https://aws.amazon.com/cli/"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to execute AWS command: {e}")


def list_s3_folders(bucket_path: str) -> List[str]:
    """
    List all folder IDs in the S3 bucket.
    
    Args:
        bucket_path: S3 bucket path (e.g., s3://image-upload-autohdr-j/)
        
    Returns:
        List of folder IDs (UUIDs)
    """
    command = [
        "aws", "s3", "ls", bucket_path
    ]
    
    returncode, stdout, stderr = run_aws_command(command)
    
    if returncode != 0:
        error_msg = stderr.strip() if stderr else "Unknown error"
        raise RuntimeError(
            f"Failed to list S3 folders.\n"
            f"Error: {error_msg}\n"
            f"Make sure AWS CLI is installed, configured, and you have access to the bucket."
        )
    
    # Parse output to extract folder names
    # AWS CLI output format: "PRE {folder_name}/"
    folder_ids: List[str] = []
    for line in stdout.strip().split("\n"):
        if line.strip() and "PRE" in line:
            folder_name = line.split()[-1].rstrip("/")
            if folder_name:
                folder_ids.append(folder_name)
    
    return folder_ids


def is_folder_downloaded(folder_id: str, local_base_dir: Path) -> bool:
    """
    Check if a folder has already been downloaded.
    
    Args:
        folder_id: Folder ID (UUID) to check
        local_base_dir: Local base directory (e.g., Path("images"))
        
    Returns:
        True if folder exists and has files, False otherwise
    """
    local_dest = local_base_dir / folder_id / "processed"
    if not local_dest.exists():
        return False
    
    # Check if directory has any files
    try:
        return any(local_dest.iterdir())
    except (OSError, PermissionError):
        return False


def load_progress(progress_file: Path) -> Set[str]:
    """
    Load set of successfully downloaded folder IDs from progress file.
    
    Args:
        progress_file: Path to progress JSON file
        
    Returns:
        Set of folder IDs that have been successfully downloaded
    """
    if not progress_file.exists():
        return set()
    
    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("downloaded", []))
    except (json.JSONDecodeError, IOError):
        return set()


def save_progress(progress_file: Path, downloaded_ids: Set[str]) -> None:
    """
    Save set of successfully downloaded folder IDs to progress file.
    
    Args:
        progress_file: Path to progress JSON file
        downloaded_ids: Set of folder IDs that have been successfully downloaded
    """
    try:
        data = {"downloaded": sorted(list(downloaded_ids))}
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Warning: Failed to save progress: {e}", file=sys.stderr)


def download_folder_images(
    bucket_path: str,
    folder_id: str,
    local_base_dir: Path
) -> bool:
    """
    Download processed images from a specific S3 folder.
    
    Args:
        bucket_path: S3 bucket path (e.g., s3://image-upload-autohdr-j/)
        folder_id: Folder ID (UUID) to download
        local_base_dir: Local base directory (e.g., Path("images"))
        
    Returns:
        True if successful, False otherwise
    """
    s3_source = f"{bucket_path}{folder_id}/processed/"
    local_dest = local_base_dir / folder_id / "processed"
    
    # Create destination directory
    local_dest.mkdir(parents=True, exist_ok=True)
    
    command = [
        "aws", "s3", "cp",
        s3_source,
        str(local_dest) + "/",
        "--recursive"
    ]
    
    print(f"Downloading {folder_id}...")
    print(f"  From: {s3_source}")
    print(f"  To: {local_dest}")
    
    try:
        returncode, stdout, stderr = run_aws_command(command)
    except RuntimeError as e:
        print(f"  ERROR: {e}")
        return False
    
    if returncode != 0:
        error_msg = stderr.strip() if stderr else stdout.strip() or "Unknown error"
        print(f"  ERROR: Failed to download {folder_id}")
        print(f"  {error_msg}")
        return False
    
    print(f"  ✓ Successfully downloaded {folder_id}")
    return True


def download_all_images(
    bucket_path: str,
    local_base_dir: str,
    folder_ids: Optional[List[str]] = None,
    limit: Optional[int] = None,
    progress_file: Optional[str] = None
) -> None:
    """
    Download processed images from S3 bucket.
    
    Args:
        bucket_path: S3 bucket path (e.g., s3://image-upload-autohdr-j/)
        local_base_dir: Local base directory (e.g., "images")
        folder_ids: Optional list of folder IDs to download.
                   If None, lists all folders from S3.
        limit: Optional limit on number of folders to download.
        progress_file: Optional path to progress file for resuming downloads.
    """
    local_path = Path(local_base_dir)
    local_path.mkdir(parents=True, exist_ok=True)
    
    # Get list of folders to download
    if folder_ids is None:
        print("Listing folders in S3 bucket...")
        folder_ids = list_s3_folders(bucket_path)
        print(f"Found {len(folder_ids)} folders in S3 bucket")
    else:
        print(f"Using {len(folder_ids)} specified folders")
    
    if not folder_ids:
        print("No folders found to download.")
        return
    
    # Apply limit if specified
    if limit is not None:
        folder_ids = folder_ids[:limit]
        print(f"Limited to first {len(folder_ids)} folders")
    
    # Load progress if resuming
    downloaded_ids: Set[str] = set()
    if progress_file:
        progress_path = Path(progress_file)
        downloaded_ids = load_progress(progress_path)
        if downloaded_ids:
            print(f"Loaded progress: {len(downloaded_ids)} folders already marked as downloaded")
    
    # Also check local filesystem for already downloaded folders
    print("Checking for already downloaded folders...")
    skipped = 0
    folders_to_download: List[str] = []
    for folder_id in folder_ids:
        if folder_id in downloaded_ids or is_folder_downloaded(folder_id, local_path):
            skipped += 1
            if folder_id not in downloaded_ids:
                downloaded_ids.add(folder_id)
        else:
            folders_to_download.append(folder_id)
    
    if skipped > 0:
        print(f"Skipping {skipped} already downloaded folders")
    
    if not folders_to_download:
        print("All folders have already been downloaded.")
        return
    
    print(f"Downloading {len(folders_to_download)} folders\n")
    
    # Download each folder
    successful = 0
    failed = 0
    
    for folder_id in folders_to_download:
        if download_folder_images(bucket_path, folder_id, local_path):
            successful += 1
            downloaded_ids.add(folder_id)
            # Save progress after each successful download
            if progress_file:
                save_progress(Path(progress_file), downloaded_ids)
        else:
            failed += 1
        print()
    
    # Summary
    print("=" * 60)
    print(f"Download complete:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Skipped (already downloaded): {skipped}")
    print(f"  Total processed: {len(folders_to_download)}")
    print("=" * 60)


def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download processed images from AWS S3 bucket"
    )
    parser.add_argument(
        "--bucket",
        type=str,
        default="s3://image-upload-autohdr-j/",
        help="S3 bucket path (default: s3://image-upload-autohdr-j/)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="images",
        help="Local output directory (default: images)"
    )
    parser.add_argument(
        "--folder-ids",
        type=str,
        nargs="+",
        default=None,
        help="Optional: Specific folder IDs to download (space-separated). "
             "If not provided, downloads all folders."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of folders to download (e.g., --limit 100)"
    )
    parser.add_argument(
        "--progress-file",
        type=str,
        default="download_progress.json",
        help="Path to progress file for resuming downloads (default: download_progress.json)"
    )
    
    args = parser.parse_args()
    
    try:
        download_all_images(
            bucket_path=args.bucket,
            local_base_dir=args.output_dir,
            folder_ids=args.folder_ids,
            limit=args.limit,
            progress_file=args.progress_file
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

