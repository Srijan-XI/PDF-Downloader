@echo off
REM Batch file to launch the PDF Downloader EXE
REM This assumes the EXE has been built and is located in the dist folder

SET "SCRIPT_DIR=%~dp0"
SET "EXE_PATH=%SCRIPT_DIR%dist\pdf_downloader.exe"

if exist "%EXE_PATH%" (
    echo Launching PDF Downloader...
    start "" "%EXE_PATH%"
) else (
    echo Error: pdf_downloader.exe not found in dist folder!
    echo Please build the EXE first by running: build_exe.ps1
    echo.
    pause
)
