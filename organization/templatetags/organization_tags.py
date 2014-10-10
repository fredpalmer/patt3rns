import logging

from django import template

logger = logging.getLogger(__name__)

register = template.Library()

# @register.filter
# def lower(value):
#     """
#     Converts a string into all lowercase
#     """
#     return value.lower()
