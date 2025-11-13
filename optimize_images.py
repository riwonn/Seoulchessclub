#!/usr/bin/env python3
"""
Image optimization script for Seoul Chess Club
Compresses WebP images to reduce file size while maintaining quality
"""

import os
from pathlib import Path
from PIL import Image

def optimize_webp_image(input_path, output_path, quality=75, max_width=800):
    """
    Optimize a WebP image by:
    1. Resizing if too large
    2. Compressing with specified quality
    3. Converting to progressive loading

    Args:
        input_path: Path to input image
        output_path: Path to save optimized image
        quality: WebP quality (1-100, default 75)
        max_width: Maximum width in pixels (default 800)
    """
    try:
        # Open image
        img = Image.open(input_path)
        original_size = os.path.getsize(input_path)

        print(f"Processing: {input_path.name}")
        print(f"  Original size: {original_size / 1024 / 1024:.2f} MB")
        print(f"  Original dimensions: {img.size}")

        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized to: {img.size}")

        # Save with optimization
        img.save(
            output_path,
            'WEBP',
            quality=quality,
            method=6,  # Slowest but best compression
            lossless=False
        )

        # Check new size
        new_size = os.path.getsize(output_path)
        reduction = ((original_size - new_size) / original_size) * 100

        print(f"  New size: {new_size / 1024 / 1024:.2f} MB")
        print(f"  Reduction: {reduction:.1f}%")
        print()

        return True

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def main():
    """Optimize all hero images"""
    images_dir = Path('/home/user/Seoulchessclub/static/images')

    # Create backup directory
    backup_dir = images_dir / 'original_backups'
    backup_dir.mkdir(exist_ok=True)

    # Find all hero images
    hero_images = sorted(images_dir.glob('hero-*.webp'))

    if not hero_images:
        print("No hero images found!")
        return

    print(f"Found {len(hero_images)} hero images to optimize\n")
    print("=" * 60)

    total_original = 0
    total_new = 0

    for img_path in hero_images:
        # Backup original
        backup_path = backup_dir / img_path.name
        if not backup_path.exists():
            import shutil
            shutil.copy2(img_path, backup_path)
            print(f"Backed up: {img_path.name}")

        # Optimize
        temp_path = img_path.with_suffix('.tmp.webp')
        if optimize_webp_image(img_path, temp_path, quality=80, max_width=800):
            # Get sizes
            original_size = os.path.getsize(img_path)
            new_size = os.path.getsize(temp_path)

            total_original += original_size
            total_new += new_size

            # Replace original with optimized
            os.replace(temp_path, img_path)
        else:
            # Clean up temp file if failed
            if temp_path.exists():
                temp_path.unlink()

    print("=" * 60)
    print("\nOptimization Complete!")
    print(f"Total original size: {total_original / 1024 / 1024:.2f} MB")
    print(f"Total new size: {total_new / 1024 / 1024:.2f} MB")
    print(f"Total reduction: {((total_original - total_new) / total_original) * 100:.1f}%")
    print(f"\nOriginal images backed up to: {backup_dir}")

if __name__ == '__main__':
    main()
