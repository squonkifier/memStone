#!/usr/bin/env bash
# Admin-Meta: Title: System Resource Monitor
# Admin-Meta: Description: A real-time, lightweight TUI dashboard showing CPU, Memory, Disk, and Network usage.
#
# Uses 'top' and 'df' in a loop to provide a quick overview of system vitals.
# Press Ctrl+C to exit the monitoring view.

echo -e "\x1b[1;34mStarting System Resource Monitor...\x1b[0m"
echo "Press Ctrl+C to stop."
echo ""

while true; do
    clear
    echo -e "\x1b[1;36m--- System Resource Monitor ---\x1b[0m"
    echo ""
    echo -e "\x1b[1;33m[ CPU & PROCESSES ]\x1b[0m"
    top -bn1 | head -n 15
    echo ""
    echo -e "\x1b[1;33m[ DISK USAGE ]\x1b[0m"
    df -h --total | grep 'total'
    echo ""
    echo -e "\x1b[1;33m[ MEMORY ]\x1b[0m"
    free -h
    echo ""
    echo -e "\x1b[1;33m[ NETWORK INTERFACES ]\x1b[0m"
    ip -brief addr show
    echo ""
    echo -e "\x1b[1;32mLast updated: $(date +%H:%M:%S)\x1b[0m"
    sleep 2
done
