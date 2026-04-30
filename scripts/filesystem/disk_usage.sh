#!/usr/bin/env bash
# stonemeta: title: Disk Summary
# stonemeta: description: Shows current filesystem layout and storage amounts
# stonemeta: command: df -h | head -20

echo "=== Filesystem Disk Usage ==="
df -h 2>/dev/null | head -20 || echo "df command not available"
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"

