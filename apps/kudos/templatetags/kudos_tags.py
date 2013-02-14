# encoding: utf-8
from kudos.models import Kudos

register = template.Library()


@register.inclusion_tag('kudos/main.html', takes_context=True)
def kudos(context, user):
    
    return {
        'to_user': user
    }
