from django.conf.urls import patterns,url
#from views import ingresar, registro_usuario
from .views import *
urlpatterns=patterns("ventas.apps.usuario.views",
	#url(r'^productos/page/(?P<pagina>.*)/$','productos_view',name='vista_productos'),
	#url(r'^producto/(?P<id_prod>.*)/$','singleProduct_view',name='vista_single_producto'),
    #url(r'^producto/(?P<id_prod>.*)/$','singleProduct_view',name='vista_single_producto'),
	url(r'^contacto/$','contacto_view',name='vista_contacto'),
	#url(r'^categoria/page/(?P<pagina>.*)/$','categoria_view',name='vista_categoria'),
	#url(r'^categoria/(?P<id_prod>.*)/$','solocate_view',name='vista_solo_categoria'),	
	#url(r'^buscar/$','buscar', name='vista_buscar'),
    url(r'^registro/$',register_view),
    url(r'^usuario/tipo/$',tipo),
    url(r'^logout/$','logout_view',name='vista_logout'),
    #url(r'^usuario/registro/$',registro_usuario),
    url(r'^usuario/ingresar/$',ingresar),
    url(r'^usuario/salir/$',salir),
    url(r'^usuario/perfil/$',pefil_usuario),
    url(r'^usuario/activar/$',activar_usuario),
    url(r'^usuario/tipo/$',tipo),

                     )
