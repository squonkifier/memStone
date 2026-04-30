#!/usr/bin/env bash
# stonemeta: title: Ping Test
# stonemeta: description: Test connectivity to hosts with ping. Checks if remote hosts are reachable.
# stonemeta: command: ping -c 4
# Sends 4 ping packets and reports packet loss and average latency.
# Useful for diagnosing network issues.

echo "Enter hostname or IP to ping (default: 8.8.8.8):"
read -r -p "> " target
target=${target:-8.8.8.8}

echo ""
echo "Pinging $target (4 packets)..."
echo ""

ping -c 4 "$target" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "\x1b[1;31mPing failed: Host unreachable or invalid hostname\x1b[0m"
fi

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
