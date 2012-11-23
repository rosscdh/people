# encoding: utf-8
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()



@register.inclusion_tag('orgchart/people_list.html', takes_context=True)
def people_list(context, office, department):
    """
    """
    people = context['object_list']['people']
    people_list = people[office][department] if office in people and department in people[office] else None
    return dict({
        'people_list': people_list,
        'MEDIA_URL': context['MEDIA_URL'],
    })
people_list.is_safe = True


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

