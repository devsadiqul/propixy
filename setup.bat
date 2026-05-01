@echo off
echo ==========================================
echo    Propixy Django Setup Script (Windows)
echo ==========================================
echo.

REM Check Python
echo Checking Python...
python --version
if errorlevel 1 (
    echo Python is required. Please install Python 3.
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo.
echo Running database migrations...
python manage.py makemigrations buildings tenants billing core
python manage.py migrate

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To create an admin user, run:
echo   python manage.py createsuperuser
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then open http://127.0.0.1:8000 in your browser
echo.
pause
