# encoding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Kudos

class AwardKudosForm(forms.ModelForm):
	"""
	Provides a Form which allows a logged in user
	to award kudos to another user
	"""
	from_user = forms.IntegerField(widget=forms.HiddenInput)
	to_user = forms.IntegerField(widget=forms.HiddenInput)
	rating = forms.IntegerField(initial=1, widget=forms.HiddenInput)
	comment = forms.CharField(help_text='Max 64 chars', widget=forms.Textarea)

	class Meta:
		model = Kudos

	def clean_from_user(self):
		assert False