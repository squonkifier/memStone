#!/usr/bin/env bash
# stonemeta: title: Local Open Ports
# stonemeta: description: Scans for open ports on localhost or a specified target. Common ports only.
#
# Scans ports 21,22,23,25,53,80,110,143,443,465,587,993,995,3306,5432,8080,8443
# Uses bash /dev/tcp for lightweight scanning (no nmap required).

echo "Enter target host (default: localhost):"
read -r -p "> " target
target=${target:-localhost}

echo ""
echo "Scanning $target for open ports..."
echo ""

ports=(21 22 23 25 53 80 110 143 443 465 587 993 995 3306 5432 8080 8443)
open_ports=()

for port in "${ports[@]}"; do
    (echo >/dev/tcp/$target/$port) 2>/dev/null
    if [ $? -eq 0 ]; then
        open_ports+=("$port")
        echo "  Port $port: OPEN"
    else
        echo "  Port $port: closed"
    fi
done

echo ""
if [ ${#open_ports[@]} -eq 0 ]; then
    echo "No open ports found."
else
    echo "Open ports: ${open_ports[*]}"
fi

echo ""
echo -e "\x1b[1;32mPress Ctrl+X to return to main menu\x1b[0m"
