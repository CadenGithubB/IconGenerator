#!/usr/bin/env python3

import os
from typing import Callable, Dict, Tuple

from PIL import Image, ImageDraw


TILE_SIZE = 32
SPACING = 1
GRID = 15
CANVAS_SIZE = 512
STEP = TILE_SIZE + SPACING
INK = (255, 255, 255, 255)


def _tile_xy(row: int, col: int) -> Tuple[int, int]:
    return col * STEP, row * STEP


def _draw_centered_text_fallback(draw: ImageDraw.ImageDraw, bbox: Tuple[int, int, int, int], text: str) -> None:
    # Intentionally minimal; not used by default.
    (x0, y0, x1, y1) = bbox
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.text((cx, cy), text, fill=INK, anchor="mm")


def _stroke(draw: ImageDraw.ImageDraw, pts, w: int = 2) -> None:
    draw.line(pts, fill=INK, width=w, joint="curve")


def _rect_outline(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, w: int = 2) -> None:
    draw.rectangle((x0, y0, x1, y1), outline=INK, width=w)


def _circle_outline(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, w: int = 2) -> None:
    draw.ellipse((x0, y0, x1, y1), outline=INK, width=w)


def icon_smiley(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _circle_outline(draw, x + 4, y + 4, x + 27, y + 27, w=2)
    draw.ellipse((x + 10, y + 12, x + 13, y + 15), fill=INK)
    draw.ellipse((x + 19, y + 12, x + 22, y + 15), fill=INK)
    draw.arc((x + 10, y + 13, x + 22, y + 25), start=20, end=160, fill=INK, width=2)


def icon_frowny(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _circle_outline(draw, x + 4, y + 4, x + 27, y + 27, w=2)
    draw.ellipse((x + 10, y + 12, x + 13, y + 15), fill=INK)
    draw.ellipse((x + 19, y + 12, x + 22, y + 15), fill=INK)
    draw.arc((x + 10, y + 18, x + 22, y + 30), start=200, end=340, fill=INK, width=2)


def icon_folder(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Folder outline
    _rect_outline(draw, x + 5, y + 11, x + 27, y + 25, w=2)
    _stroke(draw, [(x + 5, y + 11), (x + 12, y + 11), (x + 14, y + 8), (x + 27, y + 8)], w=2)


def icon_file(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 8, y + 6, x + 24, y + 26, w=2)
    _stroke(draw, [(x + 18, y + 6), (x + 24, y + 12)], w=2)
    _stroke(draw, [(x + 18, y + 6), (x + 18, y + 12), (x + 24, y + 12)], w=2)


def _wifi(draw: ImageDraw.ImageDraw, x: int, y: int, bars: int) -> None:
    # bars: 0..3
    # Dot
    if bars >= 0:
        draw.ellipse((x + 15, y + 22, x + 17, y + 24), fill=INK)
    # Arcs
    if bars >= 1:
        draw.arc((x + 11, y + 16, x + 21, y + 26), start=200, end=340, fill=INK, width=2)
    if bars >= 2:
        draw.arc((x + 8, y + 13, x + 24, y + 29), start=200, end=340, fill=INK, width=2)
    if bars >= 3:
        draw.arc((x + 5, y + 10, x + 27, y + 32), start=200, end=340, fill=INK, width=2)


def icon_wifi_0(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _wifi(draw, x, y, 0)


def icon_wifi_1(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _wifi(draw, x, y, 1)


def icon_wifi_2(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _wifi(draw, x, y, 2)


def icon_wifi_3(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _wifi(draw, x, y, 3)


def _arrow(draw: ImageDraw.ImageDraw, x: int, y: int, direction: str) -> None:
    # Simple outline arrow, 2px stroke.
    if direction == "left":
        _stroke(draw, [(x + 23, y + 16), (x + 9, y + 16)], w=2)
        _stroke(draw, [(x + 13, y + 11), (x + 9, y + 16), (x + 13, y + 21)], w=2)
    elif direction == "right":
        _stroke(draw, [(x + 9, y + 16), (x + 23, y + 16)], w=2)
        _stroke(draw, [(x + 19, y + 11), (x + 23, y + 16), (x + 19, y + 21)], w=2)
    elif direction == "up":
        _stroke(draw, [(x + 16, y + 23), (x + 16, y + 9)], w=2)
        _stroke(draw, [(x + 11, y + 13), (x + 16, y + 9), (x + 21, y + 13)], w=2)
    elif direction == "down":
        _stroke(draw, [(x + 16, y + 9), (x + 16, y + 23)], w=2)
        _stroke(draw, [(x + 11, y + 19), (x + 16, y + 23), (x + 21, y + 19)], w=2)


def icon_arrow_left(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _arrow(draw, x, y, "left")


def icon_arrow_right(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _arrow(draw, x, y, "right")


def icon_arrow_up(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _arrow(draw, x, y, "up")


def icon_arrow_down(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _arrow(draw, x, y, "down")


def icon_chevron_left(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 20, y + 10), (x + 12, y + 16), (x + 20, y + 22)], w=3)


def icon_chevron_right(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 12, y + 10), (x + 20, y + 16), (x + 12, y + 22)], w=3)


def _battery(draw: ImageDraw.ImageDraw, x: int, y: int, level: int) -> None:
    # level: 0,25,50,75,100
    body = (x + 6, y + 10, x + 25, y + 22)
    _rect_outline(draw, *body, w=2)
    # nub
    _rect_outline(draw, x + 25, y + 13, x + 28, y + 19, w=2)

    inner_x0 = x + 8
    inner_y0 = y + 12
    inner_x1 = x + 23
    inner_y1 = y + 20

    if level <= 0:
        return

    frac = max(0, min(100, level)) / 100.0
    fill_w = int((inner_x1 - inner_x0) * frac)
    if fill_w <= 0:
        return
    draw.rectangle((inner_x0, inner_y0, inner_x0 + fill_w, inner_y1), fill=INK)


def icon_battery_0(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _battery(draw, x, y, 0)


def icon_battery_25(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _battery(draw, x, y, 25)


def icon_battery_50(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _battery(draw, x, y, 50)


def icon_battery_75(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _battery(draw, x, y, 75)


def icon_battery_100(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _battery(draw, x, y, 100)


def icon_battery_charging(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _battery(draw, x, y, 50)
    # lightning bolt
    draw.polygon(
        [
            (x + 16, y + 11),
            (x + 13, y + 17),
            (x + 17, y + 17),
            (x + 14, y + 23),
            (x + 20, y + 15),
            (x + 16, y + 15),
        ],
        fill=None,
        outline=INK,
    )


def icon_plus(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 16, y + 10), (x + 16, y + 22)], w=3)
    _stroke(draw, [(x + 10, y + 16), (x + 22, y + 16)], w=3)


def icon_minus(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 10, y + 16), (x + 22, y + 16)], w=3)


def icon_check(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 10, y + 17), (x + 14, y + 21), (x + 23, y + 11)], w=3)


def icon_close(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 11, y + 11), (x + 21, y + 21)], w=3)
    _stroke(draw, [(x + 21, y + 11), (x + 11, y + 21)], w=3)


def icon_menu(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _stroke(draw, [(x + 9, y + 12), (x + 23, y + 12)], w=3)
    _stroke(draw, [(x + 9, y + 16), (x + 23, y + 16)], w=3)
    _stroke(draw, [(x + 9, y + 20), (x + 23, y + 20)], w=3)


def icon_search(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _circle_outline(draw, x + 9, y + 9, x + 20, y + 20, w=2)
    _stroke(draw, [(x + 19, y + 19), (x + 24, y + 24)], w=3)


def icon_info(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _circle_outline(draw, x + 6, y + 6, x + 26, y + 26, w=2)
    draw.ellipse((x + 15, y + 11, x + 17, y + 13), fill=INK)
    _stroke(draw, [(x + 16, y + 15), (x + 16, y + 22)], w=3)


def icon_warning(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.polygon([(x + 16, y + 7), (x + 26, y + 25), (x + 6, y + 25)], outline=INK, fill=None)
    _stroke(draw, [(x + 16, y + 12), (x + 16, y + 19)], w=3)
    draw.ellipse((x + 15, y + 21, x + 17, y + 23), fill=INK)


def icon_settings(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Simple gear-ish shape
    cx, cy = x + 16, y + 16
    _circle_outline(draw, x + 11, y + 11, x + 21, y + 21, w=2)
    for dx, dy in [(0, -9), (0, 9), (-9, 0), (9, 0), (-6, -6), (6, -6), (-6, 6), (6, 6)]:
        _stroke(draw, [(cx + dx, cy + dy), (cx + int(dx * 0.7), cy + int(dy * 0.7))], w=3)


def icon_refresh(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.arc((x + 7, y + 7, x + 25, y + 25), start=40, end=310, fill=INK, width=2)
    draw.polygon([(x + 22, y + 10), (x + 26, y + 10), (x + 24, y + 6)], fill=INK)


def icon_wifi_off(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _wifi(draw, x, y, 2)
    _stroke(draw, [(x + 9, y + 9), (x + 23, y + 23)], w=3)


def icon_sdcard(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # SD card outline with top chamfer
    draw.polygon(
        [(x + 10, y + 6), (x + 22, y + 6), (x + 26, y + 11), (x + 26, y + 26), (x + 10, y + 26)],
        outline=INK,
        fill=None,
    )
    _stroke(draw, [(x + 12, y + 10), (x + 12, y + 14)], w=2)
    _stroke(draw, [(x + 15, y + 10), (x + 15, y + 14)], w=2)
    _stroke(draw, [(x + 18, y + 10), (x + 18, y + 14)], w=2)


def icon_trash(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 11, y + 11, x + 21, y + 26, w=2)
    _stroke(draw, [(x + 9, y + 11), (x + 23, y + 11)], w=2)
    _stroke(draw, [(x + 13, y + 8), (x + 19, y + 8)], w=2)
    _stroke(draw, [(x + 12, y + 8), (x + 12, y + 11)], w=2)
    _stroke(draw, [(x + 20, y + 8), (x + 20, y + 11)], w=2)
    _stroke(draw, [(x + 14, y + 14), (x + 14, y + 23)], w=1)
    _stroke(draw, [(x + 16, y + 14), (x + 16, y + 23)], w=1)
    _stroke(draw, [(x + 18, y + 14), (x + 18, y + 23)], w=1)


def icon_upload(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 9, y + 19, x + 23, y + 25, w=2)
    _stroke(draw, [(x + 16, y + 22), (x + 16, y + 10)], w=2)
    _stroke(draw, [(x + 12, y + 14), (x + 16, y + 10), (x + 20, y + 14)], w=2)


def icon_download(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 9, y + 19, x + 23, y + 25, w=2)
    _stroke(draw, [(x + 16, y + 10), (x + 16, y + 22)], w=2)
    _stroke(draw, [(x + 12, y + 18), (x + 16, y + 22), (x + 20, y + 18)], w=2)


def icon_edit(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Pencil
    draw.polygon([(x + 10, y + 22), (x + 12, y + 24), (x + 22, y + 14), (x + 20, y + 12)], outline=INK, fill=None)
    _stroke(draw, [(x + 19, y + 11), (x + 23, y + 15)], w=2)
    _stroke(draw, [(x + 10, y + 25), (x + 14, y + 25)], w=2)


def icon_save(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Floppy-ish
    _rect_outline(draw, x + 9, y + 8, x + 23, y + 26, w=2)
    _rect_outline(draw, x + 12, y + 9, x + 20, y + 13, w=2)
    _rect_outline(draw, x + 12, y + 18, x + 20, y + 25, w=2)


def icon_home(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.polygon([(x + 8, y + 17), (x + 16, y + 9), (x + 24, y + 17)], outline=INK, fill=None)
    _rect_outline(draw, x + 11, y + 17, x + 21, y + 26, w=2)
    _rect_outline(draw, x + 14, y + 21, x + 18, y + 26, w=2)


def icon_back(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Back arrow with a stem
    _stroke(draw, [(x + 22, y + 16), (x + 11, y + 16)], w=3)
    _stroke(draw, [(x + 15, y + 11), (x + 11, y + 16), (x + 15, y + 21)], w=3)
    _stroke(draw, [(x + 22, y + 10), (x + 22, y + 22)], w=2)


def icon_lock(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 11, y + 16, x + 21, y + 26, w=2)
    draw.arc((x + 12, y + 8, x + 20, y + 18), start=200, end=340, fill=INK, width=2)
    draw.ellipse((x + 15, y + 20, x + 17, y + 22), fill=INK)


def icon_unlock(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 11, y + 16, x + 21, y + 26, w=2)
    draw.arc((x + 10, y + 8, x + 18, y + 18), start=200, end=340, fill=INK, width=2)
    _stroke(draw, [(x + 18, y + 12), (x + 21, y + 12)], w=2)
    draw.ellipse((x + 15, y + 20, x + 17, y + 22), fill=INK)


def _file_base(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _rect_outline(draw, x + 8, y + 6, x + 24, y + 26, w=2)
    _stroke(draw, [(x + 18, y + 6), (x + 24, y + 12)], w=2)
    _stroke(draw, [(x + 18, y + 6), (x + 18, y + 12), (x + 24, y + 12)], w=2)


def icon_file_text(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _stroke(draw, [(x + 11, y + 15), (x + 21, y + 15)], w=2)
    _stroke(draw, [(x + 11, y + 19), (x + 21, y + 19)], w=2)
    _stroke(draw, [(x + 11, y + 23), (x + 18, y + 23)], w=2)


def icon_file_code(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _stroke(draw, [(x + 12, y + 19), (x + 15, y + 16), (x + 12, y + 13)], w=2)
    _stroke(draw, [(x + 20, y + 13), (x + 17, y + 16), (x + 20, y + 19)], w=2)


def icon_file_image(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _rect_outline(draw, x + 11, y + 14, x + 21, y + 24, w=2)
    draw.polygon([(x + 12, y + 23), (x + 15, y + 20), (x + 17, y + 22), (x + 20, y + 18), (x + 21, y + 23)], outline=INK, fill=None)
    draw.ellipse((x + 18, y + 16, x + 20, y + 18), fill=INK)


def icon_file_zip(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _stroke(draw, [(x + 16, y + 13), (x + 16, y + 24)], w=2)
    draw.ellipse((x + 15, y + 15, x + 17, y + 17), fill=INK)
    draw.ellipse((x + 15, y + 19, x + 17, y + 21), fill=INK)
    draw.ellipse((x + 15, y + 23, x + 17, y + 25), fill=INK)


def icon_file_json(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _stroke(draw, [(x + 13, y + 14), (x + 11, y + 16), (x + 13, y + 18)], w=2)
    _stroke(draw, [(x + 19, y + 14), (x + 21, y + 16), (x + 19, y + 18)], w=2)
    _stroke(draw, [(x + 16, y + 19), (x + 16, y + 23)], w=2)


def icon_file_pdf(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _stroke(draw, [(x + 11, y + 16), (x + 11, y + 23)], w=2)
    _stroke(draw, [(x + 11, y + 16), (x + 17, y + 16)], w=2)
    _stroke(draw, [(x + 17, y + 16), (x + 17, y + 19)], w=2)
    _stroke(draw, [(x + 11, y + 19), (x + 17, y + 19)], w=2)


def icon_file_bin(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    _file_base(draw, x, y)
    _stroke(draw, [(x + 11, y + 16), (x + 21, y + 16)], w=2)
    _stroke(draw, [(x + 11, y + 20), (x + 21, y + 20)], w=2)
    _stroke(draw, [(x + 11, y + 24), (x + 21, y + 24)], w=2)


ICON_LAYOUT = [
    # row 0
    ("smiley", 0, 0),
    ("frowny", 0, 1),
    ("folder", 0, 2),
    ("file", 0, 3),
    ("wifi_0", 0, 4),
    ("wifi_1", 0, 5),
    ("wifi_2", 0, 6),
    ("wifi_3", 0, 7),
    ("arrow_left", 0, 8),
    ("arrow_right", 0, 9),
    ("arrow_up", 0, 10),
    ("arrow_down", 0, 11),
    ("chevron_left", 0, 12),
    ("chevron_right", 0, 13),
    ("battery_0", 0, 14),
    # row 1
    ("battery_25", 1, 0),
    ("battery_50", 1, 1),
    ("battery_75", 1, 2),
    ("battery_100", 1, 3),
    ("battery_charging", 1, 4),
    ("plus", 1, 5),
    ("minus", 1, 6),
    ("check", 1, 7),
    ("close", 1, 8),
    ("menu", 1, 9),
    ("search", 1, 10),
    ("info", 1, 11),
    ("warning", 1, 12),
    ("settings", 1, 13),
    ("refresh", 1, 14),
    # row 2
    ("wifi_off", 2, 0),
    ("sdcard", 2, 1),
    ("trash", 2, 2),
    ("upload", 2, 3),
    ("download", 2, 4),
    ("edit", 2, 5),
    ("save", 2, 6),
    ("home", 2, 7),
    ("back", 2, 8),
    ("lock", 2, 9),
    ("unlock", 2, 10),
    # row 3
    ("file_text", 3, 0),
    ("file_code", 3, 1),
    ("file_image", 3, 2),
    ("file_zip", 3, 3),
    ("file_json", 3, 4),
    ("file_pdf", 3, 5),
    ("file_bin", 3, 6),
]


def main() -> int:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_path = os.path.join(root, "assets", "iconsheet.png")

    img = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    icon_fns: Dict[str, Callable[[ImageDraw.ImageDraw, int, int], None]] = {
        "smiley": icon_smiley,
        "frowny": icon_frowny,
        "folder": icon_folder,
        "file": icon_file,
        "wifi_0": icon_wifi_0,
        "wifi_1": icon_wifi_1,
        "wifi_2": icon_wifi_2,
        "wifi_3": icon_wifi_3,
        "wifi_off": icon_wifi_off,
        "arrow_left": icon_arrow_left,
        "arrow_right": icon_arrow_right,
        "arrow_up": icon_arrow_up,
        "arrow_down": icon_arrow_down,
        "chevron_left": icon_chevron_left,
        "chevron_right": icon_chevron_right,
        "battery_0": icon_battery_0,
        "battery_25": icon_battery_25,
        "battery_50": icon_battery_50,
        "battery_75": icon_battery_75,
        "battery_100": icon_battery_100,
        "battery_charging": icon_battery_charging,
        "plus": icon_plus,
        "minus": icon_minus,
        "check": icon_check,
        "close": icon_close,
        "menu": icon_menu,
        "search": icon_search,
        "info": icon_info,
        "warning": icon_warning,
        "settings": icon_settings,
        "refresh": icon_refresh,
        "sdcard": icon_sdcard,
        "trash": icon_trash,
        "upload": icon_upload,
        "download": icon_download,
        "edit": icon_edit,
        "save": icon_save,
        "home": icon_home,
        "back": icon_back,
        "lock": icon_lock,
        "unlock": icon_unlock,
        "file_text": icon_file_text,
        "file_code": icon_file_code,
        "file_image": icon_file_image,
        "file_zip": icon_file_zip,
        "file_json": icon_file_json,
        "file_pdf": icon_file_pdf,
        "file_bin": icon_file_bin,
    }

    for (name, row, col) in ICON_LAYOUT:
        x, y = _tile_xy(row, col)
        fn = icon_fns.get(name)
        if fn is None:
            _draw_centered_text_fallback(draw, (x, y, x + TILE_SIZE - 1, y + TILE_SIZE - 1), name[:2])
            continue
        fn(draw, x, y)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
