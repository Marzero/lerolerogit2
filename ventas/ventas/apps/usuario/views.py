from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
#para los formularios
from django.contrib.auth.forms import AuthenticationForm
#importamos los metodos para el uso de sessiones en django
from django.contrib.auth import login, authenticate, logout
#Importamos los modelos utiles del usuario de django
from django.contrib.auth.models import User,Group
#importamos nuestros modelos
from models import Perfil
#importamos formularios
from formularios import *
from .formularios import ContactForm, LoginForm,RegisterForm
from ventas.apps.producto.models import *
# Create your views here.
from django.contrib.auth.decorators import login_required
from ventas.settings import URL_LOGIN
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q
import json

def ingresar(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                next = request.POST['next']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    request.session['carrito_de_compra']=[]
                    return HttpResponseRedirect(next)
                else:
                    mensaje = "usuario y/o password incorrecto"
        next = request.REQUEST.get('next')
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje,'next':next}
        #request.session['carrito_de_compra']-[]
        return render_to_response('usuario/ingresar.html',ctx,context_instance=RequestContext(request))
"""
def ingresar(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/usuario/tipo/")
    else:
        if request.method=='POST':
            formulario=AuthenticationForm(request.POST)
            if formulario.is_valid:
                usuario=request.POST['username']
                contrasena=request.POST['password']
                acceso=authenticate(username=usuario,password=contrasena)
                if acceso is not None:
                    if acceso.is_active:
                        login(request,acceso)
                        return HttpResponseRedirect('/')
                    else:
                        login(request,acceso)
                        return HttpResponseRedirect("/usuario/activar/")
                else:
                    return HttpResponseRedirect("/errordatos/")
        else:
            formulario=AuthenticationForm()
        return render_to_response('usuario/ingresar.html',{'formulario':formulario},context_instance=RequestContext(request))
"""
def salir(request):
    logout(request)
    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def activar_usuario(request):
    usuario=request.user
    if  usuario.is_active:
        return HttpResponseRedirect('/usuario/tipo/')
    else:
        if request.method=='POST':
            formulario=ActivarCuenta(request.POST)
            if formulario.is_valid():
                ci=request.POST['ci']
                telefono=request.POST['telefono']
                usuario=User.objects.get(username=request.user)
                #Activamos la cuenta y guardamos los datos
                usuario.is_active=True
                usuario.save()
                #Guardamos los datos del perfil
                perfil=Perfil.objects.get(user=usuario)
                perfil.ci=ci
                perfil.telefono=telefono
                perfil.save()
                return HttpResponseRedirect('/usuario/tipo/')
        else:
            formulario=ActivarCuenta()
        return render_to_response("usuario/activar_cuenta.html",{'formulario':formulario},context_instance=RequestContext(request))

