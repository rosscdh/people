# encoding: utf-8
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()



@register.inclusion_tag('orgchart/people_list.html', takes_context=True)
def people_list(context, office, department):
    """
    """
    people_list = context['object_list']['people'][office][department]
    return dict({
        'people_list': people_list,
        'MEDIA_URL': context['MEDIA_URL'],
    })
people_list.is_safe = True