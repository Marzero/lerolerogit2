from django.conf.urls import patterns, url
from views import *
urlpatterns=patterns("ventas.apps.producto.views",
	url(r'^add/producto/$','add_product_view',name= "vista_agregar_producto"),
	url(r'^edit/producto/(?P<id_prod>.*)/$','edit_product_view',name= "vista_editar_producto"),
	url(r'^buy/producto/(?P<id_prod>.*)/$','compra_view',name= "comprar_producto"),
	url(r'^getcar/$','get_carrito_compras',name= "getcarrito"),
	url(r'^add/Categoria/$','add_categoria_view',name="vista_agregar_categoria"),
	url(r'^edit/categoria/(?P<id_prod>.*)/$','edit_categoria_view',name= "vista_editar_categoria"),
	
    url(r'^productos/$',productos),
    url(r'^productos/mostrar/carrito/$',carrito_mostrar),
    url(r'^productos/cargar/carrito/(\d+)/$',cargar_carrito),
    url(r'^productos/carrito/add/(\d+)/$',carrito_add),
    url(r'^carrito/eliminar/(?P<id>\d+)/$',eliminar_de_carrito),
    url(r'^producto/(?P<id>\d+)/$',listar_producto),
    url(r'^confirmar/compra/$',confirmar_compra),
    url(r'^producto/comprar/final/$',realizar_transaccion),
    url(r'^comparador/$',comparador),
    url(r'^registrarcliente/$',registro_view),
    url(r'^clienteregistrados/$',listado_cliente),
    #-----------------------corregido
    url(r'^productos/page/(?P<pagina>.*)/$','productos_view',name='vista_productos'),
    #url(r'^producto/(?P<id_prod>.*)/$','singleProduct_view',name='vista_single_producto'),
    #url(r'^contacto/$','contacto_view',name='vista_contacto'),
    url(r'^categoria/page/(?P<pagina>.*)/$','categoria_view',name='vista_categoria'),
    url(r'^categoria/(?P<id_prod>.*)/$','solocate_view',name='vista_solo_categoria'),  
    #url(r'^buscar/$','buscar', name='vista_buscar'),
    

    #-------------reporte--------#
    url(r'^lproducto/$',list_producto),
    url(r'^crear/reporte/$',reporte_producto),

    url(r'^lcliente/$',list_cliente),
    url(r'^crear/reportecliente/$',reporte_cliente),

    url(r'^lventas/$',list_ventas),
    url(r'^crear/reporteventas/$',reporte_ventas),
    #-----------------factura---------#
    #url(r'^facturacion/(?P<id_prod>.*)/$','pro_factura',name='facturacion'),
    url(r'^facturacion/(?P<id_prod>.*)/$','pro_factura',name='facturacion'),
    #url(r'^facturacion/$',pro_factura),
    url(r'^reporfactura/(?P<id_prod>.*)/$','reporte_factura',name='proforma'),
    #url(r'^reporfactura/$',reporte_factura),
    url(r'^reporte/$',reporte),
    )
