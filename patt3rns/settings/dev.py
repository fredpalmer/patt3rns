# coding=utf-8
from __future__ import unicode_literals
import logging
import sys

from .base import *  # noqa

APP_ENV = get_current_app_env(lambda _: None)

SECRET_KEY = "&(kjhprmsmrnt$&fza^ml#q_x@09k9i70q-0jj*fgg5&#c1tcv"

# The default staticfiles storage, which is overridden in "deployed" environments
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SESSION_ENGINE = "django.contrib.sessions.backends.db"

LOGGING["handlers"]["console"]["level"] = logging.DEBUG

# Debugging settings
DEBUG = True
THUMBNAIL_DEBUG = True
THUMBNAIL_CHECK_CACHE_MISS = True  # Defaults to False and allows us to simply copy images from prod when doing db restores on other environments (e.g. dev and staging)

# Default to False and allow local and test settings to override
RAISE_TEMPLATE_ERRORS = False

manage_command = filter(lambda arg: arg.find("manage.py") != -1, sys.argv)

if len(manage_command):
    command = sys.argv.index(manage_command[0]) + 1
    if command < len(sys.argv):
        command = sys.argv[command]
        CELERY_ALWAYS_EAGER = (command == "shell") or (command == "test")
        CELERY_EAGER_PROPAGATES_EXCEPTIONS = CELERY_ALWAYS_EAGER
        TEST = command == "test"

if TEST:
    temp_installed_apps = list(INSTALLED_APPS)
    temp_installed_apps.append("django_nose")
    INSTALLED_APPS = tuple(temp_installed_apps)
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

    ADMINS = ()
    DATABASE_ROUTERS = []

    # Force templates to blow up if there is an error in them
    RAISE_TEMPLATE_ERRORS = True

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    }
    NOSE_ARGS = [
        "--failed",
        "--nocapture",
        "--logging-format=\"{}\"".format(LOGGING["formatters"]["verbose"]["format"]),
        "--logging-clear-handlers",
        "--with-timer",
        "--with-progressive",
    ]

    if "loggers" in LOGGING:
        loggers = LOGGING["loggers"]

        # Remove boto so that tests will reveal if any tests are not mocking boto properly
        if "boto" in loggers:
            del loggers["boto"]

        # Avoids some errors in the console about logging handlers not being found because we set these to propagate=False (so they won't duplicate in their own log files)
        if "celery" in loggers:
            del loggers["celery"]
        if "celery.task" in loggers:
            del loggers["celery.task"]

    PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )

    # Anecdotal optimization - needs to be verified but doesn't seem to speed up things during tests
    # BROKER_BACKEND = "memory"
    # EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
    import logging

    logging.disable(logging.CRITICAL)

    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    _temp_middleware = list(MIDDLEWARE_CLASSES)
    _temp_middleware.insert(_temp_middleware.index("django.contrib.auth.middleware.AuthenticationMiddleware") + 1, "debug_toolbar.middleware.DebugToolbarMiddleware")
    MIDDLEWARE_CLASSES = tuple(_temp_middleware)
    INSTALLED_APPS = INSTALLED_APPS + ("debug_toolbar", "django_extensions")

    location = None
    # Auto-detect redis-server running locally and allow developers to use it for caching/sessions
    # Only configure for Redis if it's running locally (TODO: check for non-daemonized as well?)
    pid_file = REDIS_CONF.get("pid-file")
    if pid_file and os.path.exists(REDIS_CONF.get("pid-file")):
        location = "{}:{}".format(
            REDIS_CONF.get("host", "127.0.0.1"),
            REDIS_CONF.get("port", 6739),
        )
    sock_file = REDIS_CONF.get("sock-file")
    if sock_file and os.path.exists(REDIS_CONF.get("sock-file")):
        location = "unix:/{}".format(REDIS_CONF.get("sock-file"))

    if location:
        SESSION_ENGINE = "django.contrib.sessions.backends.cache"
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "{}:{}".format(location, REDIS_CONF["databases"].get("default", 1)),
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                },
            }
        }

        # Null out the previous transport if set (e.g. to the database)
        BROKER_TRANSPORT = None
        BROKER_URL = "redis://{}/{}".format(location, REDIS_CONF["databases"].get("celery-broker"))

DEBUG_TOOLBAR_PANELS = (
    "debug_toolbar.panels.versions.VersionsPanel",
    # "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
)


def show_toolbar_callback(request):
    # This is a simple callback function for the SHOW_TOOLBAR_CALLBACK Django Debug Toolbar setting
    # Not a debug toolbar setting, but allows a simple override to hide it in local settings
    dev_override = getattr(sys.modules[__name__], "DEBUG_TOOLBAR_SHOW_TOOLBAR", True)
    return bool(request.META.get("REMOTE_ADDR") in INTERNAL_IPS and not request.is_ajax() and dev_override and DEBUG and not TEST)


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "patt3rns.settings.dev.show_toolbar_callback",
    # The private copy of jQuery no longer registers as an AMD module on sites that load RequireJS
    # http://django-debug-toolbar.readthedocs.org/en/1.3.2/changes.html?highlight=amd#id1
    # "JQUERY_URL": None,
    "ROOT_TAG_EXTRA_ATTRS": "ng-non-bindable",
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Attempt to override dev settings with any local overrides
try:
    # noinspection PyUnresolvedReferences
    from .local import *  # noqa

except ImportError:
    # import traceback
    # traceback.print_exc()
    pass


class InvalidString(str):
    def __mod__(self, other):
        from django.template.base import TemplateSyntaxError

        raise TemplateSyntaxError("Undefined variable or unknown value for: %s" % other)


if RAISE_TEMPLATE_ERRORS:

    for t in TEMPLATES:
        t["OPTIONS"]["string_if_invalid"] = InvalidString("%s")
