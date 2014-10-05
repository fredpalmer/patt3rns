import logging
import sys
from .base import *

APP_ENV = get_current_app_env(lambda _: None)

SECRET_KEY = "&(kjhprmsmrnt$&fza^ml#q_x@09k9i70q-0jj*fgg5&#c1tcv"

# The default staticfiles storage, which is overridden in "deployed" environments
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SESSION_ENGINE = "django.contrib.sessions.backends.db"

LOGGING["handlers"]["console"]["level"] = logging.DEBUG

# Debugging settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = True
THUMBNAIL_CHECK_CACHE_MISS = True  # Defaults to False and allows us to simply copy images from prod when doing db restores on other environments (e.g. dev and staging)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": REPO_NAME,
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": 3306,
    }
}

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
    class InvalidString(str):
        def __mod__(self, other):
            from django.template.base import TemplateSyntaxError

            raise TemplateSyntaxError("Undefined variable or unknown value for: %s" % other)

    TEMPLATE_STRING_IF_INVALID = InvalidString("%s")

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

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "patt3rns.utils.show_toolbar_callback",
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Attempt to override dev settings with any local overrides
try:
    # noinspection PyUnresolvedReferences
    from .local import *

except ImportError:
    # import traceback
    # traceback.print_exc()
    pass
