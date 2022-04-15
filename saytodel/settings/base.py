"""
Django settings for Samodelkin project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1')

SECURITY_MODE = os.getenv('SECURITY_MODE')
BACKEND_HOST = os.getenv('BACKEND_HOST')
FRONTEND_HOST = os.getenv('FRONTEND_HOST')
DATABASE_MODE = os.getenv('DATABASE_MODE')
USE_S3 = os.getenv('USE_S3', 'False').lower() in ('true', '1')

# Common django config
AUTH_USER_MODEL = 'accounts.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/api/auth/login'
LOGOUT_URL = '/api/auth/logout'

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = f'Самоделкин <{EMAIL_HOST_USER}>'

# Auth config

REST_REGISTRATION = {
    # urls
    'REGISTER_VERIFICATION_URL': f'https://{FRONTEND_HOST}/verify-user',
    'RESET_PASSWORD_VERIFICATION_URL': f'https://{FRONTEND_HOST}/reset-password',
    'REGISTER_EMAIL_VERIFICATION_URL': f'https://{FRONTEND_HOST}/verify-email',

    # general
    'USER_LOGIN_FIELDS': ('email', 'username'),
    'USER_PUBLIC_FIELDS': ('username', 'email', 'password'),
    'VERIFICATION_FROM_EMAIL': DEFAULT_FROM_EMAIL,

    # confirmation
    'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
        'subject': 'auth/confirm/subject.txt',
        'html_body': 'auth/confirm/body.html',
    },
    'REGISTER_VERIFICATION_PERIOD': datetime.timedelta(days=1),
    'REGISTER_VERIFICATION_ONE_TIME_USE': True,
    'REGISTER_VERIFICATION_AUTO_LOGIN': True,

    # reset
    'RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES': {
        'subject': 'auth/reset/subject.txt',
        'html_body': 'auth/reset/body.html',
    },
    'SEND_RESET_PASSWORD_LINK_SERIALIZER_USE_EMAIL': True,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
}

# Swagger config

DRF_YASG_EXCLUDE_VIEWS = [
    'rest_registration.api.views.profile.WrappedAPIView',
]

SWAGGER_SETTINGS = {
    'OPERATIONS_SORTER': 'alpha',
    'TAGS_SORTER': 'alpha',
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # libs
    'corsheaders',
    'storages',
    'drf_yasg',
    'rest_framework',
    'rest_registration',
    'phonenumber_field',

    # api
    'api.accounts.apps.AccountsConfig',
    'api.files.apps.FilesConfig',
    'api.mysite.apps.MysiteConfig',
    'api.crm.apps.CrmConfig',
    'api.marketplace.apps.MarketplaceConfig',
    'api.parallel.apps.ParallelConfig',

    # deleting files
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    # cors
    'corsheaders.middleware.CorsMiddleware',

    # django default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom
    'Samodelkin.middlewares.censorship.CensorshipMiddleware'
]

ROOT_URLCONF = 'Samodelkin.urls'

EMAIL_TEMPLATES_DIR = os.path.join(BASE_DIR, 'email_templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [EMAIL_TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'Samodelkin.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = ()
