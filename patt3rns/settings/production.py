# coding=utf-8
from __future__ import unicode_literals
import logging

from .base import *  # noqa

APP_ENV = get_current_app_env(lambda _: None)

RAVEN_CONFIG = {
    "dsn": "https://[user]:[password]@app.getsentry.com/[project-number]",
}

LOGGING["handlers"]["console"]["level"] = logging.INFO
