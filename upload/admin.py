import posixpath

from django.http import HttpResponse
from django.contrib import admin

from upload.models import FileUpload
from upload.settings import UPLOAD_MEDIA_URL, JQUERY_URL

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('title','upload_date','upload', 'mime_type')
# uncomment for snipshot photo editing feature
#    class Media:
#        js = (JQUERY_URL, posixpath.join(UPLOAD_MEDIA_URL, 'photo-edit.js'))
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

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if request.POST.has_key('_popup'):
            return HttpResponse('<script type="text/javascript">opener.dismissAddUploadPopup(window);</script>')
        return super(FileUploadAdmin, self).response_add(request, obj, post_url_continue)
            
        
class FileUploadPickerAdmin(admin.ModelAdmin):
    upload_fields = ()

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(FileUploadPickerAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.upload_fields:
            try:
                field.widget.attrs['class'] += " fileuploadpicker"
            except KeyError:
                field.widget.attrs['class'] = 'fileuploadpicker'
        return field

    class Media:
        js = (JQUERY_URL, posixpath.join(UPLOAD_MEDIA_URL, 'upload/model.js'))

admin.site.register(FileUpload, FileUploadAdmin)
