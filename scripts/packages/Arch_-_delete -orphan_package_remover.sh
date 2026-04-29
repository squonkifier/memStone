#!/bin/bash
# Admin-Meta: Title: Arch - Delete - Orphaned Packages
# Admin-Meta: Description: Remove orphaned packages, sometimes recovers lots of space after lots of compiling! Destructive unless you have internet access, in which case, it's safe to use with no fear. Run it and remove old packages that aren't strictly required. Usually these are compiler suites and old versions of frameworks.
#

# Remove orphaned packages, recovers lots of space. Destructive unless you have internet access
echo "Please enter your root password:"
sudo pacman -Rs $(pacman -Qdtq) 2>/dev/null

echo ""
echo -e "\x1b[1;32mComplete! Press Q to return to main menu!\x1b[0m"
