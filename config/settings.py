"""
Django settings for Visit Khorezm.

Production-ready configuration with support for:
- PostgreSQL (via DATABASE_URL) or SQLite (fallback)
- WhiteNoise for static files
- Render.com deployment
"""
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════════════
# CORE
# ═══════════════════════════════════════════════════════════════
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-visit-khorezm-change-in-production')

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        'ALLOWED_HOSTS',
        default='127.0.0.1,localhost,testserver,.onrender.com,.code.run'
    ).split(',')
    if host.strip()
]

# Production validation (soft - don't crash startup)
if not DEBUG and SECRET_KEY.startswith('django-insecure-'):
    import warnings
    warnings.warn("⚠️ Production'da SECRET_KEY env orqali sozlang!")

# ═══════════════════════════════════════════════════════════════
# APPS
# ═══════════════════════════════════════════════════════════════
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    # Local apps
    'users',
    'core',
    'hotels',
    'transport',
    'attractions',
    'events',
    'news',
    'contact',
    'restaurants',
    'tours',
    'reviews',
    'newsletter',
    'settings_app',
    'testimonials',
    'exchange_rates',
]

AUTH_USER_MODEL = 'users.User'

# ═══════════════════════════════════════════════════════════════
# MIDDLEWARE (WhiteNoise after SecurityMiddleware)
# ═══════════════════════════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ═══════════════════════════════════════════════════════════════
# DATABASE: PostgreSQL (production) or SQLite (dev)
# ═══════════════════════════════════════════════════════════════
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Render PostgreSQL
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ═══════════════════════════════════════════════════════════════
# i18n
# ═══════════════════════════════════════════════════════════════
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# ═══════════════════════════════════════════════════════════════
# STATIC FILES (WhiteNoise)
# ═══════════════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage with compression and caching
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ═══════════════════════════════════════════════════════════════
# MEDIA FILES (Cloudflare R2 - S3-compatible)
# ═══════════════════════════════════════════════════════════════
USE_R2 = config('USE_R2', default=False, cast=bool)

if USE_R2:
    # Cloudflare R2 storage
    AWS_ACCESS_KEY_ID = config('R2_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('R2_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('R2_BUCKET_NAME', default='travel-media')
    AWS_S3_ENDPOINT_URL = config('R2_ENDPOINT_URL')
    AWS_S3_REGION_NAME = 'auto'
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_DEFAULT_ACL = None  # R2 ACL qo'llab-quvvatlamaydi
    AWS_QUERYSTRING_AUTH = False  # public URL signature'siz
    AWS_S3_FILE_OVERWRITE = False
    
    # Public URL (R2.dev domen yoki custom)
    R2_PUBLIC_URL = config('R2_PUBLIC_URL').rstrip('/')
    AWS_S3_CUSTOM_DOMAIN = R2_PUBLIC_URL.replace('https://', '').replace('http://', '')
    
    # Django storages backend
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    
    MEDIA_URL = R2_PUBLIC_URL + '/'
else:
    # Local development
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# ═══════════════════════════════════════════════════════════════
# REST Framework
# ═══════════════════════════════════════════════════════════════
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
API_PAGE_SIZE = config('API_PAGE_SIZE', default=20, cast=int)
API_MAX_PAGE_SIZE = config('API_MAX_PAGE_SIZE', default=100, cast=int)

REST_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]
if DEBUG:
    REST_RENDERER_CLASSES.append('rest_framework.renderers.BrowsableAPIRenderer')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': API_PAGE_SIZE,
    'DEFAULT_RENDERER_CLASSES': REST_RENDERER_CLASSES,
    'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'contact': config('CONTACT_THROTTLE_RATE', default='5/hour'),
        'login': config('LOGIN_THROTTLE_RATE', default='10/hour'),
        'register': config('REGISTER_THROTTLE_RATE', default='5/hour'),
        'newsletter': '3/hour',
        'reviews': '10/hour',
    },
}

# ═══════════════════════════════════════════════════════════════
# JWT
# ═══════════════════════════════════════════════════════════════
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Visit Khorezm API',
    'DESCRIPTION': 'Official API for Visit Khorezm tourism portal',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ═══════════════════════════════════════════════════════════════
# SECURITY
# ═══════════════════════════════════════════════════════════════
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)

# HSTS (only in production)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)

# Render proxies requests via HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config(
        'CSRF_TRUSTED_ORIGINS',
        default='https://*.onrender.com,https://*.code.run,https://*.vercel.app'
    ).split(',')
    if origin.strip()
]

# ═══════════════════════════════════════════════════════════════
# CORS
# ═══════════════════════════════════════════════════════════════
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=DEBUG, cast=bool)
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config('CORS_ALLOWED_ORIGINS', default='').split(',')
    if origin.strip()
]

# Allow all *.onrender.com and *.vercel.app subdomains
CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^https://.*\.onrender\.com$',
    r'^https://.*\.vercel\.app$',
]

# ═══════════════════════════════════════════════════════════════
# Admin
# ═══════════════════════════════════════════════════════════════
ADMIN_SITE_HEADER = "Visit Khorezm — Admin"

# ═══════════════════════════════════════════════════════════════
# EMAIL (console backend for dev, SMTP for production)
# ═══════════════════════════════════════════════════════════════
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@visitkhorezm.uz')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@visitkhorezm.uz')
