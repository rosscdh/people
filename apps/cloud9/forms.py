# encoding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from socialregistration.forms import UserForm
from taggit.forms import TagField
from models import AdcloudInfo
from models import DEFAULT_PIC


class SimpleSearchForm(forms.Form):
    """
    Provides a basic query form to search the haystack with
    """
    q = forms.CharField(label='', required=True, initial=_('Search'))


class AccountSetupForm(UserForm):
    """
    Derrives from the socialregistration.UserForm but sets the fields
    to our specific requirements
    """
    username = forms.RegexField(r'^[\w.@+-]+$', max_length=32) # overriden username regex
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    title = forms.CharField(required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea, help_text='You are able to use Markdown for your bio. http://daringfireball.net/projects/markdown/syntax')
    department = forms.ChoiceField(choices=AdcloudInfo.DEPARTMENTS.get_choices())
    team = forms.ChoiceField(label='Team',choices=AdcloudInfo.DEVTEAMS.get_choices())
    workplace = forms.ChoiceField(label='Office',choices=AdcloudInfo.OFFICES.get_choices())
    room_number = forms.CharField(required=False)
    contact_phone = forms.CharField(required=False)
    skype = forms.CharField(required=False, help_text=_('Ensure: "Skype -> Preferences -> Privacy -> Show my status on the web" is checked'))
    twitter = forms.CharField(required=False)
    is_public = forms.BooleanField(required=False,initial=False,help_text='Ticking this box will mean that you display on the adcloud.com team page')
    skills = TagField(required=False,label=_('Tags'),help_text=_('Seperate by a comma (,)'))
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

        user.profile.title = self.cleaned_data.get('title')
        user.profile.bio = self.cleaned_data.get('bio')
        user.profile.department = self.cleaned_data.get('department')
        user.profile.workplace = self.cleaned_data.get('workplace')
        user.profile.team = self.cleaned_data.get('team')
        user.profile.room_number = self.cleaned_data.get('room_number')
        user.profile.contact_phone = self.cleaned_data.get('contact_phone')
        user.profile.skype = self.cleaned_data.get('skype')
        user.profile.twitter = self.cleaned_data.get('twitter')
        user.profile.is_public = self.cleaned_data.get('is_public')

        skills = self.cleaned_data.get('skills')
        if len(skills) > 0:
            # clear the skills
            user.profile.skills.all().delete()
            # readd the skills
            for s in skills:
                user.profile.skills.add(s)

        if self.cleaned_data.get('profile_picture'):
            user.profile.profile_picture = self.cleaned_data.get('profile_picture')

        user.profile.save()

        if not is_new:
            user.save()

        if profile:
            profile.user = user
            profile.save()

        return user, profile


class AccountEditForm(AccountSetupForm):
    """
    Derrives from the Custom AccountSetupForm which is derrived from socialregistration
    overrides the username of socialregistration which checks for username availability
    """

    def clean_username(self):
        """
        @TODO need to readd the check but cater to the fact that this is an edit thus the user
        should match the current request user object
        """
        return self.cleaned_data.get('username')

