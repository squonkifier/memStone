#!/usr/bin/env bash
# stonemeta: title: HTTP Server
# stonemeta: description: Fire up a quick webserver for local network filesharing purposes.
echo -e "\x1b[1;32m#WARNING! The local working directory will be shared: $PWD\x1b[0m"
echo ""
echo "Are you sure? Y/n"
read -p "" choice

# Only Y proceeds, everything else cancels
case $choice in
    [Yy])
        echo ""
        echo -e "\x1b[1;32mPress Ctrl+X to return to terminate webserver\x1b[0m"
        python -m http.server 8080
        ;;
    *)
        echo ""
        echo -e "\x1b[1;32mPress Ctrl+X to return to main menu!\x1b[0m"
        exit 1
        ;;
esac
