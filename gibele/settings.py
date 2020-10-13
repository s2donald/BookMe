"""
Django settings for gibele project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b3+j2=q*i#mg^c!2ndq#00y5bobz6*xq&v#7^^7&+$73_#e=8e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TIME_INPUT_FORMATS = ['%I:%M %p',]

ALLOWED_HOSTS = ['pure-fjord-45840.herokuapp.com','.pure-fjord-45840.herokuapp.com','gibele.com', '.gibele.com', '.gibele.com:8000', 'gibele.com:8000', 'www.192.168.2.19', '.192.168.2.19', 'localhost', '127.0.0.1']
SESSION_COOKIE_DOMAIN="pure-fjord-45840.herokuapp.com"
DOMAIN_NAME='pure-fjord-45840.herokuapp.com'

# Application definition

INSTALLED_APPS = [
    'django_hosts',
    'sslserver',
    'social_django',
    'widget_tweaks',
    'account.apps.AccountConfig',
    'business.apps.BusinessConfig',
    'businessadmin.apps.BusinessadminConfig',
    'consumer.apps.ConsumerConfig',
    'calendarapp.apps.CalendarappConfig',
    'django.contrib.gis',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'rest_framework',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'gibele.urls'
ROOT_HOSTCONF = 'gibele.hosts'
DEFAULT_HOST = ' '
DEFAULT_REDIRECT_URL = "https://pure-fjord-45840.herokuapp.com"

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

WSGI_APPLICATION = 'gibele.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
]

SOCIAL_AUTH_FACEBOOK_KEY = '780700556106489'
SOCIAL_AUTH_FACEBOOK_SECRET = '2b1e633621cc391cda8ad11afeed7bd6'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
   'fields': 'id, name, email,picture'
}
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dbpgb03n2p28n7',
        'USER': 'u1p3uutbam4gj6',
        'PASSWORD': 'pb478bac72f7afb6faa38d4236cdca1d49405e9b48585cf226ff06cb4cc26795b',
        'HOST':'ec2-3-232-39-206.compute-1.amazonaws.com',
        'POST':'5432',
    }
}


AUTH_USER_MODEL = 'account.Account'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL ='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

LOGIN_REDIRECT_URL = 'business:homepage'


EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@gibele.com'
EMAIL_HOST_PASSWORD = 'vEK97wFvxY27jTEhqQY8Qv6L!'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT=True

