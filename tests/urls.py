from django.conf.urls.defaults import *

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^adminfiles/', include('adminfiles.urls')),
    url(r'^admin/', include(admin.site.urls))
    )
