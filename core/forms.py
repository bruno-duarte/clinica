from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import CustomUsuario, Medico, Paciente, Especialidade, Consulta


class CustomUsuarioCreateForm(UserCreationForm):

	class Meta:
		model = CustomUsuario
		fields = {'first_name', 'last_name', 'cpf'}
		labels = {'username': 'Username/CPF'}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.cpf = self.cleaned_data['username']

		if commit:
			user.save()
		return user


class CustomUsuarioChangeForm(UserChangeForm):

	class Meta:
		model = CustomUsuario
		fields = {'first_name', 'last_name', 'cpf'}


class MedicoCreateForm(UserCreationForm):

	class Meta:
		model = Medico
		fields = {
			'first_name', 'last_name', 'cpf', 'imagem', 'especialidade', 'formacao','consultas'
		}
		labels = {
			'username': 'Username/CPF', 'imagem': 'Foto', 'especialidade': 'Especialidade', 
			'formacao': 'Formação', 'consultas' : 'Consultas'
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.cpf = self.cleaned_data['username']

		if commit:
			user.save()
		return user


class MedicoChangeForm(UserChangeForm):

	class Meta:
		model = Medico
		fields = {'first_name', 'last_name', 'cpf', 'imagem', 'especialidade', 'formacao'}


class PacienteCreateForm(UserCreationForm):

	class Meta:
		model = Paciente
		fields = {'first_name', 'last_name', 'cpf', 'imagem', 'data_nascimento'}
		labels = {'username': 'Username/CPF', 'data_nascimento': 'Data de nascimento'}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.cpf = self.cleaned_data['username']

		if commit:
			user.save()
		return user


class PacienteChangeForm(UserChangeForm):

	class Meta:
		model = Paciente
		fields = {'first_name', 'last_name', 'cpf', 'imagem', 'formacao', 'data_nascimento'}


class SignUpForm(UserCreationForm):

	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	cpf = forms.CharField(max_length=11, help_text='O CPF é obrigatório!')
	telefone = forms.CharField(max_length=15, required=False, help_text='Optional')
	email = forms.EmailField(max_length=254, help_text='Campo obrigatório')
	data_nascimento = forms.DateField(help_text='Campo obrigatório!')

	class Meta:
		model = Paciente
		fields = [ 'username', 'first_name', 'last_name', 'cpf', 'telefone', 'email', 
		           'data_nascimento', 'password1', 'password2', ]


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Paciente

		fields = ['first_name', 'last_name', 'email', 'telefone', 'imagem', 
															'data_nascimento', 'is_active']


class PasswordChangeForm(SetPasswordForm):

	class Meta:
		model = Paciente

	error_messages = dict(SetPasswordForm.error_messages, **{
		'password_incorrect': _("A senha digitada não corresponde com sua senha atual. "
								"Por favor, insira novamente."),
	})
	old_password = forms.CharField(label=("Senha Antiga"),
									widget=forms.PasswordInput)

	def clean_old_password(self):
		old_password = self.cleaned_data["old_password"]
		if not self.user.check_password(old_password):
			raise forms.ValidationError(
				self.error_messages['password_incorrect'],
				code='password_incorrect',
			)
		return old_password


class BookingForm(forms.ModelForm):

	data = forms.DateField()

	class Meta:
		model = Especialidade

		fields = ['nome']

	def clean_data(self):
		d = self.cleaned_data['data']
		if d < datetime.date.today():
			raise ValidationError(_('Data inválida'))
		return d


class BookingResultsForm(forms.ModelForm):

	class Meta:
		model = Consulta

		fields = ['data', 'hora', 'estado', 'medico', 'paciente', 'ativo']


class UpdateAppointmentsForm(forms.ModelForm):

	sintomas = forms.CharField(max_length=500)
	remedios = forms.CharField(max_length=500, required=False, help_text='Optional.')
	exames = forms.CharField(required=False, help_text='Optional.')
	estado = forms.CharField(max_length=9)

	class Meta:
		model = Consulta

		fields = ['sintomas', 'remedios', 'exames', 'estado']
