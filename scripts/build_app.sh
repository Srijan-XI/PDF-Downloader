#!/bin/bash
# Bash build script to produce a single-file Linux/macOS application using PyInstaller
#
# Usage (Linux/macOS):
#   1. Open terminal in this folder
#   2. Make script executable: chmod +x build_app.sh
#   3. Run: ./build_app.sh
#
# What this does:
#   - Creates a virtual environment 'venv' (if missing)
#   - Activates it
#   - Upgrades pip and installs packages from requirements.txt
#   - Runs PyInstaller to build a one-file application
#
# Produced artifact:
#   ./dist/pdf_downloader (Linux/macOS executable)

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Working in: $PROJECT_ROOT"

VENV_PATH="$PROJECT_ROOT/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
fi

echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Converting PNG icon to ICO format..."
python scripts/convert_icon.py
if [ ! -f "$PROJECT_ROOT/icon/logo_pdf.ico" ]; then
    echo "Warning: Icon conversion failed, building without icon..."
    ICON_ARG=""
else
    ICON_ARG="--icon=icon/logo_pdf.ico"
fi

echo "Running PyInstaller (onefile)..."
# Note: --windowed option works on macOS to hide terminal, on Linux it may not hide the console
if [ -n "$ICON_ARG" ]; then
    pyinstaller --noconfirm --onefile --windowed --name "pdf_downloader" $ICON_ARG --add-data "icon:icon" pdf_downloads.py
else
    pyinstaller --noconfirm --onefile --windowed --name "pdf_downloader" --add-data "icon:icon" pdf_downloads.py
fi

if [ -f "$PROJECT_ROOT/dist/pdf_downloader" ]; then
    echo "Build complete: $PROJECT_ROOT/dist/pdf_downloader"
    echo ""
    echo "To run the application:"
    echo "  ./dist/pdf_downloader"
    echo ""
    echo "Or use the launcher script:"
    echo "  ./run.sh"
else
    echo "Build finished but executable not found in dist/ - check PyInstaller output above for errors."
fi

echo "Done."
