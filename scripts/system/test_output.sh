#!/bin/bash
# Admin-Meta: Title: ANSI Tests
# Admin-Meta: Description: Test ANSI colors and line breaks
#

echo -e "\x1b[31mRed Text\x1b[0m"
echo -e "\x1b[1;32mBold Green\x1b[0m"
echo ""  # Empty line from echo
echo "Normal text after empty line"
echo -e "\x1b[34mBlue\x1b[0m and \x1b[33mYellow\x1b[0m mixed"
echo -e "\033[32mtest message\033[0m"
echo -e "\033[32mtest message\033[0m"
