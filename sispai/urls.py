from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^core/$', 'core.views.index'),
    url(r'^control/$', 'core.views.getParamsOfMenuBar'),
    url(r'^core/toggle/$', 'core.views.alterStatus'), 
    url(r'^registrar/$', 'core.views.registrar'),
    url(r'^$', 'core.views.logar'),

	url(r'^open$', 'core.views.poolOpen'),
	url(r'^close$', 'core.views.poolClose'),
	url(r'^getout$', 'core.views.userGetOut'),
	url(r'^getin$', 'core.views.userGetIn'),
	url(r'^fall$', 'core.views.userFall'),
	url(r'^sensors$', 'core.views.sensorError'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
