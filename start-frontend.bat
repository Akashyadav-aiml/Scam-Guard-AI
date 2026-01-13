@echo off
echo ================================================
echo   ScamGuard AI - Frontend Application
echo ================================================
echo.
echo Starting Frontend (React + Vite)...
echo.

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    npm install
)

echo.
echo Frontend starting at http://localhost:5173
echo.
start cmd /k "title Frontend Server && npm run dev"

echo.
echo ================================================
echo Frontend started in new window!
echo ================================================
echo.
pause
