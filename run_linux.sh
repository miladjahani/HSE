#!/bin/bash
echo "==================================================="
echo "  HSE Manager - Development Run Script (Linux/Mac)"
echo "==================================================="

echo "[1/3] Building React Frontend..."
cd ui_react
npm install
npm run build
cd ..

echo "[2/3] Setting up Python Virtual Environment..."
if [ ! -d "venv" ]; then
    virtualenv venv
fi
source venv/bin/activate
pip install -r requirements-fastapi.txt

echo "[3/3] Starting Application..."
python main.py
