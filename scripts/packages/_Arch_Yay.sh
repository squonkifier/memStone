#!/usr/bin/env bash
# stonemeta: title: Update Yay (Archlinux)
# stonemeta: description: Basic interactive system update for system packages + AUR packages, using the Yay package manager.
# stonemeta: command: yay

echo "Please enter your root password:"
yay --noprogressbar --noconfirm && echo "" && echo -e "\x1b[1;32mComplete! Press Ctrl+X to return to main menu!\x1b[0m"
