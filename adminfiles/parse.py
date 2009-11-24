import re

from adminfiles import settings
from adminfiles.models import FileUpload

# Upload references look like: <<< upload-slug : key=val : key2=val2 >>>
# Spaces are optional, key-val opts are optional, can be any number
# extra indirection is for testability
def _get_upload_re():
    return re.compile(r'%s\s*([\w-]+)((\s*:\s*\w+\s*=\s*[\w\s]+)*)\s*%s'
                      % (re.escape(settings.ADMINFILES_REF_START),
                         re.escape(settings.ADMINFILES_REF_END)))
UPLOAD_RE = _get_upload_re()

def get_uploads(text):
    """
    Return a generator yielding uploads referenced in the given text.

    """
    uploads = []
    for match in UPLOAD_RE.finditer(text):
        try:
            upload = FileUpload.objects.get(slug=match.group(1))
        except FileUpload.DoesNotExist:
            continue
        yield upload

def substitute_uploads(text, sub_callback):
    """
    Return text with all upload references substituted using
    sub_callback, which must accept an re match object and return the
    replacement string.

    """
    return UPLOAD_RE.sub(sub_callback, text)

def parse_match(match):
    """
    Accept an re match object resulting from an ``UPLOAD_RE`` match
    and return a two-tuple where the first element is the
    corresponding ``FileUpload`` and the second is a dictionary of the
    key=value options.

    If there is no ``FileUpload`` object corresponding to the match,
    the first element of the returned tuple is None.

    """
    try:
        upload = FileUpload.objects.get(slug=match.group(1))
    except FileUpload.DoesNotExist:
        upload = None
    options = {}
    for option in match.group(2).split(':'):
        if '=' in option:
            key, val = option.split('=')
            options[key.strip()] = val.strip()
    return (upload, options)
