# encoding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from .models import Kudos


class AwardKudosForm(forms.ModelForm):
	"""
	Provides a Form which allows a logged in user
	to award kudos to another user
	"""
	from_user = forms.IntegerField(widget=forms.HiddenInput)
	to_user = forms.IntegerField(widget=forms.HiddenInput)
	rating = forms.IntegerField(initial=1, widget=forms.HiddenInput)
	comment = forms.CharField(required=False, help_text='Max 64 chars', widget=forms.Textarea)

	class Meta:
		model = Kudos

	def clean(self):
		cleaned_data = super(AwardKudosForm, self).clean()

		to_user = User.objects.get(pk=cleaned_data['to_user'])
		from_user = User.objects.get(pk=cleaned_data['from_user'])
		cleaned_data['to_user'] = to_user
		cleaned_data['from_user'] = from_user

		if Kudos.objects.user_can_award(to_user=to_user, from_user=from_user) == False:
			forms.ValidationError(u'You cannot award kudos to yourself.. you Cheeky Monkey')

		return cleaned_data
