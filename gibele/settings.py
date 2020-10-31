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
DEBUG = False

TIME_INPUT_FORMATS = ['%I:%M %p',]

ALLOWED_HOSTS = ['pure-fjord-45840.herokuapp.com','.pure-fjord-45840.herokuapp.com','gibele.com', '.gibele.com','.gibele.ca','gibele.ca']
SESSION_COOKIE_DOMAIN= 'gibele.com'
DOMAIN_NAME= 'gibele.com'

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
    'storages',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'gibele.urls'
ROOT_HOSTCONF = 'gibele.hosts'
DEFAULT_HOST = 'www'

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

# Prod database
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'gibele1',
#         'USER': 'sdonald',
#         'PASSWORD': 'Kingston36227',
#         'POST':'5432',
#     }
# }


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
# USE_S3 = os.getenv('USE_S3') == 'TRUE'

# if USE_S3:
#     # aws settings
#     AWS_ACCESS_KEY_ID = os.getenv('AKIA5YCTBN72JSC3D4WZ')
#     AWS_SECRET_ACCESS_KEY = os.getenv('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')
#     AWS_STORAGE_BUCKET_NAME = os.getenv('django-gibele')
#     AWS_DEFAULT_ACL = None
#     AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#     AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
#     # s3 static settings
#     STATIC_LOCATION = 'static'
#     STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
#     STATICFILES_STORAGE = 'gibele.storage_backends.StaticStorage'
#     # s3 public media settings
#     PUBLIC_MEDIA_LOCATION = 'media'
#     MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
#     DEFAULT_FILE_STORAGE = 'gibele.storage_backends.PublicMediaStorage'
# else:
#     STATIC_URL = '/staticfiles/'
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#     MEDIA_URL = '/mediafiles/'
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# AWS_STORAGE_BUCKET_NAME = 'django-gibele'
# AWS_ACCESS_KEY_ID = 'AKIA5YCTBN72JSC3D4WZ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'static'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'business/static'),
# ]
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DEFAULT_FILE_STORAGE = 'gibele.storage_backends.MediaStorage'

AWS_STORAGE_BUCKET_NAME = 'django-gibele'
AWS_S3_REGION_NAME = 'us-east-1'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = 'AKIA5YCTBN72JSC3D4WZ'
AWS_SECRET_ACCESS_KEY = 'RIBukj+HMffN2oWSeR+BosSPz0tlLve+XVAxpBKc'
AWS_DEFAULT_ACL = None
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'gibele.storage_backends.StaticStorage'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'gibele.storage_backends.MediaStorage'
STATIC_URL = '/static/'
# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# MEDIA_URL ='/media/'
# MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

LOGIN_REDIRECT_URL = 'business:homepage'


EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@gibele.com'
EMAIL_HOST_PASSWORD = 'vEK97wFvxY27jTEhqQY8Qv6L!'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

CELERY_BROKER_URL = 'amqps://dtkacyby:r-kSQJMm0h2BksbAYs4l1PgXWlqSrYdo@grouse.rmq.cloudamqp.com/dtkacyby'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT=True

