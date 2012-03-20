import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = (
    ('Ross Crawford-d\'Heureuse', 'ross.crawford@adcloud.com'),
)

SITE_ID = 2 # as per c9_sites.json fixtures

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

