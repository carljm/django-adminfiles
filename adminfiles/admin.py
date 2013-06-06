from django.http import HttpResponse

from django.contrib import admin

from adminfiles.models import FileUpload
from adminfiles.settings import JQUERY_URL
from adminfiles.listeners import register_listeners

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'upload_date', 'upload', 'mime_type']
    list_editable = ['description']
    prepopulated_fields = {'slug': ('title',)}
# uncomment for snipshot photo editing feature
#    class Media:
#        js = (JQUERY_URL, 'photo-edit.js')
    def response_change(self, request, obj):
        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">'
                                'opener.dismissEditPopup(window);'
                                '</script>')
        return super(FileUploadAdmin, self).response_change(request, obj)

    def delete_view(self, request, *args, **kwargs):
        response = super(FileUploadAdmin, self).delete_view(request,
                                                            *args,
                                                            **kwargs)
        if request.POST.has_key("post") and request.GET.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">'
                                'opener.dismissEditPopup(window);'
                                '</script>')
        return response

    def response_add(self, request, *args, **kwargs):
        if request.POST.has_key('_popup'):
            return HttpResponse('<script type="text/javascript">'
                                'opener.dismissAddUploadPopup(window);'
                                '</script>')
        return super(FileUploadAdmin, self).response_add(request,
                                                         *args,
                                                         **kwargs)


class FilePickerAdmin(admin.ModelAdmin):
    adminfiles_fields = []

    def __init__(self, *args, **kwargs):
        super(FilePickerAdmin, self).__init__(*args, **kwargs)
        register_listeners(self.model, self.adminfiles_fields)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(FilePickerAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name in self.adminfiles_fields:
            try:
                field.widget.attrs['class'] += " adminfilespicker"
            except KeyError:
                field.widget.attrs['class'] = 'adminfilespicker'
        return field

    class Media:
        js = [JQUERY_URL, 'adminfiles/model.js']

admin.site.register(FileUpload, FileUploadAdmin)
