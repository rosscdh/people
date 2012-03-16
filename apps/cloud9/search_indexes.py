from haystack import indexes
from django.contrib.auth.models import User


class PeopleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    full_name = indexes.CharField(model_attr='get_full_name')
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    department = indexes.CharField(model_attr='profile__dept')
    office = indexes.CharField(model_attr='profile__office')
    content_auto = indexes.EdgeNgramField(model_attr='get_full_name')

    def get_model(self):
        return User

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.exclude(profile=None).filter(is_active=True)
