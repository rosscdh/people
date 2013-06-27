# encoding: utf-8
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
    Provide the Search Form
    """
    form = SimpleSearchForm()
    return dict({
        'search_form': form,
        'MEDIA_URL': context['MEDIA_URL'],
    })
people_search_form.is_safe = True


"""
jQuery templates use constructs like:

    {{if condition}} print something{{/if}}

This, of course, completely screws up Django templates,
because Django thinks {{ and }} mean something.

Wrap {% verbatim %} and {% endverbatim %} around those
blocks of jQuery templates and this will try its best
to output the contents with no changes.
"""

class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text
    
    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append('}}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('%}')
    return VerbatimNode(''.join(text))