from django.contrib import admin
from .models import Especialidade


@admin.register(Especialidade)
class CargoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'icone', 'ativo', 'modificado')
