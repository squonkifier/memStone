#!/usr/bin/env bash
# stonemeta: title: Webpage Scraper
# stonemeta: description: Quickly scrape files from a website. Paste your URL into the script, and then your desired extensions separated by a comma. [.zip,mp3,lol]

 if ! command -v wget &> /dev/null; then
     echo "Error: wget is required but not installed. Please install wget to
 use this script."
     exit 1
 fi

echo -e "\x1b[1;32mFiles will be saved in: $PWD/scraped\x1b[0m"
echo ""
echo "Please input a URL to scrape:"
read URL
echo ""
echo "Please input the file extensions you want to download from the page, separated by commas. [zip,mp3,omg,wow]"
echo ""
read FILETYPES
FILETYPES=$(echo "$FILETYPES" | tr ',' '|')
SCRAPED_DIR="$PWD/scraped"
mkdir -p "$SCRAPED_DIR"

echo "Fetching links from: $URL"

# Use wget to get the page content, then grep and sed to extract supported file links
# -q: quiet, no output
# -O -: output to stdout
# grep -E -o: print only matching parts (extended regex)
# href="[^"]*\.(zip|mp3|ogg|rar|tar|gz)": matches href attributes ending in supported extensions
# sed: extracts the URL from the href attribute
# Sort and uniq to remove duplicate links
LINKS=$(wget -q -O - "$URL" | \
        grep -E -o "href=\"[^\"]*\.($FILETYPES)\"" | \
        sed 's/.*href="\([^"]*\)".*/\1/' | \
        sort -u)

if [ -z "$LINKS" ]; then
    echo "No .zip, .mp3, .ogg, .rar, .tar, .gz links found on $URL."
    exit 0
fi

echo "Found the following files to download:"
echo "$LINKS"
echo ""

# Initialize counters
downloaded=0
total_bytes=0

# Loop through each found link and download
for LINK in $LINKS; do
    # Construct the full URL if the link is relative
    if [[ "$LINK" == /* ]]; then # Starts with /
        # Get the base URL (protocol://domain:port)
        BASE_URL=$(echo "$URL" | grep -oP '^https?://[^/]+')
        FULL_LINK="${BASE_URL}${LINK}"
    elif [[ "$LINK" != http* ]]; then # Not starting with http
        # Assume it's relative to the current URL path
        # Remove any file name from the URL to get the directory path
        DIR_PATH=$(echo "$URL" | sed 's/\/[^/]*$//')
        FULL_LINK="${DIR_PATH}/${LINK}"
    else
        FULL_LINK="$LINK"
    fi

    FILENAME=$(basename "$FULL_LINK")

    if [ -f "$SCRAPED_DIR/$FILENAME" ]; then
        echo "Skipping $FILENAME (already exists)."
    else
        echo "Downloading $FILENAME from $FULL_LINK..."
        # -c: continue download if partial exists, but in this case it means
        #     if file exists, skip (as no partial will be there due to -nc)
        # -nc: no clobber, don't overwrite existing files
        # -P "$SCRAPED_DIR": save files to the specified directory
        wget -q -nc -P "$SCRAPED_DIR" "$FULL_LINK"
        if [ $? -eq 0 ]; then
            echo "$FILENAME downloaded successfully."
            downloaded=$((downloaded+1))
            filesize=$(stat -c%s "$SCRAPED_DIR/$FILENAME" 2>/dev/null || echo 0)
            total_bytes=$((total_bytes + filesize))
        else
            echo "Error downloading $FILENAME."
        fi
    fi
done

# Calculate total size in MB
if [ $total_bytes -gt 0 ]; then
    total_mb=$(awk "BEGIN {printf \"%.2f\", $total_bytes/1024/1024}")
else
    total_mb="0.00"
fi

echo "Download process completed."
echo "Total files downloaded: $downloaded, Total size: ${total_mb} MB"
echo ""
echo -e "\x1b[1;32mPress Ctrl+X to return to main menu\x1b[0m"



# wget -nd -r -P /save/location -A jpeg,jpg,bmp,gif,png http://www.somedomain.com
