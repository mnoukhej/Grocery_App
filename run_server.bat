@echo off
echo ===================================================
echo Starting Grocery App Backend Server...
echo ===================================================

:: Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    python backend\server.py
) else (
    python backend\server.py
)

pause
