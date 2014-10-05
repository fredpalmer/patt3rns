""" Settings for patt3rns """
from logging.config import dictConfig
from .base import *
from .current import *

configure_email(sys.modules[__name__], APP_ENV)

dictConfig(LOGGING)
