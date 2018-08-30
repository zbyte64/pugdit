"""
Django settings for myproject project.

Generated by 'yo django-rest'.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env( # set default values and casting
    DEBUG=(bool, False),
    DEPLOYMENT=(str, 'prod'),
    SECRET_KEY=(str, 'h4@c1x9okapu5^#iurp21i(vn14s5c#1lqx!$k-#^v%rd#rn!b'),
    SITE_ID=(int, 1),
)

# Build paths inside the project like this: base('desired/local/path')
# - the path containing manage.py
#   (e.g. ~/code/pugdit)
base = environ.Path(__file__) - 2 # two folders back (/a/b/ - 2 = /)
BASE_DIR = base()
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# - the Django project root containing settings.py
# (e.g. ~/code/pugdit/pugdit)
root = environ.Path(__file__) - 1
PROJECT_ROOT = root()
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(env_file=base('.env')) # reading .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: set a SECRET_KEY environment variable to a secret value
# before deploying to production!
SECRET_KEY = env('SECRET_KEY') # default used if not in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG') # False if not in os.environ

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'graphene_django',
    'corsheaders',
    'anymail',
    'debug_toolbar',
    'django_extensions',

    'pugdit.postoffice',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.agave',
    'allauth.socialaccount.providers.amazon',
    'allauth.socialaccount.providers.angellist',
    'allauth.socialaccount.providers.asana',
    'allauth.socialaccount.providers.auth0',
    'allauth.socialaccount.providers.authentiq',
    'allauth.socialaccount.providers.baidu',
    'allauth.socialaccount.providers.basecamp',
    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.bitbucket_oauth2',
    'allauth.socialaccount.providers.bitly',
    'allauth.socialaccount.providers.cern',
    'allauth.socialaccount.providers.coinbase',
    'allauth.socialaccount.providers.dataporten',
    'allauth.socialaccount.providers.daum',
    'allauth.socialaccount.providers.digitalocean',
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.disqus',
    'allauth.socialaccount.providers.douban',
    'allauth.socialaccount.providers.draugiem',
    'allauth.socialaccount.providers.dropbox',
    'allauth.socialaccount.providers.dwolla',
    'allauth.socialaccount.providers.edmodo',
    'allauth.socialaccount.providers.eveonline',
    'allauth.socialaccount.providers.evernote',
    'allauth.socialaccount.providers.feedly',
    'allauth.socialaccount.providers.fivehundredpx',
    'allauth.socialaccount.providers.flickr',
    'allauth.socialaccount.providers.foursquare',
    'allauth.socialaccount.providers.fxa',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.hubic',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.line',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.mailru',
    'allauth.socialaccount.providers.mailchimp',
    'allauth.socialaccount.providers.meetup',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.odnoklassniki',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.orcid',
    'allauth.socialaccount.providers.paypal',
    'allauth.socialaccount.providers.persona',
    'allauth.socialaccount.providers.pinterest',
    'allauth.socialaccount.providers.reddit',
    'allauth.socialaccount.providers.robinhood',
    'allauth.socialaccount.providers.shopify',
    'allauth.socialaccount.providers.slack',
    'allauth.socialaccount.providers.soundcloud',
    'allauth.socialaccount.providers.spotify',
    'allauth.socialaccount.providers.stackexchange',
    'allauth.socialaccount.providers.stripe',
    'allauth.socialaccount.providers.trello',
    'allauth.socialaccount.providers.tumblr',
    'allauth.socialaccount.providers.twentythreeandme',
    'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.untappd',
    'allauth.socialaccount.providers.vimeo',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.weixin',
    'allauth.socialaccount.providers.windowslive',
    'allauth.socialaccount.providers.xing',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'spa.middleware.SPAMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # early, but after Gzip
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_REDIRECT_URL = '/accounts/login/'

ROOT_URLCONF = 'pugdit.urls'

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

WSGI_APPLICATION = 'pugdit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Celery settings
BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')

DEPLOYMENT = env('DEPLOYMENT')

if DEPLOYMENT == 'dev':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    CELERY_ALWAYS_EAGER = True # run tasks in same thread for development
    #CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    ADMINS = (('admin', 'admin@localhost'),)
else: # DEPLOYMENT == prod
    # SECURE_SSL_REDIRECT = True
    # add extra apps
    # INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    pass

# Media storage backend
try:
    BACKBLAZEB2_ACCOUNT_ID = env('BACKBLAZEB2_ACCOUNT_ID')
    BACKBLAZEB2_APP_KEY = env('BACKBLAZEB2_APP_KEY')
    BACKBLAZEB2_BUCKET_NAME = env('BACKBLAZEB2_BUCKET')
    DEFAULT_FILE_STORAGE = 'b2_storage.storage.B2Storage'
    # INSTALLED_APPS.append('b2_storage.authorise')
except ImproperlyConfigured: # use the default file storage to disk
    MEDIA_ROOT = root('media')
    MEDIA_URL = '/media/'

# Email sending
try:
    ANYMAIL = {
        # (exact settings here depend on your ESP...)
        "MAILGUN_API_KEY": env('MAILGUN_API_KEY'),
        # your Mailgun domain, if needed:
        "MAILGUN_SENDER_DOMAIN": env('MAILGUN_DOMAIN'),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    # or sendgrid.EmailBackend, or...
except ImproperlyConfigured:
    EMAIL_CONFIG = env.email_url(
        'EMAIL_URL', default='consolemail://')
    vars().update(EMAIL_CONFIG)


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
# set your local time zone to more easily analyse data on the backend
TIME_ZONE = 'Europe/Zagreb'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (base('pugboat/dist'),)

# Django SPA - simple setup for serving modern SPAs from Django
# https://github.com/metakermit/django-spa
STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

from .logger import LOGGING

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Django REST Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Django debug toolbar
INTERNAL_IPS = ['127.0.0.1']

# CORS header settings
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    #'example.com', # your domain
    'localhost:3000',
    '127.0.0.1:3000',
    'localhost:8000',
    '127.0.0.1:8000',
    'localhost:8081',
    '127.0.0.1:8081',
)
# CORS_ALLOW_CREDENTIALS = True

GRAPHENE = {
    # Where your Graphene schema lives
    'SCHEMA': 'pugdit.postoffice.schema.schema'
}

TEST_RUNNER = 'snapshottest.django.TestRunner'


# https://github.com/ipfs/notes/issues/15
SERVICE_BLOCKNAME = 'TODO'
IPFS_URL = env('IPFS_URL')
IPFS_API = env('IPFS_API')
SITE_ID = env('SITE_ID')
