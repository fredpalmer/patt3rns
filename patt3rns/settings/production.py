import logging
from .base import *

APP_ENV = get_current_app_env(lambda _: None)

# EMAIL_PORT = 587
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""
# EMAIL_HOST = ""

RAVEN_CONFIG = {
    "dsn": "https://[user]:[password]@app.getsentry.com/[project-number]",
}

LOGGING["handlers"]["console"]["level"] = logging.INFO

