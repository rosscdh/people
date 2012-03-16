from django import forms
from django.utils.translation import ugettext_lazy as _

from socialregistration.forms import UserForm
from models import AdcloudInfo
from models import DEFAULT_PIC, PROFILE_PIC_PATH


class SimpleSearchForm(forms.Form):
    q = forms.CharField(label='', required=True, initial=_('Search'))


class AccountSetupForm(UserForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    department = forms.ChoiceField(choices=AdcloudInfo.DEPARTMENTS.get_choices())
    contact_phone = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)


class AccountEditForm(UserForm):
    """ Used to edit the user object without interfering with the base UserForm """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    department = forms.ChoiceField(choices=AdcloudInfo.DEPARTMENTS.get_choices())
    office = forms.ChoiceField(choices=AdcloudInfo.OFFICES.get_choices())
    contact_phone = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

    def clean_username(self):
        return self.cleaned_data.get('username')

    def save(self, request, user, profile, client):
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.profile.department = self.cleaned_data.get('department')
        user.profile.contact_phone = self.cleaned_data.get('contact_phone')

        default_pic = '%s%s' % (PROFILE_PIC_PATH,DEFAULT_PIC,)
        if self.cleaned_data.get('profile_picture').path != default_pic:
            user.profile.profile_picture = self.cleaned_data.get('profile_picture')

        user.save()
        user.profile.save()
        profile.user = user
        profile.save()
        return user, profile