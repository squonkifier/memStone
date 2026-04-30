#!/usr/bin/env bash
# stonemeta: title: Readme!
# stonemeta: description: Tells you how this program works!
#
echo -e "\x1b[31m⚬○ shellStone ○⚬\x1b[0m"
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
echo -e "\x1b[1;32m# stonemeta: title: \x1b[0m"
echo "Providess script name in menu. Otherwise, parses it from .sh filename"
echo ""

echo -e "\x1b[1;32m# stonemeta: description: \x1b[0m"
echo "Provides summary of the script in the main presentation area"
echo ""

echo -e "\x1b[1;32m# stonemeta: command: \x1b[0m"
echo "Shows a representation of the script's shell commands as green text in the summary area"
