from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	
   	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^salir', 'apprevista.views.salir', name='salir'),
	url(r'^canales/(.*)$', 'apprevista.views.num', name='num'),
	url(r'^canales', 'apprevista.views.canales', name='canales'),
	url(r'^ayuda', 'apprevista.views.ayuda', name='ayuda'),
	url(r'^$', 'apprevista.views.main', name='main'),
	url(r'^(.*)$', 'apprevista.views.usuario', name='usuario'),

    # url(r'^mirevista/', include('mirevista.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
