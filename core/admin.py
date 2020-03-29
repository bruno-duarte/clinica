from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm, MedicoCreateForm, MedicoChangeForm, \
	PacienteCreateForm, PacienteChangeForm
from .models import Especialidade, CustomUsuario, Medico, Paciente, Comentario


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
	list_display = ('nome', 'icone', 'ativo', 'modificado')


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
	add_form = CustomUsuarioCreateForm
	form = CustomUsuarioChangeForm
	model = CustomUsuario
	list_display = ('first_name', 'last_name', 'email', 'telefone', 'cpf', 'is_staff')
	fieldsets = (
		(None, {'fields': ('cpf', 'password')}),
		('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone', 'email')}),
		('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
	)


@admin.register(Medico)
class MedicoAdmin(UserAdmin):
	add_form = MedicoCreateForm
	form = MedicoChangeForm
	model = Medico
	list_display = ('first_name', 'last_name', 'email', 'telefone', 'cpf', 'especialidade', 'formacao', 'is_staff')
	fieldsets = (
		(None, {'fields': ('cpf', 'password')}),
		('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone', 'email', 'imagem', 'especialidade', 'formacao')}),
		('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
	)
	

@admin.register(Paciente)
class PacienteAdmin(UserAdmin):
	add_form = PacienteCreateForm
	form = PacienteChangeForm
	model = Paciente
	list_display = ('first_name', 'last_name', 'email', 'telefone', 'cpf', 'data_nascimento', 'formacao', 'is_staff')
	fieldsets = (
		(None, {'fields': ('cpf', 'password')}),
		('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone', 'email', 'imagem', 'data_nascimento', 'formacao', 'comentarios')}),
		('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
	)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
	list_display = ('texto', 'modificado')
