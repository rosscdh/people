import factory
from django.contrib.auth.models import User

from models import Kudos


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    first_name = 'Test'
    last_name = 'User'
    is_superuser = False
    username = factory.LazyAttributeSequence(lambda a, n: '{0}_{1}'.format(a.first_name, n).lower())
    email = factory.LazyAttributeSequence(lambda a, n: '{0}.{1}+{2}@adcloud.com'.format(a.first_name, a.last_name, n).lower())


class KudosFactory(factory.Factory):
    FACTORY_FOR = Kudos
    # from_user = factory.SubFactory(UserFactory)
    # to_user = factory.SubFactory(UserFactory)