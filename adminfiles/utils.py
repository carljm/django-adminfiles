from os.path import join

from django import template
from django.conf import settings

if 'oembed' in settings.INSTALLED_APPS:
    try:
        # djangoembed
        from oembed.consumer import OEmbedConsumer
        def oembed_replace(text):
            consumer = OEmbedConsumer()
            return consumer.parse(text)
    except ImportError:
        # django-oembed
        from oembed.core import replace as oembed_replace
else:
    oembed_replace = lambda s: s

from adminfiles.parse import parse_match, substitute_uploads
from adminfiles import settings

def render_uploads(content, template_path="adminfiles/render/"):
    """
    Replace all uploaded file references in a content string with the
    results of rendering a template found under ``template_path`` with
    the ``FileUpload`` instance and the key=value options found in the
    file reference.

    So if "<<<my-uploaded-file:key=val:key2=val2>>>" is found in the
    content string, it will be replaced with the results of rendering
    the selected template with ``upload`` set to the ``FileUpload``
    instance with slug "my-uploaded-file" and ``options`` set to
    {'key': 'val', 'key2': 'val2'}.

    If the given slug is not found, the reference is replaced with the
    empty string.

    If ``djangoembed`` or ``django-oembed`` is installed, also replaces OEmbed
    URLs with the appropriate embed markup.
    
    """
    def _replace(match):
        upload, options = parse_match(match)
        return render_upload(upload, template_path, **options)
    return oembed_replace(substitute_uploads(content, _replace))


def render_upload(upload, template_path="adminfiles/render/", **options):
    """
    Render a single ``FileUpload`` model instance using the
    appropriate rendering template and the given keyword options, and
    return the rendered HTML.
    
    The template used to render each upload is selected based on the
    mime-type of the upload. For an upload with mime-type
    "image/jpeg", assuming the default ``template_path`` of
    "adminfiles/render", the template used would be the first one
    found of the following: ``adminfiles/render/image/jpeg.html``,
    ``adminfiles/render/image/default.html``, and
    ``adminfiles/render/default.html``
    
    """
    if upload is None:
        return settings.ADMINFILES_STRING_IF_NOT_FOUND
    template_name = options.pop('as', None)
    if template_name:
        templates = [template_name,
                     "%s/default" % template_name.split('/')[0],
                     "default"]
    else:
        templates = [join(upload.content_type, upload.sub_type),
                     join(upload.content_type, "default"),
                     "default"]
    tpl = template.loader.select_template(
        ["%s.html" % join(template_path, p) for p in templates])
    return tpl.render(template.Context({'upload': upload,
                                        'options': options}))
