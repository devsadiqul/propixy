# Propixy - Property Management System

A complete property management system built with **Django 4.2** and **Tailwind CSS**. Production-ready with email/password authentication, comprehensive billing, and multiple deployment options.

## Features

- **Email/Password Authentication** - Register and login with email or username
- **Password Reset** - Secure password reset via email
- **Building Management** - Add, edit, delete buildings
- **Unit Management** - Manage units within buildings with rent tracking
- **Tenant Management** - Track tenants and their unit assignments
- **Billing System** - Generate bills with configurable rates
- **Payment Tracking** - Record payments (cash, bKash) and generate receipts
- **Dashboard** - Overview with key metrics and occupancy rates
- **Dark Mode** - Toggle between light and dark themes
- **Responsive Design** - Works on all devices
- **Production Ready** - Security settings, logging, static files handling

## Quick Start (Local Development)

### Option 1: Using setup script

**Linux/macOS:**
```bash
cd django_propixy
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
cd django_propixy
setup.bat
```

### Option 2: Manual setup

```bash
# Navigate to project
cd django_propixy

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py makemigrations buildings tenants billing core
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# REQUIRED: Generate a new secret key for production
SECRET_KEY=your-super-secret-key

# Set to False in production
DEBUG=True

# Add your domain in production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Email settings (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Generate a new SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Production Deployment

### Deploy to Render (Recommended)

1. Push code to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Connect your repository
4. Render will auto-detect `render.yaml`
5. Add environment variables in Render dashboard

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy with Docker

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Deploy to VPS (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Clone and setup
git clone https://github.com/yourusername/propixy.git
cd propixy/django_propixy
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Collect static files and migrate
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser

# Run with gunicorn
gunicorn propixy.wsgi:application --bind 0.0.0.0:8000
```

## Project Structure

```
django_propixy/
├── propixy/              # Main project settings
│   ├── settings.py       # Django settings (production-ready)
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI application
│
├── core/                 # Core app (auth, dashboard)
│   ├── views.py          # Login, register, dashboard, profile
│   ├── forms.py          # Custom auth forms (email-based)
│   └── urls.py
│
├── buildings/            # Buildings app
│   ├── models.py         # Building, Unit models
│   ├── views.py          # Building/Unit CRUD
│   └── forms.py
│
├── tenants/              # Tenants app
│   ├── models.py         # Tenant model
│   ├── views.py          # Tenant CRUD
│   └── forms.py
│
├── billing/              # Billing app
│   ├── models.py         # BillingSettings, Bill models
│   ├── views.py          # Bill generation, payments
│   └── forms.py
│
├── templates/            # HTML templates with Tailwind CSS
├── static/               # Static files
├── media/                # User uploads
├── logs/                 # Log files
│
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── Procfile              # Heroku deployment
├── Dockerfile            # Docker deployment
├── docker-compose.yml    # Docker Compose
├── render.yaml           # Render deployment
└── manage.py             # Django CLI
```

## Usage Guide

1. **Register/Login** - Create account with email and password
2. **Configure Billing** - Set rates in Billing > Settings
3. **Add Buildings** - Create your properties
4. **Add Units** - Add flats/units to buildings
5. **Add Tenants** - Register tenants and assign to units
6. **Generate Bills** - Create monthly bills for occupied units
7. **Record Payments** - Track payments and print receipts

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: Tailwind CSS (CDN)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Server**: Gunicorn
- **Static Files**: WhiteNoise

## Security Features

- CSRF protection
- Password hashing (PBKDF2)
- Session-based authentication
- HTTPS enforcement (production)
- HSTS headers (production)
- XSS/Content-type sniffing protection

## License

MIT License
