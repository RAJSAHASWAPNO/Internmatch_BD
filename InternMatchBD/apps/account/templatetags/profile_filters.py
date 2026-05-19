from django import template

register = template.Library()

@register.filter
def split(value, separator):
    """
    Split a string by a given separator.
    Usage: {{ string|split:"," }}
    """
    if value:
        return value.split(separator)
    return []

@register.filter
def strip(value):
    """
    Strip whitespace from a string.
    Usage: {{ string|strip }}
    """
    if value:
        return str(value).strip()
    return value

@register.filter
def strip_tags_custom(value):
    """Remove HTML tags from string"""
    from django.utils.html import strip_tags
    return strip_tags(str(value) if value else '')
