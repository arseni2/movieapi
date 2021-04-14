from pathlib import Path
import datetime
import time
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#m@)f!-m277pbmj1(u&o_ye1do_b_+ciez4&4gr1n%oeeri(2a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
AUTH_USER_MODEL = 'apiapp.User'
ALLOWED_HOSTS = ['herokuapp.com', 'react-movie-django']
ACCOUNT_EMAIL_REQUIRED = False
import django_heroku
django_heroku.settings(locals())
# Application definition
APPEND_SLASH=False
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_jwt',
    'oauth2_provider',
    'django_filters',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'apiapp.apps.ApiappConfig',
    'rest_framework_simplejwt',
    'rest_framework_json_api',
]
SITE_ID = 1
REST_REGISTRATION = {
    'REGISTER_VERIFICATION_ENABLED': False,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_ENABLED': False,
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apiapp.back.back',

]

ROOT_URLCONF = 'api.urls'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True
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

WSGI_APPLICATION = 'api.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3"))
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

REST_FRAMEWORK = {
    #'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAdminUser',
        #'rest_framework.permissions.AllowAny',
    #),
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    #'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    #'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    #'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}


JWT_AUTH = {
     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=604800),
     'JWT_ALLOW_REFRESH': True,
     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),  # default
     'JWT_AUTH_HEADER_PREFIX': 'Barear'
 }
AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # 'social_core.backends.vk.VKOAuth2',
    # 'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

DJOSER = {
     'SEND_ACTIVATION_EMAIL': False,
     'SEND_CONFIRMATION_EMAIL': True,
     'ACTIVATION_URL': '#/activate/{uid}/{token}/',
     'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
     'PASSWORD_RESET_CONFIRM_URL': 'auth/reset/confirm/{uid}/{token}/',
     'TOKEN_MODEL': None
 }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = 'arsenij633@gmail.com'
EMAIL_HOST_PASSWORD = 'qwerty123098+'
#EMAIL_PORT = 465
#EMAIL_USE_SSL = True
#EMAIL_USE_TSL = False
EMAIL_PORT = 587
EMAIL_USE_TLS = True

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
