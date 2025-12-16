# Icon System Quick Start Guide

## 5-Minute Setup

### 1. Get Icons

Use 32x32 PNG icons from:
- [Feather Icons](https://feathericons.com/) (MIT)
- [Lucide](https://lucide.dev/) (ISC)
- Or create your own in any image editor

### 2. Add Icons to the Sprite Sheet

- Edit: `icons/assets/iconsheet.png` (32x32 tiles, 1px spacing)
- Update: `icons/iconsheet.json` (name + row/col)

### 3. Generate Embedded Icons
  
  ```bash
 # 1) Edit: icons/assets/iconsheet.png
 # 2) Update: icons/iconsheet.json
 # 3) Generate: icons_embedded.cpp
 python3 icons/scripts/generate_icons.py
  ```

### 4. Compile & Flash

That's it! Icons are now embedded in your firmware.

## Usage Examples

### OLED Display
```cpp
#include "system_utils.h"

void setup() {
    // Icons work immediately, no initialization needed
    drawIcon(&display, "folder", 0, 0, WHITE);
}
```

### Web Interface
Icons automatically appear in the file explorer. Access via:
```
http://your-device/files
```

Test icons directly:
```
http://your-device/icons/test
http://your-device/api/icon?name=folder
```

## What You Get

✓ Zero heap usage (all in flash)  
✓ Instant rendering on OLED  
✓ Automatic web serving  
✓ Text fallback if icons unavailable  
✓ ~250-550 bytes per icon  

## Next Steps

- Read `README.md` for full documentation
- Check `examples/` for sample icons
- See `docs/API.md` for advanced usage
