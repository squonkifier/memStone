#!/usr/bin/env bash
# Admin-Meta: Title: Network Connectivity Tester
# Admin-Meta: Description: Performs a series of connectivity tests including local gateway, DNS, and global internet reachability.
#
# Useful for diagnosing if an issue is local, DNS-related, or a broad ISP outage.

echo "Starting Network Connectivity Diagnostics..."
echo ""

# 1. Local Interface
echo -e "\x1b[1;34m[1/4] Checking Local Interfaces...\x1b[0m"
ip -brief addr show
echo ""

# 2. Gateway
GATEWAY=$(ip route | grep default | awk '{print $3}' | head -n 1)
if [ -n "$GATEWAY" ]; then
    echo -e "\x1b[1;34m[2/4] Pinging Default Gateway ($GATEWAY)...\x1b[0m"
    if ping -c 3 "$GATEWAY" > /dev/null 2>&1; then
        echo -e "\x1b[1;32mGateway is reachable.\x1b[0m"
    else
        echo -e "\x1b[1;31mGateway is UNREACHABLE.\x1b[0m"
    fi
else
    echo -e "\x1b[1;31mNo default gateway found.\x1b[0m"
fi
echo ""

# 3. DNS
echo -e "\x1b[1;34m[3/4] Checking DNS Resolution (google.com)...\x1b[0m"
if host google.com > /dev/null 2>&1; then
    echo -e "\x1b[1;32mDNS Resolution successful.\x1b[0m"
else
    echo -e "\x1b[1;31mDNS Resolution FAILED.\x1b[0m"
fi
echo ""

# 4. Internet
echo -e "\x1b[1;34m[4/4] Testing Global Internet Reachability (1.1.1.1)...\x1b[0m"
if ping -c 3 1.1.1.1 > /dev/null 2>&1; then
    echo -e "\x1b[1;32mInternet is reachable.\x1b[0m"
else
    echo -e "\x1b[1;31mInternet is UNREACHABLE.\x1b[0m"
fi

echo ""
echo -e "\x1b[1;32mDiagnostics complete.\x1b[0m"
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
