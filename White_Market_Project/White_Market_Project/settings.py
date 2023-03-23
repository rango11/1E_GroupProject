"""
Django settings for White_Market_Project project.

Generated by 'django-admin startproject' using Django 2.2.28.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
ALLOWED_FILE_TYPES = ['jpeg', 'jpg','png']

# For use in future
#USER_PROFILE_PHOTO_DIR = os.path.join(MEDIA_DIR, 'user_profile_photos')
USER_PROFILE_PHOTO_DIR = os.path.join(BASE_DIR, 'media/user_profile_photos')

ITEM_PHOTO_DIR = os.path.join(BASE_DIR, 'media/item_photos')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$@6=6p3#0z2s3m&-0r#%hn05!qk!_fa@4d5v+es*l+j!oizfhr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["fkgsoftware.pythonanywhere.com", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'WhiteMarket',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'White_Market_Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '1E_GroupProject', 'White_Market_Project', 'templates')],
        # 'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # Check/add this line!
                'WhiteMarket.context_processors.inSellers',
                'WhiteMarket.context_processors.getStores',
                ],
        },
    },
]

WSGI_APPLICATION = 'White_Market_Project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR, ]

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

# Start for media files
USER_PROFILE_PHOTO_ROOT = USER_PROFILE_PHOTO_DIR
USER_PROFILE_PHOTO_URL = "/media/user_profile_photos/"

ITEM_PHOTO_ROOT = ITEM_PHOTO_DIR
ITEM_PHOTO_URL = "/media/item_photos/"

LOGIN_REDIRECT_URL = "whitemarket/index"
LOGOUT_REDIRECT_URL = "index"

RECAPTCHA_PUBLIC_KEY = '6LcSvB0lAAAAAHTPYJYy09cRKsZgzbEIufwH9bL5'
RECAPTCHA_PRIVATE_KEY = '6LcSvB0lAAAAAHW35u43VFWCJaVQb1yaSePA9zc8'
