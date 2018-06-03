import os
from sys import path
from os.path import join


from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path.append(join(BASE_DIR, 'apps'))

ALLOWED_HOSTS = ['159.89.10.37', 'localhost', '0.0.0.0', '94.130.58.239', '172.17.0.1']

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
'rest_framework',
    # 'allauth.socialaccount.providers.twitter',

    # rest cors support
    'corsheaders',
    'object_detection_api',
    'face_recognition_api',
    
]

THIRD_PARTY_APPS = [
   # "django_extensions",
    "rest_framework_swagger",
]

LOCAL_APPS = [
   
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates")
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = "static/"
STATICFILES_DIRS = [
    #
]

LOGIN_REDIRECT_URL = reverse_lazy("app")
LOGIN_URL = reverse_lazy("app")



SITE_ID = 1

## User Authentication Settings

ACCOUNT_ADAPTER = 'users.adapter.MyAccountAdapter'
# Following is added to enable registration with email instead of username
AUTHENTICATION_BACKENDS = (
 # Needed to login by username in Django admin, regardless of `allauth`
 "django.contrib.auth.backends.ModelBackend",

 # `allauth` specific authentication methods, such as login by e-mail
 "allauth.account.auth_backends.AuthenticationBackend",
)

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer'
}

REST_SESSION_LOGIN = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_USERNAME_REQUIRED = True
LOGOUT_ON_PASSWORD_CHANGE = False




REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework.authentication.TokenAuthentication',

    ),
'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '9999999999999999/day',
        'user': '9999999999999999/day'
    }
}


# Change CORS settings as needed

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'localhost:9000',
    '172.17.0.1:9000'
)

CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?://)?localhost',
    r'^(https?://)?127.',
)

# Email Settings
#EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'bla.info@gmail.com'
#EMAIL_HOST_PASSWORD = 'pass'
#EMAIL_PORT = 587

#EMAIL_FILE_PATH = 'tmp/emails'
#DEFAULT_FROM_EMAIL = 'bla.info@gmail.com'
#SERVER_EMAIL = 'bla.info@gmail.com'
