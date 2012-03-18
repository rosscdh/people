from django.conf import settings
from django.contrib.sites.models import Site
from openid.extensions import ax


""" Tuple of allowed_domains """
ALLOWED_DOMAINS = getattr(settings, 'SOCIALREGISTRATION_ALLOWED_DOMAINS',
    (Site.objects.get_current(),))

""" Tuple of requested AX urls ((string)<ax_url>, (bool)<is_required>)"""
AX_URLS = getattr(settings, 'SOCIALREGISTRATION_AX_URLS',
    None)
    
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
    #@TODO extract user info from request assert False
    return user_data



""" create an ax object and append the requested AX urls and their is_required status """
def socialregistration_ax_request(auth_request):
    if AX_URLS:
        ax_request = ax.FetchRequest()
        for value in AX_URLS:
            url, is_required = value
            ax_request.add(ax.AttrInfo(url, required=is_required))
        return ax_request
    return None