# coding=utf-8
from __future__ import unicode_literals
from inspect import getsourcefile
import socket
import os

from django.core.urlresolvers import reverse_lazy

DOMAIN = "patt3rns.com"

EMAIL_ADDRESSES = {
    "support": "support@{}".format(DOMAIN),
    "no-reply": "no-reply@{}".format(DOMAIN),
}

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".{}".format(DOMAIN),  # Allow domain and subdomains
    ".{}.".format(DOMAIN),  # Also allow FQDN and subdomains
    ".elb.amazonaws.com",  # Allow domain and subdomains for AWS ELB
    ".elb.amazonaws.com.",  # Allow domain and subdomains for AWS ELB
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

BASE_DIR = os.path.abspath(os.path.curdir)
REPO_NAME = os.path.basename(BASE_DIR)

PROJECT_ROOT_APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

DEBUG = False

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
SERVER_EMAIL = "server_exceptions@%s" % socket.gethostname()

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = EMAIL_ADDRESSES["no-reply"]

LOGIN_URL = reverse_lazy("account_login")
LOGOUT_URL = reverse_lazy("logout")
LOGIN_REDIRECT_URL = reverse_lazy("dashboard")

# DATE_FORMAT
DATETIME_FORMAT = "Y-m-d H:i:s O"
# SHORT_DATE_FORMAT
# SHORT_DATETIME_FORMAT
TIME_INPUT_FORMATS = (
    "%H:%M:%S",  # "14:30:59"
    "%H:%M",  # "14:30"
    "%I:%M%p",  # "2:30PM"
    "%I:%M %p",  # "2:30 PM"
)

DATETIME_INPUT_FORMATS = (
    "%Y-%m-%d %H:%M:%S",  # "2006-10-25 14:30:59"
    "%Y-%m-%d %H:%M:%S.%f",  # "2006-10-25 14:30:59.000200"
    "%Y-%m-%d %H:%M",  # "2006-10-25 14:30"
    "%Y-%m-%d %I:%M %p",  # "2006-10-25 4:30 PM"
    "%Y-%m-%d %I:%M%p",  # "2006-10-25 4:30PM"
    "%Y-%m-%d",  # "2006-10-25"
    "%m/%d/%Y %H:%M:%S",  # "10/25/2006 14:30:59"
    "%m/%d/%Y %I:%M:%S %p",  # "10/25/2006 4:30:59 PM"
    "%m/%d/%Y %I:%M:%S%p",  # "10/25/2006 4:30:59PM"
    "%m/%d/%Y %H:%M:%S.%f",  # "10/25/2006 14:30:59.000200"
    "%m/%d/%Y %H:%M",  # "10/25/2006 14:30"
    "%m/%d/%Y %I:%M %p",  # "10/25/2006 4:30 PM"
    "%m/%d/%Y %I:%M%p",  # "10/25/2006 4:30PM"
    "%m/%d/%Y",  # "10/25/2006"
    "%m/%d/%y %H:%M:%S",  # "10/25/06 14:30:59"
    "%m/%d/%y %H:%M:%S.%f",  # "10/25/06 14:30:59.000200"
    "%m/%d/%y %H:%M",  # "10/25/06 14:30"
    "%m/%d/%y",  # "10/25/06"
    "%Y-%m-%dT%H:%M:%S.%f",  # "2013-06-16T19:30:23.703"  Added to support HTML5 datetime-local input type
    "%Y-%m-%dT%H:%M:%S",  # "2013-06-16T19:30:23"  Added to support HTML5 datetime-local input type
    "%Y-%m-%dT%H:%M",  # "2013-06-16T19:30"  Added to support HTML5 datetime-local input type
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
# NOTE: if we switch this to true then we need to make sure all time fields work
#       - the localized formats will take precedence over anything in the settings file
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
# It must end in a slash if set to a non-empty value.
MEDIA_URL = "/uploaded/"

# The absolute path to the directory where collectstatic will collect static files for deployment.
# This should be an (initially empty) destination directory for collecting your static files from their
# permanent locations into one directory for ease of deployment; it is not a place to store your static
# files permanently. You should do that in directories that will be found by staticfiles’s finders, which
# by default, are 'static/' app sub-directories and any directories you include in STATICFILES_DIRS).
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# URL to use when referring to static files located in STATIC_ROOT.
# Example: "/static/" or "http://static.example.com/"
# If not None, this will be used as the base path for asset definitions (the Media class) and the staticfiles app.
# It must end in a slash if set to a non-empty value.
# You may need to configure these files to be served in development and will definitely need to do so in production.
STATIC_URL = "/m/"

# This is not a Django built-in setting.  We use it stamp static assets during deployment with a version. During
# a build process one would simply get the sha of the current revision being built
STATIC_FILES_VERSION = "EATDEADBEEF"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "{}.db".format(REPO_NAME)),
    }
}

