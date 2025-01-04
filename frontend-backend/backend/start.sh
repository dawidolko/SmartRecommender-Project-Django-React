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

# Checking if Python is installed
echo "Checking Python installation..."
if ! command -v python &> /dev/null; then
    echo "Python is not installed or not available in PATH."
    exit 1
fi

# Checking if pip is installed
echo "Checking pip installation..."
if ! command -v pip &> /dev/null; then
    echo "pip is not installed or not available in PATH."
    exit 1
fi

# Creating virtual environment if it does not exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activating virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Installing required packages
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Installing psycopg2-binary
pip uninstall -y psycopg2-binary
pip install psycopg[c]

# Creating and applying migrations
echo "Creating and applying migrations to the database..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Error during migrations creation."
    exit 1
fi

python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error during migrations application."
    exit 1
fi

# Seeding the database
echo "Seeding the database..."
python manage.py seed
if [ $? -ne 0 ]; then
    echo "Error during database seeding."
    exit 1
fi

# Running Django server
echo "Starting Django server..."
xdg-open http://127.0.0.1:8000 &  # Opens the browser
python manage.py runserver
