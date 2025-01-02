@echo off

REM Zmienne środowiskowe
set PGPASSWORD=admin
set PGUSER=postgres
set PGDATABASE=postgres
set PGHOST=localhost
set PGPORT=5432

echo Tworzenie bazy danych 'product_recommendation'...
psql -U %PGUSER% -d %PGDATABASE% -h %PGHOST% -p %PGPORT% -c "CREATE DATABASE product_recommendation;"

if %errorlevel% neq 0 (
    echo Nie udało się utworzyć bazy danych.
    exit /b %errorlevel%
) else (
    echo Baza danych 'product_recommendation' została utworzona pomyślnie.
)

REM Aktywacja wirtualnego środowiska
echo Aktywacja wirtualnego środowiska...
call .venv\Scripts\activate

REM Instalacja wymaganych pakietów
echo Instalacja zależności...
pip install -r requirements.txt

REM Tworzenie migracji i zastosowanie ich
echo Tworzenie migracji i zastosowanie ich do bazy danych...
python manage.py makemigrations
python manage.py migrate

REM Uruchomienie serwera
echo Uruchamianie serwera Django...
python manage.py runserver

REM Otwarcie przeglądarki z aplikacją
start http://127.0.0.1:8000

pause
