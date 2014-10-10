import logging

from django import forms

# from patt3rns.models import Pattern

logger = logging.getLogger(__name__)


# noinspection PyClassHasNoInit
class ModelFormMetaBase:
    abstract = True
    fields = "__all__"
    localized_fields = "__all__"


# class PatternModelForm(forms.ModelForm):
#
#     class Meta(ModelFormMetaBase):
#         model =  Pattern
