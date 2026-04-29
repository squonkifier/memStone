#!/usr/bin/env bash
# Admin-Meta: Title: Systemd - List System Services
# Admin-Meta: Description: List all systemd services with their current status. Shows active, inactive, failed, and enabled/disabled states.
#
# Services are displayed in columns: UNIT, LOAD, ACTIVE, SUB, and DESCRIPTION.
# Use arrow keys to scroll, Q to return.

echo "Listing all systemd services..."
echo ""

systemctl list-units --type=service --all --no-pager 2>/dev/null

if [ $? -ne 0 ]; then
    echo ""
    echo -e "\x1b[1;31mError: systemd may not be available on this system.\x1b[0m"
fi

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
