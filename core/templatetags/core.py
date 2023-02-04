from django import template
from django.urls import reverse,reverse_lazy, NoReverseMatch
from django.apps import apps
from django.utils.html import format_html
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag(takes_context=True)
def get_url(context, action, obj=None):
    '''
    example 1  " get_url 'list' "
    example 2  " get_url 'create' "
    example 3  " get_url 'detail' obj  "
    the first argument is action create or list or detail or update or delete
    the second argument is a model object
    the name of url pattern so as to work
    app:model-create
    app:model-update
    app:model-delete
    app:model-detail
    '''
    if not obj:
        model = context['model']
        lower_name = model.__name__.lower()
        app = model._meta.app_label
    else:
        model = obj
        lower_name = model.__class__.__name__.lower()
        app = model._meta.app_label

    url_string = '{}:{}-{}'.format(app, lower_name, action)
    if obj:
        url = reverse_lazy(url_string, kwargs={'pk': obj.pk})
    if not obj:
        url_string = '{}:{}-{}'.format(app, lower_name, action)
        url = reverse_lazy(url_string)
    return url


@register.simple_tag(takes_context=True)
def get_template_name(context, *args):
    model = context['model']
    app = model._meta.app_label
    lower_name = model.__name__.lower()
    template_name = "{}/partials/{}_list_partial.html".format(app,lower_name)
    return template_name

@register.simple_tag(takes_context=True)
def get_generate_sidebar(context):
    request = context['request']
    urls = ""
    app_models = apps.get_app_config(context['app']).get_models()
    for model in app_models:
        try:
            url_item = reverse(
                "{}:{}-list".format(model._meta.app_label, model.__name__.lower()))
        except NoReverseMatch:
            url_item = None
        if url_item:
            item = "<div><a href='{}'".format(url_item)
            if url_item == request.path:
                item += "class='active'"
            item += ">{}</a></div>".format(model._meta.verbose_name_plural)
            print(item)
            urls += item
    return format_html(mark_safe(urls))


@register.simple_tag
def get_boolean_img(value):
    if value:
        return format_html(mark_safe('<i class="bi bi-check-lg"></i>'))
    return format_html(mark_safe('<i class="bi bi-x"></i>'))


@register.simple_tag
def get_model_name(obj):
    if obj:
        return obj.__class__.name__.lower()
    return ''


@register.simple_tag
def get_model_app(obj):
    if obj:
        return obj._meta.app_label
    return ''

@register.simple_tag
def get_geo_type(obj):
    if obj:
        return obj.geom.__class__.__name__.lower()
    return ''