#!/bin/bash

echo "=========================================="
echo "   Propixy Django Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python..."
python3 --version || { echo "Python 3 is required. Please install it."; exit 1; }

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations buildings tenants billing core
python manage.py migrate

# Create superuser prompt
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To create an admin user, run:"
echo "  python manage.py createsuperuser"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then open http://127.0.0.1:8000 in your browser"
echo ""
