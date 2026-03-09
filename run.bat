@echo off
REM Main launcher for PDF Downloader
REM Automatically detects if app needs building or can be run directly

cd /d "%~dp0"

if exist "dist\pdf_downloader.exe" (
    echo Starting PDF Downloader...
    start "" "dist\pdf_downloader.exe"
) else (
    echo PDF Downloader has not been built yet.
    echo.
    echo To build the application, run:
    echo   scripts\build_exe.ps1
    echo.
    pause
)
