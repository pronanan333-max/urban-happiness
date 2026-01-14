
# Import Django environ and initialise environment variables

import environ

env = environ.Env()

environ.Env.read_env()


from pathlib import Path

import os

import json






# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

#CSRF_TRUSTED_ORIGINS = []



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',

    'account',

    'writer',

    'client',

    'storages',
    
    'whitenoise.runserver_nostatic',

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'


AUTH_USER_MODEL = 'account.CustomUser'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'subplatform.urls'

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

WSGI_APPLICATION = 'subplatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# SQLite database (development - default)



DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': os.getenv("DB_PASSWORD_YO"),
        'HOST': 'trolley.proxy.rlwy.net',
        'PORT': '56395',
        
    }
}



# PostgreSQL database (production)


'''
import dj_database_url

DATABASES = {

    'default': dj_database_url.parse('')

}
'''


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = 'True'

EMAIL_HOST_USER = 'pronanan333@gmail.com' # - GMAIL email address
EMAIL_HOST_PASSWORD = 'ekyg hymi hocy ieaq' # - APP password

DEFAULT_FROM_EMAIL = 'pronanan333@gmail.com'  # - GMAIL email address


# Amazon S3 configuration 



# PayPal credentials

SS_CLIENT_ID = ''

SS_SECRET_ID = ''

STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
SITE_URL = os.getenv("SITE_URL")

# ดึง Price IDs แบบ dict
STRIPE_PRICES = json.loads(os.getenv("STRIPE_PRICES"))

LOGIN_URL = '/my-login/'



# RDS (Database) configuration settings:
'''
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'mydemodb1', # Enter your Database name HERE

        'USER': 'neungdb', # Enter your Database username HERE

        'PASSWORD': 'Neung01012538', # Enter your Database password HERE

        'HOST': 'mydatabase.cv4u8se62uxg.ap-southeast-2.rds.amazonaws.com', # Enter your Database host/endpoint HERE

        'PORT': '5432',
    }
}

'''
