# Agregar al inicio:
from pathlib import Path
from decouple import config
import os
import sys

# Fix para Python 3.13 con psycopg2 - DEBE IR ANTES DE CUALQUIER IMPORT DE DJANGO
if sys.version_info >= (3, 13):
    import locale
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    
    # Configurar locale para evitar problemas de encoding con psycopg2
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Cambiar SECRET_KEY:
SECRET_KEY = config('SECRET_KEY')

# Cambiar DEBUG:
DEBUG = config('DEBUG', default=False, cast=bool)

# Cambiar ALLOWED_HOSTS:
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Custom User Model
AUTH_USER_MODEL = 'usuarios.Usuario'

# En INSTALLED_APPS agregar:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    
    # Local apps
    'apps.usuarios',
    'apps.ciudadanos',
    'apps.denuncias',
    'apps.personal',
    'apps.notificaciones',
    'apps.reportes',
    'apps.categorias',
]

# En MIDDLEWARE agregar CORS:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Agregar esto
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Configurar base de datos:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 0,
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'TIME_ZONE': None,
    }
}

# Password validation
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
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Al final del archivo agregar:

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # Sin autenticación por defecto
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Todos los endpoints públicos por defecto
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
CORS_ALLOW_CREDENTIALS = True

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config('JWT_REFRESH_TOKEN_LIFETIME', default=1440, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')