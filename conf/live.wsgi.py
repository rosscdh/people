import os
import sys
import site

site.addsitedir('/home/adcloud/.virtualenvs/people/lib/python2.7/site-packages')
site.addsitedir('/home/adcloud/.virtualenvs/people/lib/python2.7')
site.addsitedir('/home/adcloud/webapps/people')
site.addsitedir('/home/adcloud/webapps/people/people')

activate_this = os.path.expanduser("/home/adcloud/.virtualenvs/people/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

project = '/home/adcloud/webapps/people/people/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

os.environ['DJANGO_SETTINGS_MODULE'] = 'people.settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()