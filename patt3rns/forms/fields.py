import types

from django import forms
from patt3rns.forms import widgets as patt3rns_widgets


class CharField(forms.CharField):
    def clean(self, value):
        if isinstance(value, types.StringTypes):
            value = value.strip()

        value = super(CharField, self).clean(value)

        # Yes we do it again in after the base class runs
        if isinstance(value, types.StringTypes):
            value = value.strip()
        return value


class DateField(forms.DateField):
    widget = patt3rns_widgets.DateInput


class DateTimeField(forms.DateTimeField):
    widget = patt3rns_widgets.DateTimeInput


class TimeField(forms.TimeField):
    widget = patt3rns_widgets.TimeInput
