from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ventas.apps.producto.formularios import addProductForm,addCategoria,addPedido,addProducto
from ventas.settings import URL_LOGIN
from models import *
from formularios import *
import hashlib
import datetime
import pdb
# Create your views here.
#-------------paginador
from django.contrib.auth.decorators import login_required
from ventas.settings import URL_LOGIN
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q
import json
import simplejson
#-------------------------------inicio de clientes------------------------------------------#
from django.contrib.auth.models import User, Group #importamos los modelos User y Group de django
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm #importamos los formularios para las sessiones en django
from django.contrib.auth import login, authenticate, logout #importamos los metodos para el uso de sessiones en django
#from formularios import ClienteRegistro #importamos el formulario para el registro de usuarios
from .formularios import *
from .models import *
#-------------------reportes-----------
import os
import StringIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string

def registro_view(request):
    #preguntamos si el usuario inicio session
    """if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:"""
    form2=cliente.objects.all()
    if request.method=='POST':
        formulario=UserCreationForm(request.POST)
        formulario2=ClienteRegistro(request.POST)
        
        if formulario.is_valid() and formulario2.is_valid():
            usuario=request.POST['username']
            formulario.save()
            nombre=request.POST['nombre']
            apellidos=request.POST['apellidos']
            email=request.POST['email']
            ci=request.POST['ci']
            telefono=request.POST['telefono']
            tipo_usuario=request.POST['tipo']
            #sexo=request.POST['rsexo']
            dia=request.POST['sdia']
            mes=request.POST['smes']
            anio=request.POST['sanio']
            fecha_nacimiento=anio+"-"+mes+"-"+dia
            nuevo_usuario=User.objects.get(username=usuario)
            if tipo_usuario=='Cliente':
                grupo,crear_grupo=Group.objects.get_or_create(name='Cliente')
            if tipo_usuario=='Vendedor':
                grupo,crear_grupo=Group.objects.get_or_create(name='Vendedor')
            perfil=cliente.objects.create(User=nuevo_usuario,fecha_nacimiento=fecha_nacimiento,ci=ci,telefono=telefono)
            if crear_grupo != None:
                nuevo_usuario.groups.add(grupo)
                nuevo_usuario.is_actived=True
                nuevo_usuario.is_staff=False
                nuevo_usuario.is_superuser=False
                nuevo_usuario.first_name=nombre
                nuevo_usuario.last_name=apellidos
                nuevo_usuario.email=email
                nuevo_usuario.save()
                error=False
                mensaje="El usuario fue registrado"
                return render_to_response('producto/registrarcliente.html',{'error':error,'mensaje':mensaje,'form2':form2},context_instance=RequestContext(request))
    else:
        formulario=UserCreationForm()
        formulario2=ClienteRegistro()
        
    listadia=range(1,32)
    listames=range(1,13)
    listaanio=range(2014,1905,-1)
    return render_to_response("producto/registrarcliente.html",{'formulario':formulario,'formulario2':formulario2,'listaanio':listaanio,'form2':form2,'listames':listames,'listadia':listadia},context_instance=RequestContext(request))

@login_required(login_url=URL_LOGIN)
def listado_cliente(request):
    form=cliente.objects.all()
    return render_to_response("producto/clienteregistrado.html",{"form":form},RequestContext(request))

    

#-------------------------------fin de clientes------------------------------------------#
def categoria_view(request,pagina):
    if request.method=="POST":
        if "product_id" in request.POST:
            try:
                id_producto = request.POST['product_id']
                p = categoriaProducto.objects.get(pk=id_producto)
                mensaje = {"status":"True","product_id":p.id}
                p.delete() # Elinamos objeto de la base de datos
                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
            except:
                mensaje = {"status":"False"}
                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
    lista_cat = categoriaProducto.objects.filter() # Select * from ventas_productos where status = True
    paginator = Paginator(lista_cat,5) # Cuantos productos quieres por pagina? = 3
    try:
        page = int(pagina)
    except:
        page = 1
    try:
        productos = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productos = paginator.page(paginator.num_pages)
    ctx = {'productos':productos}
    return render_to_response('usuario/categoria.html',ctx,context_instance=RequestContext(request))
