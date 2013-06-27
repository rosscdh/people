# encoding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import update_object
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required


from models import AdcloudInfo
from views import EmployeeEdit, ContactPhoneQRCode

employees_list = AdcloudInfo.objects.select_related('user').filter(user__is_superuser=False, user__is_active=True)


urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login/$', 'apps.cloud9.views.login', name='login'),

    url(r'^people/(?P<pk>.+)/qr/contactphone/$', login_required(ContactPhoneQRCode.as_view()), name='phone_qr'),
    url(r'^people/(?P<slug>.*)/edit/$', login_required(EmployeeEdit.as_view()), name='employee_edit'),
    url(r'^people/(?P<slug>.*)/$', login_required(object_detail), {'queryset': employees_list, 'template_name': 'cloud9/employee_detail.html', 'slug_field': 'user__username'}, name='employee_detail'),

    url(r'^', 'apps.cloud9.views.default', name='default'),
)
