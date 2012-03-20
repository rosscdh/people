import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# is the live environment after all
DEBUG = False

ADMINS = (
    ('Ross Crawford-d\'Heureuse', 'ross.crawford@adcloud.com'),
)

SITE_ID = 2 # as per c9_sites.json fixtures

# setup for webfaction paths
MEDIA_ROOT = os.path.join(PROJECT_DIR, '../../media/people')
STATIC_ROOT = os.path.join(PROJECT_DIR, '../../static/people')

