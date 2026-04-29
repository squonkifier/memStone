#!/usr/bin/env bash
# Admin-Meta: Title: Current Active Root Processes
# Admin-Meta: Description: Performs a quick audit of common security-related settings including open ports, running root processes, and sudo access.
#
# Note: Some checks may require sudo to be fully effective.

echo -e "\x1b[1;35m--- Initiating Quick Security Audit ---\x1b[0m"
echo ""

# 1. Open Listening Ports
echo -e "\x1b[1;34m[1/3] Checking for listening network ports...\x1b[0m"
if command -v ss >/dev/null 2>&1; then
    ss -tuln | grep LISTEN
else
    netstat -tuln | grep LISTEN
fi
echo ""

# 2. Processes running as Root
echo -e "\x1b[1;34m[2/3] Listing processes running with root privileges...\x1b[0m"
ps aux | awk '$1 == "root" {print $0}' | head -n 20
echo "... (showing first 20 root processes)"
echo ""

# 3. Sudo Privileges
echo -e "\x1b[1;34m[3/3] Checking current user's sudo capabilities...\x1b[0m"
sudo -l -n 2>/dev/null | grep -v "is not allowed to run sudo" || echo "No special sudo privileges detected for current user."
echo ""

echo -e "\x1b[1;32mAudit complete.\x1b[0m"
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
