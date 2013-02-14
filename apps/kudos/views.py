from django.views.generic import CreateView
from mixins import JSONResponseMixin


class AwardKudosView(JSONResponseMixin, CreateView):
	def post(self, request, *args, **kwargs):
		assert False


class UndoAwardKudosView(JSONResponseMixin, CreateView):
	def post(self, request, *args, **kwargs):
		assert False