# Heroku setup database
if os.environ.get("DATABASE_URL"):
    # Parse database configuration from $DATABASE_URL
    import dj_database_url

    DATABASES["default"] = dj_database_url.config()

# The list of finder backends that know how to find static files in various locations.
# The default will find files stored in the STATICFILES_DIRS setting (using django.contrib.staticfiles.finders.FileSystemFinder)
# and in a static subdirectory of each app (using django.contrib.staticfiles.finders.AppDirectoriesFinder).
# If multiple files with the same name are present, the first file that is found will be used.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "pipeline.finders.AppDirectoriesFinder",
    "pipeline.finders.FileSystemFinder",
    "pipeline.finders.PipelineFinder",
)

# This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder
# is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
# Don't forget to use absolute paths, not relative paths.
# Always use forward slashes, even on Windows.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "lib", "bower_components"),
)

# Used by the django template context processor to put the appropriate debug value in a template's context
INTERNAL_IPS = ("127.0.0.1",)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            os.path.join(PROJECT_ROOT_APP_DIR, "templates"),
            os.path.join(PROJECT_ROOT_APP_DIR, "templates", "account"),
        ),
        "OPTIONS": {
            "loaders": (
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ),
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    },
]

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

ROOT_URLCONF = "patt3rns.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "patt3rns.wsgi.application"

INSTALLED_APPS = (
    # Django apps should be installed first in general (e.g. if User model app registration needed for signals)
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "patt3rns",
    "portal",
    "organization",
    "pipeline",
    "rest_framework",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# The user is required to enter a username when signing up. Note that the
# user will be asked to do so even if ACCOUNT_AUTHENTICATION_METHOD is set
# to email. Set to False when you do not wish to prompt the user to enter a
# username.
ACCOUNT_USERNAME_REQUIRED = False

# The user is required to hand over an e-mail address when signing up.
ACCOUNT_EMAIL_REQUIRED = True

# Specifies the login method to use -- whether the user logs in by entering
# his username, e-mail address, or either one of both. Possible values
# are "username" | "email" | "username_email"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# A string pointing to a custom form class (e.g. "myapp.forms.SignupForm")
# that is used during signup to ask the user for additional input
# (e.g. newsletter signup, birth date). This class should implement a
# "save" method, accepting the newly signed up user as its only parameter.
# ACCOUNT_SIGNUP_FORM_CLASS = "identity.forms.SignupForm"

# A callable (or string of the form "some.module.callable_name") that takes
# a user as its only argument and returns the display name of the user. The
# default implementation returns user.username.
ACCOUNT_USER_DISPLAY = lambda user: user.email

# Attempt to bypass the signup form by using fields (e.g. username, email)
# retrieved from the social account provider. If a conflict arises due to a
# duplicate e-mail address the signup form will still kick in.
# Set to False for flow through to any custom forms after signup
# SOCIALACCOUNT_AUTO_SIGNUP = False

# SOCIALACCOUNT_PROVIDERS = {
#     "facebook": {
#         "SCOPE": ["email", "publish_stream", "manage_pages"],
#         "METHOD": "oauth2"
#     }
# }
# endregion django-allauth settings

RAVEN_CONFIG = {
    "dsn": "http://public:secret@example.com/1",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s: %(levelname)s/%(processName)s] - %(name)s - %(message)s",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "null": {
            "level": "NOTSET",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "NOTSET",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # NOTE: This is typically level:ERROR.  However, this let's Sentry manage the emails for most errors
        "mail_admins": {
            "level": "CRITICAL",
            "filters": ["require_debug_false", ],
            "class": "django.utils.log.AdminEmailHandler"
        },
        # http://raven.readthedocs.org/en/latest/config/logging.html
        # So error, exception, critical get sent to Sentry as well
        "sentry": {
            "level": "ERROR",
            "filters": ["require_debug_false", ],
            "class": "logging.NullHandler",
            # If one decides to use Sentry, then replace the previous line with the following:
            # "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },

    },
    "root": {
        "handlers": ["console", "mail_admins", "sentry"],
        "level": "NOTSET",
    },
    "loggers": {
        "django": {
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "level": "DEBUG",
            "propagate": True,
        },
        "django.db.backends": {
            "level": "ERROR",
            "propagate": True,
        },
        "boto": {
            "level": "ERROR",
            "propagate": True,
        },
        "py.warnings": {
            "handlers": ["console"],
            "propagate": False,
        },
    }
}

# Django f's up logging by trying by merging our with theirs even though we specify to disable_existing_loggers
# http://stackoverflow.com/questions/20282521/django-request-logger-not-propagated-to-root
# We need to do this ourselves at the end of settings evaluation by simply calling dictConfig with the logging settings
LOGGING_CONFIG = None

