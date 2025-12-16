#!/usr/bin/env python3
""" 
Manifest-driven icon generator.

Inputs:
- icons/iconsheet.json (manifest)
- icons/assets/iconsheet.png (sprite sheet)

Output:
- icons_embedded.cpp (generated in project root)

This avoids managing hundreds of individual icon PNG files.
"""

import io
import json
import os
import sys
from typing import Any, Dict, List, Tuple

from PIL import Image


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


def _load_manifest(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _crop_tile(sheet: Image.Image, x: int, y: int, tile_size: int) -> Image.Image:
    return sheet.crop((x, y, x + tile_size, y + tile_size))


def _png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def _bitmap_1bpp_32x32(img: Image.Image, tile_size: int, threshold: int) -> bytes:
    # OLED output is 32x32. If the source tile isn't 32x32, resize to match.
    if tile_size != 32:
        img = img.resize((32, 32), resample=Image.NEAREST)

    gray = img.convert("L")
    out = bytearray()
    for y in range(32):
        for x0 in range(0, 32, 8):
            b = 0
            for bit in range(8):
                x = x0 + bit
                px = gray.getpixel((x, y))
                if px > threshold:
                    b |= (1 << bit)
            out.append(b)
    _require(len(out) == 128, "Internal error: expected 128-byte bitmap")
    return bytes(out)


def _c_array(name: str, data: bytes, cols: int = 16) -> str:
    lines = []
    lines.append(f"static const uint8_t PROGMEM {name}[] = {{")
    for i in range(0, len(data), cols):
        chunk = data[i : i + cols]
        lines.append("  " + ", ".join(f"0x{b:02X}" for b in chunk) + ",")
    lines.append("};")
    return "\n".join(lines)


def _generate_cpp(icons: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append('#include "icons_embedded.h"')
    lines.append("")
    lines.append("// Auto-generated icon arrays")
    lines.append("// DO NOT EDIT - regenerate with icons/scripts/generate_icons.py")
    lines.append("")

    # Arrays
    for icon in icons:
        name = icon["name"]
        png = icon["png"]
        bmp = icon["bmp"]
        lines.append(f"// {name} PNG data ({len(png)} bytes)")
        lines.append(_c_array(f"icon_{name}_png", png))
        lines.append("")
        lines.append(f"// {name} monochrome bitmap (32x32 = 128 bytes)")
        lines.append(_c_array(f"icon_{name}_bitmap", bmp, cols=8))
        lines.append("")

    # Registry
    lines.append("// Icon registry")
    lines.append("const EmbeddedIcon EMBEDDED_ICONS[] PROGMEM = {")
    for icon in icons:
        name = icon["name"]
        lines.append(f'  {{"{name}", icon_{name}_png, {len(icon["png"])}, icon_{name}_bitmap, 32, 32}},')
    lines.append("};")
    lines.append("")
    lines.append(f"const size_t EMBEDDED_ICONS_COUNT = {len(icons)};")
    lines.append("")

    # Lookup
    lines.append("const EmbeddedIcon* findEmbeddedIcon(const char* name) {")
    lines.append("  for (size_t i = 0; i < EMBEDDED_ICONS_COUNT; i++) {")
    lines.append("    char iconName[32];")
    lines.append("    strcpy_P(iconName, (PGM_P)pgm_read_ptr(&EMBEDDED_ICONS[i].name));")
    lines.append("    if (strcmp(iconName, name) == 0) {")
    lines.append("      return &EMBEDDED_ICONS[i];")
    lines.append("    }")
    lines.append("  }")
    lines.append("  return nullptr;")
    lines.append("}")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    icons_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    manifest_path = os.path.join(icons_root, "iconsheet.json")
    _require(os.path.exists(manifest_path), f"Missing manifest: {manifest_path}")

    manifest = _load_manifest(manifest_path)

    tile_size = int(manifest.get("tileSize", 16))
    spacing = int(manifest.get("spacing", 1))
    threshold = int(manifest.get("threshold", 128))
    sheet_rel = manifest.get("sheet", "assets/iconsheet.png")
    sheet_path = os.path.join(icons_root, sheet_rel)

    _require(os.path.exists(sheet_path), f"Missing sprite sheet image: {sheet_path}")

    icons_list = manifest.get("icons", [])
    _require(isinstance(icons_list, list) and len(icons_list) > 0, "Manifest has no icons[]")

    sheet = Image.open(sheet_path)

    icons_out: List[Dict[str, Any]] = []
    seen = set()

    for item in icons_list:
        _require(isinstance(item, dict), "icons[] entries must be objects")
        name = item.get("name")
        _require(isinstance(name, str) and len(name) > 0, "icons[] entry missing name")
        _require(name.isidentifier(), f"Icon name '{name}' must be a valid C identifier (letters/digits/underscore, not starting with digit)")
        _require(name not in seen, f"Duplicate icon name in manifest: {name}")
        seen.add(name)

        if "x" in item and "y" in item:
            x = int(item["x"])
            y = int(item["y"])
        else:
            row = int(item.get("row", 0))
            col = int(item.get("col", 0))
            step = tile_size + spacing
            x = col * step
            y = row * step

        tile = _crop_tile(sheet, x, y, tile_size)
        _require(tile.size == (tile_size, tile_size), f"Failed to crop tile for {name}")

        png = _png_bytes(tile)
        bmp = _bitmap_1bpp_32x32(tile, tile_size=tile_size, threshold=threshold)

        icons_out.append({"name": name, "png": png, "bmp": bmp})

    cpp = _generate_cpp(icons_out)

    out_cpp_path = os.path.join(repo_root, "icons_embedded.cpp")
    with open(out_cpp_path, "w", encoding="utf-8") as f:
        f.write(cpp)

    total_png = sum(len(i["png"]) for i in icons_out)
    total_bmp = 128 * len(icons_out)

    print(f"Generated: {out_cpp_path}")
    print(f"Icons: {len(icons_out)}")
    print(f"Approx flash usage: png={total_png}B + bmp={total_bmp}B + registry")
    print("")
    print("Next steps:")
    print("  1) Build + flash firmware")
    print("  2) Verify in browser:")
    print("     - http://<device-ip>/icons/test")
    print("     - http://<device-ip>/api/icon?name=folder")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}")
        raise SystemExit(1)
