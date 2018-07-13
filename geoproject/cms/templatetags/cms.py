from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.simple_tag
def add_title(object, value):
    title = '{} {}'.format(value, object.__class__.__name__)
    return title


@register.simple_tag
def create_title(object, value):
    title = '{} {}'.format(object.__class__.__name__, value)
    return title


@register.simple_tag
def url_create(object, value):
    model = object.__class__.__name__.lower()
    url_link = reverse_lazy('{}-{}'.format(model, value))
    return url_link


@register.simple_tag
def url_update(object, value):
    model = object.__class__.__name__.lower()
    url_link = reverse_lazy('{}-{}'.format(model, value), kwargs={'pk': object.pk})
    return url_link


@register.simple_tag
def url_delete(object, value):
    model = object.__class__.__name__.lower()
    url_link = reverse_lazy('{}-{}'.format(model, value), kwargs={'pk': object.pk})
    return url_link
