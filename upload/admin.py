from django.http import HttpResponse
from django.contrib import admin

from upload.models import FileUpload
from upload.settings import UPLOAD_MEDIA_URL

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('title','upload_date','upload', 'mime_type')
# uncomment for snipshot photo editing feature
#    class Media:
#        js = ['%sjquery.js' % (UPLOAD_MEDIA_URL), '%sphoto-edit.js' % (UPLOAD_MEDIA_URL)]
    def response_change(self, request, obj):
        if request.POST.has_key("_popup"):
            return HttpResponse(
                '<script type="text/javascript">opener.dismissEditPopup(window);</script>')
        return super(FileUploadAdmin, self).response_change(request, obj)

    def delete_view(self, request, object_id, extra_context=None):
        response = super(FileUploadAdmin, self).delete_view(request, object_id, extra_context)
        if request.POST.has_key("post") and request.GET.has_key("_popup"):
            return HttpResponse(
                '<script type="text/javascript">opener.dismissEditPopup(window);</script>')
        return response
        
class FileUploadPickerAdmin(admin.ModelAdmin):
    upload_fields = ()

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(FileUploadPickerAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.upload_fields:
            try:
                field.widget.attrs['class'] = "%s fileuploadpicker" % (field.widget.attrs['class'],)
            except KeyError:
                field.widget.attrs['class'] = 'fileuploadpicker'
        return field

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js', 'upload/model.js')

admin.site.register(FileUpload, FileUploadAdmin)
