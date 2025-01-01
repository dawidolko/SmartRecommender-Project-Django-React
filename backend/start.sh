#!/bin/bash

# Aktywacja środowiska wirtualnego (jeśli używasz)
if [ -f env/bin/activate ]; then
    source env/bin/activate
fi

# Uruchomienie serwera Django
python manage.py runserver
