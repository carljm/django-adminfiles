from django import template

from adminfiles.utils import render_uploads as _render

register = template.Library()

@register.filter
def render_uploads(content,
                   template_name="adminfiles/render.html"):
    """
    Render uploaded file references in a content string
    (i.e. translate "<<<my-uploaded-file>>>" to '<a
    href="/path/to/my/uploaded/file">My uploaded file</a>').
    
    Just wraps ``adminfiles.utils.render_uploads``.

    """
    return _render(content, template_name)
render_uploads.is_safe = True

