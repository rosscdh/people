# encoding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
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


class OrganizationChart(TemplateView):
    """
    """
    template_name = 'orgchart/chart.html'

    def get(self, request, **kwargs):
        selected_office = kwargs['office']

        lists = dict({
            'offices': [(i, unicode(n)) for i,n in AdcloudInfo.OFFICES.get_choices()],
            'depts': [],
            'people': None,
        })

        office_id = [c for c,n in lists['offices'] if n.lower() == selected_office.lower()][0]

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

        chart_height = 100/len(lists['depts']) * 5
        print chart_height
        return render_to_response(self.template_name, {
                'object_list': lists,
                'people_list': people_queryset,
                'selected_office': selected_office,
                'chart_height': chart_height
            },context_instance=RequestContext(request))

