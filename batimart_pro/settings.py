"""
Django settings for batimart_pro project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv 
from django.utils.translation import gettext_lazy as _
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR=os.path.join(BASE_DIR,'static') 
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

if not DEBUG:
	SECURE_SSL_REDIRECT = True
	ADMINS = [(os.getenv('SUPER_USER'), os.getenv('EMAIL'))]
	SESSION_COOKIE_SECURE = True
	CSRF_COOKIE_SECURE = True 

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'social_django',
    'crispy_forms',
    'crispy_bootstrap4',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'modeltranslation',
    'core',
    'services',
    
    

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'requestlogs.middleware.RequestLogsMiddleware',
    'accounts.middleware.SessionTimeoutMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', default='')

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY', default='')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET', default='')

# Habilitar login social apenas se as chaves estiverem configuradas
ALLOW_SOCIAL_LOGIN = os.getenv('ALLOW_SOCIAL_LOGIN', 'False').lower() == 'true'
SITE_ID = 1

# Configurações do Provider
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGIN_REDIRECT_URL = '/dashboard/'

REST_FRAMEWORK={ 
    'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
}

# Configuração padrão de Logs 
LOGGING = { # update 03/11/2024 
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'info.log',
            'when': 'midnight',  # Rotaciona a cada meia-noite
            'backupCount': 7,  # Mantém logs dos últimos 7 dias
            'formatter': 'verbose',  # Configuração de formatação
        },
    },
    'loggers': {
        'requestlogs': {
            'handlers': ['requestlogs_to_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
}

REQUESTLOGS = {
    'SECRETS': ['password', 'token'],
    'METHODS': ('PUT', 'PATCH', 'POST', 'DELETE'),
}
AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'batimart_pro.urls'

# URLs de redirecionamento após login/logout
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'  # Redireciona para a home page após o logout

# URL da página de login
LOGIN_URL = '/accounts/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR
        ],  # Adicione esta linha
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.page_config',
                'config.context_processors.site_config',
            ],
        },
    },
]


WSGI_APPLICATION = 'batimart_pro.wsgi.application'

# Adicione estas linhas ao final do arquivo settings.py

# Configuração de timeout da sessão (em segundos)
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':os.path.join(BASE_DIR, 'db.sqlite3'),
        #'NAME': os.getenv('NAME_DB'),
        #'USER':os.getenv('USER_DB'),
        #'PASSWORD': os.getenv('PASSWORD_DB'),
        #'HOST':os.getenv('HOST_DB'),
        #'PORT':os.getenv('PORT_DB'), 
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Europe/Paris'
LANGUAGE = [
    ('fr', _('French')),
    ('en', _('English')),
    ('pt-br', _('Brazilian Portuguese')),
    ('pt', _('Portuguese')),
        
        # Adicione outros idiomas conforme necessário
    ]
LOCALE_PATHS = [
    os.path.join(BASE_DIR,  'locale'),
]

# Formatos de data e hora para França
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'd/m/Y H:i'

# Formato de moeda para Euro
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '
NUMBER_GROUPING = 3
DECIMAL_SEPARATOR = ','

# Configurações adicionais de internacionalização
LANGUAGES_BIDI = [] # Línguas da direita para esquerda
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'

# Cache para traduções
USE_I18N_CACHE = True
I18N_CACHE_KEY_PREFIX = 'i18n'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/' 



# ... outras configurações ...

# Configurações para testes
# Configurações para testes
    
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Adicione estas configurações no final do arquivo settings.py

# Configurações de e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') 
EMAIL_PORT = os.getenv('EMAIL_PORT') 
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') 
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL


