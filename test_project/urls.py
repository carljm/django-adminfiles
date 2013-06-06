from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(admin.site.urls)),
    url(r'^adminfiles/', include('adminfiles.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