def pefil_usuario(request):
    if request.user.is_authenticated():
        usuario=request.user
        if  usuario.is_active:
            context = {
                'usuario'  : usuario,
                'nombre' : usuario.get_full_name(),
                'perfil' : usuario.get_profile(),
                }
            return render_to_response("usuario/usuario_perfil.html",context,context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/usuario/activar/")
    else:
        return HttpResponseRedirect("/usuario/ingresar/")

def tipo(request):
    if request.user.is_authenticated():
        usuario=request.user
        grupo=usuario.groups.all()
        for g in grupo:
            if g.name=='Cliente':
                return HttpResponseRedirect("/usuario/perfil/")
            if g.name=='Vendedor':
                return HttpResponseRedirect("/vendedor/perfil/")
    else:
        return HttpResponseRedirect("/")

def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            u = User.objects.create_user(username=usuario,email=email,password=password_one)
            u.save() # Guardar el objeto
            return render_to_response('usuario/thanks_register.html',context_instance=RequestContext(request))
        else:
            ctx = {'form':form}
            return  render_to_response('usuario/register.html',ctx,context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('usuario/register.html',ctx,context_instance=RequestContext(request))


"""
def registro_usuario(request):
    if request.method=='POST':
        formulario=fusuario(request.POST)
        formulario2=fperfil(request.POST)
        if formulario.is_valid() and formulario2.is_valid():
            usuario=request.POST['username']
            formulario.save()
            anio=request.POST['fecha_nacimiento_year']
            mes=request.POST['fecha_nacimiento_month']
            dia=request.POST['fecha_nacimiento_day']
            fecha_nacimiento=anio+"-"+mes+"-"+dia
            sexo=request.POST['sexo']
            #obtenemos el usuario
            nuevo_usuario=User.objects.get(username=usuario)
            perfil=Perfil.objects.create(user=nuevo_usuario,fecha_nacimiento=fecha_nacimiento,sexo=sexo)
            #Seleccionamos el grupo de clientes y si no existe lo creamos
            grupo,crear_grupo=Group.objects.get_or_create(name='Cliente')
            if crear_grupo != None:
                #Como es un usuario normal lo enviamos al grupo de clientes
                nuevo_usuario.groups.add(grupo)
                #Cambiamos algunos atributos como el activo y lo colocamos en falso ya que falta por activar su cuenta
                nuevo_usuario.is_active=False
                nuevo_usuario.is_staff=False
                nuevo_usuario.is_superuser=False
                nuevo_usuario.save()
                return HttpResponseRedirect("/usuario/ingresar/")
            else:
                return HttpResponseRedirect("/error/")
    else:
        formulario=fusuario()
        formulario2=fperfil()
    return render_to_response("usuario/registro_usuario.html",{'formulario':formulario,'formulario2':formulario2},context_instance=RequestContext(request))
"""
#def solocate_view(request,id_prod):
#    prod = categoriaProducto.objects.get(id=id_prod)
     # Obteniendo las categorias del producto encontrado
#    ctx = {'producto':prod}
#    return render_to_response('usuario/solocate.html',ctx,context_instance=RequestContext(request))

"""def buscar(request):
    if request.method=="POST":
        Aqui ira otra busqueda igual que abajo
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
        return HttpResponse(html)"""
"""def categoria_view(request,pagina):
    if request.method=="POST":
        if "product_id" in request.POST:
            try:
                id_producto = request.POST['product_id']
                p = categoriaProducto.objects.get(pk=id_producto)
                mensaje = {"status":"True","product_id":p.id}
                p.delete() # Elinamos objeto de la base de datos
                return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
            except:
                mensae = {"status":"False"}
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
"""
@login_required(login_url=URL_LOGIN)
def contacto_view(request):
    info_enviado = False # Definir si se envio la informacion o no se envio
    email = ""
    titulo = ""
    texto = ""
    if request.method == "POST":
        formulario = ContactForm(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['Email']
            titulo = formulario.cleaned_data['Titulo']
            texto = formulario.cleaned_data['Texto']

            # Configuracion enviando mensaje via GMAIL
            #to_admin = 'alexexc2@gmail.com'
            #html_content = "Informacion recibida de [%s] <br><br><br>***Mensaje****<br><br>%s"%(email,texto)
            #msg = EmailMultiAlternatives('Correo de Contacto',html_content,'from@server.com',[to_admin])
            #msg.attach_alternative(html_content,'text/html') # Definimos el contenido como HTML
            #msg.send() # Enviamos  en correo
    else:
        formulario = ContactForm()
    ctx = {'form':formulario,'email':email,'titulo':titulo,'texto':texto,'info_enviado':info_enviado}
    return render_to_response('usuario/contacto.html',ctx,context_instance=RequestContext(request))

"""def productos_view(request,pagina):
    if request.method=="POST":
        if "product_id" in request.POST:
            try:
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
"""
def singleProduct_view(request,id_prod):
    prod = producto.objects.get(id=id_prod)
    cats = prod.categorias.all() # Obteniendo las categorias del producto encontrado
    ctx = {'producto':prod,'categorias':cats}
    return render_to_response('usuario/SingleProducto.html',ctx,context_instance=RequestContext(request))



