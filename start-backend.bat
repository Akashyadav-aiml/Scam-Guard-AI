@echo off
echo ================================================
echo   ScamGuard AI - Domain Safety Checker
echo ================================================
echo.
echo Starting Backend Server (FastAPI)...
echo.

cd backend

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies if needed
echo Installing/checking dependencies...
pip install -q -r requirements.txt

REM Start backend
echo.
echo Backend starting at http://localhost:8000
echo API Docs at http://localhost:8000/docs
echo.
start cmd /k "title Backend Server && python main.py"

echo.
echo ================================================
echo Backend started in new window!
echo ================================================
echo.
pause
