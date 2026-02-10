@echo off
REM Quick Start Script for Local OCR Server
REM Double-click this file to start the server

echo ============================================================
echo   Local OCR Server - Quick Start
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Ollama is not installed
    echo Please install Ollama from: https://ollama.com/download
    pause
    exit /b 1
)

echo [2/4] Checking Ollama installation...
ollama --version

REM Check if required packages are installed
echo [3/4] Installing Python dependencies...
pip install -r requirements.txt --quiet

echo [4/4] Starting OCR server...
echo.
echo ============================================================
echo   Server will start on http://localhost:5000
echo   Press Ctrl+C to stop the server
echo ============================================================
echo.
echo IMPORTANT: In another terminal window, run:
echo    ngrok http 5000
echo.
echo Then copy the ngrok URL to Apps Script Settings
echo ============================================================
echo.

python server.py

pause
