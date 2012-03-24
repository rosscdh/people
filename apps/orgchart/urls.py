# encoding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import update_object
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page

from views import OrganizationChart, OrganizationChartHTML5


urlpatterns = patterns('',
    url(r'^chart/$', login_required(cache_page(60 * 15)(OrganizationChart.as_view())), name='default'),
    url(r'^chart/nocache/$', login_required(OrganizationChart.as_view()), name='default_nocache'),
    url(r'^chart/html5/$', login_required(cache_page(60 * 15)(OrganizationChartHTML5.as_view())), name='html5'),
    url(r'^chart/html5/nocache/$', login_required(OrganizationChartHTML5.as_view()), name='html5_nocache'),
)
