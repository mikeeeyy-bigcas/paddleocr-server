@echo off
echo ========================================
echo  PaddleOCR Local Server Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements_paddleocr.txt

echo.
echo [2/3] Downloading PaddleOCR models (first time only, ~500MB)...
echo This may take a few minutes...
echo.

echo [3/3] Starting PaddleOCR server...
echo.
python paddleocr_server.py

pause
