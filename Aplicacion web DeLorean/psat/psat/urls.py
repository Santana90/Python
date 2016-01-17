from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'psat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ayuda', 'apprevista.views.ayuda', name='ayuda'),
    url(r'^(.*)$', 'apprevista.views.usuario', name='usuario'),
    url(r'^$', "app.views.main"),
    url(r'^admin/', include(admin.site.urls)),
)
