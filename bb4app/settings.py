"""
Django settings for bb4app project.
"""
import os
from pathlib import Path
import configparser
import dj_database_url

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load config.ini
config = configparser.ConfigParser()
config.read(BASE_DIR / 'config.ini')

# Security settings
SECRET_KEY = "django-insecure-4s*l!k#$3__k+vao$gsr+ybji#^%k5z8t0+i7teq3=s1jp09%v"
DEBUG = os.getenv('DEBUG', config.get('DEFAULT', 'DEBUG', fallback='True')) == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')  # Replace '*' with your Render domain later

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'crispy_forms',
    'bb4main',  # Your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'bb4app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'bb4main' / 'templates'],
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

WSGI_APPLICATION = 'bb4app.wsgi.application'
# Database
# DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL', config.get('POSTGRESQL', 'DATABASE_URL'))
print("DATABASE_URL:", DATABASE_URL)  # Debugging line
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}
# Static files (with WhiteNoise)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 3
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/logout'
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = True

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', config.get('GOOGLE', 'CLIENT_ID', fallback='13679971103-8pmsi7ec03vssg6qlqd82fji6t2u57mt.apps.googleusercontent.com'))
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', config.get('GOOGLE', 'CLIENT_SECRET', fallback='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'))

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': 'https://bb4-django.onrender.com/accounts/google/login/callback/' if not DEBUG else 'http://localhost:8000/accounts/google/login/callback/',
        }
    }
}

# CSRF settings
CSRF_COOKIE_SECURE = not DEBUG
CSRF_TRUSTED_ORIGINS = ['https://bb4-django.onrender.com', 'http://localhost:8000']

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', config.get('EMAIL', 'EMAIL_HOST_USER', fallback='codekalpa@gmail.com'))
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', config.get('EMAIL', 'EMAIL_HOST_PASSWORD', fallback='jofc idrj vjlw rmec'))
# ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_EMAIL_REQUIRED = True

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'