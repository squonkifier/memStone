#!/bin/bash
# stonemeta: title: Delete Orphaned Packages
# stonemeta: description: Remove orphaned packages, sometimes recovers lots of space after lots of compiling! Destructive unless you have internet access, in which case, it's safe to use with no fear. Run it and remove old packages that aren't strictly required. Usually these are compiler suites and old versions of frameworks.
# stonemeta: command: pacman -Rs $(pacman -Qdtq)
#

# Track total size of deleted packages in bytes
total_deleted=0

# Get list of orphaned packages
orphans=$(pacman -Qdtq 2>/dev/null)

if [ -n "$orphans" ]; then
    # Calculate total size of orphaned packages before removal
    echo "Calculating space to recover from orphaned packages..."
    for pkg in $orphans; do
        size=$(pacman -Qi "$pkg" 2>/dev/null | grep -i "installed size" | sed 's/.*: //' | numfmt --from=iec 2>/dev/null || echo 0)
        if [ -n "$size" ] && [ "$size" != "0" ]; then
            total_deleted=$((total_deleted + size))
        fi
    done
    
    total_mb=$((total_deleted / 1024 / 1024))
    echo -e "\x1b[1;32mRecovering approximately ${total_mb} MB from orphaned packages\x1b[0m"
    echo ""
fi

# Remove orphaned packages, recovers lots of space. Destructive unless you have internet access
echo "Please enter your root password:"
sudo pacman -Rs $(pacman -Qdtq) 2>/dev/null

echo ""
total_mb=$((total_deleted / 1024 / 1024))
echo -e "\x1b[1;32mComplete! Recovered approximately ${total_mb} MB. Press Q to return to main menu!\x1b[0m"
