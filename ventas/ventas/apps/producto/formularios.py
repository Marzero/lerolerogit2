#encoding:utf-8
from django.forms import ModelForm
from django.db import models
from django import forms
from models import *

class addProductForm(forms.ModelForm):
	class Meta:
		model   = producto
		exclude = {'status',}

"""
class addProductForm(forms.Form):
	nombre = forms.CharField(widget=forms.TextInput())
	descripcion = forms.CharField(widget=forms.TextInput())
	imagen 		= forms.ImageField(required=False)
	precio		= forms.DecimalField(required=True)
	stock		= forms.IntegerField(required=True)

	def clean(self):
		return self.cleaned_data
"""
class addCategoria(forms.ModelForm):
	class Meta:
		model=categoriaProducto

class fbuscar(forms.Form):
    texto=forms.CharField(max_length=50, label="Buscar productos")

class fcarrito(ModelForm):
    class Meta:
        model=Carrito
        exclude=['producto','id_sesion','estado']


opciones_tipo=(
	('Cliente','Cliente'),
	#('Vendedor','Vendedor'),
)
class ClienteRegistro(forms.Form):
	nombre=forms.CharField(required=True,help_text="Este campo es requerido")
	apellidos=forms.CharField(required=True,help_text="Este campo es requerido")
	email=forms.EmailField(required=True,help_text="Este campo es requerido")
	ci=forms.CharField(required=True,help_text="Este campo es requerido")
	telefono=forms.CharField(required=False)
	tipo=forms.ChoiceField(choices=opciones_tipo,label="Tipo de Usuario",help_text="Selecciona el tipo de usuario")
	#podemos crear nuestra propia validacion
	def clean_ci(self):
	    txt_ci = self.cleaned_data.get("ci")
	    cadena=str(txt_ci)
	    tam=len(cadena)
	    if tam < 7 or tam > 8:
	        raise forms.ValidationError("Ingrese un ci valido")
	    return txt_ci
class addPedido(forms.ModelForm):
	class Meta:
		model=Pedido
class addProducto(forms.ModelForm):
	class Meta:
		model=producto