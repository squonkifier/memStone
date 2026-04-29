#!/usr/bin/env bash
# Admin-Meta: Title: Block device info
# Admin-Meta: Description: Shows basic information about attached storage drives
#

lsblk -f
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
