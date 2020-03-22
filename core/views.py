from django.views.generic import TemplateView
from .models import Especialidade, Medico


class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['especialidades'] = Especialidade.objects.order_by('?').all()
		return context


class AboutView(TemplateView):
	template_name = 'about.html'

	def get_context_data(self, **kwargs):
		context = super(AboutView, self).get_context_data(**kwargs)
		context['medicos'] = Medico.objects.order_by('?').all().filter()[:4]
		return context


class ContactView(TemplateView):
	template_name = 'contact.html'


class ElementsView(TemplateView):
	template_name = 'elements.html'


class NewsView(TemplateView):
	template_name = 'news.html'


class ServicesView(TemplateView):
	template_name = 'services.html'

	def get_context_data(self, **kwargs):
		context = super(ServicesView, self).get_context_data(**kwargs)
		context['especialidades'] = Especialidade.objects.all()
		return context

