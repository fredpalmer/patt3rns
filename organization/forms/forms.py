import logging

from django import forms

from organization.models.models import Pattern

from patt3rns import forms as patt3rns_forms

logger = logging.getLogger(__name__)


class PatternModelForm(forms.ModelForm):
    class Meta(patt3rns_forms.ModelFormMetaBase):
        model = Pattern