def productos_view(request,pagina):
    if request.method=="POST":
        if "product_id" in request.POST:
            #pdb.set_trace()
            try:
               # pdb.set_trace()
                id_producto = request.POST['product_id']
                p = producto.objects.get(pk=id_producto)
                mensaje = {"status":"True","product_id":p.id}
                p.delete() # Elinamos objeto de la base de datos
                return HttpResponse(json.dumps(mensaje),mimetype='application/json')
            except:
                mensaje = {"status":"False"}
                return HttpResponse(json.dumps(mensaje),mimetype='application/json')
    lista_prod = producto.objects.filter(status=True) # Select * from ventas_productos where status = True
    paginator = Paginator(lista_prod,5) # Cuantos productos quieres por pagina? = 3
    try:
        page = int(pagina)
    except:
        page = 1
    try:
        productos = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productos = paginator.page(paginator.num_pages)
    ctx = {'productos':productos}
    return render_to_response('usuario/productos.html',ctx,context_instance=RequestContext(request))
#-----------------detalle de producto y categoria----------------
"""def singleProduct_view(request,id_prod):
    prod = producto.objects.get(id=id_prod)
    cats = prod.categorias.all() # Obteniendo las categorias del producto encontrado
    ctx = {'producto':prod,'categorias':cats}
    return render_to_response('producto/SingleProducto.html',ctx,context_instance=RequestContext(request))"""
def solocate_view(request,id_prod):
    prod = categoriaProducto.objects.get(id=id_prod)
     # Obteniendo las categorias del producto encontrado
    ctx = {'producto':prod}
    return render_to_response('usuario/solocate.html',ctx,context_instance=RequestContext(request))

#---------------------CARRITO--------------------------
def productos(request):
    lista_productos=producto.objects.all()
    return render_to_response("producto/productos.html",{'lista_productos':lista_productos},context_instance=RequestContext(request))

def carrito_mostrar(request):
    if not "contador" in request.session:
        request.session['contador'] = 0
    return HttpResponse(request.session['contador'])

def cargar_carrito(request,id):
    pro=producto.objects.get(id=int(id))
    fcarr=fcarrito()
    return render_to_response("producto/fcarrito.html",{'fcarr':fcarr,'pro':pro},context_instance=RequestContext(request))

def listar_producto(request,id):
    pro=producto.objects.get(id=int(id))
    return render_to_response("producto/productos_lista.html",{'producto':pro},context_instance=RequestContext(request))

def carrito_add(request,id):
    if request.method=="POST":
        cant=request.POST['cantidad']
        if int(cant)>0:
            if not "id_sesion" in request.session:
                request.session["id_sesion"]=hashlib.md5(str(datetime.datetime.now())).hexdigest()
            pro=producto.objects.get(id=int(id))
            carr=Carrito.objects.create(id_sesion=request.session["id_sesion"],estado=False,producto=pro,cantidad=int(cant))
            contador=request.session['contador']
            request.session['contador']=contador+1
    return HttpResponse(request.session['contador'])

