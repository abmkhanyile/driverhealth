"""
Django settings for driver_health project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DH_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'user_accounts',
    'home',
    'training_courses',
    'careers',
    'dhclients',
    'companies',
    'countries',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'driver_health.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'driver_health.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['driver_health/templates'],
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

WSGI_APPLICATION = 'driver_health.wsgi.application'
ASGI_APPLICATION = "driver_health.asgi.application"

AUTH_USER_MODEL = 'user_accounts.CustomUser'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dh_db',
        'USER': 'postgres',
        'PASSWORD': 'ayaman',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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



LOGIN_EXEMPT_URLS = (
    r'^$',
    r'^homepage/$',
    r'^pricing/',
    r'^articles/',
    r'^gallery/',
    r'^contact_us/',
    r'^user_accounts/logout_success/$',
    r'^user_accounts/register/$',
    r'^user_accounts/register-success/$',
    r'^user_accounts/auth/$',
    r'^user_accounts/password_reset/$',
    r'^user_accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    r'^user_accounts/pre-registration/$',
    r'^user_accounts/pre-info-collection/$',
    r'^user_accounts/info-submitted/$',
    r'^user_accounts/password_reset/done/$',
    r'^user_accounts/reset/done/$',
    r'^user_accounts/auto_complete_search/$',
    r'^user_accounts/registration-success/$',
    r'^user_accounts/payment_success/$',
    r'^user_accounts/payment_cancelled/$',
    r'^user_accounts/password_change/$',
    r'^user_accounts/get-user/$',
    r'^user_accounts/find_geolayout/$',
    r'^user_accounts/invoice/(?P<inv_id>\d+)/$',
    r'^user_accounts/company-registration/',
    r'^province/(?P<province_pk>\d+)/$',
    r'^legal/',
    r'^about_us/$',
    r'^frontpage_headings/read_more/$',
    r'^newsletter/newsletter_list/$',
    r'^newsletter/newsletter/$',
    r'^upcoming_events/events/$',
    r'^training_academy/create-enquiry/(?P<course_type>\d+)/$',
)


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, '../static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

LOGIN_URL = '/user_accounts/login/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field





AWS_STORAGE_BUCKET_NAME = os.environ.get('DH_TRAINING_BUCKET_NAME')
AWS_S3_REGION_NAME = 'eu-west-2'   #'us-east-2'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'      #this line enables files to be served from aws s3

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'   

STATICFILES_LOCATION = 'static'         
# STATICFILES_STORAGE = 'farmerzone.custom_storages.StaticStorage'
STATIC_URL = 'https://{}/'.format(AWS_S3_CUSTOM_DOMAIN)       #uncomment this line to enable serving from aws s3

MEDIAFILES_LOCATION = 'media'  
MEDIA_URL = 'htts://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)    

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}


SITE_ID=1


# Activate Django-Heroku.
import django_heroku
TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'
# django_heroku.settings(locals(), staticfiles=False)



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS=['https://driver-training.herokuapp.com', 'https://*.driverhealth.co.za']


