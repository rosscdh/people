# encoding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from socialregistration.forms import UserForm
from models import AdcloudInfo
from models import DEFAULT_PIC, PROFILE_PIC_PATH


class SimpleSearchForm(forms.Form):
    q = forms.CharField(label='', required=True, initial=_('Search'))


class AccountSetupForm(UserForm):
    username = forms.RegexField(r'^[\w.@+-]+$', max_length=32) # overriden username regex
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    department = forms.ChoiceField(choices=AdcloudInfo.DEPARTMENTS.get_choices())
    workplace = forms.ChoiceField(choices=AdcloudInfo.OFFICES.get_choices())
    contact_phone = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=True)

    def save(self, request, user, profile, client):
        is_new = user.id is None

        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        """ setup the user.profile record as we save the current user object """
        if is_new:
            user.save()

        user.profile.department = self.cleaned_data.get('department')
        user.profile.workplace = self.cleaned_data.get('workplace')
        user.profile.contact_phone = self.cleaned_data.get('contact_phone')

        default_pic = '%s/%s' % (PROFILE_PIC_PATH,DEFAULT_PIC,)
        
        if self.cleaned_data.get('profile_picture') and (isinstance(self.cleaned_data.get('profile_picture'), InMemoryUploadedFile) or self.cleaned_data.get('profile_picture').path != default_pic):
            user.profile.profile_picture = self.cleaned_data.get('profile_picture')

        user.profile.save()

        profile.user = user
        profile.save()
        return user, profile

class AccountEditForm(AccountSetupForm):
    """ Used to edit the user object without interfering with the base UserForm """

    def clean_username(self):
        return self.cleaned_data.get('username')

