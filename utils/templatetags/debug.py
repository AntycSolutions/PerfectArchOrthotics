from django import template
register = template.Library()


@register.simple_tag
def get_attr(model_instance, attr_name):
    return getattr(model_instance, attr_name, '')


@register.simple_tag
def get_dir(model_instance):
    return dir(model_instance)


@register.simple_tag
def get_dict(model_instance):
    return model_instance.__dict__


@register.assignment_tag
def sql_queries():
    from django.db import connection
    return connection.queries
