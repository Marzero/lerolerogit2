#encoding:utf-8
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    Email   = forms.EmailField(widget=forms.TextInput())
    Titulo  = forms.CharField(widget=forms.TextInput())
    Texto   = forms.CharField(widget=forms.Textarea())


class ActivarCuenta(forms.Form):
    ci=forms.CharField(widget=forms.TextInput(attrs={'maxlength':8}), required=True)
    telefono=forms.CharField(max_length=7,required=True)

lista_anios = range(2013,1905,-1)
CHOICES = (('1', 'Hombre',), ('2', 'Mujer',))
class fperfil(ModelForm):
    fecha_nacimiento=forms.DateField(initial='dia-mes-anio',widget=SelectDateWidget(years=lista_anios))
    sexo=forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    class Meta:
        model=Perfil
        exclude = ['user','imagen','ci','telefono']

class fusuario(UserCreationForm):
    username = forms.CharField(max_length=40,required=True,help_text=False,label="Nombre de usuario")
    password2 = forms.CharField(help_text=False,label="Contraseña de confirmacion",widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=40,required=True,label="Nombre")
    last_name=forms.CharField(max_length=50,required=True,label="Apellidos")
    email=forms.EmailField(max_length=60,required=True,label="Email",widget=forms.TextInput)
    class Meta:
        model=User
        fields=("username","password1","password2","first_name","last_name","email")
    def save(self, commit=True):
        user=super(fusuario,self).save(commit=False)
        user.first_name=self.cleaned_data.get("first_name")
        user.last_name=self.cleaned_data.get("last_name")
        user.email=self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class RegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput())
    email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
    password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
    password_two = forms.CharField(label="Confirmar password",widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya existe')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado')

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coinciden')
















