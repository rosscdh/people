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
    """
    template_name = 'orgchart/chart.html'

    def get(self, request):

        selected_office = request.GET.get('office', 'cologne')

        query = dict({
            'office': request.GET.get('office', None),
            'dept': request.GET.get('dept', None),
            'tag': request.GET.get('tag', None),
        })


        people_queryset = AdcloudInfo.objects \
                            .select_related('user') \
                            .exclude(user__is_superuser=True) \
                            .order_by('user__last_name', 'user__first_name')

        lists = dict({
            'offices': [(i, unicode(n)) for i,n in AdcloudInfo.OFFICES.get_choices()],
            'depts': [(i, unicode(n)) for i,n in AdcloudInfo.DEPARTMENTS.get_choices()],
            'people': None,
        })

        people = {}
        # add people to departments
        for p in people_queryset:
            if not p.workplace in people:
                people[p.workplace] = {}
            if not p.department in people[p.workplace]:
                people[p.workplace][p.department] = []
            people[p.workplace][p.department].append(p)



        lists['people'] = people

        return render_to_response(self.template_name, {
                'object_list': lists,
                'people_list': people_queryset,
                'selected_office': selected_office
            },context_instance=RequestContext(request))

