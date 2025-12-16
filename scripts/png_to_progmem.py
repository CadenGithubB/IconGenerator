#!/usr/bin/env python3
"""
PNG to PROGMEM Converter
Converts 16x16 PNG icons to Arduino PROGMEM byte arrays for embedded icons.
Generates both PNG data (for web) and monochrome bitmap (for OLED).

NOTE: This script is legacy/one-off. Preferred workflow is:
  icons/assets/iconsheet.png + icons/iconsheet.json -> icons/scripts/generate_icons.py
"""

import sys
import os
from PIL import Image
import io

def png_to_progmem(png_path, icon_name):
    """Convert PNG to PROGMEM arrays"""
    
    # Read PNG file
    with open(png_path, 'rb') as f:
        png_data = f.read()
    
    # Open image for bitmap conversion
    img = Image.open(png_path)
    
    if img.size != (16, 16):
        print(f"Warning: {png_path} is {img.size}, expected 16x16. Resizing...")
        img = img.resize((16, 16), Image.Resampling.LANCZOS)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Convert to 1-bit monochrome bitmap
    bitmap = []
    for y in range(16):
        for x in range(0, 16, 8):
            byte = 0
            for bit in range(8):
                if x + bit < 16:
                    pixel = img.getpixel((x + bit, y))
                    if pixel > 128:  # Threshold
                        byte |= (1 << bit)
            bitmap.append(byte)
    
    # Generate C code
    output = []
    
    # PNG data array
    output.append(f"// {icon_name} PNG data ({len(png_data)} bytes)")
    output.append(f"static const uint8_t PROGMEM icon_{icon_name}_png[] = {{")
    
    for i in range(0, len(png_data), 16):
        chunk = png_data[i:i+16]
        hex_str = ', '.join(f'0x{b:02X}' for b in chunk)
        output.append(f"  {hex_str},")
    
    output.append("};")
    output.append("")
    
    # Bitmap array
    output.append(f"// {icon_name} monochrome bitmap (16x16 = 32 bytes)")
    output.append(f"static const uint8_t PROGMEM icon_{icon_name}_bitmap[] = {{")
    
    for i in range(0, len(bitmap), 8):
        chunk = bitmap[i:i+8]
        hex_str = ', '.join(f'0x{b:02X}' for b in chunk)
        output.append(f"  {hex_str},")
    
    output.append("};")
    output.append("")
    
    return '\n'.join(output), len(png_data)

def generate_icon_registry(icons):
    """Generate the icon registry array"""
    output = []
    
    output.append("// Icon registry")
    output.append("const EmbeddedIcon EMBEDDED_ICONS[] PROGMEM = {")
    
    for name, size in icons:
        output.append(f'  {{"{name}", icon_{name}_png, {size}, icon_{name}_bitmap, 16, 16}},')
    
    output.append("};")
    output.append("")
    output.append(f"const size_t EMBEDDED_ICONS_COUNT = {len(icons)};")
    
    return '\n'.join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python png_to_progmem.py <icon1.png> [icon2.png ...]")
        print("Example: python png_to_progmem.py folder.png file.png")
        print("")
        print("Preferred workflow:")
        print("  1) Edit icons/assets/iconsheet.png")
        print("  2) Update icons/iconsheet.json")
        print("  3) Run: python3 icons/scripts/generate_icons.py")
        sys.exit(1)
    
    icons = []
    arrays = []
    
    for png_path in sys.argv[1:]:
        if not os.path.exists(png_path):
            print(f"Error: {png_path} not found")
            continue
        
        icon_name = os.path.splitext(os.path.basename(png_path))[0]
        print(f"Converting {png_path} -> {icon_name}")
        
        array_code, png_size = png_to_progmem(png_path, icon_name)
        arrays.append(array_code)
        icons.append((icon_name, png_size))
    
    # Generate complete output
    output = []
    output.append("#include \"icons_embedded.h\"")
    output.append("")
    output.append("// Auto-generated icon arrays")
    output.append("// DO NOT EDIT - regenerate with tools/png_to_progmem.py")
    output.append("")
    
    output.extend(arrays)
    output.append(generate_icon_registry(icons))
    
    output.append("")
    output.append("const EmbeddedIcon* findEmbeddedIcon(const char* name) {")
    output.append("  for (size_t i = 0; i < EMBEDDED_ICONS_COUNT; i++) {")
    output.append("    char iconName[32];")
    output.append("    strcpy_P(iconName, (PGM_P)pgm_read_ptr(&EMBEDDED_ICONS[i].name));")
    output.append("    if (strcmp(iconName, name) == 0) {")
    output.append("      return &EMBEDDED_ICONS[i];")
    output.append("    }")
    output.append("  }")
    output.append("  return nullptr;")
    output.append("}")
    
    # Write to icons_embedded.cpp (project root)
    # This script lives in icons/scripts/, so we go two levels up
    output_path = "../../icons_embedded.cpp"
    with open(output_path, 'w') as f:
        f.write('\n'.join(output))
    
    print(f"\nGenerated {output_path}")
    print(f"Total icons: {len(icons)}")
    print(f"Total flash usage: ~{sum(size for _, size in icons) + len(icons) * 32} bytes")
    print("")
    print("Next steps:")
    print("  1) Build + flash firmware")
    print("  2) Verify:")
    print("     - http://<device-ip>/icons/test")
    print("     - http://<device-ip>/api/icon?name=folder")

if __name__ == '__main__':
    main()
