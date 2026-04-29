#!/usr/bin/env bash
# Admin-Meta: Title: List Users
# Admin-Meta: Description: Shows currently logged in users
#

echo "=== System Users ==="
printf "%-20s %-8s %-8s %s\n" "USER" "UID" "GID" "HOME"
printf "%-20s %-8s %-8s %s\n" "----" "---" "---" "----"

while IFS=: read -r user _ uid gid gecos home shell; do
    [[ "$uid" -ge 1000 ]] || continue
    printf "%-20s %-8s %-8s %s\n" "$user" "$uid" "$gid" "$home"
done < /etc/passwd

echo ""
echo "Total: $(awk -F: '$3 >= 1000 {count++} END {print count}' /etc/passwd) regular users"
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
