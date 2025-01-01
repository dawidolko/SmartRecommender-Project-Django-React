@echo off
:: Aktywacja środowiska wirtualnego (jeśli używasz)
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
)

:: Uruchomienie serwera Django
python manage.py runserver

:: Zatrzymanie skryptu po zakończeniu
pause
