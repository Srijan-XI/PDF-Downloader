#!/bin/bash
# Bash script to launch the PDF Downloader application
# This assumes the app has been built and is located in the dist folder

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXE_PATH="$SCRIPT_DIR/dist/pdf_downloader"

if [ -f "$EXE_PATH" ]; then
    echo "Launching PDF Downloader..."
    "$EXE_PATH"
else
    echo "Error: pdf_downloader not found in dist folder!"
    echo "Please build the application first by running: ./build_app.sh"
    echo ""
    read -p "Press Enter to continue..."
fi
