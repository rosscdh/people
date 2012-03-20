from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from apps.cloud9.forms import SimpleSearchForm

register = template.Library()


@register.inclusion_tag('cloud9/partial/user_can_edit.html', takes_context=True)
def user_can_edit(context):
    """
    Test if the user can edit the currently viewed user
    @TODO turn this into a reuseable decorator function
    that can be used in the view as well
    """
    user_can_edit = True if context['object'] == context['request'].user else False
    user_can_edit = True if context['request'].user.is_staff == True or context['request'].user.is_superuser == True else user_can_edit
    return { 'user_can_edit': user_can_edit, 'object': context['object'] }


@register.inclusion_tag('cloud9/search/form.html', takes_context=True)
def people_search_form(context):
    """
    Provide the Haystack Search Form
    """
    form = SimpleSearchForm()
    return dict({
        'search_form': form,
        'MEDIA_URL': context['MEDIA_URL'],
    })
people_search_form.is_safe = True