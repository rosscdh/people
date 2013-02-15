# encoding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from views import AwardKudosView


urlpatterns = patterns('',
    url(r'^award/$', login_required(AwardKudosView.as_view()), name='award'),
)
