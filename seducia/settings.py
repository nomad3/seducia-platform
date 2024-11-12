# seducia/settings.py

import os
import environ
from pathlib import Path

# Inicializar django-environ
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Aplicaciones instaladas
INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps de terceros
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    # Aplicaciones locales
    'main_app',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Agregar protección CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'seducia.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directorio de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Context processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Requerido por admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'seducia.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Configuración de LangChain y LangSmith
LANGCHAIN_API_KEY = env('LANGCHAIN_API_KEY', default='')
LANGSMITH_API_KEY = env('LANGSMITH_API_KEY', default='')

# Claves de API de redes sociales
SOCIAL_MEDIA_API_KEYS = {
    "facebook": env("FACEBOOK_API_KEY", default=""),
    "instagram": env("INSTAGRAM_API_KEY", default=""),
    "tinder": env("TINDER_API_KEY", default=""),
    "threads": env("THREADS_API_KEY", default=""),
    "grinder": env("GRINDER_API_KEY", default=""),
}

# Campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuraciones de seguridad adicionales
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
X_FRAME_OPTIONS = 'DENY'

# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{',},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose',},
    },
    'root': {'handlers': ['console'], 'level': 'INFO',},
}
SOCIAL_MEDIA_API_KEYS = {
    "facebook": env("FACEBOOK_API_KEY", default=""),
    "instagram": env("INSTAGRAM_API_KEY", default=""),
    # ... otras plataformas ...
}