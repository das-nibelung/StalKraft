# core/templatetags/safe_url.py
from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag
def safe_url(name, *args, **kwargs):
    """
    Пытается сделать reverse(name, ...). Если имени нет — возвращает default (или '#').
    Использование: {% safe_url 'services' default='/services/' %}
    """
    default = kwargs.pop("default", "#")
    try:
        return reverse(name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return default


@register.simple_tag(takes_context=True)
def is_active(context, *names):
    """
    Возвращает 'active', если текущий url_name среди переданных.
    Использование: class="{% is_active 'services' 'about' %}"
    """
    resolver_match = getattr(context.get("request"), "resolver_match", None)
    if resolver_match and resolver_match.url_name in names:
        return "active"
    return ""
