from datetime import datetime, date, timedelta

from django import template
from django.db.models import Q

from core.models import (
	Consulta, Paciente, CustomUsuario, Notificacao
)


register = template.Library()


@register.simple_tag
def tem_vaga(medico, hora, data):
	d = datetime.strptime(data, '%Y-%m-%d').date()
	vaga = Consulta.objects.filter(
		Q(medico__exact=medico) & Q(hora=hora) & Q(data=d)
	).exclude(estado__exact='Cancelada')
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


@register.simple_tag
def total_consultas(usuario):
	total = Consulta.objects.filter(medico__exact=usuario).count()
	return total


@register.simple_tag
def total_prox_consultas(usuario):
	total = Consulta.objects.filter(
		Q(medico__exact=usuario) & 
		Q(data__gt=datetime.today())
	).count()
	return total


@register.simple_tag
def total_consultas_hoje(usuario):
	total = Consulta.objects.filter(
		Q(medico__exact=usuario) & 
		Q(data=datetime.today())
	).count()
	return total


@register.simple_tag
def map_mes():
	mes = datetime.today().month
	meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
	         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	return meses[mes-1]


@register.simple_tag
def total_consultas_realizadas(usuario):
	total = Consulta.objects.filter(
		Q(medico__exact=usuario) & 
		Q(estado__exact='Realizada') & 
		Q(data=datetime.today())
	).count()
	return total


@register.simple_tag
def porcentagem_consultas(usuario):
	todas_consultas = Consulta.objects.all().count()
	consultas_usuario = Consulta.objects.filter(medico__exact=usuario).count()
	try:
		p = int((consultas_usuario/todas_consultas)*100)
	except ZeroDivisionError:
		p = 0
	return p


@register.simple_tag
def porcentagem_consultas_hoje(usuario):
	todas_consultas = Consulta.objects.filter(Q(medico__exact=usuario)).count()
	consultas_hoje = Consulta.objects.filter(
		Q(medico__exact=usuario) & 
		Q(data=datetime.today())
	).count()
	try:
		p = int((consultas_hoje/todas_consultas)*100)
	except ZeroDivisionError:
		p = 0
	return p


@register.simple_tag
def porcentagem_consultas_realizadas(usuario):
	consultas_hoje = Consulta.objects.filter(
		Q(medico__exact=usuario) &
		Q(data=datetime.today())
	).count()
	consultas_realizadas = Consulta.objects.filter(
		Q(medico__exact=usuario) & 
		Q(estado__exact='Realizada') & 
		Q(data=datetime.today())
	).count()
	try:
		p = int((consultas_realizadas/consultas_hoje)*100)
	except ZeroDivisionError:
		p = 0
	return p


@register.simple_tag
def caminho(url):
	return url


@register.simple_tag
def calcula_idade(id):
	paciente = Paciente.objects.get(pk=id)
	hoje = datetime.today()
	nascimento = paciente.data_nascimento
	idade = hoje.year - nascimento.year
	if hoje.month < nascimento.month:
		idade -= 1
	elif hoje.month == nascimento.month:
		if hoje.day < nascimento.day:
			idade -= 1
	return idade


def inteiro_em_string(inteiro):
	if inteiro >= 10:
		return str(inteiro)
	else:
		return '0' + str(inteiro)


@register.simple_tag
def mostra_data_nascimento(id):
	paciente = Paciente.objects.get(pk=id)
	data_nascimento = (
		inteiro_em_string(paciente.data_nascimento.day) + 
		'/' + 
		inteiro_em_string(paciente.data_nascimento.month) + 
		'/' + 
		str(paciente.data_nascimento.year)
	)
	return data_nascimento


@register.simple_tag
def iniciais_nome(id):
	usuario = CustomUsuario.objects.get(pk=id)
	return usuario.first_name[0] + usuario.last_name[0]


@register.simple_tag
def pode_cancelar(consulta):
	hora = int(consulta.hora.horario[0] + consulta.hora.horario[1])
	data_cons = datetime(consulta.data.year, consulta.data.month, consulta.data.day, hora)
	delta = data_cons - datetime.today()
	return delta.days >= 1
	