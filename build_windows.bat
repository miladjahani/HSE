@echo off
echo ===================================================
echo   HSE Manager - Build EXE Script (Windows)
echo ===================================================

echo [1/3] Building React Frontend...
cd ui_react
call npm install
call npm run build
cd ..

echo [2/3] Setting up Python Virtual Environment...
if not exist "venv" (
    virtualenv venv
)
call venv\Scripts\activate
pip install -r requirements-fastapi.txt
pip install pyinstaller

echo [3/3] Compiling EXE using PyInstaller...
pyinstaller --noconfirm --onefile --windowed --name "HSE_Mine_Manager_V2" --icon "assets\app_icon.ico" --add-data "ui_react\dist;ui_react\dist" --add-data "assets;assets" main.py

echo ===================================================
echo   Done! Your executable is located in the 'dist' folder.
echo ===================================================
pause
