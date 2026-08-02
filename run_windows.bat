@echo off
echo ===================================================
echo   HSE Manager - Development Run Script (Windows)
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

echo [3/3] Starting Application...
python main.py

pause
