from django.conf.urls.defaults import *

urlpatterns = patterns('adminfiles.views',
    url(r'download/$', 'download', name="adminfiles_download"),
    url(r'youtube/$', 'youtube', name="adminfiles_youtube"),
    url(r'flickr/$', 'flickr', name="adminfiles_flickr"),
    url(r'images/$', 'images', name="adminfiles_images"),
    url(r'files/$', 'files', name="adminfiles_files"),
    url(r'^$', 'all', name="adminfiles_all"),
)
