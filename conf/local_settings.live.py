import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# is the live environment after all
DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ('Ross Crawford-d\'Heureuse', 'ross.crawford@adcloud.com'),
)

SITE_ID = 2 # as per c9_sites.json fixtures

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, '../data/live.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': 'adcloud_people',
        # 'USER': 'adcloud_people',
        # 'PASSWORD': '68ca3e0c',
        # 'HOST': '127.0.0.1',
        # 'PORT': '',
    }
}

# setup for webfaction paths
MEDIA_ROOT = os.path.join(PROJECT_DIR, '../media')
STATIC_ROOT = os.path.join(PROJECT_DIR, '../static')


STATICFILES_DIRS = (
    ("base", os.path.join(PROJECT_DIR, '../static/base/')),
    ("cloud9", os.path.join(PROJECT_DIR, '../static/cloud9/')),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PROJECT_DIR, '../data/people_cache'),
    }
}
