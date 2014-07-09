from django.contrib import admin
from models import *
# Register your models here.
class productoAdmin(admin.ModelAdmin):
	list_display = ('nombre','thumbnail','precio','stock')
	list_filter = ('nombre','precio')
	search_fields = ['nombre','precio']
	fields = ('nombre','descripcion',('precio','stock','imagen'),'categorias','status')




admin.site.register(Pedido)
admin.site.register(cliente)
admin.site.register(producto,productoAdmin)
admin.site.register(categoriaProducto)
