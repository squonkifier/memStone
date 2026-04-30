#!/usr/bin/env bash
# stonemeta: title: Delete Package Caches
# stonemeta: description: Clean the package manager cache. Removes old package files to free up disk space.
# stonemeta: command: rm -rf .cache/yay, /var/cache/pacman
#

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

echo "Deleting package caches. Proceed? Y/n"
read -p "> " choice

case $choice in
    [Yy])
        echo ""
        echo "Please enter your root password:"
        echo ""

        # Calculate sizes before deletion
        echo -e "\x1b[1;32mCalculating space to recover...\x1b[0m"
        echo ""
        calc_size /var/cache/pacman/pkg
        calc_size /home/$USER/.cache/yay

        sudo rm -Rf /var/cache/pacman/pkg/*.tar.* /var/cache/pacman/pkg/*.pkg.tar.* 2>/dev/null
        # backup some yay config stuff, then wipe out yay cache and replace config files
        cp /home/$USER/.cache/yay/vcs.json /tmp/vcs.json 2>/dev/null
        cp /home/$USER/.cache/yay/completion.cache /tmp/completion.cache 2>/dev/null
        rm -Rf /home/$USER/.cache/yay/* 2>/dev/null
        # replace those yay backups
        cp /tmp/vcs.json /home/$USER/.cache/yay/vcs.json 2>/dev/null
        cp /tmp/completion.cache /home/$USER/.cache/yay/completion.cache 2>/dev/null

        echo ""
        total_mb=$((total_deleted / 1024 / 1024))
        echo -e "\x1b[1;32mCache cleaned successfully! Recovered ${total_mb} MB\x1b[0m"
        ;;
    *)
        echo -e "\x1b[1;32mOperation cancelled.\x1b[0m"
        ;;
esac

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
