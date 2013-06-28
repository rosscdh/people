"""
Fabric file to deploy the adcloud website

Author: Ross Crawford-d'Heureuse <sendrossemail@gmail.com>
Date: 2013-06-27

Deploy using fabric
```fab (production|staging) <task_name>```

Deploy the application
```fab production deploy```

Install your local requirements to stage/production
```fab production install_requirements_from_local```

Back the database up as a .json fixure

```fab production db_backup download_db_backup```

"""
from __future__ import with_statement

import os
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files

import datetime

debug = True

env.project = 'people'
env.local_project_path = os.path.dirname(os.path.abspath(__file__))
env.environment = 'local'
env.sha = None
env.zip_file = None
env.db_backup_file = None

env.db_backup_file = '~/%s-fixtures%s.json' % (env.project, datetime.datetime.utcnow().strftime("%Y-%m-%d"),)

@task
def production():
  env.environment = 'live'
  env.hosts = ['adcloud@adcloud.webfactional.com']
  env.app_name = 'people'
  env.project_name = 'people'
  env.virtualenv = '/home/adcloud/.virtualenvs/people/'
  env.activate_virtualenv = 'source %s/bin/activate' % env.virtualenv
  env.remote_app_path = '/home/adcloud/webapps/%s/' % env.app_name
  env.remote_project_path = '%s%s/' % (env.remote_app_path, env.project_name,)
  env.remote_versions_path = '%sversions/' % env.remote_app_path

@task
def install_requirements_from_local():
  put('%s/requirements.txt' % env.local_project_path, '~/requirements.txt')
  with prefix(env.activate_virtualenv):
    run('pip install -r ~/requirements.txt --use-mirrors')
    #run('pip install mysql-python')
    run('unlink ~/requirements.txt')

@task
@hosts(['localhost'])
def git_sha():
  lcd(env.local_project_path)
  env.sha = local('git rev-parse --short --verify HEAD', capture=True)
  return env.sha

@task
@hosts(['localhost'])
def git_export():
  with lcd(env.local_project_path):
    gsha = git_sha()
    zip_file = '%s.zip' % gsha
    local('git archive --format zip --output /tmp/%s --prefix=%s/ master'%(zip_file, gsha,), capture=False)
  return zip_file


@task
def prepare_deploy():
  env.zip_file = git_export()
  put('/tmp/%s' % env.zip_file, '~/')


@task
def conclude_deploy():
  if env.zip_file and files.exists(env.zip_file):
    run('unlink %s' % env.zip_file)

  if env.backup_db == 'y':
    download_db_backup()

@task
def db_backup():
  with prefix(env.activate_virtualenv):
    run('python %smanage.py dumpdata > %s' % (env.remote_project_path, env.db_backup_file,))

@task
def download_db_backup():
  get(env.db_backup_file, '.')
  run('unlink %s' % env.db_backup_file)


@task
def deploy():
  env.backup_db = prompt('Do you want to back the database up? (y/n)', default='n')
  if env.backup_db == 'y':
    db_backup()

  prepare_deploy()

  # ensure the versions dir exists
  run('mkdir -p %s' % env.remote_versions_path)

  # extract project zip file
  with cd(env.remote_versions_path):
    run('unzip ~/%s -d %s' % (env.zip_file, env.remote_versions_path,))

  with cd(env.remote_app_path):
    """ link in the newley uploaded version"""
    env.version_path = '%s%s/' % (env.remote_versions_path, env.sha)

    if files.exists(env.version_path):
      if files.exists(env.remote_project_path[0:-1]):
        run('unlink %s' % env.remote_project_path[0:-1]) # remove the trailing / so we can unlink it
      run('ln -s %s %s' % (env.version_path, env.remote_project_path[0:-1],))

  with cd(env.version_path):
    run('cp %sconf/%s.local_settings.py local_settings.py' % (env.version_path, env.environment))
    run('cp %sconf/%s.wsgi.py wsgi.py' % (env.version_path, env.environment))

  with prefix(env.activate_virtualenv):
    with cd(env.remote_project_path):
      run('python manage.py collectstatic --noinput')

  with cd(env.remote_app_path):
    run('./apache2/bin/restart')

  conclude_deploy()

