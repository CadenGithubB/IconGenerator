This is a set of Python scripts that is used to generate the icons for the Hardware One project.

1. Edit `icons/assets/iconsheet.png` (Draw within the 32x32 tiles, dont edit 1px spacing).
2. Add/update entries in `icons/iconsheet.json` (Add the name of the icon and the row/col numbers).
3. Run `python3 icons/scripts/generate_icons.py` (This step is when the tiles are converted to code. This re-'draws' `icons_embedded.cpp` and _**completely**_ erases what was there previously).
4. Move `icons_embedded.cpp` to the Folder for the Hardware One project.
5. Great Success
