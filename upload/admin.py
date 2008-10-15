from django.contrib import admin

from upload.models import FileUpload
from upload.settings import UPLOAD_MEDIA_URL

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('title','upload_date','upload', 'mime_type')
# uncomment for snipshot photo editing feature
#    class Media:
#        js = ['%sjquery.js' % (UPLOAD_MEDIA_URL), '%sphoto-edit.js' % (UPLOAD_MEDIA_URL)]

admin.site.register(FileUpload, FileUploadAdmin)
