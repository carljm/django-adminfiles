from itertools import chain

from django.db.models.signals import pre_save, post_save, pre_delete

from django.contrib.contenttypes.models import ContentType

from adminfiles.models import FileUpload, FileUploadReference
from adminfiles.parse import get_uploads
from adminfiles import settings

def get_ctype_kwargs(obj):
    return {'content_type': ContentType.objects.get_for_model(obj),
            'object_id': obj.id}

def _get_field(instance, field):
    """
    This is here to support ``MarkupField``. It's a little ugly to
    have that support baked-in; other option would be to have a
    generic way (via setting?) to override how attribute values are
    fetched from content model instances.

    """
    
    value = getattr(instance, field)
    if hasattr(value, 'raw'):
        value = value.raw
    return value

referring_models = set()
            
def register_listeners(model, fields):

    def _update_references(sender, instance, **kwargs):
        ref_kwargs = get_ctype_kwargs(instance)
        for upload in chain(*[get_uploads(_get_field(instance, field))
                              for field in fields]):
            FileUploadReference.objects.get_or_create(**dict(ref_kwargs,
                                                             upload=upload))

    def _delete_references(sender, instance, **kwargs):
        ref_kwargs = get_ctype_kwargs(instance)
        FileUploadReference.objects.filter(**ref_kwargs).delete()

    if settings.ADMINFILES_USE_SIGNALS:
        referring_models.add(model)
        post_save.connect(_update_references, sender=model, weak=False)
        pre_delete.connect(_delete_references, sender=model, weak=False)


def _update_content(sender, instance, created=None, **kwargs):
    """
    Re-save any content models referencing the just-modified
    ``FileUpload``.

    We don't do anything special to the content model, we just re-save
    it. If signals are in use, we assume that the content model has
    incorporated ``render_uploads`` into some kind of rendering that
    happens automatically at save-time.

    """
    if created: # a brand new FileUpload won't be referenced
        return
    for ref in FileUploadReference.objects.filter(upload=instance):
        try:
            obj = ref.content_object
            if obj:
                obj.save()
        except AttributeError:
            pass

def _register_upload_listener():
    if settings.ADMINFILES_USE_SIGNALS:
        post_save.connect(_update_content, sender=FileUpload)
_register_upload_listener()

def _disconnect_upload_listener():
    post_save.disconnect(_update_content)
