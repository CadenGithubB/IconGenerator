# Icon System Documentation

## Do This (Step-by-step)

1. Edit `icons/assets/iconsheet.png` (32x32 tiles, 1px spacing).
2. Add/update entries in `icons/iconsheet.json` (name + row/col).
3. Run `python3 icons/scripts/generate_icons.py` (regenerates `icons_embedded.cpp`).
4. Build + flash firmware.
5. Verify:
   - `http://<device-ip>/icons/test`
   - `http://<device-ip>/api/icon?name=folder`

## Overview
Unified PNG-based icon system that works across OLED display, web interface, and future TFT displays.

**Key Features:**
- Icons embedded in flash (PROGMEM) at compile time
- Zero heap allocation for embedded icons
- Automatic fallback to text labels if icons unavailable
- No LittleFS dependency for core icons

## Icon Format
- **Size**: 32x32 pixels (native)
- **Format**: PNG (any color depth)
- **Storage**: Embedded in flash as PROGMEM byte arrays
- **Web Display**: Served directly as PNG (32x32)

## Storage Requirements
- ~200-500 bytes PNG data per icon (for web)
- 128 bytes monochrome bitmap per icon (for OLED)
- ~250-550 bytes total per icon in flash
- 20 icons ≈ 5-11KB total flash usage
- **Zero heap usage** - all data in PROGMEM

## Usage

### OLED Display
```cpp
#include "system_utils.h"

// Draw embedded icon on OLED (zero heap, instant)
drawIcon(&display, "folder", 0, 0, WHITE);
drawIcon(&display, "file", 16, 0, WHITE);
```

### Web Interface
Icons are automatically served from embedded PROGMEM via `/api/icon` endpoint:
```html
<!-- Embedded icon (32x32) -->
<img src="/api/icon?name=folder" width="32" height="32" 
     style="image-rendering: pixelated;">
```

The file explorer automatically uses icons with text fallback.

### Custom Rendering
```cpp
uint8_t buffer[128];  // 32x32 monochrome = 128 bytes
uint8_t width, height;

// Loads from embedded PROGMEM
if (loadIconData("folder", buffer, sizeof(buffer), width, height)) {
    // Use buffer for custom rendering
}
```

## Adding Icons to Firmware

### Step 1: Add 32x32 Icons to the Sprite Sheet

**Recommended Tools:**
- **Figma** - Design at 32x32, export as PNG
- **GIMP** - Create/edit 32x32 PNG images
- **ImageMagick** - Batch convert existing icons

**ImageMagick Conversion:**
```bash
# Convert any image to 32x32 PNG
convert input.png -resize 32x32 -background white -alpha remove output.png

# Batch convert from SVG
for f in *.svg; do
    convert "$f" -resize 32x32 -background white -alpha remove "${f%.svg}.png"
done
```

**Icon Sources (Free/Open):**
- **Feather Icons** (MIT) - https://feathericons.com/
- **Lucide** (ISC) - https://lucide.dev/
- **Heroicons** (MIT) - https://heroicons.com/

### Step 2: Generate Embedded Icons (Recommended)
 
Maintain just two files:
 - `icons/assets/iconsheet.png` (sprite sheet)
 - `icons/iconsheet.json` (manifest mapping icon names to tile positions)
 
Then generate:
```bash
python3 icons/scripts/generate_icons.py
 
# Output: icons_embedded.cpp (auto-generated in project root)
```

### Step 3: Compile and Flash

Icons are now embedded in firmware. No LittleFS upload needed!

## Example Icon Set
Recommended starter icons:
- `folder.png` - Directory/folder
- `file.png` - Generic file
- `settings.png` - Settings/configuration
- `wifi.png` - WiFi/network status
- `sensor.png` - Sensor data
- `warning.png` - Warning/alert
- `check.png` - Success/checkmark
- `cross.png` - Error/cancel
- `info.png` - Information
- `home.png` - Home/dashboard

## Performance
- **OLED**: direct bitmap draw (no PNG decode in firmware)
- **Web**: Instant (direct PNG serving)
- **Memory**: zero heap for embedded icons
- **Flash**: PNG + bitmap + registry

## Future Enhancements
- Caching decoded bitmaps for faster OLED rendering
- RGB565 support for color TFT displays
- Icon sprite sheets for web optimization
- Multiple size variants (8x8, 24x24, 32x32)
