"""
WSGI config for temp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patt3rns.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

# Cling intercepts static files and serves them
application = Cling(get_wsgi_application())
