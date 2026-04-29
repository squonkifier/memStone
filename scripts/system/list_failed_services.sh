#!/usr/bin/env bash
# Admin-Meta: Title: Systemd - List Errored Services
# Admin-Meta: Description: List all systemd services that have failed, are inactive, or are in a halted state. Helps identify services that need attention.
#
# Shows failed units, inactive (dead) services, and services with error conditions.
# Use arrow keys to scroll, Q to return.

echo "=== Failed Services ==="
echo ""
FAILED=$(systemctl list-units --type=service --state=failed --no-pager --no-legend 2>/dev/null)

if [ -z "$FAILED" ]; then
    echo -e "\x1b[1;32mNo failed services found.\x1b[0m"
else
    echo "$FAILED"
fi

echo ""
echo "=== Inactive (Dead) Services ==="
echo ""
INACTIVE=$(systemctl list-units --type=service --state=inactive --no-pager --no-legend 2>/dev/null)

if [ -z "$INACTIVE" ]; then
    echo -e "\x1b[1;32mNo inactive services found.\x1b[0m"
else
    echo "$INACTIVE"
fi

echo ""
echo "=== Services with Error Conditions ==="
echo ""
# Show services that are not active and not just dead (e.g., activating, deactivating, failed)
systemctl list-units --type=service --state=activating --state=deactivating --state=failed --no-pager --no-legend 2>/dev/null | \
    awk '!seen[$0]++'

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
