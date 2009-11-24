import os
import mimetypes

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.images import get_image_dimensions

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from adminfiles.settings import ADMINFILES_UPLOAD_TO

if 'tagging' in settings.INSTALLED_APPS:
    from tagging.fields import TagField
else:
    TagField = None

class FileUpload(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to=ADMINFILES_UPLOAD_TO)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(blank=True, max_length=200)
    content_type = models.CharField(editable=False, max_length=100)
    sub_type = models.CharField(editable=False, max_length=100)

    if TagField:
        tags = TagField()
    
    class Meta:
        ordering = ['upload_date', 'title']

    def __unicode__(self):
        return self.title

    def mime_type(self):
        return '%s/%s' % (self.content_type, self.sub_type)

    def type_slug(self):
        return slugify(self.sub_type)

    def is_image(self):
        return self.content_type == 'image'

    def _get_dimensions(self):
        try:
            return self._dimensions_cache
        except AttributeError:
            if self.is_image():
                self._dimensions_cache = get_image_dimensions(self.upload.path)
            else:
                self._dimensions_cache = (None, None)
        return self._dimensions_cache
    
    def width(self):
        return self._get_dimensions()[0]
    
    def height(self):
        return self._get_dimensions()[1]
    
    def save(self, *args, **kwargs):
        (mime_type, encoding) = mimetypes.guess_type(self.upload.path)
        try:
            [self.content_type, self.sub_type] = mime_type.split('/')
        except:
            self.content_type = 'text'
            self.sub_type = 'plain'
        super(FileUpload, self).save()

class FileUploadReference(models.Model):
    """
    Tracks which ``FileUpload``s are referenced by which content models.

    """
    upload = models.ForeignKey(FileUpload)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('upload', 'content_type', 'object_id')
