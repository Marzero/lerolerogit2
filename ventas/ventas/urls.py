from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ventas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include("ventas.apps.sistema.urls")),
    url(r'^',include("ventas.apps.usuario.urls")),
    url(r'^',include("ventas.apps.producto.urls")),
    #La siguiente url es necesaria para acceder a los archivos media como las imagenes subidas por el usuario
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
    ),
)
