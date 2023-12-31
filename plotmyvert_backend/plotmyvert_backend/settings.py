"""
Django settings for plotmyvert_backend project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

PLOTMYVERT_BACKEND_DEVELOPMENT_KEY = 'django-insecure--2!j34xs%rv#v6-f9t_v_5_(c4zsy7r0%1f4r2%xl$vux-5iv('
SECRET_KEY = os.environ.get('PLOTMYVERT_BACKEND_SECRET_KEY', PLOTMYVERT_BACKEND_DEVELOPMENT_KEY)
DEBUG = SECRET_KEY == PLOTMYVERT_BACKEND_DEVELOPMENT_KEY

if DEBUG:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:3000']
    CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:3000']
else:  
    ALLOWED_HOSTS = ['vert.duz.ie', 'http://127.0.0.1']
    CSRF_TRUSTED_ORIGINS = ['https://vert.duz.ie']
    CORS_ALLOWED_ORIGINS = ['https://vert.duz.ie']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
                'propagate': False,
            },
        },
    }
    
print('DEBUG:', DEBUG)
print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
print("CSRF_TRUSTED_ORIGINS:", CSRF_TRUSTED_ORIGINS)
print("CORS_ALLOWED_ORIGINS:", CORS_ALLOWED_ORIGINS)

# Application definition

CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = "plotmyvert_backend_api.User"

DATETIME_FORMAT = 'Y-m-d H:i:s.uuuuuu'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'plotmyvert_backend_api.apps.PlotmyvertBackendApiConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plotmyvert_backend.urls'

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

WSGI_APPLICATION = 'plotmyvert_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db/db.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'