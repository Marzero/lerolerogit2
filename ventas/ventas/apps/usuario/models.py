from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Perfil(models.Model):
    user = models.ForeignKey(User, unique=True)
    fecha_nacimiento=models.DateField()
    imagen =models.ImageField(null=True,upload_to='img')
    sexo = models.IntegerField(null=False)
    ci=models.IntegerField(null=True,unique=True)
    telefono = models.IntegerField(null=True)