# encoding: utf-8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from annoying.fields import AutoOneToOneField
from apps.util import get_namedtuple_choices

DEFAULT_PIC_PATH = 'employees/pics/'
DEFAULT_PIC = '%sdefault-pic.jpg' % (DEFAULT_PIC_PATH,)
PROFILE_PIC_PATH = '%s/%s' % (settings.MEDIA_ROOT,DEFAULT_PIC_PATH,)


class AdcloudInfo(models.Model):
    DEV = 1
    SALES = 2
    MARKETING = 4
    CLOUDMAN = 8
    SSP = 16
    DSP = 32
    OFFICEADMIN = 64
    DEPARTMENTS = get_namedtuple_choices('DEPARTMENTS', (
                        (DEV,'DEV',_('Development')),
                        (SALES,'SALES',_('Product Management')),
                        (CLOUDMAN,'CLOUDMAN',_('Cloud Management')),
                        (SSP,'SSP',_('Supply Side')),
                        (DSP,'DSP',_('Demand Side')),
                        (OFFICEADMIN,'OFFICEADMIN',_('Administration')),
                        (MARKETING,'MARKETING',_('Marketing & PR')),
                    ))
    COLOGNE = 1
    MADRID = 2
    PARIS = 4
    OFFICES = get_namedtuple_choices('OFFICES', (
                        (COLOGNE,'COLOGNE',_(u'Cologne')),
                        (MADRID,'MADRID',_('Madrid')),
                        (PARIS,'PARIS',_('Paris')),
                    ))
    user = AutoOneToOneField(User, primary_key=True, related_name='profile')
    department = models.IntegerField(choices=DEPARTMENTS.get_choices(), default=DEPARTMENTS.DEV)
    workplace = models.IntegerField(choices=OFFICES.get_choices(), default=OFFICES.COLOGNE)
    contact_phone = models.CharField(max_length=24,blank=True,null=True)
    profile_picture = models.ImageField(upload_to=PROFILE_PIC_PATH, blank=False, null=False)
    skype = models.CharField(max_length=64,blank=True,null=True)

    skills = TaggableManager()

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.user.username, self.dept, self.office)

    @property
    def dept(self):
        department = [unicode(dept) for d,dept in self.DEPARTMENTS.get_choices() if d == int(self.department)]
        if len(department) == 0:
            department.append(self.DEPARTMENTS.DEV)

        return u'%s' % (department[0],)

    @property
    def office(self):
        office = [unicode(workplace) for o,workplace in self.OFFICES.get_choices() if o == int(self.workplace)]
        if len(office) == 0:
            office.append(self.OFFICES.COLOGNE)
        return u'%s' % (office[0],)
