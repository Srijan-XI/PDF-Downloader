#!/bin/bash
# Main launcher for PDF Downloader (Linux/macOS)
# Automatically detects if app needs building or can be run directly

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "dist/pdf_downloader" ]; then
    echo "Starting PDF Downloader..."
    ./dist/pdf_downloader
else
    echo "PDF Downloader has not been built yet."
    echo ""
    echo "To build the application, run:"
    echo "  chmod +x scripts/build_app.sh"
    echo "  ./scripts/build_app.sh"
    echo ""
    read -p "Press Enter to continue..."
fi
