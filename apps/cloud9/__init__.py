from django.conf import settings
from django.contrib.sites.models import Site

""" Tuple of allowed_domains """
ALLOWED_DOMAINS = getattr(settings, 'SOCIALREGISTRATION_ALLOWED_DOMAINS',
    (Site.objects.get_current(),))

def is_valid_domain(domain):
    """ method to ensure that the email provided by teopenid provider is allowed """
    if domain in ALLOWED_DOMAINS:
        return True
    else:
        return False


def socialregistration_initial_data(request, user, profile, client):
    user_data = {
        'username': 'test',
        'email': 'test@test.com',
        'first_name': '',
        'last_name': '',
        'profile_picture': '',
    }
    assert False
    return user_data