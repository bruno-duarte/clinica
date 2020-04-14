from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Especialidade, Medico, Paciente, Horario, Consulta
from .forms import SignUpForm, ProfileForm, PasswordChangeForm, BookingForm, BookingResultsForm
from datetime import datetime


class IndexView(TemplateView):
	
	model = Paciente
	form_class = BookingForm
	success_url = reverse_lazy('index')
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['especialidades'] = Especialidade.objects.order_by('?').all()
		context['pacientes'] = Paciente.objects.order_by('?').all().filter()[:4]
		context['consultas'] = Consulta.objects.filter(Q(paciente__exact=self.request.user.id))
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


class ChangePasswordView(views.PasswordChangeView):
	
	model = Paciente
	form_class = PasswordChangeForm
	success_url = reverse_lazy('index')
	template_name = 'commons/change-password.html'

	def form_valid(self, form, *args, **kwargs):
		messages.success(self.request, 'Senha alterada com sucesso.')
		return super(ChangePasswordView, self).form_valid(form, *args, **kwargs)

	def form_invalid(self, form, *args, **kwargs):
		messages.error(self.request, 'Senha antiga não confere, ou nova senha não foi confirmada.')
		return super(ChangePasswordView, self).form_invalid(form, *args, **kwargs)


class PrescriptionsView(CreateView):
	
	model = Paciente
	form_class = ProfileForm
	success_url = reverse_lazy('index')
	template_name = 'commons/prescriptions.html'


class MedicalRecordsView(CreateView):
	
	model = Paciente
	form_class = ProfileForm
	success_url = reverse_lazy('index')
	template_name = 'commons/medical-records.html'


class BookingView(CreateView):
	
	model = Paciente
	form_class = BookingForm
	success_url = reverse_lazy('index')
	template_name = 'commons/booking.html'

	def get_context_data(self, **kwargs):
		context = super(BookingView, self).get_context_data(**kwargs)
		context['especialidades'] = Especialidade.objects.filter()
		return context
	

class BookingResultsView(CreateView):
	
	model = Paciente
	form_class = BookingResultsForm
	success_url = reverse_lazy('index')
	template_name = 'commons/booking-results.html'

	def get_context_data(self, **kwargs):
		todas_esp = Especialidade.objects.all()
		dias_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui','Sex', 'Sab']
		meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 
		         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
		esp = {}
		
		for e in todas_esp:
			esp[e.nome] = e.id
		
		id_esp = esp[self.request.GET.get('especialidade')]
		str_data = self.request.GET.get('data')
		
		data = datetime.strptime(str_data, '%Y-%m-%d').date()
		dia = int(data.strftime("%w"))
		data = dias_semana[dia] + ', ' + str(data.day) + ' de ' + meses[data.month-1]
		
		context = super(BookingResultsView, self).get_context_data(**kwargs)
		context['medicos'] = Medico.objects.filter(Q(especialidade__exact=id_esp))
		context['data'] = data
		context['str_data'] = str_data
		context['horarios'] = Horario.objects.all()
		context['consultas'] = Consulta.objects.all()
		return context	


class UpdateConsultaView(UpdateView):

	model = Consulta
	fields = ['estado']
	success_url = reverse_lazy('index')
	template_name = 'commons/booking-upd.html'

	def get_context_data(self, **kwargs):
		context = super(UpdateConsultaView, self).get_context_data(**kwargs)
		context['consultas'] = Consulta.objects.filter(Q(paciente__exact=self.request.user.id))
		return context

