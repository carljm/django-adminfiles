from os.path import join
from django.conf import settings

UPLOAD_MEDIA_URL = getattr(settings, 'UPLOAD_MEDIA_URL', None)
if not UPLOAD_MEDIA_URL:
    media_url = settings.MEDIA_URL
    if not media_url.endswith('/'):
        media_url = '%s/' % media_url
    UPLOAD_MEDIA_URL = '%supload_media/' % media_url

UPLOAD_RELATIVE_PATH = getattr(settings, 'UPLOAD_RELATIVE_PATH', 'uploads')
