@echo off
SETLOCAL EnableDelayedExpansion

echo =================================
echo Starting Frontend Setup Script
echo =================================

:: Checking Node.js
echo Checking Node.js...
call node -v
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js not found
    pause
    exit /b 1
)

:: Checking npm  
echo Checking npm...
call npm -v
IF %ERRORLEVEL% NEQ 0 (
    echo Error: npm not found
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
call npm install

echo.
echo Installing additional packages...
call npm install react-toastify react-countup jwt-decode axios react-router-dom framer-motion lucide-react

echo.
echo Starting development server...
start "" http://localhost:3000
npm start

ENDLOCAL