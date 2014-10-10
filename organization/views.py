# Create your views here.
import logging

from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class IdentityHome(TemplateView):
    template_name = "organization/index.html"
