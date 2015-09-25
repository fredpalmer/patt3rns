# coding=utf-8
from __future__ import unicode_literals
from logging.config import dictConfig

from .base import *  # noqa
from .current import *  # noqa

configure_email(sys.modules[__name__], APP_ENV)

dictConfig(LOGGING)
