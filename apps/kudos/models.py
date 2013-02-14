from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from apps.util import get_namedtuple_choices

import datetime

class KudosManager(models.Manager):
	def award_to(self, to_user, from_user, **kwargs):
		return self.create(from_user=from_user, to_user=to_user, **kwargs)

	def user_total(self, user):
		return self.filter(to_user=user).count()

	def user_total_by_month(self, user, date=None):
		if date is None:
			date = datetime.datetime.today()
		return self.filter(to_user=user, date_awarded__month=date.month).count()

	def user_can_award(self, to_user, from_user):
		date = datetime.datetime.today()
		return self.filter(to_user=to_user, from_user=from_user, date_awarded__month=date.month).count() == 0


class Kudos(models.Model):
	RATINGS = get_namedtuple_choices('RATINGS', (
		(1,'nice',_('Nice!')),
		(2,'cool',_('Cool man!')),
		(3,'super',_('Totally Super!')),
		(4,'rocking',_('Rocks me out')),
		(5,'amazing',_('Freaking Amazing')),
	))
	from_user = models.ForeignKey(User, related_name='from')
	to_user = models.ForeignKey(User, related_name='to')
	rating = models.IntegerField(null=False, choices=RATINGS.get_choices(), default=RATINGS.nice)
	comment = models.CharField(max_length=64)
	date_awarded = models.DateTimeField(auto_now_add=True)

	objects = KudosManager()