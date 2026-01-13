@echo off
echo ================================================
echo   ScamGuard AI - Complete Application
echo ================================================
echo.
echo Starting both Backend and Frontend servers...
echo.

REM Start Backend
echo [1/2] Starting Backend Server...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -q -r requirements.txt
start cmd /k "title ScamGuard Backend && python main.py"
cd ..

timeout /t 3 /nobreak > nul

REM Start Frontend
echo [2/2] Starting Frontend Server...
cd frontend
if not exist node_modules (
    echo Installing dependencies...
    npm install
)
start cmd /k "title ScamGuard Frontend && npm run dev"
cd ..

echo.
echo ================================================
echo Both servers started successfully!
echo ================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
pause > nul
