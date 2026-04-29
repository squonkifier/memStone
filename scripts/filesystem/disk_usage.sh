#!/usr/bin/env bash
# Admin-Meta: Title: Disk Summary
# Admin-Meta: Description: Shows current filesystem layout and storage amounts
#

echo "=== Filesystem Disk Usage ==="
df -h 2>/dev/null | head -20 || echo "df command not available"
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"

