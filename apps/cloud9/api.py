import os 
from django.conf import settings
from django.conf.urls.defaults import url
from django.contrib.sites.models import Site
from django.db.models import Q
from django.core.urlresolvers import reverse

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.cache import SimpleCache
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from sorl.thumbnail import get_thumbnail

from people.apps.cloud9.models import AdcloudInfo as Person


v1_public_api = Api(api_name='v1')

available_formats = ['json']

Site = Site.objects.get(id=settings.SITE_ID)


class PersonResource(ModelResource):
    class Meta:
        queryset = Person.objects.select_related('user').filter(is_public=True, user__is_active=True, user__is_superuser=False).order_by('user__first_name', 'user__last_name')
        resource_name = 'people'
        serializer = Serializer(formats=available_formats)
        filtering = {
            "user__first_name": ALL,
            "user__last_name": ALL,
            "title": ALL,
            "contact_phone": ALL,
            "skype": ALL,
            "twitter": ALL,
        }
        cache = SimpleCache(timeout=300)

    def dehydrate(self, bundle):
        bundle.data['full_name'] = bundle.obj.user.get_full_name()
        bundle.data['first_name'] = bundle.obj.user.first_name
        bundle.data['last_name'] = bundle.obj.user.last_name
        bundle.data['email'] = bundle.obj.user.email
        bundle.data['skills'] = [s.name.lower() for s in bundle.obj.user.profile.skills.all()]
        bundle.data['department'] = Person.DEPARTMENTS.get_desc(bundle.data['department'])
        bundle.data['workplace'] = Person.OFFICES.get_desc(bundle.data['workplace'])
        bundle.data['team'] = Person.DEVTEAMS.get_desc(bundle.data['team'])
        bundle.data['profile_url'] = reverse('cloud9:employee_detail', kwargs={'slug': bundle.obj.user.username})

        if bundle.obj.profile_picture:
            try:
                picture = get_thumbnail(bundle.obj.profile_picture, '120x120', crop='center', quality=99)
                thumb = get_thumbnail(bundle.obj.profile_picture, '72x72', crop='center', quality=99)
                bundle.data['profile_picture'] = 'http://%s%s' % (Site.domain, picture.url,)
                bundle.data['profile_thumb'] = 'http://%s%s' % (Site.domain, thumb.url,)
            except:
                bundle.data['profile_picture'] = None
                bundle.data['profile_thumb'] = None

        return bundle


class ExtendedPersonResource(PersonResource):
    def build_filters(self, filters=None):
            if filters is None:
                filters = {}

            orm_filters = super(ExtendedPersonResource, self).build_filters(filters)

            return orm_filters

    class Meta(PersonResource.Meta):
        queryset = Person.objects.select_related('user').filter(user__is_active=True, user__is_superuser=False).order_by('user__first_name', 'user__last_name')
        resource_name = 'all/people'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=300)



""" Register the api resources """
v1_public_api.register(PersonResource())
v1_public_api.register(ExtendedPersonResource())
