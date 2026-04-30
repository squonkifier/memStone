#!/usr/bin/env bash
# stonemeta: title: Block device info
# stonemeta: description: Shows basic information about attached storage drives
# stonemeta: command: lsblk -f

lsblk -f
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
