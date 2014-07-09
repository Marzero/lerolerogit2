from django.db import models
from django.contrib.auth.models import User
# Create your models here.
"""
class cliente(models.Model):
    
    nombre      = models.CharField(max_length=200)
    apellidos   = models.CharField(max_length=200)
    status      = models.BooleanField(default=True)

    def __unicode__(self):
        nombreCompleto = "%s %s"%(self.nombre,self.apellidos)
        return nombreCompleto
"""
class cliente(models.Model):
    User = models.ForeignKey(User,unique=True)
    fecha_nacimiento=models.DateField()
    #sexo=models.IntegerField(null=False)
    ci = models.IntegerField(null=False)
    telefono=models.IntegerField(null=False,max_length=8)
    def __unicode__(self):
        return self.ci
        
class categoriaProducto(models.Model):
    nombre  = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=400)

    def __unicode__(self):
        return self.nombre
class producto(models.Model):
    def url(self,filename):
        ruta = "MultimediaData/Producto/%s/%s"%(self.nombre,str(filename))
        return ruta

    def thumbnail(self):
        return '<a href="/media/%s"><img src="/media/%s" width=50px heigth=50px/></a>'%(self.imagen,self.imagen)

    thumbnail.allow_tags = True

    nombre      =models.CharField(max_length=30,null=False)
    descripcion =models.CharField(max_length=500,null=False)
    status      = models.BooleanField(default=True)
    precio      =models.FloatField(null=False)
    imagen      =models.ImageField(upload_to="producto",null=True)
    stock       =models.IntegerField(default=0)
    categorias  = models.ManyToManyField(categoriaProducto,null=True,blank=True)
    compatibilidad=models.ManyToManyField('self',null=True,blank=True)
    def __unicode__(self):
        return self.nombre

class Pedido(models.Model):
    cliente=models.ForeignKey(User)
    producto=models.ManyToManyField(producto)
    cantidad=models.IntegerField()
    precio_total=models.FloatField()
    fecha=models.DateTimeField(auto_now_add=True)
    #def __unicode__(self):
     #   return self.producto

class Carrito(models.Model):
    id_sesion=models.CharField(max_length=200)
    estado=models.BooleanField ( default = False )
    producto=models.ForeignKey(producto)
    cantidad=models.IntegerField()

	
