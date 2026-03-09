<#
PowerShell build script to produce a single-file Windows EXE using PyInstaller.

Usage (PowerShell):
  1. Open PowerShell in this folder.
  2. If needed, allow script execution for this session:
       Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  3. Run: .\build_exe.ps1

What this does:
  - Creates a virtual environment `venv` (if missing)
  - Activates it
  - Upgrades pip and installs packages from requirements.txt
  - Runs PyInstaller to build a one-file, windowed EXE (no console)

Produced artifact:
  ./dist/pdf_downloader.exe
#>

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "Working in: $projectRoot"

$venvPath = Join-Path $projectRoot 'venv'
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvPath
}

Write-Host "Activating virtual environment..."
& "$venvPath\Scripts\Activate.ps1"

Write-Host "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip
pip install -r .\requirements.txt

Write-Host "Converting PNG icon to ICO format..."
python scripts\convert_icon.py
if (-not (Test-Path ".\icon\logo_pdf.ico")) {
    Write-Host "Warning: Icon conversion failed, building without icon..." -ForegroundColor Yellow
    $iconArg = ""
} else {
    $iconArg = "--icon=icon\logo_pdf.ico"
}

Write-Host "Running PyInstaller (onefile, windowed)..."
# Use windowed mode because this is a Tkinter GUI; remove --windowed to keep console.
# Add icon folder to the bundle for runtime access
if ($iconArg) {
    pyinstaller --noconfirm --onefile --windowed --name "pdf_downloader" $iconArg --add-data "icon;icon" "pdf_downloads.py"
} else {
    pyinstaller --noconfirm --onefile --windowed --name "pdf_downloader" --add-data "icon;icon" "pdf_downloads.py"
}

if (Test-Path (Join-Path $projectRoot 'dist\pdf_downloader.exe')) {
    Write-Host "Build complete: $(Join-Path $projectRoot 'dist\pdf_downloader.exe')"
} else {
    Write-Host "Build finished but EXE not found in dist\ - check PyInstaller output above for errors." -ForegroundColor Yellow
}

Write-Host "Done.\n"
