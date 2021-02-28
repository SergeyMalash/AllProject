from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channels',
    'corsheaders',
    'widget_tweaks',

    'messenger.apps.MessengerConfig',
    'anonymous.apps.AnonymousConfig',
    'shortener.apps.ShortenerConfig',
    'accounts.apps.AccountsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AllProject.urls'

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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DJANGO_DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DJANGO_DB_USER'),
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
        'HOST': os.getenv('DJANGO_DB_HOST'),
        'PORT': os.getenv('DJANGO_DB_PORT'),
    }
}


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = os.getenv("DJANGO_EMAIL_BACKEND", 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_DEFAULT_EMAIL')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST')
EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT')
EMAIL_USE_SSL = bool(os.getenv('DJANGO_EMAIL_USE_SSL'))

CELERY_BROKER_URL = os.getenv('CELERY_BROKER', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER', 'redis://127.0.0.1:6379/0')
CELERY_TASK_SERIALIZER = 'json'

WSGI_APPLICATION = 'AllProject.wsgi.application'
ASGI_APPLICATION = "AllProject.routing.application"

AUTH_USER_MODEL = 'accounts.Account'

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(
                os.getenv('REDIS_HOST', '127.0.0.1'),
                os.getenv('REDIS_PORT', 6379)
            )]
        },
    },
}
