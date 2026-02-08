from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    """Convert markdown text to HTML."""
    try:
        return mark_safe(md.markdown(value, extensions=['fenced_code', 'codehilite', 'tables']))
    except Exception:
        return value
