@echo off

REM Environment variables for PostgreSQL
set PGPASSWORD=admin
set PGUSER=postgres
set PGDATABASE=postgres
set PGHOST=localhost
set PGPORT=5432

REM Creating the database
echo Creating database 'product_recommendation'...
psql -U %PGUSER% -d %PGDATABASE% -h %PGHOST% -p %PGPORT% -c "DROP DATABASE IF EXISTS product_recommendation;" >nul 2>&1
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
pip install colorama

REM Installing psycopg2-binary
echo Installing psycopg...
pip install psycopg2-binary
pip install djangorestframework-simplejwt
pip install Pillow
python -m textblob.download_corpora
pip3 install textblob colorama tqdm
pip3 install pandas numpy scikit-learn matplotlib seaborn nltk

REM Create media directory if it doesn't exist
if not exist "media" (
    echo Creating media directory...
    mkdir media
)

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

REM Creating cache table
echo Creating cache table...
python manage.py createcachetable
if %errorlevel% neq 0 (
    echo Error during cache table creation.
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
start "" http://127.0.0.1:8000

REM Run check_media.py if it exists
if exist "check_media.py" (
    echo Running media check...
    python check_media.py
)

REM Start Django server
python manage.py runserver

pause