from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import datetime
import re

register = template.Library()

@register.filter
def twitterize(value):
    """
    Method to parse for @username and link to profile
    as well as #hashtag and link to search
    """
    if value:
        at_usernames = re.findall(r'(@\S+)', value)
        for i in at_usernames:
            value = value.replace(i, '<a target="_NEW" href="http://www.twitter.com/'+ i.replace('@', '') +'">'+ i +'</a>')

        hashtags = re.findall(r'(#\S+)', value)
        for i in hashtags:
            value = value.replace(i, '<a target="_NEW"  href="http://twitter.com/#!/search/%23'+ i.replace('#', '') +'">'+ i +'</a>')

        return mark_safe(value)
    else:
        return value
twitterize.is_safe = True


TWEET_MAX_LEN = 140
@register.filter
def tweet_len_diff(value):
    """
    Method to subtract current string len - 140 (twitter max len)
    """
    if not type(value) == int:
        value = int(value)
    return mark_safe(TWEET_MAX_LEN - value)
tweet_len_diff.is_safe = True