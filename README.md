# This is a set of Python scripts that is used to generate the icons for the Hardware One project.

## Usage Guide: 

### First-Time Setup (if an iconsheet.png doesn't exist)
1. **Generate blank template**: `python3 icons/scripts/icon_template_generator.py`
   - Creates a 512x512 canvas with a 15x15 grid of 32x32 slots (1px spacing)
   - Output: `icon_template.png` — copy this to `icons/assets/iconsheet.png`

### Adding/Editing Icon Visuals
2. **Edit `icons/assets/iconsheet.png`**
   - Draw within the 32x32 tiles (don't edit the 1px spacing lines)

### Adding/Editing Icon Registry
3. **Add/update entries in `icons/iconsheet.json`**
   - Add: `{"name": "icon_name", "row": X, "col": Y}`
   - Row/col are 0-indexed

### Export icon
4. **Run `python3 icons/scripts/generate_icons.py`**
   - Reads manifest + iconsheet.png → generates `icons_embedded.cpp`
   - **Warning:** This completely regenerates the file and as a result it erases previous content

5. **Great Success.** You now have 32x32 icons for your project in a format that requires no heap allocation.
