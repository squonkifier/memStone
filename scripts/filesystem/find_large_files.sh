#!/usr/bin/env bash
# Admin-Meta: Title: Find Large Files
# Admin-Meta: Description: Find large files taking up space. Scans from a starting directory and lists files sorted by size.
#
# Shows the 20 largest files in the specified directory and subdirectories.
# Useful for tracking down space hogs.

echo "Enter directory to scan (default: /home):"
read -r -p "> " target_dir
target_dir=${target_dir:-/home}

if [ ! -d "$target_dir" ]; then
    echo -e "\x1b[1;31mError: Directory '$target_dir' not found.\x1b[0m"
    echo ""
    echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
    exit 1
fi

echo ""
echo "Scanning '$target_dir' for large files (top 20)..."
echo "This may take a moment..."
echo ""
du -ah "$target_dir" 2>/dev/null | sort -rh | head -20

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
