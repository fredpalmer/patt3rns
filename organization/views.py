# coding=utf-8
from __future__ import unicode_literals
import logging

from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class IdentityHome(TemplateView):
    template_name = "organization/index.html"
