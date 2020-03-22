from django.contrib import admin
from .models import Especialidade, Medico


@admin.register(Especialidade)
class CargoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'icone', 'ativo', 'modificado')


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'especialidade', 'formacao')