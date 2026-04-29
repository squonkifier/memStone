#!/usr/bin/env bash
# Admin-Meta: Title: Process Monitor
# Admin-Meta: Description: Shows top processes by CPU and memory usage. Real-time system resource overview.
#
# Displays the top 15 processes sorted by CPU usage, then memory usage.
# Similar to 'top' but in a compact, one-shot format.

echo "=== Top Processes by CPU & Memory ==="
echo ""
echo "CPU-bound processes:"
echo "-------------------"
ps aux --sort=-%cpu | head -16 | awk '{printf "%-10s %6s%% %6s%% %s\n", $1, $3, $4, $11}'
echo ""
echo "Memory-bound processes:"
echo "----------------------"
ps aux --sort=-%mem | head -16 | awk '{printf "%-10s %6s%% %6s%% %s\n", $1, $3, $4, $11}'
echo ""
echo "System load average:"
uptime 2>/dev/null | sed 's/^.*load/Load/'
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
