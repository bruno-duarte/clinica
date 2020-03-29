from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUsuario, Medico, Paciente


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
		fields = {'first_name', 'last_name', 'cpf', 'imagem', 'especialidade', 'formacao'}
		labels = {'username': 'Username/CPF', 'imagem': 'Foto', 'especialidade': 'Especialidade', 'formacao': 'Formação'}

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
		fields = [
			'username',
			'first_name', 
			'last_name', 
			'cpf',
			'telefone', 
			'email', 
			'data_nascimento', 
			'password1', 
			'password2', 
		]


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Paciente
		fields = [
			'username',
			'first_name', 
			'last_name', 
			'email',
		]

