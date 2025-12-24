import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils import timezone

load_dotenv()

USE_TZ = "America/Chicago"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_IP"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'mintcastiq',   # replace with your actual app name
    'domain.ingest.apps.IngestConfig',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Recommended default for new projects
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Base directory of the project (same level as manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JS, images)
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads, optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = [
    '192.168.50.74',
    '127.0.0.1',
    'localhost'
]

ROOT_URLCONF = "mintcastiq.urls"
DEBUG = True
SECRET_KEY = "o&840xb#!4t70!$m!!^og*xf(rk8z*c#d)+&risl5ibtgh@vd^"
