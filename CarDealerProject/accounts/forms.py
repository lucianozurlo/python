from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-light mt-2'}),
    )

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label='Usuario', 
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    password1 = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    password2 = forms.CharField(
        label='Repetir contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    first_name = forms.CharField(
        label='Nombre', 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    last_name = forms.CharField(
        label='Apellido', 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    email = forms.EmailField(
        label='E-mail',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    avatar = forms.ImageField(
        label='Avatar',
        widget=forms.FileInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'avatar']

class AvatarForm(forms.Form):
    avatar = forms.ImageField(label='Avatar')

class UserEditForm(forms.Form):
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    last_name = forms.CharField(
        label='Apellido',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    email = forms.EmailField(
        label='E-mail:',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    avatar = forms.ImageField(
        label='Avatar',
        widget=forms.FileInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        required=False)

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'avatar']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))
    password2 = forms.CharField(
        label="Repetir nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")

        if not authenticate(username=self.user.username, password=current_password):
            raise forms.ValidationError("La contraseña actual es incorrecta.")

        return cleaned_data
