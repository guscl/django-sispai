from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^core/$', 'core.views.index'),
    url(r'^core/toggle/$', 'core.views.alterStatus'),
    url(r'^core/sensors/$', 'core.views.alterSensorStatus'),
    url(r'^core/message/$', 'core.views.saveAsLog'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
