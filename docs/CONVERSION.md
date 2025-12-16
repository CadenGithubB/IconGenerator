# Icon Conversion Guide

## Overview

The recommended workflow uses a sprite sheet + manifest to generate embedded icons.

- **Preferred:** `icons/scripts/generate_icons.py` (sprite sheet + manifest -> `icons_embedded.cpp`)
- **Legacy:** `icons/scripts/png_to_progmem.py` (individual PNGs -> `icons_embedded.cpp`)

## Preferred: Sprite Sheet + Manifest

### Inputs
- `icons/assets/iconsheet.png`
- `icons/iconsheet.json`

The sprite-sheet tiles are typically **32x32** (with 1px spacing). During generation:
- **Web PNG output** stays at the source tile size (e.g. 32x32)
- **OLED bitmap output** is **32x32** (1bpp)

### Command
```bash
python3 icons/scripts/generate_icons.py
```

### Output
- `icons_embedded.cpp` (generated in project root)

---

## Legacy: Per-PNG Conversion Script Usage (Not Recommended)

### Basic Usage
```bash
python3 icons/scripts/png_to_progmem.py icon1.png icon2.png icon3.png
```

### Output
Generates `../icons_embedded.cpp` with:
- PNG data arrays (for web serving)
- Monochrome bitmap arrays (for OLED)
- Icon registry
- Lookup function

### Example
```bash
cd icons
python3 png_to_progmem.py folder.png file.png settings.png wifi.png

# Output:
# Generated ../icons_embedded.cpp
# Total icons: 4
# Total flash usage: ~2048 bytes
```

---

## Input Requirements

### Image Specifications
- **Size:** Exactly 32x32 pixels
- **Format:** PNG (any color depth)
- **Naming:** Lowercase, alphanumeric + underscore
  - ✓ Good: `folder.png`, `wifi_signal.png`
  - ✗ Bad: `Folder Icon.png`, `wifi-signal.png`

### Auto-Resizing
If image is not 32x32, script automatically resizes using Lanczos resampling.

---

## Conversion Process

### 1. PNG Data Extraction
- Reads raw PNG file bytes
- Stores in PROGMEM array for web serving
- Preserves original PNG format

### 2. Bitmap Generation
- Converts to grayscale
- Applies threshold (128)
- Packs into 1-bit monochrome bitmap
- 128 bytes per 32x32 icon

### 3. Code Generation
```cpp
// Generated output example
static const uint8_t PROGMEM icon_folder_png[] = {
  0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
  // ... PNG data
};

static const uint8_t PROGMEM icon_folder_bitmap[] = {
  0x00, 0x00, 0xFE, 0x03, 0x02, 0x04, 0xFF, 0x0F,
  // ... bitmap data
};
```

---

## Preparing Icons

### From SVG (Recommended)
```bash
# Single icon
convert icon.svg -resize 32x32 -background white -alpha remove icon.png

# Batch convert
for f in *.svg; do
    convert "$f" -resize 32x32 -background white -alpha remove "${f%.svg}.png"
done
```

### From Existing PNG
```bash
# Resize and optimize
convert large_icon.png -resize 32x32 -background white -alpha remove small_icon.png
```

### From Figma/Sketch
1. Create 32x32 artboard
2. Design icon
3. Export as PNG (1x scale)

---

## Optimization Tips

### Reduce File Size
```bash
# Use pngcrush
pngcrush -brute input.png output.png

# Use optipng
optipng -o7 icon.png

# Use ImageMagick with compression
convert icon.png -quality 95 -define png:compression-level=9 optimized.png
```

### Design Guidelines
- Use simple, clear shapes
- Avoid fine details (32x32 is still small)
- High contrast works best for OLED
- Test at actual size before converting

---

## Troubleshooting

### "Image not 32x32"
Script auto-resizes, but quality may suffer. Resize manually for best results.

### "Module 'PIL' not found"
Install Pillow:
```bash
pip3 install Pillow
```

### "Permission denied"
Make script executable:
```bash
chmod +x png_to_progmem.py
```

### Icons look bad on OLED
- Increase contrast in source image
- Use thicker lines
- Test threshold value (edit script line 28)

---

## Advanced: Custom Threshold

Edit `png_to_progmem.py` to adjust monochrome threshold:

```python
# Line 28 - default threshold
if pixel > 128:  # Change 128 to adjust

# Lower value = more white pixels
# Higher value = more black pixels
```

---

## Batch Processing

### Process entire directory
```bash
cd icons
python3 png_to_progmem.py *.png
```

### Selective processing
```bash
# Only UI icons
python3 png_to_progmem.py ui_*.png

# Only sensor icons
python3 png_to_progmem.py sensor_*.png
```

---

## Output Verification

After conversion, check `icons_embedded.cpp`:

1. **Icon count:** Matches input files
2. **Array sizes:** PNG data + 32 bytes bitmap per icon
3. **Registry:** All icons listed in `EMBEDDED_ICONS[]`
4. **Names:** Match input filenames (without .png)

---

## Integration

After running script:

1. Verify `icons_embedded.cpp` generated
2. Compile Arduino project
3. Flash to device
4. Icons available immediately via:
   - `drawIcon(&display, "folder", 0, 0, WHITE)`
   - `http://device/api/icon?name=folder`
