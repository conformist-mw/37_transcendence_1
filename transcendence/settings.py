import os
import raven
from configurations import Configuration, values


class BaseConfig(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = values.SecretValue(environ_name='SECRET_KEY')
    ALLOWED_HOSTS = []
    ROOT_URLCONF = 'transcendence.urls'
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
    WSGI_APPLICATION = 'transcendence.wsgi.application'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'users',
        'raven.contrib.django.raven_compat',
    ]
    MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
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

    RAVEN_CONFIG = {
        'dsn': values.Value(environ_name='RAVEN_SECRET'),
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    }


class Dev(BaseConfig):
    ALLOWED_HOSTS = ['*']
    DEBUG = True


class Production(BaseConfig):
    pass
