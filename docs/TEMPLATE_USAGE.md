# Icon Template Usage Guide

## Overview

The icon template system allows you to draw multiple 32x32 icons on a single 512x512px canvas, then automatically extract them into individual PNG files.

## Template Files

Template files are available in `assets/templates/`:

1. **`icon_template.png`** - Grid template with visual guides
2. **`icon_template_blank.png`** - Blank white canvas

## Grid Layout

### Specifications
- **Canvas:** 512x512 pixels
- **Icon size:** 32x32 pixels
- **Spacing:** 1 pixel between icons
- **Grid:** 15x15 = **225 icon slots**

### Icon Positions
Icons are positioned at:
- **First row:** (0,0), (33,0), (66,0), (99,0)...
- **First column:** (0,0), (0,33), (0,66), (0,99)...
- **Pattern:** Each icon starts at `(col*33, row*33)`

### Visual Layout
```
┌─────────────────────────────────────┐
│ [32x32] 1px [32x32] 1px [32x32] ... │ Row 1
│                                     │
│ 1px gap                             │
│                                     │
│ [32x32] 1px [32x32] 1px [32x32] ... │ Row 2
│                                     │
│ ...                                 │
└─────────────────────────────────────┘
```

## Workflow

### Step 1: Generate Template

```bash
# Scripts live in icons/scripts
cd icons

# With grid guides (recommended)
python3 scripts/icon_template_generator.py --tile-size 32 --spacing 1 -o assets/templates/icon_template.png

# Blank canvas
python3 scripts/icon_template_generator.py --blank -o assets/templates/icon_template_blank.png
```

### Step 2: Draw Icons

1. Open `icon_template.png` in your pixel art editor:
   - [Piskel](https://www.piskelapp.com/) (web-based)
   - [Aseprite](https://www.aseprite.org/)
   - [GIMP](https://www.gimp.org/)
   - [Photoshop](https://www.adobe.com/products/photoshop.html)

2. Draw your icons in the 32x32 grid squares

3. Save the file when done

### Step 3: Extract Icons

```bash
# Extract all non-blank icons
python3 icons/scripts/extract_icons.py icons/assets/iconsheet.png --output icons/.generated/extracted_icons --prefix icon

# Custom output directory
python3 icons/scripts/extract_icons.py icons/assets/iconsheet.png --output icons/.generated/my_icons --prefix icon
```

Output:
```
extracted_icons/
├── icon_001.png
├── icon_002.png
├── icon_003.png
└── ...
```

### Step 4: Convert to PROGMEM

```bash
# Recommended: use the manifest-driven generator (no per-icon files needed)
python3 icons/scripts/generate_icons.py
```

## Tips & Tricks

### Pixel Art Editors

**Web-Based (Free):**
- [Piskel](https://www.piskelapp.com/) - Simple, great for beginners
- [Pixilart](https://www.pixilart.com/) - Social features
- [Lospec Pixel Editor](https://lospec.com/pixel-editor/) - Clean interface

**Desktop (Free):**
- [GIMP](https://www.gimp.org/) - Full-featured
- [Krita](https://krita.org/) - Artist-focused
- [Paint.NET](https://www.getpaint.net/) - Windows only

**Desktop (Paid):**
- [Aseprite](https://www.aseprite.org/) - Best for pixel art ($20)
- [Photoshop](https://www.adobe.com/products/photoshop.html) - Industry standard

### Drawing Guidelines

1. **Use the grid** - Each 32x32 square is one icon
2. **High contrast** - Works better on OLED displays
3. **Simple shapes** - 32x32 is small, avoid fine details
4. **Test at actual size** - Zoom out to see how it looks
5. **Leave 1px spacing** - Don't draw in the gaps

### Naming Icons

After extraction, rename icons to meaningful names:
```bash
cd extracted_icons
mv icon_001.png folder.png
mv icon_002.png file.png
mv icon_003.png wifi.png
```

Then convert:
```bash
cd ../..
python3 icons/scripts/generate_icons.py
```

### Batch Processing

Create multiple icon sets:
```bash
# UI icons
python3 icons/scripts/icon_template_generator.py --tile-size 32 --spacing 1 -o ui_template.png
# ... draw UI icons ...
python3 icons/scripts/extract_icons.py ui_template.png -o ui_icons -p ui

# Sensor icons
python3 icons/scripts/icon_template_generator.py --tile-size 32 --spacing 1 -o sensor_template.png
# ... draw sensor icons ...
python3 icons/scripts/extract_icons.py sensor_template.png -o sensor_icons -p sensor

# Convert all
cd ../..
python3 icons/scripts/generate_icons.py
```

## Examples

### Example 1: Basic Icon Set

1. Generate template:
   ```bash
   python3 icons/scripts/icon_template_generator.py --tile-size 32 --spacing 1
   ```

2. Open `icon_template.png` in Piskel

3. Draw icons:
   - Position (0,0): Folder icon
   - Position (33,0): File icon
   - Position (66,0): WiFi icon
   - Position (99,0): Settings icon

4. Save and extract:
   ```bash
   python3 icons/scripts/extract_icons.py icon_template.png
   ```

5. Rename:
   ```bash
   cd extracted_icons
   mv icon_001.png folder.png
   mv icon_002.png file.png
   mv icon_003.png wifi.png
   mv icon_004.png settings.png
   ```

6. Convert:
   ```bash
   cd ../../..
   python3 icons/scripts/generate_icons.py
   ```

### Example 2: Icon Library

Create a full library of 50+ icons:

1. Plan your icon set (sketch on paper)
2. Generate template
3. Draw all icons in one session
4. Extract and rename in batches
5. Convert to PROGMEM

## Troubleshooting

### Icons Not Extracting

**Problem:** `extract_icons.py` skips all icons

**Solution:** Ensure icons aren't pure white (RGB 255,255,255)
- Add at least one black or colored pixel
- Check that you saved the file after drawing

### Grid Misalignment

**Problem:** Icons don't align with grid in editor

**Solution:** 
- Ensure editor is set to 1:1 zoom (100%)
- Check that canvas is exactly 512x512px
- Some editors may have pixel grid settings

### Icons Look Wrong

**Problem:** Extracted icons are corrupted or wrong size

**Solution:**
- Verify template is 512x512px
- Check that you didn't resize the canvas
- Ensure 1px spacing is maintained

## Advanced: Custom Grid

Edit `icon_template_generator.py` to customize:

```python
# Change icon size
icon_size = 32  # For 32x32 icons

# Change spacing
spacing = 1  # For 1px gaps

# Change canvas size
img = Image.new('RGB', (1024, 1024), 'white')  # Larger canvas
```

Then update `extract_icons.py` with matching values.

## Reference

### Command Reference

```bash
# Generate templates
python3 icons/scripts/icon_template_generator.py              # With grid
python3 icons/scripts/icon_template_generator.py --blank      # Blank canvas
python3 icons/scripts/icon_template_generator.py -o custom.png # Custom filename

# Extract icons
python3 icons/scripts/extract_icons.py template.png           # Default extraction
python3 icons/scripts/extract_icons.py template.png -o dir    # Custom output dir
python3 icons/scripts/extract_icons.py template.png -p name   # Custom prefix

# Convert to PROGMEM
python3 icons/scripts/generate_icons.py           # All icons
```

### Grid Math

- **Icons per row:** `512 / 33 = 15`
- **Total slots:** `15 × 15 = 225`
- **Icon at (col, row):** `x = col*33, y = row*33`
- **Icon number:** `row * 15 + col + 1`

---

**Next:** See [CONVERSION.md](CONVERSION.md) for sprite-sheet-to-firmware generation details
