# encoding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import update_object
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page

from views import OrganizationChartView, DevChartView


urlpatterns = patterns('',
    url(r'^teams/(?P<team>.+)/$', login_required(DevChartView.as_view()), name='teams'),
    url(r'^(?P<office>.+)/$', login_required(OrganizationChartView.as_view()), name='default'),
)
