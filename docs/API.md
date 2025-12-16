# Icon System API Reference

## Core Functions

### `bool initIconSystem()`
Initialize icon system (optional).

**Returns:** `true` if successful

**Example:**
```cpp
void setup() {
    initIconSystem();  // Optional
}
```

---

### `bool drawIcon(Adafruit_SSD1306* display, const char* name, int x, int y, uint16_t color = WHITE)`
Draw icon on OLED display.

**Parameters:**
- `display` - Pointer to Adafruit_SSD1306 display object
- `name` - Icon name (without .png extension)
- `x`, `y` - Screen coordinates
- `color` - Pixel color (default: WHITE)

**Returns:** `true` if icon found and drawn

**Memory:** Zero heap allocation (reads from PROGMEM)

**Example:**
```cpp
drawIcon(&display, "folder", 0, 0, WHITE);
drawIcon(&display, "file", 16, 0, WHITE);
drawIcon(&display, "wifi_3", 32, 0, WHITE);
```

---

### `bool loadIconData(const char* name, uint8_t* buffer, size_t bufferSize, uint8_t& width, uint8_t& height)`
Load raw icon bitmap data for custom rendering.

**Parameters:**
- `name` - Icon name
- `buffer` - Output buffer (minimum 128 bytes)
- `bufferSize` - Size of buffer
- `width` - Output: icon width (32)
- `height` - Output: icon height (32)

**Returns:** `true` if icon loaded

**Example:**
```cpp
uint8_t buffer[128];
uint8_t width, height;

if (loadIconData("folder", buffer, sizeof(buffer), width, height)) {
    // Custom rendering with buffer
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            // Process bitmap data
        }
    }
}
```

---

### `bool iconExists(const char* name)`
Check if icon is available (embedded).

**Parameters:**
- `name` - Icon name

**Returns:** `true` if icon exists

**Example:**
```cpp
if (iconExists("folder")) {
    drawIcon(&display, "folder", 0, 0, WHITE);
} else {
    display.print("[DIR]");
}
```

---

## Web API

### `GET /api/icon?name={iconName}`
Serve embedded icon as PNG.

**Parameters:**
- `name` - Icon name (without .png extension)

**Response:**
- Content-Type: `image/png`
- Cache-Control: `public, max-age=86400`
- Status: 200 (success), 404 (not found)

**Example:**
```html
<img src="/api/icon?name=folder" width="20" height="20">
<img src="/api/icon?name=file" width="20" height="20">
```

---

## Embedded Icon Structure

### `EmbeddedIcon`
```cpp
struct EmbeddedIcon {
    const char* name;           // Icon name
    const uint8_t* pngData;     // PNG file data (PROGMEM)
    size_t pngSize;             // PNG size in bytes
    const uint8_t* bitmapData;  // Monochrome bitmap (PROGMEM)
    uint8_t width;              // Icon width (32)
    uint8_t height;             // Icon height (32)
};
```

### `const EmbeddedIcon* findEmbeddedIcon(const char* name)`
Find embedded icon by name (internal use).

**Parameters:**
- `name` - Icon name

**Returns:** Pointer to EmbeddedIcon or `nullptr`

---

## Bitmap Format

Icons are stored as 1-bit monochrome bitmaps:
- **Size:** 32x32 pixels = 128 bytes
- **Format:** LSB first, row-major
- **Layout:** 8 pixels per byte, 4 bytes per row
- **Compatible with:** Adafruit_GFX `drawBitmap()`

**Byte Layout:**
```
Byte 0-3:   Row 0 (pixels 0-31)
Byte 4-7:   Row 1 (pixels 0-31)
...
Byte 124-127: Row 31 (pixels 0-31)
```

---

## Performance

| Operation | Time | Heap Usage |
|-----------|------|------------|
| `drawIcon()` | ~1ms | 0 bytes |
| `loadIconData()` | ~0.5ms | 0 bytes |
| `iconExists()` | ~0.1ms | 0 bytes |
| Web serve | ~5ms | 256 bytes (temp buffer) |

---

## Error Handling

All functions return `false` on failure:
- Icon not found
- Invalid buffer size
- Display pointer null

**Best Practice:**
```cpp
if (!drawIcon(&display, "folder", 0, 0, WHITE)) {
    // Fallback to text
    display.print("[DIR]");
}
```
