#!/usr/bin/env bash
# Admin-Meta: Title: Arch - Delete - Yay & Pacman Caches
# Admin-Meta: Description: Clean the package manager cache. Removes old package files to free up disk space.
#
# WARNING: This deletes cached .pkg files. You won't be able to downgrade without re-downloading.
# The cache is safe to clear if you have working internet access.

echo "Choose Y/n and press enter"
read -p "> " choice

case $choice in
    [Yy])
        echo ""
        echo "Please enter your root password:"

        sudo paccache -r 2>/dev/null || sudo rm -Rf /var/cache/pacman/pkg/*.tar.* /var/cache/pacman/pkg/*.pkg.tar.* 2>/dev/null
        # backup some yay config stuff, then wipe out yay cache and replace config files
        echo -e "\x1b[1;32mDeleting the yay and AUR cache\x1b[0m"
        cp /home/$USER/.cache/yay/vcs.json /tmp/vcs.json 2>/dev/null
        cp /home/$USER/.cache/yay/completion.cache /tmp/completion.cache 2>/dev/null
        #calculate some sizes to show the user
        rm -Rf /home/$USER/.cache/yay/* 2>/dev/null
        # replace those yay backups
        cp /tmp/vcs.json /home/$USER/.cache/yay/vcs.json 2>/dev/null
        cp /tmp/completion.cache /home/$USER/.cache/yay/completion.cache 2>/dev/null

        echo ""
        echo -e "\x1b[1;32mCache cleaned successfully!\x1b[0m"
        ;;
    *)
        echo -e "\x1b[1;32mOperation cancelled.\x1b[0m"
        ;;
esac

echo ""
echo -e "\x1b[1;32mPress Q to return to main menu\x1b[0m"
