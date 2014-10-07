from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


DATETIME_PICKER_TEMPLATE = u"""
<div class="input-group datetimepicker">
    <input {attrs} />
    <span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span>
    </span>
</div>
"""


def datetime_input_render(instance, name, value, attrs=None):
    final_attrs = instance.build_attrs(attrs, type=instance.input_type, name=name)

    # Only add the "value" attribute if a value is non-empty.
    if value:
        # noinspection PyProtectedMember
        final_attrs["value"] = force_unicode(instance._format_value(value))

    return mark_safe(DATETIME_PICKER_TEMPLATE.format(attrs=flatatt(final_attrs)))


class DateTimeInput(forms.DateTimeInput):
    # noinspection PyShadowingBuiltins
    def __init__(self, attrs=None, format=None):
        """
        NOTE:   The format for the value (used for strptime) and the format for the datetimepicker
                must align for this to work correctly
        """
        # noinspection PyShadowingBuiltins
        format = format or "%m/%d/%Y %H:%M"
        super(DateTimeInput, self).__init__(attrs, format)

        # Sets the default format for javascript
        # if "data-date-format" not in self.attrs:
        #     self.attrs["data-date-format"] = "MM/YY/YYYY hh:mm A/PM"

        self.attrs["class"] = "form-control"

    def render(self, name, value, attrs=None):
        return datetime_input_render(self, name, value, attrs)


class DateInput(forms.DateInput):
    # noinspection PyShadowingBuiltins
    def __init__(self, attrs=None, format=None):
        """
        NOTE:   The format for the value (used for strptime) and the format for the datetimepicker
                must align for this to work correctly
        """
        # noinspection PyShadowingBuiltins
        if not format:
            format = "%m/%d/%Y"

        super(DateInput, self).__init__(attrs, format)

        # Sets the default format
        # if "data-date-format" not in self.attrs:
        #     self.attrs["data-date-format"] = format.replace("%", "").replace("m", "MM").replace("Y", "YYYY").replace("d", "YY")

        self.attrs["class"] = "form-control"
        self.attrs["data-date-pickTime"] = "false"

    def render(self, name, value, attrs=None):
        return datetime_input_render(self, name, value, attrs)


class TimeInput(forms.TimeInput):
    # noinspection PyShadowingBuiltins
    def __init__(self, attrs=None, format=None):
        """
        NOTE:   The format for the value (used for strptime) and the format for the datetimepicker
                must align for this to work correctly
        """
        format = format or "%H:%M"
        super(TimeInput, self).__init__(attrs, format)

        # Sets the default format for javascript
        # if "data-date-format" not in self.attrs:
        #     self.attrs["data-date-format"] = "HH:MM"

        self.attrs["class"] = "form-control"
        self.attrs["data-date-pickDate"] = "false"

    def render(self, name, value, attrs=None):
        return datetime_input_render(self, name, value, attrs)
