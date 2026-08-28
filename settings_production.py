"""
Production settings for sumithrakp_website project.
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This file lives at the repo root, so BASE_DIR is its own directory
# (unlike sumithrakp_website/settings.py, which is one level down).
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# The public host this site is served on. Requests arrive from the local
# LiteSpeed proxy with Host: 127.0.0.1:8090, so CanonicalHostMiddleware
# rewrites them back to this value (see main/middleware.py).
CANONICAL_HOST = os.environ.get('CANONICAL_HOST', 'sumithrakp.com').strip()
CANONICAL_PROTO = os.environ.get('CANONICAL_PROTO', 'https')

_DEFAULT_ALLOWED_HOSTS = ','.join(
    h for h in (CANONICAL_HOST, f'www.{CANONICAL_HOST}', '127.0.0.1', 'localhost') if h
)
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', _DEFAULT_ALLOWED_HOSTS).split(',')
    if h.strip()
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'main',
]

MIDDLEWARE = [
    # First: restores the public host/scheme behind the loopback proxy, so
    # ALLOWED_HOSTS, the SSL redirect and CSRF origin checks below all see
    # the real request.
    'main.middleware.CanonicalHostMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sumithrakp_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.theme_context',
                'main.context_processors.site_settings_context',
                'main.context_processors.client_portal_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'sumithrakp_website.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('DB_NAME', 'sumithrakp_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise settings for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Private files (client deliverables, AI outputs) - never URL-served
PRIVATE_MEDIA_ROOT = BASE_DIR / 'private_media'

# Allow client sketch/plan uploads up to 15 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'main.authentication.EmailMobileBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Login URLs
LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'

# Trusted origins for CSRF. The browser posts with
# Origin: https://sumithrakp.com, so that origin must be trusted explicitly --
# matching ALLOWED_HOSTS is not enough for Django's origin check.
_DEFAULT_CSRF_ORIGINS = ','.join(
    f'{CANONICAL_PROTO}://{h}'
    for h in (CANONICAL_HOST, f'www.{CANONICAL_HOST}')
    if CANONICAL_HOST
)
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CSRF_TRUSTED_ORIGINS', _DEFAULT_CSRF_ORIGINS).split(',')
    if o.strip()
]

# LiteSpeed terminates TLS and proxies plain HTTP to gunicorn. Without this,
# request.is_secure() is always False: secure cookies are never honoured and
# SECURE_SSL_REDIRECT below would redirect-loop.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security Settings
# Default False: the http -> https redirect belongs at the edge, in .htaccess
# (see deploy/htaccess-proxy.txt). Django only sees the proxied HTTP request.
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'