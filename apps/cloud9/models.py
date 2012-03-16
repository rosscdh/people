from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from apps.util import get_namedtuple_choices

DEFAULT_PIC_PATH = 'employees/pics/'
DEFAULT_PIC = '%sdefault-pic.jpg' % (DEFAULT_PIC_PATH,)
PROFILE_PIC_PATH = '%s%s' % (settings.MEDIA_ROOT,DEFAULT_PIC_PATH,)


class AdcloudInfo(models.Model):
    TECH = 1
    SALES = 2
    MARKETING = 4
    DEPARTMENTS = get_namedtuple_choices('DEPARTMENTS', (
                        (TECH,'TECH','Tech'),
                        (SALES,'SALES','Sales'),
                        (MARKETING,'MARKETING','Marketing'),
                    ))
    user = models.OneToOneField(User, parent_link=True, related_name='profile')
    department = models.IntegerField(choices=DEPARTMENTS.get_choices(), default=DEPARTMENTS.TECH)
    contact_phone = models.CharField(max_length=24,blank=True,null=True)
    profile_picture = models.ImageField(upload_to=PROFILE_PIC_PATH, default=DEFAULT_PIC, blank=True, null=True)

    @property
    def dept(self):
        department = [dept for d,dept in self.DEPARTMENTS.get_choices() if d == self.department]
        return u'%s' % (department[0],)

    @property
    def thumbnail(self):
        thumb = self.profile_picture if self.profile_picture else DEFAULT_PIC
        return '%s' % (thumb,)

