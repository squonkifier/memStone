#!/usr/bin/env bash
# Admin-Meta: Title: Directory Sizes
# Admin-Meta: Description: Shows the size of each subdirectory in the current or specified path.
#
# Lists all immediate subdirectories sorted by size (largest first).
# Helps identify which directories are using the most space.

echo "Enter directory to analyze (default: current working directory):"
read -r -p "> " target_dir
target_dir=${target_dir:-.}

if [ ! -d "$target_dir" ]; then
    echo -e "\x1b[1;31mError: Directory '$target_dir' not found.\x1b[0m"
    echo ""
    echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
    exit 1
fi

echo ""
echo "Directory sizes in '$target_dir':"
echo "================================="
du -sh "$target_dir"/*/ 2>/dev/null | sort -rh
echo ""
echo "Total:"
du -sh "$target_dir" 2>/dev/null

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
