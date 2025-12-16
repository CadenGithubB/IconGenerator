#!/usr/bin/env python3
"""
Icon Extractor
Extracts individual 32x32 icons from a sprite sheet template
"""

from PIL import Image
import os
import sys

def extract_icons(template_path, output_dir="extracted_icons", prefix="icon", tile_size=32, spacing=1):
    """
    Extract icons from template sprite sheet
    
    Args:
        template_path: Path to template PNG
        output_dir: Directory to save extracted icons
        prefix: Prefix for icon filenames (e.g., "icon_01.png")
        tile_size: Size of each icon tile in pixels (default: 32)
        spacing: Spacing between tiles in pixels (default: 1)
    """
    
    if not os.path.exists(template_path):
        print(f"Error: Template not found: {template_path}")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load template
    img = Image.open(template_path)
    
    # Calculate grid dimensions (start at 0)
    icons_per_row = img.size[0] // (tile_size + spacing)
    icons_per_col = img.size[1] // (tile_size + spacing)
    
    print(f"Extracting icons from: {template_path}")
    print(f"Icon size: {tile_size}x{tile_size}px")
    print(f"Grid: {icons_per_row}x{icons_per_col}")
    
    extracted_count = 0
    skipped_count = 0
    
    # Extract each icon
    for row in range(icons_per_col):
        for col in range(icons_per_row):
            # Calculate icon position (0-based grid)
            x = col * (tile_size + spacing)
            y = row * (tile_size + spacing)
            
            # Extract icon region
            icon = img.crop((x, y, x + tile_size, y + tile_size))
            
            # Check if icon is blank (all white or transparent)
            if is_blank(icon):
                skipped_count += 1
                continue
            
            # Save icon
            icon_num = row * icons_per_row + col + 1
            filename = f"{prefix}_{icon_num:03d}.png"
            filepath = os.path.join(output_dir, filename)
            icon.save(filepath)
            
            extracted_count += 1
            print(f"Extracted: {filename} (position {col},{row})")
    
    print(f"Extraction complete!")
    print(f"Extracted: {extracted_count} icons")
    print(f"Skipped (blank): {skipped_count} icons")
    print(f"Output directory: {output_dir}")
    
    if extracted_count > 0:
        print("\nNext steps:")
        print("  1) If you want embedded icons, update icons/iconsheet.json (names + row/col)")
        print("  2) Generate icons_embedded.cpp:")
        print("     python3 icons/scripts/generate_icons.py")
        print("  3) Build + flash firmware")
        print("  4) Verify:")
        print("     - http://<device-ip>/icons/test")
        print("     - http://<device-ip>/api/icon?name=folder")

def is_blank(icon):
    """Check if icon is blank (all white or transparent)"""
    # Convert to RGB if needed
    if icon.mode == 'RGBA':
        # Check if all pixels are transparent or white
        pixels = list(icon.getdata())
        for pixel in pixels:
            r, g, b, a = pixel
            if a > 0 and (r < 250 or g < 250 or b < 250):
                return False
        return True
    else:
        # Check if all pixels are white
        pixels = list(icon.getdata())
        for pixel in pixels:
            if isinstance(pixel, tuple):
                r, g, b = pixel[:3]
                if r < 250 or g < 250 or b < 250:
                    return False
            else:
                if pixel < 250:
                    return False
        return True

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract icons from template')
    parser.add_argument('template', help='Path to template PNG')
    parser.add_argument('--output', '-o', default='extracted_icons', help='Output directory')
    parser.add_argument('--prefix', '-p', default='icon', help='Icon filename prefix')
    parser.add_argument('--tile-size', type=int, default=32, help='Icon tile size in pixels (default: 32)')
    parser.add_argument('--spacing', type=int, default=1, help='Spacing between tiles in pixels (default: 1)')
    
    args = parser.parse_args()
    
    extract_icons(args.template, args.output, args.prefix, tile_size=args.tile_size, spacing=args.spacing)
