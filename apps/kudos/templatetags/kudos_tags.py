# encoding: utf-8
from django import template
from apps.kudos.models import Kudos

register = template.Library()


@register.inclusion_tag('kudos/main.html', takes_context=True)
def kudos_main(context, user):
	icons = ['null-as-ratings-is-1-based','icon-ok','icon-thumbs-up','icon-star','icon-fire','icon-heart']
	return {
		'can_award': Kudos.objects.user_can_award(to_user=user, from_user=context['user'])
		,'total': Kudos.objects.user_total(user)
		,'monthly_total': Kudos.objects.user_total_by_month(user)
		,'ratings': [{'icon': icons[rating],'rating':rating, 'name':unicode(name)} for rating,name in Kudos.RATINGS.get_choices()]
    }
