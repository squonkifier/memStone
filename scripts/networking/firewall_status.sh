#!/usr/bin/env bash
# Admin-Meta: Title: Firewall Status
# Admin-Meta: Description: Check iptables/nftables firewall rules. Shows current ruleset summary.
#
# Attempts to use multiple firewall backends (nft, iptables, ufw) and reports status.
# Useful for verifying firewall is active and configured.

echo "=== Firewall Status ==="
echo ""

# Try nftables first
if command -v nft &>/dev/null; then
    echo "Backend: nftables"
    echo "Ruleset summary:"
    nft list ruleset 2>/dev/null | head -30 || echo "  (unable to list rules)"
    echo ""
# Try iptables legacy
elif command -v iptables &>/dev/null; then
    echo "Backend: iptables"
    echo "Filter table:"
    iptables -L -n --line-numbers 2>/dev/null | head -30 || echo "  (unable to list rules - may need sudo)"
    echo ""
# Try ufw
elif command -v ufw &>/dev/null; then
    echo "Backend: ufw"
    ufw status verbose 2>/dev/null || echo "  (unable to get status)"
    echo ""
else
    echo "No recognized firewall backend found (nft, iptables, ufw)."
    echo ""
fi

# Check if firewalld is running
if systemctl is-active firewalld &>/dev/null; then
    echo "firewalld: ACTIVE"
elif service firewalld status &>/dev/null 2>&1; then
    echo "firewalld: ACTIVE"
fi

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
