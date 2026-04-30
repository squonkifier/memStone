#!/usr/bin/env bash
# stonemeta: title: WAV to OGG converter
# stonemeta: description: Converts all .wav files in your current directory into Ogg Vorbis files, then deletes the WAVs. Quality level 8. Big space savings. REQUIRES FFMPEG
# stonemeta: command: for f in *.wav; do ffmpeg -i "$f" -c:a libvorbis -q:a 8 "${f%.wav}.ogg" && rm "$f"
#

 if ! command -v ffmpeg &> /dev/null; then
     echo "Error: wget is required but not installed. Please install wget to
 use this script."
     exit 1
 fi

# Check for WAV files before proceeding
shopt -s nullglob
wav_files=(*.wav)
shopt -u nullglob

if [ ${#wav_files[@]} -eq 0 ]; then
    echo "No WAV files found in the current directory. Exiting."
    exit 0
fi

# Convert each WAV file to OGG Vorbis
for f in "${wav_files[@]}"; do
    ffmpeg -i "$f" -c:a libvorbis -q:a 8 "${f%.wav}.ogg" && rm "$f"
done
