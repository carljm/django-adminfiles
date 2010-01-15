from django.core.management.base import NoArgsCommand, CommandError
from adminfiles.settings import ADMINFILES_USE_SIGNALS

from django.contrib import admin

from adminfiles.models import FileUploadReference
from adminfiles.listeners import referring_models

class Command(NoArgsCommand):
    """
    Delete all ``FileUploadReference`` instances, then re-save all
    instances of all models which might contain references to uploaded
    files. This ensures that file upload references are in a
    consistent state, and renderings of uploads are brought
    up-to-date.

    Should only be necessary in unusual circumstances (such as just
    after loading a fixture on a different deployment, where
    e.g. MEDIA_URL might differ, which would affect the rendering of
    links to file uploads).

    Likely to be quite slow if used on a large data set.

    """
    def handle_noargs(self, **options):
        if not ADMINFILES_USE_SIGNALS:
            raise CommandError('This command has no effect if '
                               'ADMINFILES_USE_SIGNALS setting is False.')

        FileUploadReference.objects.all().delete()

        # apps register themselves as referencing file uploads by
        # inheriting their admin options from FilePickerAdmin
        admin.autodiscover()
        for model in referring_models:
            print "Syncing %s" % model.__name__
            for obj in model._default_manager.all():
                obj.save()
