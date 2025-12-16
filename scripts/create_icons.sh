#!/bin/bash
# Example script to create basic icons using ImageMagick
# Requires: ImageMagick (brew install imagemagick)

set -e

echo "Creating example 16x16 icons..."

# Create output directory
mkdir -p generated_icons

# Function to create a simple icon
create_icon() {
    local name=$1
    local color=$2
    local shape=$3
    
    case $shape in
        "folder")
            convert -size 16x16 xc:white \
                -fill "$color" \
                -draw "rectangle 2,4 14,12" \
                -draw "rectangle 2,4 6,6" \
                generated_icons/${name}.png
            ;;
        "file")
            convert -size 16x16 xc:white \
                -fill "$color" \
                -draw "rectangle 4,2 12,14" \
                -draw "polygon 12,2 12,6 8,2" \
                generated_icons/${name}.png
            ;;
        "circle")
            convert -size 16x16 xc:white \
                -fill "$color" \
                -draw "circle 8,8 8,2" \
                generated_icons/${name}.png
            ;;
        "square")
            convert -size 16x16 xc:white \
                -fill "$color" \
                -draw "rectangle 3,3 13,13" \
                generated_icons/${name}.png
            ;;
    esac
    
    echo "Created: ${name}.png"
}

# Create basic icons
create_icon "folder" "black" "folder"
create_icon "file" "black" "file"
create_icon "circle" "black" "circle"
create_icon "square" "black" "square"

echo ""
echo "Icons created in generated_icons/"
echo "Next steps:"
echo "  1) (Legacy) Convert these icons to embedded arrays:"
echo "     python3 icons/scripts/png_to_progmem.py icons/scripts/generated_icons/*.png"
echo "  2) (Preferred) Put icons into icons/assets/iconsheet.png, update icons/iconsheet.json, then run:"
echo "     python3 icons/scripts/generate_icons.py"
