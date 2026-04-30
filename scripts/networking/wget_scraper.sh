#!/usr/bin/env bash
# stonemeta: title: Webpage Scraper
# stonemeta: description: Quickly scrape files from a website. Paste your URL into the script, and it will download loose files from the wepage. Supports zip|mp3|ogg|rar|tar|gz

echo -e "\x1b[1;32mFiles will be saved in: $PWD\x1b[0m"
echo "Please input a URL to scrape:"
read URL
DOWNLOAD_DIR="." # Current working directory

echo "Fetching links from: $URL"

# Use wget to get the page content, then grep and sed to extract .zip and .mp3 links
# -q: quiet, no output
# -O -: output to stdout
# grep -E -o: print only matching parts (extended regex)
# href="[^"]*\.(zip|mp3)": matches href attributes ending in .zip or .mp3
# sed: extracts the URL from the href attribute
# Sort and uniq to remove duplicate links
LINKS=$(wget -q -O - "$URL" | \
        grep -E -o 'href="[^"]*\.(zip|mp3|ogg|rar|tar|gz)"' | \
        sed 's/.*href="\([^"]*\)".*/\1/' | \
        sort -u)

if [ -z "$LINKS" ]; then
    echo "No .zip or .mp3 links found on $URL."
    exit 0
fi

echo "Found the following .zip and .mp3 files to download:"
echo "$LINKS"
echo ""

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

    if [ -f "$DOWNLOAD_DIR/$FILENAME" ]; then
        echo "Skipping $FILENAME (already exists)."
    else
        echo "Downloading $FILENAME from $FULL_LINK..."
        # -c: continue download if partial exists, but in this case it means
        #     if file exists, skip (as no partial will be there due to -nc)
        # -nc: no clobber, don't overwrite existing files
        # -P "$DOWNLOAD_DIR": save files to the specified directory
        wget -q -nc -P "$DOWNLOAD_DIR" "$FULL_LINK"
        if [ $? -eq 0 ]; then
            echo "$FILENAME downloaded successfully."
        else
            echo "Error downloading $FILENAME."
        fi
    fi
done

echo "Download process completed."



# wget -nd -r -P /save/location -A jpeg,jpg,bmp,gif,png http://www.somedomain.com
