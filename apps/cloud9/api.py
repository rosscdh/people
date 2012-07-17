from django.conf import settings
from django.conf.urls.defaults import url
from django.contrib.sites.models import Site

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.cache import SimpleCache

from sorl.thumbnail import get_thumbnail

from people.apps.cloud9.models import AdcloudInfo as Person


v1_public_api = Api(api_name='v1')

available_formats = ['json']

Site = Site.objects.get(id=settings.SITE_ID)


class PersonResource(ModelResource):
    class Meta:
        queryset = Person.objects.select_related('user').filter(is_public=True,user__is_active=True,user__is_superuser=False).order_by('user__first_name', 'user__last_name')
        resource_name = 'people'
        serializer = Serializer(formats=available_formats)

    def dehydrate(self, bundle):
        bundle.data['full_name'] = bundle.obj.user.get_full_name()
        bundle.data['first_name'] = bundle.obj.user.first_name
        bundle.data['last_name'] = bundle.obj.user.last_name
        bundle.data['department'] = Person.DEPARTMENTS.get_desc(bundle.data['department'])
        bundle.data['workplace'] = Person.OFFICES.get_desc(bundle.data['workplace'])

        if bundle.obj.profile_picture:
            picture = get_thumbnail(bundle.obj.profile_picture, '120x120', crop='center', quality=99)
            thumb = get_thumbnail(bundle.obj.profile_picture, '72x72', crop='center', quality=99)

            bundle.data['profile_picture'] = 'http://%s%s' % (Site.domain, picture.url,)
            bundle.data['profile_thumb'] = 'http://%s%s' % (Site.domain, thumb.url,)

        return bundle


class ExtendedPersonResource(PersonResource):
    class Meta:
        queryset = Person.objects.select_related('user').filter(user__is_active=True,user__is_superuser=False).order_by('user__first_name', 'user__last_name')
        resource_name = 'all/people'
        serializer = Serializer(formats=available_formats)    



""" Register the api resources """
v1_public_api.register(PersonResource())
v1_public_api.register(ExtendedPersonResource())
