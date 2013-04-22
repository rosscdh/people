from django.contrib import messages
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from apps.kudos.models import Kudos
from apps.kudos.forms import AwardKudosForm

from mixins import JSONResponseMixin

import user_streams


class AwardKudosView(FormMixin, ProcessFormView):
	form_class = AwardKudosForm

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')

	def form_valid(self, form):
		form.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form):
		messages.error(self.request, form.errors)
		return HttpResponseRedirect(self.get_success_url())

	def render_to_response(self, **kwargs):
		self.form_valid(kwargs.get('form'))
		return HttpResponseRedirect(self.get_success_url())


class KudosActivityView(TemplateView):
	template_name = 'kudos/activity.html'

	def get_context_data(self, **kwargs):
		backend = user_streams.get_backend()
		stream = backend.filter_stream()
		return {
			'object_list': stream.select_related('content_object, user, user__profile').all().order_by('-created_at')
		}