from django import template

register = template.Library()


@register.simple_tag
def echo(message=''):
    return message


@register.simple_tag
def free(*args, **kwargs):
    pass
