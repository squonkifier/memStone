#!/usr/bin/env bash
# stonemeta: title:  Export Packagelist (Archlinux)
# stonemeta: description: Export a list of all installed packages to ~/.packagelist.log
# stonemeta: command: pacman -Qq

pacman -Qq | tee ~/packagelist.log
echo ""
        echo -e "\x1b[1;32mPackagelist exported to ~/packagelist.log\x1b[0m"
