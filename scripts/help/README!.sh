#!/usr/bin/env bash
# Admin-Meta: Title: Readme!
# Admin-Meta: Description: Tells you how this program works!
#
echo -e "\x1b[31m⚬○ squonkAdmin ○⚬\x1b[0m"
echo "tiny terminal UI for fancy presentation of pre-commented shell scripts stored locally"
echo ""

echo -e "\x1b[31m⚬○ Usage ○⚬\x1b[0m"
echo "⇆⇅ - Move Selection"
echo "Q - Return to Main Menu"
echo "Enter - Activate Script"
echo ""
echo "categories are auto-populated with .sh and .py scripts placed in their respective folder category names inside ./scripts"
echo "./scripts/filesystem/test.sh shows up in the filesystem category, ./scripts/networking/another.sh in networking, etc"
echo ""

echo -e "\x1b[31m⚬○ Meta-data ○⚬\x1b[0m"
echo "Metadata defined inside the .sh or .py itself is shown in the main menu, to help with organization and reminders. Use a comment as shown below to add metadata."
echo ""
echo -e "\x1b[1;32m# Admin-Meta: Title: \x1b[0m"
echo "Providess script name in menu. Otherwise, parses it from .sh filename"
echo ""

echo -e "\x1b[1;32m# Admin-Meta: Description: \x1b[0m"
echo "Provides summary of the script in the main presentation area"
echo ""

echo -e "\x1b[1;32m# Admin-Meta: Category: \x1b[0m"
echo "TBD"
