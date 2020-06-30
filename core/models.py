from __future__ import unicode_literals
from stdimage.models import StdImageField
from datetime import datetime, date
import uuid

from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


def get_file_path(_instance, filename):
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4(), ext)
	return filename


class SingletonModel(models.Model):

	class Meta:
		abstract = True

	def delete(self, *args, **kwargs):
		pass

	def set_cache(self):
		cache.set(self.__class__.__name__, self)

	def save(self, *args, **kwargs):
		self.pk = 1
		super(SingletonModel, self).save(*args, **kwargs)
		self.set_cache()

	@classmethod
	def load(cls):
		if cache.get(cls.__name__) is None:
			obj, created = cls.objects.get_or_create(pk=1)
			if not created:
				obj.set_cache()
		return cache.get(cls.__name__)


class SiteSettings(SingletonModel):

	endereco = models.CharField(max_length=255, default='Mitlton Str. 26-27 London UK')
	telefone = models.CharField(max_length=255, default='+5585999999999')
	email = models.EmailField(max_length=255, default='clinica@email.com')
	suporte = models.EmailField(default='support@email.com')
	account_sid = models.CharField(max_length=255, default='ACbcad883c9c3e9d9913a715557dddff88')
	auth_token = models.CharField(max_length=255, default='abd4d45dd57dd79b86dd51df2e2a6cd7')

	class Meta:
		verbose_name = 'Configuração do Site'
		verbose_name_plural = 'Configurações do Site' 

	def __str__(self):
		return 'Configurações'


class Base(models.Model):
	
	criado = models.DateField('Criação', auto_now_add=True)
	modificado = models.DateField('Atualização', auto_now=True)
	ativo = models.BooleanField('Ativo', default=True)

	class Meta:
		abstract = True


class Especialidade(Base):
	
	CHOICES = (
		('Cardiologia', 'Cardiologia'),
		('Cirurgia', 'Cirurgia'),
		('Clínica Geral', 'Clínica Geral'),
		('Gastroenterologia', 'Gastroenterologia'),
		('Neurologia', 'Neurologia'),
		('Odontologia', 'Odontologia'), 
		('Oftalmologia', 'Oftalmologia'), 
		('Ortopedia', 'Ortopedia'), 
		('Pediatria', 'Pediatria'),
	)
	nome = models.CharField('Especialidade', max_length=50, choices=CHOICES)
	descricao = models.TextField('Descricao', max_length=200)
	icone = StdImageField('Icone', upload_to=get_file_path, variations={
		'thumb': {'width': 41, 'height': 49, 'crop': True}
	})

	class Meta:
		verbose_name = 'Especialidade'
		verbose_name_plural = 'Especialidades'

	def __str__(self):
		return self.nome


class Consulta(Base):
	
	CHOICES = (
		('Agendada', 'Agendada'),
		('Cancelada', 'Cancelada'),
		('Espera', 'Espera'),
		('Realizada', 'Realizada'),
	)
	data = models.DateField('Data da Consulta')
	hora = models.ForeignKey(
		'core.Horario', 
		verbose_name='Horário', 
		on_delete=models.CASCADE
	)
	sintomas = models.TextField('Sintomas', max_length=500, null=True, blank=True)
	remedios = models.TextField('Remedios', max_length=500, null=True, blank=True)
	exames = models.TextField('Exames', max_length=500, null=True, blank=True)
	estado = models.CharField('Estado', max_length=9, choices=CHOICES, default='Agendada')
	medico = models.ForeignKey(
		'core.Medico', 
		verbose_name='Médico', 
		on_delete=models.CASCADE,
		related_name='medico_consulta_set'
	)
	paciente = models.ForeignKey(
		'core.Paciente', 
		verbose_name='Paciente', 
		on_delete=models.CASCADE,
		related_name='paciente_consulta_set'
	)
	motivo_cancelamento = models.TextField(
		'Motivo do Cancelamento', max_length=100, null=True, blank=True
	)

	@property
	def expirada(self):
		hoje = date.today()
		hora = int(self.hora.horario[0] + self.hora.horario[1])
		agora = datetime.now()
		if hoje == self.data and self.estado != 'Realizada':
			return agora.hour > hora
		return hoje > self.data and self.estado != 'Realizada'

	class Meta:
		verbose_name = 'Consulta'
		verbose_name_plural = 'Consultas'


class Pessoa(AbstractUser):

	CHOICES = (
		('Masculino', 'Masculino'),
		('Feminino', 'Feminino'),
	)
	is_staff = models.BooleanField('Membro da equipe', default=False)
	cpf = models.CharField('CPF', max_length=15, unique=True)
	telefone = models.CharField('Telefone', max_length=17)
	email = models.EmailField('E-mail', unique=True)
	imagem = StdImageField('Imagem', upload_to=get_file_path, null=True, blank=True, variations={
		'thumb': {'width': 264, 'height': 276, 'crop': True}
	})
	formacao = models.CharField('Formacao', max_length=30, default='')
	sexo = models.CharField('Sexo',  max_length=9, choices=CHOICES)

	class Meta:
		abstract = True


