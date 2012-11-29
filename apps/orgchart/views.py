# encoding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import Http404
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from apps.cloud9.models import AdcloudInfo

import math


class OrganizationChartView(TemplateView):
    """
    """
    template_name = 'orgchart/chart.html'

    def get(self, request, **kwargs):
        selected_office = kwargs['office']

        lists = dict({
            'segments': [(i, unicode(n), reverse('orgchart:default', kwargs={'office': slugify(n.lower())})) for i,n in AdcloudInfo.OFFICES.get_choices()],
            'depts': [],
            'people': None,
        })

        office_id = [c for c,n,u in lists['segments'] if n.lower() == selected_office.lower()][0]

        people_queryset = AdcloudInfo.objects \
                            .select_related('user') \
                            .exclude(user__is_superuser=True) \
                            .filter(workplace=office_id) \
                            .order_by('user__last_name', 'user__first_name')

        people = {}
        # add people to departments
        for p in people_queryset:
            if not p.department in people:
                people[p.department] = []
                lists['depts'].append((p.department, unicode(AdcloudInfo.DEPARTMENTS.get_desc(p.department))))
            people[p.department].append(p)

        lists['people'] = people

        chart_height = (len(lists['depts']) * 110) + (len(lists['people']) * 35)

        return render_to_response(self.template_name, {
                'show_all': False,
                'object_list': lists,
                'people_list': people_queryset,
                'selected_item': selected_office,
                'chart_height': chart_height
            },context_instance=RequestContext(request))


class DevChartView(TemplateView):
    """
    """
    template_name = 'orgchart/chart_dev-team.html'

    def get(self, request, **kwargs):
        selected_team = kwargs['team']

        lists = dict({
            'segments': [(-1, 'All Teams', reverse('orgchart:teams', kwargs={'team': 'all'}))] + [(i, unicode(n), reverse('orgchart:teams', kwargs={'team': slugify(n.lower())})) for i,n in AdcloudInfo.DEVTEAMS.get_choices() if i != AdcloudInfo.DEVTEAMS.NONE],
            'depts': [],
            'people': None,
        })

        team_id = None
        if selected_team in lists['depts']:
            team_id = [c for c,n in AdcloudInfo.DEVTEAMS.get_choices() if slugify(n.lower()) == slugify(selected_team.lower())][0]

        people_queryset = AdcloudInfo.objects \
                            .select_related('user') \
                            .exclude(user__is_superuser=True) \
                            .filter(department=AdcloudInfo.DEPARTMENTS.DEV)

        if team_id:
            people_queryset = people_queryset.filter(team=team_id)

        people_queryset = people_queryset.order_by('user__last_name', 'user__first_name')

        people = {}
        # add people to departments
        for p in people_queryset:
            if p.team != AdcloudInfo.DEVTEAMS.NONE:
                if p.team not in people:
                    people[p.team] = []
                    #lists['depts'].append((p.team, unicode(AdcloudInfo.DEVTEAMS.get_desc(p.team))))
                people[p.team].append(p)


        lists['people'] = people

        chart_height = (len(lists['segments']) * 110) + (len(lists['people']) * 35)

        if team_id:
            lists['segments'] = [(i,n,u) for i,n,u in lists['segments'] if team_id == i]


        return render_to_response(self.template_name, {
                'show_all': True,
                'object_list': lists,
                'people_list': people_queryset,
                'selected_item': selected_team,
                'chart_height': chart_height
            },context_instance=RequestContext(request))

