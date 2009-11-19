from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from adminfiles.parse import parse_match, substitute_uploads

register = template.Library()

@register.filter
def render_uploads(text,
                   template_name="adminfiles/render.html",
                   autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    tpl = template.loader.get_template(template_name)
    def _replace(match):
        upload, options = parse_match(match)
        if upload is None:
            return u''
        return tpl.render(template.Context({'upload': upload,
                                            'options': options}))
    return mark_safe(substitute_uploads(esc(text), _replace))
render_uploads.needs_autoescape = True

