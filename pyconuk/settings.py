"""
Django settings for pyconuk project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import functools
import os

import environ
import sentry_sdk
import structlog
from django.contrib.messages import constants
from sentry_sdk.integrations.django import DjangoIntegration

from .closing_times import get_closing_time

env = environ.Env()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Used for distinguishing settings that are unset in production.
ENVVAR_SENTINAL = "not-for-production"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
SECRET_KEY = env("SECRET_KEY", default=ENVVAR_SENTINAL)
DEBUG = env("DEBUG", default=False)
ALLOWED_HOSTS = ["localhost", "2019.pyconuk.org"]


# Application definition

INSTALLED_APPS = [
    "pyconuk",
    "cfp",
    "whitenoise",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "bootstrap4",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pyconuk.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "pyconuk.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {"default": env.db(default="postgres://localhost/pyconuk")}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "{asctime} {levelname} {module} {message}", "style": "{"}
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "console"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "pyconuk": {"handlers": ["console"], "level": "INFO"},
    },
}

# http://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    timestamper,
]

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


# Authentication
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Custom User Model
AUTH_USER_MODEL = "pyconuk.User"


# Messages
# Configure messages error tag to use the value "danger" to work with
# Bootstraps alerts.
MESSAGE_TAGS = {constants.ERROR: "danger"}


# THIRD PARTY APPS
# Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]

# Sentry
sentry_sdk.init(dsn=env("SENTRY_DSN", default=None), integrations=[DjangoIntegration()])


# PROJECT SETTINGS
# Closing times
closing_time = functools.partial(get_closing_time, env)
BADGE_EDITING_CLOSE_AT = closing_time("BADGE_EDITING_CLOSE_AT")
CFP_CLOSE_AT = closing_time("CFP_CLOSE_AT")
