from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import update_object
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from models import AdcloudInfo
from views import EmployeeEdit

employees_list = User.objects.all()

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login/$', 'apps.cloud9.views.login', name='login'),
    url(r'^employees/$', login_required(object_list), {'queryset': employees_list, 'template_name': 'cloud9/employee_list.html'}, name='employee_list'),
    url(r'^employee/(?P<slug>.*)/edit/$', login_required(EmployeeEdit.as_view()), name='employee_edit'),
    url(r'^employee/(?P<slug>.*)/$', login_required(object_detail), {'queryset': employees_list, 'template_name': 'cloud9/employee_detail.html', 'slug_field': 'username'}, name='employee_detail'),
    url(r'^', 'apps.cloud9.views.default', name='default'),
)
