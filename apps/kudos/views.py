from django.views.generic import FormView

from apps.kudos.models import Kudos
from apps.kudos.forms import AwardKudosForm

from mixins import JSONResponseMixin


class AwardKudosView(FormView):
	form_class = AwardKudosForm
	success_url = '/'


class UndoAwardKudosView(FormView):
	pass