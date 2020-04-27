from __future__ import unicode_literals
from datetime import datetime
from weasyprint import HTML, CSS
from background_task import background

from django.views.generic.base import RedirectView
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import (
	Especialidade, Medico, Paciente, Horario, Consulta, Notificacao
)
from .forms import ( 
	SignUpForm, ProfileForm, PasswordChangeForm, BookingForm, BookingResultsForm, 
	UpdateAppointmentsForm
)


class IndexView(TemplateView):
	
	model = Paciente
	form_class = BookingForm
	success_url = reverse_lazy('index')
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['especialidades'] = Especialidade.objects.order_by('?').all()
		context['pacientes'] = Paciente.objects.order_by('?').all().filter()[:4]
		context['medicos'] = Medico.objects.order_by('?').all().filter()[:4]
		context['horarios'] = Horario.objects.all()
		context['consultas_paciente'] = Consulta.objects.filter(
			Q(paciente__exact=self.request.user.id)
		).order_by('data')
		context['prox_consultas'] = Consulta.objects.filter(
			Q(medico__exact=self.request.user.id) & 
			Q(data__gt=datetime.today())
		)
		context['total_notificacoes'] = Notificacao.objects.filter(
			Q(paciente__exact=self.request.user.id) &
			Q(lida__exact=False)
		).order_by('criada').count()
		context['notificacoes'] = Notificacao.objects.filter(
			Q(paciente__exact=self.request.user.id),
			Q(lida__exact=False)
		).order_by('criada')[:4]
		try:
			medico = Medico.objects.filter(Q(id=self.request.user.id))
			context['medico'] = medico[0]
		except IndexError:
			context['medico'] = []
		context['data_hoje'] = datetime.today()
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
		context['medicos'] = Medico.objects.filter(
			Q(especialidade__exact=id_esp)
		).order_by('first_name')
		context['data'] = data
		context['str_data'] = str_data
		context['horarios'] = Horario.objects.all()
		context['consultas'] = Consulta.objects.all()
		return context	


class CancelConsultaView(UpdateView):

	model = Consulta
	fields = ['estado']
	success_url = reverse_lazy('index')
	template_name = 'commons/cancel.html'

	def get_context_data(self, **kwargs):
		context = super(CancelConsultaView, self).get_context_data(**kwargs)
		context['consultas'] = Consulta.objects.filter(Q(paciente__exact=self.request.user.id))
		return context


class AppointmentsView(TemplateView):
	
	model = Consulta
	form_class = BookingResultsForm
	success_url = reverse_lazy('index')
	template_name = 'commons/today-appointments.html'

	def get_context_data(self, **kwargs):
		context = super(AppointmentsView, self).get_context_data(**kwargs)
		context['consultas_hoje'] = Consulta.objects.filter(
			Q(medico__exact=self.request.user.id) & 
			Q(data__exact=datetime.today())
		)
		try:
			medico = Medico.objects.filter(Q(id=self.request.user.id))
			context['medico'] = medico[0]
		except IndexError:
			context['medico'] = []
		return context


class UpdateConsultaView(UpdateView):

	model = Consulta
	form_class = UpdateAppointmentsForm
	success_url = reverse_lazy('index')
	template_name = 'commons/update.html'

	def get_context_data(self, **kwargs):
		context = super(UpdateConsultaView, self).get_context_data(**kwargs)
		context['consultas'] = Consulta.objects.filter(
			Q(paciente__exact=self.request.user.id)
		)
		return context

class AllAppointmentsView(TemplateView):
	
	model = Consulta
	success_url = reverse_lazy('index')
	template_name = 'commons/appointments.html'

	def get_context_data(self, **kwargs):
		context = super(AllAppointmentsView, self).get_context_data(**kwargs)
		context['todas_consultas'] = Consulta.objects.filter(
			Q(medico__exact=self.request.user.id)
		).order_by('-data')
		try:
			medico = Medico.objects.filter(Q(id=self.request.user.id))
			context['medico'] = medico[0]
		except IndexError:
			pass
		return context


class ReportView(View):

	template_name = 'commons/report.html'

	def get(self, request, *args, **kwargs):
		try:
			c = Consulta.objects.filter(Q(id__exact=kwargs['pk']))
			c = c[0]
		except IndexError:
			pass
		html_string = render_to_string('commons/report.html', {'consulta': c})
		html = HTML(string=html_string, base_url=request.build_absolute_uri())
		html.write_pdf(target='/tmp/report.pdf', stylesheets=[
			CSS(string='@page { size: A4; margin: 2cm }')
		])
		fs = FileSystemStorage('/tmp')
		with fs.open('report.pdf') as pdf:
			response = HttpResponse(pdf, content_type='report.pdf')
			response['Content-Disposition'] = 'inline; filename="report.pdf"'
		return response 


class RemoveDataView(UpdateView):
	
	model = Paciente
	form_class = ProfileForm
	success_url = reverse_lazy('index')
	template_name = 'commons/remove.html'


class NotificationView(TemplateView):
	
	model = Paciente
	template_name = 'commons/notification.html'

	def get_context_data(self, **kwargs):
		context = super(NotificationView, self).get_context_data(**kwargs)
		context['notificacoes'] = Notificacao.objects.filter(
			Q(paciente__exact=self.request.user.id)
		).order_by('criada')


class ConfirmView(UpdateView):

	model = Consulta
	fields = ['estado']
	success_url = reverse_lazy('index')
	template_name = 'commons/confirm.html'


@background(schedule=24*60*60)
def update_status_of_appoint(user_id):
	Consulta.objects.filter(
		(Q(estado = 'Agendada') | Q(estado = 'Espera')) &
		Q(data__lte = date.today())
	).update(estado='Expirada')


