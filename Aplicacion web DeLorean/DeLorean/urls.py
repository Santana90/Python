from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DeLorean.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^todas', 'app.views.main',),
	url(r'^$','app.views.main',),
	url(r'^logout','app.views.logout_view',),
	url(r'^ayuda','app.views.Ayuda',),
	url(r'^privado','app.views.privado',),
	url(r'^todas','app.views.Todas',),
	url(r'^incidencias','app.views.incidencias',),
	#url(r'^$',TemplateView.as_view(template_name="index.html")),
	url(r'^rss', 'app.views.principal_rss'),
	url(r'^(.*)/rss$', 'app.views.usuario_rss'),
	url(r'^(.*)$', 'app.views.usuario'),

)
