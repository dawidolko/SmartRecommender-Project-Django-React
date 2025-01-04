@echo off

REM Environment variables for PostgreSQL
set PGPASSWORD=admin
set PGUSER=postgres
set PGDATABASE=postgres
set PGHOST=localhost
set PGPORT=5432

REM Creating the database
echo Creating database 'product_recommendation'...
psql -U %PGUSER% -d %PGDATABASE% -h %PGHOST% -p %PGPORT% -c "CREATE DATABASE product_recommendation;" >nul 2>&1

if %errorlevel% neq 0 (
    echo Failed to create the database or it already exists.
) else (
    echo Database 'product_recommendation' created successfully.
)

REM Checking if Python and pip are available
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not available in PATH.
    exit /b %errorlevel%
)

echo Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed or not available in PATH.
    exit /b %errorlevel%
)

REM Creating virtual environment if it does not exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activating virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Installing required packages
echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

REM Installing psycopg2-binary
pip uninstall psycopg2-binary
pip install psycopg[c]
@REM pip install psycopg2-binary

REM Creating and applying migrations
echo Creating and applying migrations to the database...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error during migrations creation.
    exit /b %errorlevel%
)

python manage.py migrate
if %errorlevel% neq 0 (
    echo Error during migrations application.
    exit /b %errorlevel%
)

REM Seeding the database
echo Seeding the database...
python manage.py seed
if %errorlevel% neq 0 (
    echo Error during database seeding.
    exit /b %errorlevel%
)

REM Running Django server
echo Starting Django server...
start http://127.0.0.1:8000
python manage.py runserver

pause
