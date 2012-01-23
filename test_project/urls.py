from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include(admin.site.urls)),
    (r'^adminfiles/', include('adminfiles.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
