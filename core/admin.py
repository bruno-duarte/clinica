from __future__ import unicode_literals
from datetime import date, timedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from .forms import (
	CustomUsuarioCreateForm, CustomUsuarioChangeForm, MedicoCreateForm, MedicoChangeForm,
	PacienteCreateForm, PacienteChangeForm
)
from .models import ( 
	Especialidade, CustomUsuario, Medico, Paciente, Comentario, Horario, Consulta, SiteSettings,
	Notificacao
)


admin.site.site_header = "Clínica MedArt"
admin.site.site_title = "Admistração"
admin.site.index_title = "Admistração Clínica"


class SingletonModelAdmin(admin.ModelAdmin):
	
	actions = None  

	def has_delete_permission(self, request, obj=None):
	    return False

	def has_add_permission(self, request):
	    return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
	
	pass


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
	
	list_display = ('nome', 'ativo', 'modificado')


class ConsultasPeriodoListFilter(admin.SimpleListFilter):

	title = _('periodo')
	parameter_name = 'intervalo'

	def lookups(self, request, model_admin):
		return (
			('proximas', _('à partir de amanhã')),
		    ('hoje', _('hoje')),
		    ('sete_dias', _('últimos sete dias')),
		    ('trinta_dias', _('últimos trinta dias')),
		    ('esse_ano', _('esse ano')),
		)

	def queryset(self, request, queryset):
		if self.value() == 'proximas':
			todas_consultas = Consulta.objects.select_related('medico')
			consultas_por_periodo = todas_consultas.filter(data__gt=date.today())
			return queryset.filter(id__in=consultas_por_periodo.values('medico'))
		if self.value() == 'hoje':
			todas_consultas = Consulta.objects.select_related('medico')
			consultas_por_periodo = todas_consultas.filter(data=date.today())
			return queryset.filter(id__in=consultas_por_periodo.values('medico'))
		if self.value() == 'sete_dias':
			uma_semana_atras = date.today() - timedelta(days=7)
			todas_consultas = Consulta.objects.select_related('medico')
			consultas_por_periodo = todas_consultas.filter(data__gte=uma_semana_atras)
			return queryset.filter(id__in=consultas_por_periodo.values('medico'))
		if self.value() == 'trinta_dias':
			trinta_dias_atras = date.today() - timedelta(days=30)
			todas_consultas = Consulta.objects.select_related('medico')
			consultas_por_periodo = todas_consultas.filter(data__gte=trinta_dias_atras)
			return queryset.filter(id__in=consultas_por_periodo.values('medico'))
		if self.value() == 'esse_ano':
			todas_consultas = Consulta.objects.select_related('medico')
			consultas_por_periodo = todas_consultas.filter(data__year=date.today().year)
			return queryset.filter(id__in=consultas_por_periodo.values('medico'))


@admin.register(Medico)
class MedicoAdmin(UserAdmin):
	
	add_form = MedicoCreateForm
	form = MedicoChangeForm
	model = Medico
	
	list_display = ('first_name', 'last_name', 'email', 'telefone', 'cpf', 
							'especialidade', 'is_staff', 'total_de_consultas')
	list_filter = ('especialidade', ConsultasPeriodoListFilter)
	fieldsets = (
		(None, {'fields': ('cpf', 'password')}),
		('Informações Pessoais', {'fields': (
			'first_name', 'last_name', 'telefone', 'email', 'imagem', 'especialidade', 'sexo',
			'formacao', 'consultas'
		)}),
		('Permissões', {'fields': (
			'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
		)}),
		('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
	)
	readonly_fields = ['last_login', 'date_joined']

	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		queryset = queryset.annotate(
		    _total_de_consultas=Count('consultas', distinct=True),
		)
		return queryset 

	def total_de_consultas(self, obj):
	    return obj._total_de_consultas

	def change_view(self, request, object_id, form_url='', extra_context=None):
		consultas = Consulta.objects.filter(medico__exact=object_id)
		if len(consultas) > 0:
			extra_context = dict(show_save=True, show_save_and_continue=True, show_delete=False)
		else:
			extra_context = dict(show_save=True, show_save_and_continue=True, show_delete=True)
		template_response = super().change_view(request, object_id, form_url, extra_context)
		return template_response

	total_de_consultas.admin_order_field = '_total_de_consultas'


class TemConsultaListFilter(admin.SimpleListFilter):

	title = _('consulta')
	parameter_name = 'paciente'

	def lookups(self, request, model_admin):
		return (
		    ('com_consulta', _('com consulta')),
		    ('sem_consulta', _('sem consulta')),
		)

	def queryset(self, request, queryset):
		todas_consultas = Consulta.objects.select_related('paciente')
		if self.value() == 'com_consulta':
			return queryset.filter(id__in=todas_consultas.values('paciente'))
		if self.value() == 'sem_consulta':
			return queryset.exclude(id__in=todas_consultas.values('paciente'))
	

@admin.register(Paciente)
class PacienteAdmin(UserAdmin):
	
	add_form = PacienteCreateForm
	form = PacienteChangeForm
	model = Paciente
	actions = None 
	
	list_display = (
		'first_name', 'last_name', 'email', 'telefone', 'cpf', 'data_nascimento', 'sexo', 'tem_consulta'
	)
	fieldsets = (
		(None, {'fields': ('cpf', 'password')}),
		('Informações Pessoais', {'fields': (
			'first_name', 'last_name', 'telefone', 'email', 'imagem', 'data_nascimento', 
			'sexo', 'formacao', 'comentarios')}),
		('Permissões', {'fields': (
			'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
		)}),
		('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
	)
	readonly_fields = ['last_login', 'date_joined']
	list_filter = (TemConsultaListFilter,)
	
	def tem_consulta(self, obj):
		todas_consultas = Consulta.objects.select_related('paciente')
		paciente_com_consulta = Paciente.objects.filter(id__in=todas_consultas.values('paciente'))
		for paciente in paciente_com_consulta:
			if obj.id == paciente.id:
				return True
		return False 

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request):
		return False

	def save_model(self, request, obj, form, change):
		pass

	tem_consulta.boolean = True


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
	
	list_display = ('horario', )


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
	
	list_display = ('id', 'data', 'hora', 'estado', 'medico', 'paciente', 'ativo')

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request):
		return False

	def save_model(self, request, obj, form, change):
		pass


