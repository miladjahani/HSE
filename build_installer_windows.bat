@echo off
echo ===================================================
echo   HSE Manager - Build Installer Script (Windows)
echo ===================================================

echo [1/4] Building React Frontend...
cd ui_react
call npm install
call npm run build
cd ..

echo [2/4] Setting up Python Virtual Environment...
if not exist "venv" (
    virtualenv venv
)
call venv\Scripts\activate
pip install -r requirements-fastapi.txt
pip install pyinstaller

echo [3/4] Compiling EXE using PyInstaller...
pyinstaller --noconfirm --onefile --windowed --name "HSE_Mine_Manager_V2" --icon "assets\app_icon.ico" --add-data "ui_react\dist;ui_react\dist" --add-data "assets;assets" main.py

echo [4/4] Creating Setup Package using Inno Setup...
set "INNO_COMPILER=C:\Program Files (x86)\Inno Setup 6\iscc.exe"

if exist "%INNO_COMPILER%" (
    "%INNO_COMPILER%" installer.iss
    echo ===================================================
    echo   Done! Your setup installer is located in the 'dist' folder.
    echo   Name: HSE_Mine_Manager_Setup.exe
    echo ===================================================
) else (
    echo ===================================================
    echo   ERROR: Inno Setup compiler not found.
    echo   Please download and install Inno Setup 6 from:
    echo   https://jrsoftware.org/isdl.php
    echo.
    echo   Once installed, run this script again.
    echo   Meanwhile, the standalone EXE is available in the 'dist' folder.
    echo ===================================================
)
pause
