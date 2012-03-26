# encoding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import Http404
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from apps.cloud9.models import AdcloudInfo


class OrganizationChart(TemplateView):
    """
    Search for people, makes use of the django-haystack app
    is basically a modified custom view of the GenericList.employee_list in cloud9.urls
    """
    template_name = 'orgchart/chart.html'

    def get(self, request):

        query = dict({
            'office': request.GET.get('office', None),
            'dept': request.GET.get('dept', None),
            'tag': request.GET.get('tag', None),
        })

        queryset = SearchQuerySet() \
                    .using('default') \
                    .order_by('last_name','first_name')

        lists = dict({
            'offices': [unicode(name) for id,name in AdcloudInfo.OFFICES.get_choices()],
            'depts': [unicode(name) for id,name in AdcloudInfo.DEPARTMENTS.get_choices()],
            'people': None,
        })

        people_queryset = queryset
        people = dict({
        })

        for p in people_queryset:
            if not p.office in people:
              people[p.office] = dict({})

            if not p.department in people:
              people[p.office][p.department] = []

            people[p.office][p.department].append(p)

        lists['people'] = people

        return render_to_response(self.template_name, {
                'object_list': lists,
            },context_instance=RequestContext(request))
