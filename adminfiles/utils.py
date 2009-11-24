from django import template

from adminfiles.parse import parse_match, substitute_uploads
from adminfiles import settings

def render_uploads(content, template_name="adminfiles/render.html"):
    """
    Replace all uploaded file references in a content string with the
    results of rendering ``template_name`` with the ``FileUpload``
    instance and the key=value options found in the file reference.

    For instance, if "<<<my-uploaded-file:key=val:key2=val2>>>" is
    found in the content string, it will be replaced with the results
    of rendering ``template_name`` with ``upload`` set to the
    ``FileUpload`` instance with slug "my-uploaded-file" and
    ``options`` set to {'key': 'val', 'key2': 'val2'}.

    If the given slug is not found, the reference is replaced with the
    empty string.
    
    """
    tpl = template.loader.get_template(template_name)
    def _replace(match):
        upload, options = parse_match(match)
        if upload is None:
            return settings.ADMINFILES_STRING_IF_NOT_FOUND
        return tpl.render(template.Context({'upload': upload,
                                            'options': options}))
    return substitute_uploads(content, _replace)
