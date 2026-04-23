"""
Django settings for Smart Garbage Complaint System.

This settings file configures:
- Database (SQLite for simplicity)
- Email backend (Gmail SMTP for real notifications)
- Media file handling (for complaint image uploads)
- Authentication redirects
- Static file serving

For production deployment, update SECRET_KEY, DEBUG, and ALLOWED_HOSTS.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── BASE DIRECTORY ──────────────────────────────────────────────────────────
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SECURITY SETTINGS ──────────────────────────────────────────────────────
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-smartgarbage-dev-key-change-in-production-2024'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

# ─── INSTALLED APPS ──────────────────────────────────────────────────────────
# Register the complaints app alongside Django's built-in apps
INSTALLED_APPS = [
    'django.contrib.admin',       # Django admin panel
    'django.contrib.auth',        # Authentication framework
    'django.contrib.contenttypes',# Content type framework
    'django.contrib.sessions',    # Session management
    'django.contrib.messages',    # Flash messaging framework
    'django.contrib.staticfiles', # Static file management
    'django.contrib.humanize',    # Template filters for human-readable values
    'complaints',                 # Our garbage complaint app
]

# ─── MIDDLEWARE ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'garbage_project.urls'

# ─── TEMPLATES ────────────────────────────────────────────────────────────────
# Configure Django to find templates in the project-level 'templates' directory
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project-level templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'garbage_project.wsgi.application'

# ─── DATABASE ─────────────────────────────────────────────────────────────────
# Using SQLite for simplicity — perfect for development and small deployments.
# For production, consider PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── PASSWORD VALIDATION ─────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 4}},
]

# ─── INTERNATIONALIZATION ────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Indian Standard Time for Swachh Bharat context
USE_I18N = True
USE_TZ = True

# ─── STATIC FILES ────────────────────────────────────────────────────────────
# CSS, JavaScript, Images used by the application (not user-uploaded)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Project-level static directory
STATIC_ROOT = BASE_DIR / 'staticfiles'    # For collectstatic in production

# ─── MEDIA FILES (User Uploads) ──────────────────────────────────────────────
# Complaint images are stored here
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── EMAIL CONFIGURATION (Gmail SMTP) ────────────────────────────────────────
# To use Gmail:
# 1. Enable 2-Factor Authentication on your Google account
# 2. Generate an "App Password" at https://myaccount.google.com/apppasswords
# 3. Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file
#
# For development/testing without email, Django will print emails to console.
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'  # Prints to terminal by default
)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Smart Garbage System <noreply@garbagesystem.com>')

# Municipal authority email — complaints are forwarded here
MUNICIPAL_EMAIL = os.getenv('MUNICIPAL_EMAIL', 'municipal.authority@example.com')

# ─── AUTHENTICATION ──────────────────────────────────────────────────────────
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ─── DEFAULT PRIMARY KEY ─────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