def confirmar_compra(request):
    if request.user.is_authenticated():
        id_sesion=request.session["id_sesion"]
        carr=Carrito.objects.filter(id_sesion=id_sesion)
        return render_to_response("producto/confirmar_compra.html",{'carr':carr},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/usuario/ingresar/")

def eliminar_de_carrito(request,id):
    if "contador" in request.session:
        contador=request.session['contador']
        request.session['contador']=contador-1
        carr=Carrito.objects.get(id=int(id))
        carr.delete()
        return HttpResponseRedirect("/confirmar/compra/")
    else:
        return HttpResponseRedirect("/productos/")
def realizar_transaccion(request):
    if request.user.is_authenticated():
        usuario=request.user
        u=User.objects.get(username=usuario)
        """Aqui para realizar la transaccion solo lo agregaremos en nuestra tabla pedido"""
        id_sesion=request.session["id_sesion"]
        carr=Carrito.objects.filter(id_sesion=id_sesion)
        #pdb.set_trace()
        """RECORREMOS EL CARRITO EN UN FOR PARA REALIZAR LA TRANSACCION"""
        for i in carr:
            pre_total=float(i.producto.precio*i.cantidad)
            """SELECCIONAMOS EL PRODUCTO PARA REDUCIR EL STOCK"""
            pro=producto.objects.get(id=i.producto.id)
            trans=Pedido.objects.create(cliente=u,cantidad=i.cantidad,precio_total=pre_total)
            """NUESTRA CLASE TIENE UNA RELACION DE MUCHOS A MUCHOS ASI QUE LA AGREGAMOS DE ESTA FORMA"""
            trans.producto.add(pro)
            trans.save()
            stock=pro.stock
            pro.stock=stock-i.cantidad
            pro.save()
        """Eliminamos el carrito"""
        carr.delete()
        request.session['contador']=0
        return HttpResponse("Se realizo la transaccion")
    else:
        return HttpResponseRedirect("/usuario/ingresar/")

@login_required(login_url=URL_LOGIN)
def edit_product_view(request,id_prod):
    info = "iniciado"
    prod = producto.objects.get(pk=id_prod)
    if request.method == "POST":
        form = addProductForm(request.POST,request.FILES,instance=prod)
        if form.is_valid():
            edit_prod = form.save(commit=False)
            form.save_m2m()
            edit_prod.status = True
            edit_prod.save() # Guardamos el objeto
            info = "Correcto"
            return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
    else:
        form = addProductForm(instance=prod)
    ctx = {'form':form,'informacion':info}
    return render_to_response('producto/editProducto.html',ctx,context_instance=RequestContext(request))

#_-------------ADD PRO
@login_required(login_url=URL_LOGIN)
def add_product_view(request):
    info = "iniciado"
    if request.method == "POST":
        form = addProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else:
            info="from  no valido"
            return HttpResponseRedirect('/producto/')
    else:
        form = addProductForm()
    ctx = {'form':form,'informacion':info}
    return render_to_response('producto/addProducto.html',ctx,context_instance=RequestContext(request))

@login_required(login_url="/auth/login/")
def add_categoria_view(request):
    catego=categoriaProducto.objects.all()
    if request.method=="POST":
        info="inicializando"
        form=addCategoria(request.POST,request.FILES)
        if form.is_valid():
            descripcion=form.cleaned_data['descripcion']
            nombre=form.cleaned_data['nombre']
            c=categoriaProducto()
            c.nombre=nombre
            c.descripcion=descripcion
            c.save()
            info="se guardo exitosamente"
        else:
            info="datos incorrectos"
        form=addCategoria()
        ctx={'form':form,'informacion':info,'catego':catego}
        return render_to_response("producto/addCategoria.html",ctx,context_instance=RequestContext(request))
    else:
        form=addCategoria()
        ctx={'form':form,'catego':catego}
        return render_to_response("producto/addCategoria.html",ctx,context_instance=RequestContext(request))


def compra_view(request,id_prod):
    if request.user.is_authenticated():
        """p=producto.objects.get(id=id_prod)
        cli=request.user
        print cli.email
        f=Factura()
        f.comprador=cli
        f.producto_comprado=p


        f.total=p.precio
        f.fecha=date.Today()    
        f.fecha_cambio=date.Today()+timedelta(days=28)
        f.save()"""

        p=producto.objects.get(id=id_prod)
        lista=request.session['carrito_de_compra']+[]
        print lista
        lista.append(p)
        print lista
        request.session['carrito_de_compra']=lista
        return HttpResponseRedirect('/productos/page/1/')
    else:
        return HttpResponseRedirect('/login/')

def get_carrito_compras(request):
    productos=request.session['carrito_de_compra']
    return render_to_response("producto/c_compras.html",{'productos':productos},context_instance=RequestContext(request))

def edit_categoria_view(request,id_prod):
    info = "iniciado"
    prod =  categoriaProducto.objects.get(pk=id_prod)
    if request.method == "POST":
        form = addCategoria(request.POST,instance=prod)
        if form.is_valid():
            edit_prod = form.save(commit=False)
            form.save_m2m()
            edit_prod.status = True
            edit_prod.save() # Guardamos el objeto
            info = "Correcto"
            return HttpResponseRedirect('/categoria/%s/'%edit_prod.id)
    else:
        form = addCategoria(instance=prod)
    ctx = {'form':form,'informacion':info}
    return render_to_response('producto/editCategoria.html',ctx,context_instance=RequestContext(request))


#CHELOOOOOOOOOOOOOOOOO

def comparador_multiple(ids,ids2):
    lista=producto.objects.all()
    comp=lista[ids].compatibilidad.all()
    comp2=lista[ids2]
    componente2=lista[ids]
    longitud=len(comp)
    for i in range(longitud):
        pdb.set_trace()
        if comp2==comp[i]:
            return "el elemeneto    "+str(comp2)+"    es compatible con "+str(componente2)
        else:
            return "el elemeneto    "+str(comp2)+"     NO es compatible con "+str(componente2)


def comparador_multiple(ids,ids2):
    lista=producto.objects.all()
    comp=lista[ids].compatibilidad.all()
    comp2=lista[ids2]
    componente2=lista[ids]
    longitud=len(comp)
    for i in range(longitud):
        print i
        if comp2==comp[i]:
            return "el elemeneto    "+str(comp2)+"    es compatible con "+str(componente2)
    return "el elemeneto    "+str(comp2)+"     NO es compatible con "+str(componente2)
def comparador(request):
    lista1=producto.objects.all()
    lista2=producto.objects.all()
    idval=range(3,30)
    mensaje="seleccione articulos"
    resp="elemento no seleccionado"
    if request.method=='POST':
        idss=int(request.POST['art1'])-3
        idss2=int(request.POST['art2'])-3
        idss3=int(request.POST['art3'])-3
        idss4=int(request.POST['art4'])-3
        idss5=int(request.POST['art5'])-3
        idss6=int(request.POST['art6'])-3
        mensaje=comparador_multiple(idss,idss2)
        if idss3>2:
            mensaje2=comparador_multiple(idss,idss3)
        else: 
            mensaje2=resp
        if idss4>2:
            mensaje3=comparador_multiple(idss,idss4)
        else:
            mensaje3=resp
        if idss5>2:
            mensaje4=comparador_multiple(idss,idss5)
        else:
            mensaje4=resp
        if idss6>2: 
            mensaje5=comparador_multiple(idss,idss6)
        else:
            mensaje5=resp
        var={'lista1':lista1,'lista2':lista2,'mensaje':mensaje,'mensaje2':mensaje2,'mensaje3':mensaje3,'mensaje4':mensaje4,'mensaje5':mensaje5,'idval':idval}
        return render_to_response('producto/comparador.html',var,RequestContext(request))
    else:
        var={'lista1':lista1,'lista2':lista2,'mensaje':mensaje,'idval':idval}
        return render_to_response('producto/comparador.html',var,RequestContext(request))
#--------------------reportes de producto--------------------------#
@login_required(login_url=URL_LOGIN)
def list_producto(request):
    rpro=producto.objects.all()
    return render_to_response("producto/productoLista.html",{'rpro':rpro},context_instance=RequestContext(request))
@login_required(login_url=URL_LOGIN)
def reporte_producto(request):
    rpro=producto.objects.all()
    html=render_to_string("producto/reporte.html",{'pagesize':'A4','rpro':rpro},context_instance=RequestContext(request))
    return generar_reporte_producto(html)
def generar_reporte_producto(html):
    resultado=StringIO.StringIO()
    pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")),resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")
