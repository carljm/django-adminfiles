from django.conf.urls.defaults import *

urlpatterns = patterns('upload.views',
    url(r'download/$', 'download'),
    url(r'youtube/$', 'youtube'),
    url(r'flickr/$', 'flickr'),
    url(r'images/$', 'images'),
    url(r'files/$', 'files'),
    url(r'^$', 'all'),
)
