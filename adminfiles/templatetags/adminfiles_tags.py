from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from adminfiles.utils import render_uploads as _render

register = template.Library()

@register.filter
def render_uploads(content,
                   template_name="adminfiles/render.html",
                   autoescape=None):
    """
    Render uploaded file references in a content string
    (i.e. translate "<<<my-uploaded-file>>>" to '<a
    href="/path/to/my/uploaded/file">My uploaded file</a>').
    
    Just wraps ``adminfiles.utils.render_uploads`` with proper
    template autoescape handling.

    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(esc(_render(content, template_name)))
render_uploads.needs_autoescape = True

