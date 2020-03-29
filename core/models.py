from django.db import models
from stdimage.models import StdImageField
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


def get_file_path(_instance, filename):
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4(), ext)
	return filename


class Base(models.Model):
	criados = models.DateField('Criação', auto_now_add=True)
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
	icone = StdImageField('Icone', upload_to=get_file_path, \
		variations={'thumb': {'width': 41, 'height': 49, 'crop': True}})

	class Meta:
		verbose_name = 'Especialidade'
		verbose_name_plural = 'Especialidades'

	def __str__(self):
		return self.nome


class Pessoa(AbstractUser):

	is_staff = models.BooleanField('Membro da equipe', default=False)
	cpf = models.CharField('CPF', max_length=15, unique=True)
	telefone = models.CharField('Telefone', max_length=15)
	email = models.EmailField('E-mail', unique=True)
	imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 264, 'height': 276, 'crop': True}})
	formacao = models.CharField('Formacao', max_length=30, default='')

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
		return self.cpf

	objects = UsuarioManager()


class MedicoManager(UsuarioManager):
	
	use_in_migrations = True

	def _create_user(self, cpf, password, especialidade, formacao, **extra_fields):
		if not cpf and not especialidade:
			raise ValueError('CPF e especialidade obrigatórios!')
		user = self.model(cpf=cpf, especialidade=especialidade, formacao=formacao, username=cpf, **extra_fields)
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
	especialidade = models.ForeignKey('core.Especialidade', verbose_name='Especialidade', on_delete=models.CASCADE, null=True, blank=True)

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
	data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
	comentarios = models.ForeignKey('core.Comentario', verbose_name='Comentario', on_delete=models.CASCADE, null=True, blank=True)

	REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'data_nascimento']

	class Meta:
		verbose_name = 'Paciente'
		verbose_name_plural = 'Pacientes'

	def __str__(self):
		return self.first_name

	objects = PacienteManager()


class Comentario(Base):
	
	texto = models.TextField('Comentario', max_length=500)
	usuario = models.ForeignKey('core.Paciente', verbose_name='Paciente', on_delete=models.CASCADE, default='')

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'

	def __str__(self):
		return self.texto


