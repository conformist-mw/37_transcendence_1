from pathlib import Path

import raven
from configurations import Configuration, values


class BaseConfig(Configuration):
    BASE_DIR = Path(__file__).resolve().parents[1]
    SECRET_KEY = values.SecretValue(environ_name='SECRET_KEY')
    ALLOWED_HOSTS = []
    ROOT_URLCONF = 'transcendence.urls'
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'
    WSGI_APPLICATION = 'transcendence.wsgi.application'
    AUTH_USER_MODEL = 'users.User'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'users.apps.UsersConfig',
        'raven.contrib.django.raven_compat',
    ]
    MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',  # noqa
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
    DATABASES = values.DatabaseURLValue(values.Value(environ_name='DB_URI'))

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
        },
    ]

    RAVEN_CONFIG = {
        'dsn': values.Value(environ_name='RAVEN_SECRET'),
        'release': raven.fetch_git_sha(BASE_DIR),
    }


class Dev(BaseConfig):
    ALLOWED_HOSTS = ['*']
    DEBUG = True


class Production(BaseConfig):
    pass