#---------------reporte de clientes--------------#
@login_required(login_url=URL_LOGIN)
def list_cliente(request):
    clien=cliente.objects.all()
    return render_to_response("producto/clienteLista.html",{'clien':clien},context_instance=RequestContext(request))
@login_required(login_url=URL_LOGIN)
def reporte_cliente(request):
    clien=cliente.objects.all()
    htmll=render_to_string("producto/reportecliente.html",{'pagesize':'A4','clien':clien},context_instance=RequestContext(request))
    return generar_reporte_producto(htmll)
def generar_reporte_cliente(htmll):
    resultado=StringIO.StringIO()
    pdf=pisa.pisaDocument(StringIO.StringIO(htmll.encode("UTF:8")),resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")
@login_required(login_url=URL_LOGIN)
def list_ventas(request):
    pedido=Pedido.objects.all()
    return render_to_response("producto/listventa.html",{'pedido':pedido},context_instance=RequestContext(request))
@login_required(login_url=URL_LOGIN)
def reporte_ventas(request):
    pedido=Pedido.objects.all()
    htm=render_to_string("producto/reporteventas.html",{'pagesize':'A4','pedido':pedido},context_instance=RequestContext(request))
    return generar_factura(htm)
def generar_ventas(htl):
    resultado=StringIO.StringIO()
    pdf=pisa.pisaDocument(StringIO.StringIO(htm.encode("UTF:8")),resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")
#--------------------------proforma de factura----------#
@login_required(login_url=URL_LOGIN)
def pro_factura(request,id_prod):
    pedido= Pedido.objects.get(id=id_prod)
    #cats = prod.producto.all() # Obteniendo las categorias del producto encontrado
    #ctx = {'Pedido':prod,'Producto':cats}
    #return render_to_response('producto/factura',ctx,context_instance=RequestContext(request))
    #lista=list(Pedido.objects.filter(ped__id=producto))
    #pedidolista=Pedido.objects.all()
    #produc=producto.objects.all()
    #prod = Pedido.objects.get(id=id_prod)
    #pedido=Pedido.objects.all()
    return render_to_response("producto/factura.html",{'pedido':pedido},context_instance=RequestContext(request))
def reporte_factura(request,id_prod):
    pedido=Pedido.objects.get(id=id_prod)
   # pedido=Pedido.objects.all()
    htl=render_to_string("producto/reportefactura.html",{'pagesize':'A4','pedido':pedido},context_instance=RequestContext(request))
    return generar_factura(htl)
def generar_factura(htl):
    resultado=StringIO.StringIO()
    pdf=pisa.pisaDocument(StringIO.StringIO(htl.encode("UTF:8")),resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")
#---------------------------------
@login_required(login_url=URL_LOGIN)
def reporte(request):
    return render_to_response("producto/todosreportes.html",context_instance=RequestContext(request))
