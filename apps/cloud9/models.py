# encoding: utf-8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from annoying.fields import AutoOneToOneField
from apps.util import get_namedtuple_choices

import uuid

DEFAULT_PIC_PATH = 'employees/pics/'
DEFAULT_PIC = '%sdefault-pic.jpg' % (DEFAULT_PIC_PATH,)


""" Method to uniquify the uploaded people image """
def avatar_upload_path_handler(instance, filename):
    uid = uuid.uuid1()
    return "{path}{id}-{file}".format(path=DEFAULT_PIC_PATH, id=uid, file=filename)


"""
Adcloud infor User.profile object used to store additional User info
"""
class AdcloudInfo(models.Model):
    DEV = 1
    SALES = 2
    MARKETING = 4
    CLOUDMAN = 8
    SSP = 16
    DSP = 32
    OFFICEADMIN = 64
    MANAGEMENT = 128
    DEPARTMENTS = get_namedtuple_choices('DEPARTMENTS', (
                        (DEV,'DEV',_('Development')),
                        (SALES,'SALES',_('Product Management')),
                        (CLOUDMAN,'CLOUDMAN',_('Cloud Management')),
                        (SSP,'SSP',_('Supply Side')),
                        (DSP,'DSP',_('Demand Side')),
                        (OFFICEADMIN,'OFFICEADMIN',_('Administration')),
                        (MARKETING,'MARKETING',_('Marketing & PR')),
                        (MANAGEMENT,'MANAGEMENT',_('Management')),
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
    room_number = models.CharField(max_length=24,blank=True,null=True)
    contact_phone = models.CharField(max_length=24,blank=True,null=True)
    profile_picture = models.ImageField(upload_to=avatar_upload_path_handler, blank=False, null=False)
    skype = models.CharField(max_length=64,blank=True,null=True)
    twitter = models.CharField(max_length=64,blank=True,null=True)
    is_public = models.BooleanField(blank=True,default=False)

    skills = TaggableManager()

    class Meta:
      ordering = ['user__last_name','user__first_name','workplace','department']

    def __unicode__(self):
        return u'%s - %s (%s) - %s' % (self.user.username, self.dept, self.office, self.profile_picture)

    def get_twitter_username(self):
        if self.twitter not in [None,'','None']:
            twittername = self.twitter
        else:
            twittername = 'adcloud'
        return u'@%s' %(twittername,)

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

    def get_skills(self):
        tags = self.skills.all()
        if len(tags) > 0:
            skills = [unicode(tag.name) for tag in tags]
            return ', '.join(skills)
        return None

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^annoying.fields.AutoOneToOneField"])