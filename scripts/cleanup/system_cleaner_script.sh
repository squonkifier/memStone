#!/bin/bash
# Admin-Meta: Title: Logs Cleaner
# Admin-Meta: Description: Deletes basic system caches and logs for quick, clean recovery of storage space

# Track total size of deleted files in bytes
total_deleted=0

# Function to calculate size of path before deletion, echo MB recovered, and add to total
calc_size() {
    if [ -e "$1" ]; then
        local size=$(du -sb "$1" 2>/dev/null | cut -f1)
        total_deleted=$((total_deleted + size))
        local size_mb=$((size / 1024 / 1024))
        echo "Recovered ${size_mb} MB from $1"
        echo ""
    fi
}

# Vacuum the systemlog journal. shit gets out of hand
echo ""
echo "Please enter your root password:"
sudo journalctl --vacuum-time=1m 2>/dev/null
echo -e "\x1b[1;32mVacuuming system journal using journalctl\x1b[0m"
echo "journalctl --vacuum-time=1m"
echo ""

# delete pacman package cache
echo -e "\x1b[1;32mDeleting the package manager cache\x1b[0m"
calc_size /var/cache/pacman/pkg
sudo rm -Rf /var/cache/pacman/pkg/* 2>/dev/null
echo ""

# remove old kernel dump logs
echo -e "\x1b[1;32mDeleting old kernel logs and crash dumps\x1b[0m"
calc_size /var/lib/systemd/coredump
sudo rm -Rf /var/lib/systemd/coredump/* 2>/dev/null
echo ""

# remove debug symbols. i dont know what this shit is but roll tide bitch
echo -e "\x1b[1;32mDeleting /usr/lib/debug. This one might be dangerous lol, roll tide\x1b[0m"
calc_size /usr/lib/debug
sudo rm -Rf /usr/lib/debug/* 2>/dev/null
echo ""

# Display total size of deleted files in MB
total_mb=$((total_deleted / 1024 / 1024))
echo -e "Total size of deleted files: \x1b[1;32m${total_mb} MB\x1b[0m"
echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"

