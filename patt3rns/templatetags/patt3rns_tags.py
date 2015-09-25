# coding=utf-8
from __future__ import unicode_literals
import logging
import re
import types

import bs4
from django import forms, template
from django.template import defaultfilters, Node
from django.forms.forms import BoundField

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter(name="object_type")
def object_type(arg):
    output = u""
    if isinstance(arg, object):
        output = arg.__class__.__name__
    else:
        logger.warning("Parameter => \"%s\" was not an object, no action was taken", arg)
    return output


@register.filter(name="input_type")
def input_type(field, value):
    if isinstance(value, types.StringTypes):
        if isinstance(field, BoundField):
            field.field.widget.input_type = value
            logger.debug("Changed input widget type to => %s", value)
        else:
            logger.warning("%s was not a field (no action was taken)", field)
    else:
        logger.warning("%s name_value param was incorrect (no action was taken)", field)

    return field


@register.filter(name="required")
def required(field):
    if isinstance(field, BoundField):
        if field.field.required:
            attrs = field.field.widget.attrs
            attrs["required"] = "required"
            logger.debug("Added required attribute to field => %s", field.name)
    else:
        logger.warning("%s was not a field (no action was taken)", field)
    return field


@register.filter(name="attr")
def attr(field, name_value):
    """
    Adds an attribute to the field's widget
    """
    if isinstance(name_value, types.StringTypes):
        if isinstance(field, BoundField) and isinstance(name_value, types.StringTypes):
            attrs = field.field.widget.attrs
            # noinspection PyUnresolvedReferences
            parts = name_value.split("=")
            if len(parts) == 2:
                attr_key = parts[0]
                attr_value = parts[1]
                logger.debug("Added attribute %s=%s to field %s", attr_key, attr_value, field.name)
                attrs[attr_key] = attr_value
            else:
                logger.warning("\"%s\" was not a parseable value. Use key=value (no action was taken)", name_value)
        else:
            logger.warning("%s was not a field (no action was taken)", field)
    else:
        logger.warning("%s name_value param was incorrect (no action was taken)", field)

    return field


@register.filter(name="data")
def data(field, value):
    """
    Adds data attributes to the field
    """
    return attr(field, "data-%s" % value)


@register.filter(name="placeholder")
def placeholder(field, custom_placeholder=None):
    """
    Adds placeholder text to the field using custom_placeholder or defaults to the label
    """
    if isinstance(field, BoundField):
        attrs = field.field.widget.attrs
        attrs["placeholder"] = custom_placeholder or defaultfilters.striptags(field.help_text) or field.label
        if field.field.required:
            attrs["required"] = "required"
    else:
        logger.warning("%s was not a field, no action was taken", field)

    return field


@register.filter(name="class")
def add_class(form_or_field, klass_name):
    """
    Adds a class to the field or each field in a form for rendering
    """

    def _add_class(bf, name_of_class):
        attrs = bf.field.widget.attrs
        classes = attrs.get("class")
        if not classes:
            classes = [name_of_class, ]
        else:
            classes = classes.split(" ")
            classes.append(name_of_class)
            classes = list(set(classes))

        attrs["class"] = " ".join(classes)

    if isinstance(form_or_field, forms.BaseForm):
        for bound_field in form_or_field:
            _add_class(bound_field, klass_name)

    elif isinstance(form_or_field, BoundField):
        _add_class(form_or_field, klass_name)
    else:
        logger.warning("%s was not a form or field, no action was taken", form_or_field)

    return form_or_field


orig_prettify = bs4.BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r"\1" * indent_width, orig_prettify(self, encoding, formatter))


bs4.BeautifulSoup.prettify = prettify


class PrettyPrintNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        html = bs4.BeautifulSoup(self.nodelist.render(context))
        return html.prettify()


@register.tag()
def pretty(parser, token):
    nodelist = parser.parse(("endpretty",))
    parser.delete_first_token()
    return PrettyPrintNode(nodelist)
