#!/usr/bin/env bash
# Admin-Meta: Title: Arch - Update - Pacman
# Admin-Meta: Description: Basic interactive system update for base system packages, using the core Pacman package manager.
#

echo "Please enter your root password:"
sudo pacman -Syyu

echo ""
echo -e "\x1b[1;32mComplete! Press Q to return to main menu!\x1b[0m"

