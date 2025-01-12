@echo off
echo =================================
echo Starting Frontend Setup Script
echo ==================================

:: Checking if Node.js is installed
node -v >nul 2>&1
IF ERRORLEVEL 1 (
echo Error: Node.js is not installed. Please install Node.js and try again.
pause
exit /b
)

:: Installing dependencies
echo Installing dependencies...
npm install
npm install react-toastify
npm install react-countup

:: Installing axios
echo Installing axios...
npm install axios

:: Installing react-router-dom
echo Installing react-router-dom...
npm install react-router-dom

:: Building the application
echo Building the project...
npm run build

:: Starting the application
echo Starting the development server...
npm start
pause