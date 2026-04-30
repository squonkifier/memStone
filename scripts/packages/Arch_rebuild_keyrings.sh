#!/usr/bin/env bash
# stonemeta: title: Rebuild keys (Archlinux)
# stonemeta: description: Totally wipe and reload your package manager keyring.
# stonemeta: command: pacman-key --init && pacman-key --populate

echo "Are you sure? Y/n"
read -p "" choice

# Only Y proceeds, everything else cancels
case $choice in
    [Yy])
    echo "Please enter your root password:"
        sudo rm -rf /etc/pacman.d/gnupg
        sudo pacman-key --init
        sudo pacman-key --populate archlinux
        echo ""
        echo -e "\x1b[1;32mComplete! Press Ctrl+X to return to main menu!\x1b[0m"
        ;;
    *)
        echo -e "\x1b[1;32mPress Ctrl+X to return to main menu!\x1b[0m"
        exit 1
        ;;
esac
