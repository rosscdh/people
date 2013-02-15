# encoding: utf-8
from django import template
from apps.kudos.models import Kudos
from apps.kudos.forms import AwardKudosForm

register = template.Library()

icons = ['null-as-ratings-is-1-based','icon-ok','icon-thumbs-up','icon-star','icon-fire','icon-heart']
ratings = [{'icon': icons[rating],'rating':rating, 'name':unicode(name)} for rating,name in Kudos.RATINGS.get_choices()]


@register.inclusion_tag('kudos/main.html', takes_context=True)
def kudos_main(context, to_user):
	from_user = context['user']
	can_award = Kudos.objects.user_can_award(to_user=to_user, from_user=from_user)
	form = AwardKudosForm(initial={'from_user': from_user.pk, 'to_user': to_user.pk}) if can_award == True else None
	return {
		'can_award': can_award
		,'form': form
		,'to_user': to_user
		,'from_user': from_user
		,'total': Kudos.objects.user_total(to_user)
		,'monthly_total': Kudos.objects.user_total_by_month(to_user)
		,'ratings': ratings
		,'kudos_list': Kudos.objects.select_related('user').filter(to_user=to_user)
		,'icons': icons
		,'MEDIA_URL': context.get('MEDIA_URL')
    }


@register.filter
def rating_icon(value):
    try:
    	icon = icons[value]
    except:
    	icon = icons[1]
    return icon
rating_icon.is_safe = True


@register.filter
def rating_name(value):
    for r in ratings:
		if value == r.get('rating'):
			rating_name = r.get('name')
			break
    return rating_name
rating_name.is_safe = True
