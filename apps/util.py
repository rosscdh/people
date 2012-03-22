# encoding: utf-8
"""
In order to provide clean access to constants used in model definitions
This class provides a simple lookup mechnism which allows static reference to named values
instead of having to hardcode the numeric variable
"""
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages


def get_namedtuple_choices(name, choices_tuple):
    """Factory function for quickly making a namedtuple suitable for use in a
    Django model as a choices attribute on a field. It will preserve order.

    Usage::

        class MyModel(models.Model):
            COLORS = get_namedtuple_choices('COLORS', (
                (0, 'BLACK', 'Black'),
                (1, 'WHITE', 'White'),
            ))
            colors = models.PositiveIntegerField(choices=COLORS)

        >>> MyModel.COLORS.BLACK
        0
        >>> MyModel.COLORS.get_choices()
        [(0, 'Black'), (1, 'White')]

        class OtherModel(models.Model):
            GRADES = get_namedtuple_choices('GRADES', (
                ('FR', 'FR', 'Freshman'),
                ('SR', 'SR', 'Senior'),
            ))
            grade = models.CharField(max_length=2, choices=GRADES)

        >>> OtherModel.GRADES.FR
        'FR'
        >>> OtherModel.GRADES.get_choices()
        [('FR', 'Freshman'), ('SR', 'Senior')]

    """
    class Choices(namedtuple(name, [name for val,name,desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val,name,desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)

    return Choices._make([val for val,name,desc in choices_tuple])


"""
Decorator to ensure you can only edit your own profile
unless you are an admin or mod
"""
def user_is_self_or_admin( request, viewed_user ):
    if not request.user.is_authenticated():
        messages.error(request, _('You need to be logged in.'))
        return HttpResponseRedirect( reverse('cloud9:employee_list') )

    if request.user != viewed_user and (not request.user.is_staff and not request.user.is_superuser ):
        messages.error(request, _('You are trying to access someones profile without permission. You are a very norty person.'))
        return HttpResponseRedirect( reverse('cloud9:employee_list') )

    return True

