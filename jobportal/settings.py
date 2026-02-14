from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# SECURITY
# ===============================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret-key")

DEBUG = False # keep True until everything works

ALLOWED_HOSTS = [
    "ai-job-portal-o7m2.onrender.com",
    "127.0.0.1",
]



# ===============================
# APPLICATIONS
# ===============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'jobs',
    'applications',
    'messaging',
    'ats',
]


# ===============================
# MIDDLEWARE
# ===============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jobportal.urls'

WSGI_APPLICATION = 'jobportal.wsgi.application'


# ===============================
# TEMPLATES
# ===============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# ===============================
# DATABASE (SQLite Only)
# ===============================

import os
import dj_database_url

if os.environ.get("DATABASE_URL"):
    # Production (Render PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    # Local development (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ===============================
# PASSWORD VALIDATION
# ===============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===============================
# CUSTOM USER
# ===============================

AUTH_USER_MODEL = 'accounts.CustomUser'


# ===============================
# INTERNATIONALIZATION
# ===============================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ===============================
# STATIC FILES
# ===============================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ===============================
# MEDIA FILES
# ===============================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===============================
# AUTH REDIRECTS
# ===============================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    "https://ai-job-portal-o7m2.onrender.com",
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===============================
# PRODUCTION SECURITY (RENDER)
# ===============================

import os

if os.environ.get("RENDER"):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        "https://ai-job-portal-o7m2.onrender.com",
    ]
