"""
Honk Settings.
"""

import environ
from pathlib import Path

from google.oauth2 import service_account

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# reading .env files
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = env('SECRET_KEY')

DEBUG: bool = env('DEBUG')

ALLOWED_HOSTS: list[str] = ['localhost', '127.0.0.1', 'honk.rafaelmc.net']

CSRF_TRUSTED_ORIGINS: list[str] = ['https://honk.rafaelmc.net']

# Application definition

INSTALLED_APPS: list[str] = [
    'circus.apps.CircusConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'honk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'honk.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sqlite_data' / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

VALIDATOR_PATH = 'django.contrib.auth.password_validation.'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': VALIDATOR_PATH + 'UserAttributeSimilarityValidator'},
    {'NAME': VALIDATOR_PATH + 'MinimumLengthValidator'},
    {'NAME': VALIDATOR_PATH + 'CommonPasswordValidator'},
    {'NAME': VALIDATOR_PATH + 'NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "/"
STORAGES = {
    "default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage"
    },
}

# GOOGLE_APPLICATION_CREDENTIALS =
GS_BUCKET_NAME = 'honkhonk'
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    f"{BASE_DIR}/gcp-honk-credentials.json"
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
