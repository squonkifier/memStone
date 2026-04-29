#!/usr/bin/env bash
# Admin-Meta: Title: Arch - Refresh keys
# Admin-Meta: Description: Did your updates start to fail with low trust or GPG style errors? Might be an old keyring. Update it with this!
#

echo "Are you sure? Y/n"
read -p ": " choice

# Handle empty input as 'n', accept both cases
case $choice in
    [Yy])
    echo "Please enter your root password:"
        sudo pacman-key --refresh-keys
        sudo pacman-key --populate archlinux
        echo ""
        echo -e "\x1b[1;32mComplete! Press Q to return to main menu!\x1b[0m"
        ;;
    [Nn]|"")
        echo -e "\x1b[1;32mPress Q to return to main menu!\x1b[0m"
        exit 1
        ;;
    *)
        echo ""
        echo -e "\x1b[1;32mInvalid choice. Please select Y or n, or press Q to return to menu\x1b[0m"
        exit 1
        ;;
esac
