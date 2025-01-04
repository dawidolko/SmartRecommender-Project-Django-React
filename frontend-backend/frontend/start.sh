#!/bin/bash

echo "================================="
echo "Starting Frontend Setup Script"
echo "================================="

# Sprawdzenie, czy Node.js jest zainstalowany
if ! command -v node &> /dev/null
then
    echo "Error: Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

# Instalacja zależności
echo "Installing dependencies..."
npm install

# Instalacja axios
echo "Installing axios..."
npm install axios

# Instalacja react-router-dom
echo "Installing react-router-dom..."
npm install react-router-dom

# Budowanie aplikacji
echo "Building the project..."
npm run build

# Uruchamianie aplikacji
echo "Starting the development server..."
npm start
