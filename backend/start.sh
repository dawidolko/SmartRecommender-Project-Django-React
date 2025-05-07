#!/bin/bash

# Environment variables for PostgreSQL
export PGPASSWORD="admin"
export PGUSER="postgres"
export PGDATABASE="postgres"
export PGHOST="localhost"
export PGPORT="5432"

echo "================================="
echo "Starting SmartRecommender Setup"
echo "================================="

# Drop and recreate database to ensure clean state
echo "Recreating database 'product_recommendation'..."
psql -U "$PGUSER" -d "$PGDATABASE" -h "$PGHOST" -p "$PGPORT" -c "DROP DATABASE IF EXISTS product_recommendation;" > /dev/null 2>&1
psql -U "$PGUSER" -d "$PGDATABASE" -h "$PGHOST" -p "$PGPORT" -c "CREATE DATABASE product_recommendation;" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Failed to create the database. Check PostgreSQL connection."
    exit 1
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
echo "Installing dependencies..."
pip3 install --upgrade pip

# Install packages individually to ensure all dependencies are met
echo "Installing critical packages first..."
pip3 install django psycopg[c] psycopg2-binary django-environ

echo "Installing additional required packages..."
pip3 install djangorestframework djangorestframework-simplejwt
pip3 install textblob colorama tqdm
pip3 install Pillow
pip3 install pandas numpy scikit-learn matplotlib seaborn nltk

# Download required NLTK data for TextBlob
echo "Downloading NLTK data for TextBlob..."
python3 -m textblob.download_corpora

# Create media directory if it doesn't exist
if [ ! -d "media" ]; then
    echo "Creating media directory..."
    mkdir -p media
fi

# Reset migrations to ensure clean state
echo "Resetting migrations state..."
python3 manage.py migrate --fake zero

# Creating and applying migrations
echo "Creating and applying migrations to the database..."
python3 manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Warning: Issue during migrations creation, continuing anyway..."
fi

# Apply migrations with fake-initial to handle existing tables
echo "Applying migrations..."
python3 manage.py migrate --fake-initial
if [ $? -ne 0 ]; then
    echo "Warning: Issue during migrations application, trying regular migrate..."
    python3 manage.py migrate
    if [ $? -ne 0 ]; then
        echo "Error: Failed to apply migrations. Trying with --fake option..."
        python3 manage.py migrate --fake
    fi
fi

# Seeding the database
echo "Seeding the database..."
python3 manage.py seed
if [ $? -ne 0 ]; then
    echo "Warning: Error during database seeding, but continuing..."
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

echo "================================="
echo "Setup complete! Server starting..."
echo "================================="

# Start the Django server
python3 manage.py runserver