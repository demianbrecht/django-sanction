from django.conf import settings
from django.views.generic import TemplateView

from django_sanction.util import get_def

class Home(TemplateView):
	template_name = "home.html"

	def get_context_data(self, **kwargs):
		return {
			"providers": (get_def(p)() for p in settings.SANCTION_PROVIDERS)
		}