TEST = False

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# noinspection PyUnresolvedReferences
PIPELINE_YUGLIFY_BINARY = os.path.join(BASE_DIR, "node_modules", ".bin", "yuglify")
PIPELINE_JS_COMPRESSOR = "pipeline.compressors.uglifyjs.UglifyJSCompressor"
PIPELINE_UGLIFYJS_BINARY = os.path.join(BASE_DIR, "node_modules", ".bin", "uglifyjs")

# These are custom settings that are not part of pipeline
APP_PIPELINE_OUTPUT_DIR = "pipeline"
APP_PIPELINE_CSS_DIR = os.path.join(APP_PIPELINE_OUTPUT_DIR, "css")
APP_PIPELINE_JS_DIR = os.path.join(APP_PIPELINE_OUTPUT_DIR, "js")

PIPELINE_CSS = {
    "api": {
        "source_filenames": (
            "bootstrap/dist/css/bootstrap.min.css",
        ),
        "output_filename": os.path.join(APP_PIPELINE_CSS_DIR, "api.css"),
    },
    "app": {
        "source_filenames": (
            "bootstrap/dist/css/bootstrap.min.css",
            "bootstrap/dist/css/bootstrap-theme.min.css",
            "css/app.css",
        ),
        "output_filename": os.path.join(APP_PIPELINE_CSS_DIR, "base.css"),
    },
    "design": {
        "source_filenames": (
            "bootstrap/dist/css/bootstrap.min.css",
            "bootstrap/dist/css/bootstrap-theme.min.css",
            "css/design.css",
        ),
        "output_filename": os.path.join(APP_PIPELINE_CSS_DIR, "design.css"),
    },
    "portal": {
        "source_filenames": (
            "bootstrap/dist/css/bootstrap.min.css",
            "bootstrap/dist/css/bootstrap-theme.min.css",
            "css/portal.css",
        ),
        "output_filename": os.path.join(APP_PIPELINE_CSS_DIR, "base-portal.css"),
    },
}

PIPELINE_JS = {
    "api": {
        "source_filenames": (
            "jquery/dist/jquery.js",
            "bootstrap/dist/js/bootstrap.js",
        ),
        "output_filename": os.path.join(APP_PIPELINE_JS_DIR, "api.js"),
    },
    "app": {
        "source_filenames": (
            "knockout/dist/knockout.js",
            "knockout-mapping/knockout.mapping.js",
            "jquery/dist/jquery.js",
            "jquery.cookie/jquery.cookie.js",
            "bootstrap/dist/js/bootstrap.js",
            "js/app.js",
            "moment/min/moment.min.js",
            "js/ajax-setup.js",
            "js/aui/aui-min.js",
        ),
        "output_filename": os.path.join(APP_PIPELINE_JS_DIR, "base.js"),
    },
    "portal": {
        "source_filenames": (
            "jquery/dist/jquery.min.js",
            "bootstrap/dist/js/bootstrap.min.js",
            "js/portal.js",
        ),
        "output_filename": os.path.join(APP_PIPELINE_JS_DIR, "base-portal.js"),
    },
}

# To test bundling locally, set this in a local settings file and run collectstatic.
# PIPELINE_ENABLED = True

# Used to map template directory for simple indexing of static html
DESIGNER_PLAYGROUND = "design"

REDIS_CONF = {
    "databases": {
        "default": 1,
        # This should be a different database number than the cache uses
        "celery-broker": 2,
        "staticfiles": 3,
    },
    "pid-file": "/usr/local/var/run/{}-redis.pid".format(REPO_NAME),
    "sock-file": "/tmp/{}-redis.sock".format(REPO_NAME),
    "host": "127.0.0.1",
    "port": 6379,
}


def configure_email(this_module, app_environment):
    admins = (("{} Admin".format(DOMAIN), "admin+{}@{}".format(app_environment, DOMAIN)),)
    email_subject_prefix = "[Django ({} {})] ".format(DOMAIN, app_environment.upper())

    setattr(this_module, "ADMINS", admins)
    setattr(this_module, "MANAGERS", admins)
    setattr(this_module, "EMAIL_SUBJECT_PREFIX", email_subject_prefix)


def get_current_app_env(obj):
    """
    This function has to be defined in the module that calls it to work properly
    :return: The current application environment (e.g. dev, staging, production)
    """
    if not obj:
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured("obj must be defined in the settings module calling this function, e.g.:  get_current_app_env(lambda _: None)")

    source_file = getsourcefile(obj)
    source_file = os.path.basename(os.path.realpath(source_file))
    return source_file[:-3]
