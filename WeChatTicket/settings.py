
"""
Django settings for WeChatTicket project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os
import json
import logging
import urllib.parse
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurations load from file
CONFIGS = json.loads(open(os.path.join(BASE_DIR, 'configs.json')).read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIGS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIGS['DEBUG']

# SECURITY WARNING: don't run with IGNORE_WECHAT_SIGNATURE turned on in production!
# IGNORE_WECHAT_SIGNATURE = CONFIGS['IGNORE_WECHAT_SIGNATURE']
IGNORE_WECHAT_SIGNATURE = True

# SECURITY WARNING: keep the WeChat token, appid and secret used in production secret!
WECHAT_TOKEN = CONFIGS['WECHAT_TOKEN']
WECHAT_APPID = CONFIGS['WECHAT_APPID']
WECHAT_SECRET = CONFIGS['WECHAT_SECRET']

ALLOWED_HOSTS = ['59.66.138.77', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'django.contrib.admin',

    'wechat',
    'adminpage',
    'userpage',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WeChatTicket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': False,
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

# Enable template cache when it is in production
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]


WSGI_APPLICATION = 'WeChatTicket.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONFIGS['DB_NAME'],
        'USER': CONFIGS['DB_USER'],
        'PASSWORD': CONFIGS['DB_PASS'],
        'HOST': CONFIGS['DB_HOST'],
        'PORT': CONFIGS['DB_PORT'],
        'TEST': {
            'CHARSET': 'utf8'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Site and URL
SITE_DOMAIN = CONFIGS['SITE_DOMAIN'].rstrip('/')


def get_url(path, params=None):
    full_path = urllib.parse.urljoin(SITE_DOMAIN, path)
    if params:
        return full_path + ('&' if urllib.parse.urlparse(full_path).query else '?') + urllib.parse.urlencode(params)
    else:
        return full_path


# Logging configurations
logging.basicConfig(
    format='%(levelname)-7s [%(asctime)s] %(module)s.%(funcName)s:%(lineno)d  %(message)s',
    level=logging.DEBUG if DEBUG else logging.WARNING,
)

# Django registration

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window;

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = CONFIGS["EMAIL_USE_TLS"]
EMAIL_HOST = CONFIGS["EMAIL_HOST"]
EMAIL_PORT = CONFIGS["EMAIL_PORT"]
EMAIL_HOST_USER = CONFIGS["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = CONFIGS["EMAIL_HOST_PASSWORD"]
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER