"""
Django settings for my_project_2 project.
"""

from pathlib import Path
import os
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-typerlimjza2d^xf%bows+u=)!32a&h_rllwz9=csee!_y9sy!'
DEBUG = True
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'schedule',
    'users',  
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

ROOT_URLCONF = 'my_project_2.urls'

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

WSGI_APPLICATION = 'my_project_2.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ НАСТРОЙКИ АУТЕНТИФИКАЦИИ ============
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'index'

# ============ EMAIL ДЛЯ ВОССТАНОВЛЕНИЯ ПАРОЛЯ ============
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# ============ НАСТРОЙКИ ДЛЯ АВАТАРОК ============
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============ НАСТРОЙКИ ЛОГИРОВАНИЯ ============
LOG_DIR = BASE_DIR / 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Базовое логирование (ЛР6)
logging.basicConfig(
    level=logging.INFO,
    filename=str(LOG_DIR / 'app_basic.log'),
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Расширенные настройки логирования с хэндлерами (ЛР7)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(name)s %(filename)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file_rotating': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'app_rotating.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
            'level': 'DEBUG',
        },
        'timed_rotating': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': str(LOG_DIR / 'app_timed.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'standard',
            'level': 'INFO',
        },
    },
    'loggers': {
        'users': {
            'handlers': ['console', 'file_rotating', 'timed_rotating'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'schedule': {
            'handlers': ['console', 'file_rotating', 'timed_rotating'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'catalog': {
            'handlers': ['console', 'file_rotating'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}