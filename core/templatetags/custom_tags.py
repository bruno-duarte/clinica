from django import template

register = template.Library()


from core.models import Consulta
from django.db.models import Q
from datetime import datetime
@register.simple_tag
def tem_vaga(medico, hora, data):
	d = datetime.strptime(data, '%Y-%m-%d').date()
	vaga = Consulta.objects.filter(
		Q(medico__exact=medico) & Q(hora=hora) & Q(data=d)
	)
	if len(vaga) == 0:
		return True
	else:
		return False


@register.simple_tag
def mesmo_usuario(data, hora, estado, medico, usuario):
	d = datetime.strptime(data, '%Y-%m-%d').date()
	usuario = Consulta.objects.filter(
		Q(data=d) & 
		Q(hora=hora) & 
		Q(estado=estado) & 
		Q(medico__exact=medico) & 
		Q(paciente__exact=usuario)  
	)
	if len(usuario) > 0:
		return True
	else:
		return False


@register.simple_tag
def tem_consulta(usuario):
	consultas = Consulta.objects.filter(Q(paciente__exact=usuario))
	if len(consultas) > 0:
		return True
	else:
		return False

