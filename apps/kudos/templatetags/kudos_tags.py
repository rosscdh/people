# encoding: utf-8
from django import template
from apps.kudos.models import Kudos
from apps.kudos.forms import AwardKudosForm

register = template.Library()


@register.inclusion_tag('kudos/main.html', takes_context=True)
def kudos_main(context, to_user):
	from_user = context['user']
	icons = ['null-as-ratings-is-1-based','icon-ok','icon-thumbs-up','icon-star','icon-fire','icon-heart']
	can_award = Kudos.objects.user_can_award(to_user=to_user, from_user=from_user)
	form = AwardKudosForm(initial={'from_user': from_user.pk, 'to_user': to_user.pk}) if can_award == True else None
	return {
		'can_award': can_award
		,'form': form
		,'to_user': to_user
		,'from_user': from_user
		,'total': Kudos.objects.user_total(to_user)
		,'monthly_total': Kudos.objects.user_total_by_month(to_user)
		,'ratings': [{'icon': icons[rating],'rating':rating, 'name':unicode(name)} for rating,name in Kudos.RATINGS.get_choices()]
    }
