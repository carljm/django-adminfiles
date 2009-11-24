import posixpath
from django.conf import settings

JQUERY_URL = getattr(
    settings, 'JQUERY_URL',
    'http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js')

if not ((':' in JQUERY_URL) or (JQUERY_URL.startswith('/'))):
    JQUERY_URL = posixpath.join(settings.MEDIA_URL, JQUERY_URL)

ADMINFILES_MEDIA_URL = getattr(settings, 'ADMINFILES_MEDIA_URL',
                               settings.MEDIA_URL)

ADMINFILES_UPLOAD_TO = getattr(settings, 'ADMINFILES_UPLOAD_TO', 'adminfiles')

ADMINFILES_THUMB_ORDER = getattr(settings, 'ADMINFILES_THUMB_ORDER',
                                 ('-upload_date',))

ADMINFILES_USE_SIGNALS = getattr(settings, 'ADMINFILES_USE_SIGNALS', False)
                                 
ADMINFILES_REF_START = getattr(settings, 'ADMINFILES_REF_START', '<<<')

ADMINFILES_REF_END = getattr(settings, 'ADMINFILES_REF_END', '>>>')

ADMINFILES_STRING_IF_NOT_FOUND = getattr(settings,
                                         'ADMINFILES_STRING_IF_NOT_FOUND',
                                         u'')

FLICKR_USER = getattr(settings, 'FLICKR_USER', None)
FLICKR_API_KEY = getattr(settings, 'FLICKR_API_KEY', None)
YOUTUBE_USER = getattr(settings, 'YOUTUBE_USER', None)
