#!/bin/bash

# Environment variables for PostgreSQL
export PGPASSWORD="admin"
export PGUSER="postgres"
export PGDATABASE="postgres"
export PGHOST="localhost"
export PGPORT="5432"

# Creating the database
echo "Creating database 'product_recommendation'..."
psql -U "$PGUSER" -d "$PGDATABASE" -h "$PGHOST" -p "$PGPORT" -c "CREATE DATABASE product_recommendation;" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Failed to create the database or it already exists."
else
    echo "Database 'product_recommendation' created successfully."
fi

# Checking if Python3 is installed
echo "Checking Python3 installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed or not available in PATH."
    exit 1
fi

# Checking if pip3 is installed
echo "Checking pip3 installation..."
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed or not available in PATH."
    exit 1
fi

# Creating virtual environment if it does not exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activating virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Installing required packages
echo "Installing dependencies from requirements.txt..."
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install Pillow

# Installing psycopg
echo "Installing psycopg..."
pip3 uninstall -y psycopg2-binary
pip3 install psycopg[c]
pip3 install djangorestframework-simplejwt

# Create media directory if it doesn't exist
if [ ! -d "media" ]; then
    echo "Creating media directory..."
    mkdir -p media
fi

# Creating and applying migrations
echo "Creating and applying migrations to the database..."
python3 manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Error during migrations creation."
    exit 1
fi

python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error during migrations application."
    exit 1
fi

# Seeding the database
echo "Seeding the database..."
python3 manage.py seed
if [ $? -ne 0 ]; then
    echo "Error during database seeding."
    exit 1
fi

# Running check_media.py if it exists
if [ -f "check_media.py" ]; then
    echo "Running media check..."
    python3 check_media.py
fi

# Running Django server
echo "Starting Django server..."
# Use different browser open command depending on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://127.0.0.1:8000 &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://127.0.0.1:8000 &
fi

# Start the Django server
python3 manage.py runserver