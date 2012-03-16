from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('cloud9/partial/user_can_edit.html', takes_context=True)
def user_can_edit(context):
    user_can_edit = True if context['object'] == context['request'].user else False
    user_can_edit = True if context['request'].user.is_staff == True or context['request'].user.is_superuser == True else user_can_edit
    return { 'user_can_edit': user_can_edit, 'object': context['object'] }