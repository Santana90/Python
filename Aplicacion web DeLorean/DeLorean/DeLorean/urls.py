from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DeLorean.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^ayuda', 'app.views.main',),
	#url(r'^todas', 'app.views.main',),
	url(r'^$','app.views.main',),
	url(r'^logout','app.views.logout_view',),
	url(r'^(.*)$', 'app.views.usuario'),
	#url(r'^$',TemplateView.as_view(template_name="index.html")),
	url(r'^(?P<path>.*)$', 'django.views.static.serve',{'document_root':
		'templates/delicious_fruit/'}),
	url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
		'templates/delicious_fruit/images/'}),
)
