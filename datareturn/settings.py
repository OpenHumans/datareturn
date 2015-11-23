import os

from django.conf import global_settings

from env_tools import apply_env


# Apply the environment variables in the .env file.
apply_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Required by django-allauth
    'django.contrib.sites',

    # Main app for this site.
    'datareturn',

    # Third party apps
    'allauth',
    'allauth.account',
    'markdown_deux',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Allow login with token instead of password.
    'datareturn.backends.UserTokenBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'datareturn.urls'

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
                # We use Sites and associated config to customize templates.
                'datareturn.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'datareturn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Sites required by django-allauth.
SITE_ID = 1

# Open Humans base URL. Defaults to main site, can be changed for dev purposes.
OPEN_HUMANS_SERVER = os.getenv('OPEN_HUMANS_SERVER', 'https://www.openhumans.org')

OPEN_HUMANS_REDIRECT_URI = os.getenv('OPEN_HUMANS_REDIRECT_URI')

OPEN_HUMANS_CLIENT_ID = os.getenv('OPEN_HUMANS_CLIENT_ID')
OPEN_HUMANS_CLIENT_SECRET = os.getenv('OPEN_HUMANS_CLIENT_SECRET')

# File storage on S3 and AWS credentials.
DEFAULT_FILE_STORAGE = 'datareturn.models.PrivateStorage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_S3_STORAGE_BUCKET_NAME')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = 'staticfiles'

# Settings for django-allauth and account interactions.
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = 'home'

############################################################
# Heroku settings
if os.getenv('HEROKU_SETUP') in ['true', 'True']:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # Allow all host headers
    ALLOWED_HOSTS = ['*']

# Email set up.
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', global_settings.EMAIL_BACKEND)
if os.getenv('EMAIL_USE_TLS') in ['true', 'True']:
    EMAIL_USE_TLS = True
else:
    EMAIL_USE_TLS = global_settings.EMAIL_USE_TLS
EMAIL_HOST = os.getenv('EMAIL_HOST', global_settings.EMAIL_HOST)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', global_settings.EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD',
                                global_settings.EMAIL_HOST_PASSWORD)
EMAIL_PORT = int(os.getenv('EMAIL_PORT', str(global_settings.EMAIL_PORT)))
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', global_settings.DEFAULT_FROM_EMAIL)
