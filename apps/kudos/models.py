from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from apps.util import get_namedtuple_choices

import datetime


class KudosManager(models.Manager):
	def award_to(self, to_user, from_user, **kwargs):
		return self.create(from_user=from_user, to_user=to_user, **kwargs)

	def user_total(self, user):
		r = self.filter(to_user=user).aggregate(Sum('rating'))
		total = r['rating__sum'] if r['rating__sum'] is not None else 0
		return total

	def user_total_by_month(self, user, date=None):
		if date is None:
			date = datetime.datetime.today()
		r = self.filter(to_user=user, date_awarded__month=date.month).aggregate(Sum('rating'))
		monthly_total = r['rating__sum'] if r['rating__sum'] is not None else 0
		return monthly_total

	def user_can_award(self, to_user, from_user):
		date = datetime.datetime.today()

		if to_user.pk == from_user.pk:
			return False

		r = self.filter(to_user=to_user, from_user=from_user, date_awarded__month=date.month).aggregate(Sum('rating'))
		return r['rating__sum'] == None


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
	comment = models.CharField(max_length=64, null=True)
	date_awarded = models.DateTimeField(auto_now_add=True)

	objects = KudosManager()

	def __unicode__(self):
		return u'%s - %s' % (self.rating, self.comment)


# import the signals like this so they are always loaded
from .signals import *