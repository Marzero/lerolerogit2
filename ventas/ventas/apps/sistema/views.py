from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from ventas.apps.producto.formularios import *
#importamos Q para realizar consultas mas avanzadas
from django.db.models import Q
from ventas.apps.producto.models import *
# Create your views here.
def portal(request):
    formulario=fbuscar()
    return render_to_response("sistema/portal.html",{'fbuscar':formulario},context_instance=RequestContext(request))

def buscar(request):
    if request.method=="POST":
        """Aqui ira otra busqueda igual que abajo"""
        return HttpResponse("hecho")
    else:
        texto=request.GET["texto"]
        busqueda=(
            Q(nombre__icontains=texto) |
            Q(descripcion__icontains=texto) |
            Q(precio__icontains=texto)
        )
        resultados=producto.objects.filter(busqueda).distinct()
        html="<ul class='ul_lista'>"
        for i in resultados:
            html=html+"<li><a href='/producto/"+str(i.id)+"/'>"+i.nombre+"</a></li>"
        html=html+"<ul>"
        return HttpResponse(html)