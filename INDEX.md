# Icon System Documentation Index

Complete documentation for the embedded PROGMEM icon system.

## 📚 Documentation

### Getting Started
- **[README.md](README.md)** - Complete system overview and features
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - 5-minute setup guide

### Reference
- **[docs/API.md](docs/API.md)** - Complete API reference for all functions
- **[docs/CONVERSION.md](docs/CONVERSION.md)** - PNG to PROGMEM conversion guide
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🛠️ Tools

- **[scripts/generate_icons.py](scripts/generate_icons.py)** - Generate `icons_embedded.cpp` from `assets/iconsheet.png` + `iconsheet.json`
  ```bash
  python3 icons/scripts/generate_icons.py
  ```
 
- **[scripts/png_to_progmem.py](scripts/png_to_progmem.py)** - Convert individual PNG icons to PROGMEM (legacy/one-off)
  ```bash
  python3 icons/scripts/png_to_progmem.py folder.png file.png
  ```

## 📋 Examples

### Arduino/C++
- **[examples/example_usage.ino](examples/example_usage.ino)** - Complete Arduino examples
  - Basic icon drawing
  - Icon grids and layouts
  - Icons with text
  - Conditional display with fallback
  - Custom rendering
  - Status bars and menus
  - Buttons with icons
  - Status bars
  - JavaScript integration
  - CSS styling

### Web/HTML
- **[examples/web_integration.html](examples/web_integration.html)** - Web integration examples
  - Basic icon display
  - File browser UI
  - Buttons with icons
  - Status bars
  - JavaScript integration
  - CSS styling

### Shell Scripts
- **[scripts/create_icons.sh](scripts/create_icons.sh)** - ImageMagick icon generation

## 🎯 Quick Reference

### OLED Usage
```cpp
#include "system_utils.h"

drawIcon(&display, "folder", 0, 0, WHITE);
```

### Web Usage
```html
<img src="/api/icon?name=folder" width="20" height="20">
```

### Convert Icons
```bash
python3 icons/scripts/generate_icons.py
```

## 📁 Folder Structure

```
icons/
├── INDEX.md                    # This file
├── README.md                   # Main documentation
├── iconsheet.json              # Manifest: icon names -> tile positions
├── scripts/                    # Runnable scripts (this is the "sub-program")
│   ├── generate_icons.py       # Primary workflow (sheet + manifest -> icons_embedded.cpp)
│   ├── png_to_progmem.py       # Legacy: per-PNG conversion
│   ├── icon_template_generator.py
│   ├── extract_icons.py
│   └── create_icons.sh
├── assets/                     # Inputs (things you edit)
│   ├── iconsheet.png           # Sprite sheet (512x512 grid)
│   └── templates/              # Template PNGs for pixel editors
│
├── docs/                       # Detailed documentation
│   ├── QUICKSTART.md          # Quick setup guide
│   ├── API.md                 # API reference
│   ├── CONVERSION.md          # Conversion guide
│   ├── TEMPLATE_USAGE.md      # Sprite sheet template workflow
│   └── TROUBLESHOOTING.md     # Problem solving
│
└── examples/                   # Usage examples
    ├── example_usage.ino      # Arduino examples
    ├── web_integration.html   # Web examples
```

## 🔑 Key Features

✓ **Zero Heap Usage** - All icons in PROGMEM flash  
✓ **Instant Rendering** - ~1ms on OLED  
✓ **Automatic Fallback** - Text labels if icons unavailable  
✓ **Web Integration** - Served via `/api/icon` endpoint  
✓ **Small Footprint** - ~250-550 bytes per icon  

## 🚀 Workflow

1. **Edit** `icons/assets/iconsheet.png`
2. **Map** tile positions in `icons/iconsheet.json`
3. **Generate** with `python3 icons/scripts/generate_icons.py`
3. **Compile** and flash firmware
4. **Use** in OLED and web interfaces

## 📖 Documentation Topics

| Topic | File | Description |
|-------|------|-------------|
| Overview | README.md | System features and architecture |
| Quick Start | docs/QUICKSTART.md | 5-minute setup |
| API Reference | docs/API.md | All functions and parameters |
| Conversion | docs/CONVERSION.md | PNG to PROGMEM process |
| Troubleshooting | docs/TROUBLESHOOTING.md | Common issues |
| Arduino Examples | examples/example_usage.ino | OLED usage patterns |
| Web Examples | examples/web_integration.html | Browser integration |
| Icon Creation | scripts/create_icons.sh | Generate icons |

## 💡 Common Tasks

### Add New Icon
```bash
# 1. Draw into icons/assets/iconsheet.png
# 2. Add entry to icons/iconsheet.json
# 3. Generate embedded icons
python3 icons/scripts/generate_icons.py
# 4. Compile and flash
```

### Use Icon on OLED
```cpp
drawIcon(&display, "myicon", x, y, WHITE);
```

### Use Icon on Web
```html
<img src="/api/icon?name=myicon" width="20" height="20">
```

### Check Icon Exists
```cpp
if (iconExists("myicon")) {
    // Icon available
}
```

## 🔧 Requirements

- **Python:** 3.x with Pillow (for conversion)
- **Tools:** ImageMagick (optional, for icon creation)

## 📊 Memory Usage

| Component | Flash | Heap |
|-----------|-------|------|
| Icon system code | ~2KB | 0 bytes |
| Per icon (PNG + bitmap) | ~250-550 bytes | 0 bytes |
| 20 icons total | ~5-11KB | 0 bytes |

## 🎨 Icon Sources

Free/open-source icon libraries:
- [Feather Icons](https://feathericons.com/) (MIT)
- [Lucide](https://lucide.dev/) (ISC)
- [Heroicons](https://heroicons.com/) (MIT)

## 📝 Notes

- Icons embedded at compile time (no LittleFS needed)
- Automatic text fallback for missing icons
- Web icons cached for 24 hours
- OLED icons rendered directly from flash
- Zero runtime memory allocation

---

**For questions or issues, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**