class UsuarioManager(BaseUserManager):
	
	use_in_migrations = True

	def _create_user(self, cpf, password, **extra_fields):
		if not cpf:
			raise ValueError('CPF obrigatório!')
		user = self.model(cpf=cpf, username=cpf, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, cpf, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(cpf, password, **extra_fields)

	def create_superuser(self, cpf, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser precisa ter is_superuser=True')

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser precisa ter is_staff=True')

		return self._create_user(cpf, password, **extra_fields)


class CustomUsuario(Pessoa):

	USERNAME_FIELD = 'cpf'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

	def __str__(self):
		return self.first_name

	class Meta:
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'

	objects = UsuarioManager()


class MedicoManager(UsuarioManager):
	
	use_in_migrations = True

	def _create_user(self, cpf, password, especialidade, formacao, **extra_fields):
		if not cpf and not especialidade:
			raise ValueError('CPF e especialidade obrigatórios!')
		user = self.model(
			cpf=cpf, especialidade=especialidade, formacao=formacao, username=cpf, **extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, cpf, especialidade, formacao, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(cpf, especialidade, formacao, password, **extra_fields)

	def create_superuser(self, cpf, especialidade, formacao, password, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser precisa ter is_staff=True')

		return self._create_user(cpf, especialidade, formacao, password, **extra_fields)

class Medico(CustomUsuario):
	
	especialidade = models.ForeignKey(
		'core.Especialidade', 
		verbose_name='Especialidade', 
		on_delete=models.CASCADE, 
		null=True, 
		blank=True
	)
	consultas = models.ManyToManyField(Consulta, related_name='consultas_medico_set', blank=True)

	REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'especialidade']

	class Meta:
		verbose_name = 'Médico'
		verbose_name_plural = 'Médicos'

	def __str__(self):
		return self.first_name

	objects = MedicoManager()


class PacienteManager(BaseUserManager):
	
	use_in_migrations = True

	def _create_user(self, cpf, password, data_nascimento, **extra_fields):
		if not cpf and not data_nascimento:
			raise ValueError('CPF e data de nascimento obrigatórios!')
		user = self.model(cpf=cpf, username=cpf, data_nascimento=data_nascimento, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, cpf, data_nascimento, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(cpf, password, data_nascimento, **extra_fields)


class Paciente(CustomUsuario):
	
	data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
	comentarios = models.ForeignKey(
		'core.Comentario', 
		verbose_name='Comentario', 
		on_delete=models.CASCADE, 
		null=True, 
		blank=True
	)
	consultas = models.ManyToManyField(Consulta, related_name='consultas_paciente_set')

	REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'data_nascimento']

	class Meta:
		verbose_name = 'Paciente'
		verbose_name_plural = 'Pacientes'

	def __str__(self):
		return self.first_name

	objects = PacienteManager()


class Comentario(Base):
	
	texto = models.TextField('Comentario', max_length=500)
	usuario = models.ForeignKey(
		'core.Paciente', verbose_name='Paciente', on_delete=models.CASCADE
	)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'

	def __str__(self):
		return self.texto


class Horario(models.Model):

	CHOICES = (
		('08h-09h', '08h-09h'),
		('09h-10h', '09h-10h'),
		('10h-11h', '10h-11h'),
	)
	horario = models.CharField('Horario', max_length=7, choices=CHOICES)

	def __str__(self):
		return self.horario

	class Meta:
		verbose_name = 'Horário'
		verbose_name_plural = 'Horários'


class Notificacao(models.Model):

	criada = models.DateField('Criação', auto_now_add=True)
	paciente = models.ForeignKey(
		'core.Paciente',
		verbose_name='Notificação',
		on_delete=models.CASCADE, 
		related_name='paciente_notificacao_set'
	)
	mensagem = models.TextField('Mensagem', max_length=500, null=True, blank=True)
	consulta = models.ForeignKey(
		'core.Consulta',
		verbose_name='Consulta',
		on_delete=models.CASCADE, 
		null=True, 
		blank=True,
		related_name='consulta_notificacao_set'
	)
	lida = models.BooleanField(default=False)


def cria_notificacao(sender, instance, **kwargs):
	if instance.estado == 'Cancelada':
		query = Consulta.objects.filter(
			Q(data__exact=instance.data),
			Q(hora__exact=instance.hora),
			Q(estado__exact='Espera')
		)
		if query.count() > 0:
			dias_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui','Sex', 'Sab']
			meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 
		         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
			dia = int(instance.data.strftime("%w"))
			data = dias_semana[dia] + ', ' + str(instance.data.day) + ' de ' + \
				meses[instance.data.month-1]
		
			notificacao = Notificacao(
				paciente=query[0].paciente, 
				mensagem=f'A vaga para {data} e horario {instance.hora} foi aberta, ',
				consulta = query[0]
			)
			notificacao.save()


def atualiza_consultas_medico(sender, instance, **kwargs):
	m = Medico.objects.get(pk=instance.medico.id)
	m.consultas.add(instance)


def marca_como_lida(sender, instance, **kwargs):
	if instance.estado == 'Agendada' or instance.estado == 'Cancelada':
		try:
			notificacao = Notificacao.objects.get(consulta=instance)
			if notificacao:
				notificacao.lida = True
				notificacao.save(update_fields=['lida'])
		except ObjectDoesNotExist:
			pass


post_save.connect(cria_notificacao, sender=Consulta)
post_save.connect(atualiza_consultas_medico, sender=Consulta)
post_save.connect(marca_como_lida, sender=Consulta)

