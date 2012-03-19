# encoding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.http import Http404
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet
from socialregistration.views import Setup

from forms import AccountEditForm
from models import AdcloudInfo


def default(request):
    is_loggedin = request.user.is_authenticated()
    if not is_loggedin:
        return redirect(reverse('cloud9:login'))
    elif is_loggedin:
        return redirect(reverse('cloud9:employee_list'))
    else:
        return render_to_response('cloud9/base.html', {'request':request}, context_instance=RequestContext(request))


def login(request):
    return render_to_response('cloud9/login.html', {'request':request}, context_instance=RequestContext(request))


class EmployeeEdit(Setup):
    """
    Inherited form teh base Setup form and catering to edit flow
    """
    template_name = 'socialregistration/edit.html'

    def get_form(self):
        """
        Override the default to use the EmployeeEdit form
        """
        return self.import_attribute('apps.cloud9.forms.AccountEditForm')

    def get_initial_data(self, request, user, profile, client):
        """
        Overridden
        """
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'department': user.profile.department,
            'workplace': user.profile.workplace,
            'contact_phone': user.profile.contact_phone,
            'profile_picture': user.profile.profile_picture,
        }
        return data

    def get(self, request, slug):
        """
        Overriden
        """
        user = get_object_or_404(User, username=slug)
        try:
            profile = user.profile
        except AdcloudInfo.DoesNotExist:
            profile = AdcloudInfo.objects.get_or_create(user=user)
        client = None

        form = self.get_form()(initial=self.get_initial_data(request, user, profile, client))

        return self.render_to_response(dict(form=form, object=user))

    def post(self, request, slug):
        """
        Save the user and profile, login and send the right signals.
        """
        from socialregistration.contrib.openid.models import OpenIDProfile
        user = get_object_or_404(User, username=slug)
        try:
            profile = OpenIDProfile.objects.get(user=user)
        except OpenIDProfile.DoesNotExist:
            profile = OpenIDProfile.objects.get_or_create(user=user)
        client = None

        form = self.get_form()(request.POST, request.FILES)

        if not form.is_valid():
            return self.render_to_response(dict(form=form))

        user, profile = form.save(request, user, profile, client)

        user = profile.authenticate()

        return redirect(self.get_next(request))


class PeopleSearch(View):
    """
    Search for people
    """
    template_name = 'cloud9/employee_list.html'

    def get(self, request):
        query = request.GET.get('q', '')

        queryset = SearchQuerySet().using('default').filter(content=query)

        if queryset.count() == 1:
            person = queryset[0]
            return redirect(reverse('cloud9:employee_detail', kwargs={ 'slug': person.username }))
        else:
            return render_to_response(
              'cloud9/employee_list.html', {
                'object_list': queryset,
              },
              context_instance=RequestContext(request)
            )