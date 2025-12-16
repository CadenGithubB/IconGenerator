# Icon System Troubleshooting

## Common Issues

### Icons Not Displaying on OLED

**Symptom:** `drawIcon()` returns false, no icon appears

**Causes & Solutions:**

1. **Icon not embedded**
   ```cpp
   // Check if icon exists
   if (!iconExists("myicon")) {
       Serial.println("Icon not found!");
   }
   ```
   - Solution: Update `icons/iconsheet.json` and re-run `icons/scripts/generate_icons.py`
   - Verify icon name matches (case-sensitive)

2. **Display pointer null**
   ```cpp
   // Ensure display is initialized
   if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
       Serial.println("Display init failed");
   }
   ```

3. **Wrong coordinates**
   ```cpp
   // Icons are 32x32, check bounds
   // For 128x64 display: x <= 112, y <= 48
   drawIcon(&display, "folder", 0, 0, WHITE);  // OK
   drawIcon(&display, "folder", 120, 0, WHITE); // Clipped!
   ```

---

### Icons Not Showing on Web

**Symptom:** Broken image icon in browser

**Causes & Solutions:**

1. **Icon endpoint not registered**
   - Check web_server.cpp has:
   ```cpp
   static httpd_uri_t iconGet = { 
       .uri = "/api/icon", 
       .method = HTTP_GET, 
       .handler = handleIconGet, 
       .user_ctx = NULL 
   };
   httpd_register_uri_handler(server, &iconGet);
   ```

2. **Wrong URL format**
   ```html
   <!-- Wrong -->
   <img src="/api/icon/folder">
   
   <!-- Correct -->
   <img src="/api/icon?name=folder">
   ```

3. **Icon name mismatch**
   - Check browser console (F12)
   - Verify icon name in `icons_embedded.cpp`

---

**Error:** `'findEmbeddedIcon' was not declared`

**Solution:** Include icons_embedded.h
```cpp
#include "icons_embedded.h"
```

---

**Error:** `multiple definition of 'EMBEDDED_ICONS'`

**Solution:** Ensure icons_embedded.cpp is only compiled once
- Check it's not included in multiple places
- Should be in project root, not in subdirectories

---

### Conversion Script Issues

**Error:** `ModuleNotFoundError: No module named 'PIL'`

**Solution:** Install Pillow
```bash
pip3 install Pillow
```

---

**Error:** `Permission denied: generate_icons.py`

**Solution:** Make executable
```bash
chmod +x generate_icons.py
```

---

**Warning:** `Image not 32x32, resizing...`

**Solution:** Resize before conversion for best quality
```bash
convert input.png -resize 32x32 output.png
```

---

### Memory Issues

**Symptom:** Heap fragmentation, crashes

**Check:**
```cpp
Serial.printf("Free heap: %u\n", ESP.getFreeHeap());
```

**Causes:**
- Icons use PROGMEM (flash), not heap
- Check for other memory leaks

**Solution:**
- Use embedded icons (zero heap)

---

### Performance Issues

**Symptom:** Slow icon rendering

**Benchmarks:**
- Embedded icon: ~1ms

**Solution:**
- Ensure icons are embedded (check `iconExists()` returns true immediately)

---

### Icon Quality Issues

**Symptom:** Icons look pixelated or blurry on OLED

**Causes:**
1. Source image low quality
2. Threshold too high/low
3. Not designed for 32x32

**Solutions:**
1. Design icons specifically for 32x32
2. Use high contrast
3. Test at actual size before converting
4. Adjust threshold in conversion script

---

### Web Caching Issues

**Symptom:** Old icon still showing after update

**Solution:** Clear browser cache or force refresh
```
Chrome/Firefox: Ctrl+Shift+R (Cmd+Shift+R on Mac)
```

Or update cache headers in web_server.cpp:
```cpp
httpd_resp_set_hdr(req, "Cache-Control", "no-cache");
```

---

## Debug Checklist

### OLED Icons
- [ ] Display initialized successfully
- [ ] Icon exists (`iconExists()` returns true)
- [ ] Coordinates within display bounds
- [ ] `display.display()` called after drawing
- [ ] Correct color (WHITE/BLACK)

### Web Icons
- [ ] Icon endpoint registered in web_server.cpp
- [ ] Correct URL format (`/api/icon?name=...`)
- [ ] Icon name matches embedded name
- [ ] Browser console shows no 404 errors
- [ ] Cache cleared if testing updates

### Conversion
- [ ] Pillow installed (`pip3 install Pillow`)
- [ ] PNG files are 32x32 (or will be resized)
- [ ] Script has execute permissions
- [ ] Output file `icons_embedded.cpp` generated
- [ ] Icon names valid (lowercase, no spaces)

---

## Getting Help

If issues persist:

1. **Check serial output** for debug messages
   ```cpp
   Serial.begin(115200);
   // Look for [Icons] messages
   ```

2. **Verify icon registry**
   ```cpp
   extern const size_t EMBEDDED_ICONS_COUNT;
   Serial.printf("Embedded icons: %d\n", EMBEDDED_ICONS_COUNT);
   ```

3. **Test with known-good icon**
   ```cpp
   // folder and file should always work
   if (!drawIcon(&display, "folder", 0, 0, WHITE)) {
       Serial.println("Basic icon failed!");
   }
   ```

4. **Check flash usage**
   ```
   Arduino IDE: Sketch → Verify/Compile
   Look for: "Sketch uses X bytes (Y%) of program storage space"
   ```
