"""
"""
from mocktest import *
from factories import UserFactory, KudosFactory

from models import Kudos
import datetime


class TestKudos(mocktest.TestCase):
	def setUp(self):
		self.usera = UserFactory.create()
		self.userb = UserFactory.create()
		self.userc = UserFactory.create()


	def test_award_to(self):
		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, rating=Kudos.RATINGS.nice, comment='well done')
		assert Kudos.objects.all().count() == 1
		k = Kudos.objects.all()[0]
		assert k.rating == Kudos.RATINGS.nice
		assert k.comment == 'well done'

	def test_user_total(self):
		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, rating=Kudos.RATINGS.nice, comment='well done')
		assert Kudos.objects.user_total(user=self.userb) == 1

		for i in range(1,5):
			Kudos.objects.award_to(to_user=self.userb, from_user=self.usera)

		assert Kudos.objects.user_total(user=self.userb) == 5

	def user_total_by_month(self):
		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera)
		assert Kudos.objects.user_total_by_month(user=self.userb) == 1

		for i in range(1,5):
			Kudos.objects.award_to(to_user=self.userb, from_user=self.usera)
		assert Kudos.objects.user_total_by_month(user=self.userb) == 5

		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, date_awarded=datetime.datetime(2013,01,01,00,00,00))
		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, date_awarded=datetime.datetime(2013,01,01,00,00,00))
		assert Kudos.objects.user_total_by_month(user=self.userb, date=datetime.datetime(2013,01,01,00,00,00)) == 2

		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, date_awarded=datetime.datetime(2013,05,01,00,00,00))
		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, date_awarded=datetime.datetime(2013,05,07,00,00,00))
		Kudos.objects.award_to(to_user=self.userb, from_user=self.usera, date_awarded=datetime.datetime(2013,05,14,00,00,00))
		assert Kudos.objects.user_total_by_month(user=self.userb, date=datetime.datetime(2013,05,01,00,00,00)) == 3

