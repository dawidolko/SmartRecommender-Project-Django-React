@echo off
SETLOCAL EnableDelayedExpansion

echo =================================
echo Starting Frontend Setup Script
echo =================================

:: Checking if Node.js is installed
echo Checking Node.js installation...
node -v >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js is not installed. Please install Node.js and try again.
    pause
    exit /b 1
)

:: Checking if npm is installed
echo Checking npm installation...
npm -v >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: npm is not installed or not working properly.
    pause
    exit /b 1
)

:: Creating node_modules directory if it doesn't exist
if not exist "node_modules" (
    echo node_modules directory doesn't exist. Creating...
    mkdir node_modules
)

:: Installing dependencies
echo Installing dependencies...
call npm install

:: Installing additional packages
echo Installing additional packages...
call npm install react-toastify
call npm install react-countup
call npm install jwt-decode
call npm install axios
call npm install react-router-dom
call npm install framer-motion
call npm install lucide-react

:: Verify that package.json exists
if not exist "package.json" (
    echo Error: package.json not found. Please make sure you're in the correct directory.
    pause
    exit /b 1
)

:: Ask user if they want to build the application
echo.
echo Would you like to build the application before starting the development server? (Y/N)
set /p BUILD_CHOICE=
if /i "%BUILD_CHOICE%"=="Y" (
    echo Building the project...
    call npm run build
    
    if %ERRORLEVEL% NEQ 0 (
        echo Error occurred during build.
        pause
        exit /b 1
    )
    
    echo Build completed successfully.
)

:: Starting the application
echo.
echo Starting the development server...
start "" http://localhost:3000
call npm start

pause
ENDLOCAL