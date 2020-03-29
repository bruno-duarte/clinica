from django.views.generic import FormView
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Especialidade, Medico, Paciente
from .forms import SignUpForm, ProfileForm


class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['especialidades'] = Especialidade.objects.order_by('?').all()
		context['pacientes'] = Paciente.objects.order_by('?').all().filter()[:4]
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


class SignupView(CreateView):
	form_class = SignUpForm
	success_url = reverse_lazy('index')
	template_name = 'commons/signup.html'


class ProfileView(UpdateView):
	model = Paciente
	form_class = ProfileForm
	success_url = reverse_lazy('index')
	template_name = 'commons/profile.html'

