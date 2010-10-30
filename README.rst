=================
django-adminfiles
=================

A file upload manager and picker for the Django admin, with support
for browsing and embedding from Flickr, Youtube, Vimeo, etc.

Upload files and view uploaded files (with thumbnails) in a
file-picker underneath any content textarea. Click on a file to add a
reference to it into the content area.

Inline file references can be customized per-mime-type to automate the
correct presentation of each file: <img> tags (with additional markup
as needed) for images, links for downloadable files, even embedded
players for audio or video files. See `the screencast`_.

.. _the screencast: http://vimeo.com/8940852

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-adminfiles

or get the `in-development version`_::

    pip install django-adminfiles==tip

.. _in-development version: http://bitbucket.org/carljm/django-adminfiles/get/tip.gz#egg=django_adminfiles-tip

Dependencies
------------

``django-adminfiles`` requires `Django`_ 1.1 or later,
`sorl-thumbnail`_ and the `Python Imaging Library`_.

`djangoembed`_ or `django-oembed`_ is required for OEmbed
functionality. `flickrapi`_ is required for browsing Flickr photos, `gdata`_
for Youtube videos.

.. _Django: http://www.djangoproject.com/
.. _sorl-thumbnail: http://pypi.python.org/pypi/sorl-thumbnail
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _django-oembed: http://pypi.python.org/pypi/django-oembed
.. _djangoembed: http://pypi.python.org/pypi/djangoembed
.. _gdata: http://pypi.python.org/pypi/gdata
.. _flickrapi: http://pypi.python.org/pypi/flickrapi

Usage
=====

To use django-adminfiles in your Django project:

    1. Add ``'adminfiles'`` to your ``INSTALLED_APPS`` setting.

    2. Make the contents of the ``adminfiles/media/adminfiles``
       directory available at ``MEDIA_URL/adminfiles`` (or
       ``ADMINFILES_MEDIA_URL/adminfiles/``, see `ADMINFILES_MEDIA_URL`_). 
       This can be done by through your webserver configuration, via an app
       such as `django-staticfiles`_, or by copying the files or making a
       symlink.

    3. Add ``url(r'^adminfiles/', include('adminfiles.urls'))`` in your
       root URLconf.

    4. Inherit content model admin options from
       `FilePickerAdmin`_.

In addition, you may want to set the ``THUMBNAIL_EXTENSION`` setting for
`sorl-thumbnail`_ to ``"png"`` rather than the default ``"jpg"``, so that
images with alpha transparency aren't broken when thumbnailed in the
adminfiles file-picker.

.. _django-staticfiles: http://pypi.python.org/pypi/django-staticfiles

FilePickerAdmin
===============

For each model you'd like to use the ``django-adminfiles`` picker
with, inherit that model's admin options class from
``adminfiles.admin.FilePickerAdmin`` instead of the usual
``django.contrib.admin.ModelAdmin``, and set the ``adminfiles_fields``
attribute to a list/tuple of the names of the content fields it is
used with.

For instance, if you have a ``Post`` model with a ``content``
TextField, and you'd like to insert references into that TextField
from a ``django-adminfiles`` picker::

    from django.contrib import admin

    from adminfiles.admin import FilePickerAdmin

    from myapp.models import Post

    class PostAdmin(FilePickerAdmin):
        adminfiles_fields = ('content',)

    admin.site.register(Post, PostAdmin)

The picker displays thumbnails of all uploaded images, and appropriate
icons for non-image files. It also allows you to filter and view only
images or only non-image files. In the lower left it contains links to
upload a new file or refresh the list of available files.

If you click on a file thumbnail/icon, a menu pops up with options to
edit or delete the uploaded file, or insert it into the associated
content field. To modify the default insertion options, set the
`ADMINFILES_INSERT_LINKS`_ setting.

File references
===============

When you use the file upload picker to insert an uploaded file
reference in a text content field, it inserts something like
``<<<my-file-slug>>>``, built from the `ADMINFILES_REF_START`_ and
`ADMINFILES_REF_END`_ settings and the slug of the ``FileUpload``
instance.

The reference can also contain arbitrary key=value option after the
file slug, separated by colons, e.g.:
``<<<my-file-slug:class=left>>>``.

These generic references allow you to use ``django-adminfiles`` with
raw HTML content or any type of text markup. They also allow you to
change uploaded files and have old references to the file pick up the
change (as long as the slug does not change). The URL path to the
file, or other metadata like the height or width of an image, are not
hardcoded in your content.

Rendering references
--------------------

These references need to be rendered at some point into whatever
markup you ultimately want. The markup produced by the rendering is
controlled by the Django templates under ``adminfiles/render/``.

The template used is selected according to the mime type of the file
upload referenced. For instance, for rendering a file with mime type
``image/jpeg``, the template used would be the first template of the
following that exists: ``adminfiles/render/image/jpeg.html``,
``adminfiles/render/image/default.html``,
``adminfiles/render/default.html``.

If a file should be rendered as if it had a different mime type
(e.g. an image you want to link to rather than display), pass the
``as`` option with the mime type you want it rendered as (where either
the sub-type or the entire mime-type can be replaced with
``default``). For instance, with the default available templates if
you wanted to link to an image file, you could use
``<<<my-image:as=default>>>``.

Two rendering templates are included with ``django-adminfiles``:
``adminfiles/render/image/default.html`` (used for any type of image)
and ``adminfiles/render/default.html`` (used for any other type of
file). These default templates produce an HTML ``img`` tag for images
and a simple ``a`` link to other file types. They also respect three
key-value options: ``class``, which will be used as the the ``class``
attribute of the ``img`` or ``a`` tag; ``alt``, which will be the
image alt text (images only; if not provided ``upload.title`` is used
for alt text); and ``title``, which will override ``upload.title`` as
the link text of the ``a`` tag (non-images only).

You can easily override these templates with your own, and provide
additional templates for other file types. The template is rendered
with the following context:

``upload``
    The ``FileUpload`` model instance whose slug field matches the
    reference. Useful attributes of this instance include
    ``upload.upload`` (a `Django File object`_), ``upload.title``,
    ``upload.description``, ``upload.mime_type`` (first and second
    parts separately accessible as ``upload.content_type`` and
    ``upload.sub_type``) and ``upload.is_image`` (True if
    ``upload.content_type`` is "image"). Images also have
    ``upload.height`` and ``upload.width`` available.

``options``
    A dictionary of the key=value options in the reference.

If a reference is encountered with an invalid slug (no ``FileUpload``
found in the database with that slug), the value of the
`ADMINFILES_STRING_IF_NOT_FOUND`_ setting is rendered instead
(defaults to the empty string).

.. _Django File object: http://docs.djangoproject.com/en/dev/ref/files/file/

render_uploads template filter
------------------------------

``django-adminfiles`` provides two methods for making the actual
rendering happen. The simple method is a template filter:
``render_uploads``. To use it, just load the ``adminfiles_tags`` tag
library, and apply the ``render_uploads`` filter to your content field::

    {% load adminfiles_tags %}

    {{ post.content|render_uploads }}

The ``render_uploads`` filter just replaces any file upload references
in the content with the rendered template (described above).

The filter also accepts an optional argument: an alternate base path
to the templates to use for rendering each uploaded file
reference. This path will replace ``adminfiles/render`` as the base
path in the mime-type-based search for specific templates. This allows
different renderings to be used in different circumstances::

    {{ post.content|render_uploads:"adminfiles/alt_render" }}

For a file of mime type ``text/plain`` this would use one of the
following templates: ``adminfiles/alt_render/text/plain.html``,
``adminfiles/alt_render/text/default.html``, or
``adminfiles/alt_render/default.html``.

render_upload template filter
-----------------------------

If you have a ``FileUpload`` model instance in your template and wish
to render just that instance using the normal rendering logic, you can
use the ``render_upload`` filter. This filter accepts options in the
same "key=val:key2=val2" format used for passing options to
inline-embedded files; the special option ``template_path`` specifies
an alternate base path for finding rendering templates::

    {{ my_upload|render_upload:"template_path=adminfiles/alt_render:class=special" }}

pre-rendering at save time
--------------------------

In some cases, markup in content fields is pre-rendered when the model
is saved, and stored in the database or cache. In this case, it may be
preferable to also render the uploaded file references in that step,
rather than re-rendering them every time the content is displayed in
the template.

To use this approach, first you need to integrate the function
``adminfiles.utils.render_uploads`` into your existing content
pre-rendering process, which should be automatically triggered by
saving the content model. 

The ``adminfiles.utils.render_uploads`` function takes a content
string as its argument and returns the same string with all uploaded
file references replaced, same as the template tag. It also accepts a
``template_path`` argument, which is the same as the argument accepted
by the `render_uploads template filter`_.

Integrating this function in the markup-rendering step is outside the
scope of ``django-adminfiles``. For instance, if using
`django-markitup`_ with Markdown to process content markup, the
``MARKITUP_FILTER`` setting might point to a function like this::

    from markdown import markdown
    from adminfiles.utils import render_uploads

    def markup_filter(markup):
        return markdown(render_uploads(markup))

Once this is done, set the `ADMINFILES_USE_SIGNALS`_ setting to
True. Now ``django-adminfiles`` will automatically track all
references to uploaded files in your content models. Anytime an
uploaded file is changed, all content models which reference it will
automatically be re-saved (and thus updated with the new uploaded
file).

.. _django-markitup: http://bitbucket.org/carljm/django-markitup

Embedding media from other sites
================================

``django-adminfiles`` allows embedding media from any site that supports the
OEmbed protocol. OEmbed support is provided via `djangoembed`_ or
`django-oembed`_, one of which must be installed for embedding to work.

If a supported OEmbed application is installed, the `render_uploads template
filter`_ will also automatically replace any OEmbed-capable URLs with the
appropriate embed markup (so URLs from any site supported by the installed
OEmbed application can simply be pasted in to the content manually).

In addition, ``django-adminfiles`` provides views in its filepicker to
browse Flickr photos, Youtube videos, and Vimeo videos and insert
their URLs into the context textarea with a click. To enable these
browsing views, set the `ADMINFILES_YOUTUBE_USER`_,
`ADMINFILES_VIMEO_USER`_, or `ADMINFILES_FLICKR_USER`_ and
`ADMINFILES_FLICKR_API_KEY`_ settings (and make sure the
`dependencies`_ are satisfied).

To add support for browsing content from another site, just create a
class view that inherits from ``adminfiles.views.OEmbedView`` and add
its dotted path to the `ADMINFILES_BROWSER_VIEWS`_ setting. See the
existing views in ``adminfiles/views.py`` for details.

To list the available browsing views and their status (enabled or
disabled, and why), ``django-adminfiles`` provides an
``adminfiles_browser_views`` management command, which you can run
with ``./manage.py adminfiles_browser_views``.

Settings
========

ADMINFILES_REF_START
--------------------

Marker indicating the beginning of an uploaded-file reference in text
content. Defaults to '<<<'.

If you set this to something insufficiently distinctive (a string
that's likely to show up otherwise in your content), all bets are off.

Special regex characters are escaped, thus you can safely set it to
something like '[[[', but you can't do advanced regex magic with it.

ADMINFILES_REF_END
------------------

Marker indicating the end of an uploaded-file reference in text
content. Defaults to '>>>'.

If you set this to something insufficiently distinctive (a string
that's likely to show up otherwise in your content), all bets are off.

Special regex characters are escaped, thus you can safely set it to
something like ']]]', but you can't do advanced regex magic with it.

ADMINFILES_USE_SIGNALS
----------------------

A boolean setting: should ``django-adminfiles`` track which content
models reference which uploaded files, and re-save those content
models whenever a referenced uploaded file changes? 

Set this to True if you already pre-render markup in content fields at
save time and want to render upload references at that same save-time
pre-rendering step.

Defaults to False. If this setting doesn't make sense to you, you can
safely just leave it False and use the `render_uploads template
filter`_.

ADMINFILES_STRING_IF_NOT_FOUND
------------------------------

The string used to replace invalid uploaded file references (given
slug not found). Defaults to ``u''``.

ADMINFILES_STDICON_SET
----------------------

Django-adminfiles ships with a few icons for common file types, used
for displaying non-image files in the file-picker. To enable a broader
range of mime-type icons, set this setting to the name of an icon set
included at `stdicon.com`_, and icons from that set will be linked.

.. _stdicon.com: http://www.stdicon.com

ADMINFILES_INSERT_LINKS
-----------------------

By default, the admin file picker popup menu for images allows
inserting a reference with no options, a reference with "class=left",
or a reference with "class=right". For non-images, the default popup
menu only allows inserting a reference without options. To change the
insertion options for various file types, set
``ADMINFILES_INSERT_LINKS`` to a dictionary mapping mime-types (or
partial mime-types) to a list of insertion menu options. For instance,
the default setting looks like this::

    ADMINFILES_INSERT_LINKS = {
        '': [('Insert Link', {})],
        'image': [('Insert', {}),
                  ('Insert (left)', {'class': 'left'}),
                  ('Insert (right)', {'class': 'right'})]
    }

Each key in the dictionary can be the first segment of a mime type
(e.g. "image"), or a full mime type (e.g. "audio/mpeg"), or an empty
string (the default used if no mime type matches). For any given file
the most specific matching entry is used. The dictionary should always
contain a default entry (empty string key), or some files may have no
insertion options.

Each value in the dictionary is a list of menu items. Each menu item
is a two-tuple, where the first entry is the user-visible name for the
insertion option, and the second entry is a dictionary of options to
be added to the inserted file reference.

ADMINFILES_MEDIA_URL
--------------------

Some projects separate user-uploaded media at ``MEDIA_URL`` from
static assets. If you keep static assets at a URL other than
``MEDIA_URL``, just set ``ADMINFILES_MEDIA_URL`` to that URL, and make
sure the contents of the ``adminfiles/media/adminfiles`` directory are
available at ``ADMINFILES_MEDIA_URL/adminfiles/``.

ADMINFILES_UPLOAD_TO
--------------------

The ``upload_to`` argument that will be passed to the ``FileField`` on
``django-admin-upload``'s ``FileUpload`` model; determines where
``django-adminfiles`` keeps its uploaded files, relative to
``MEDIA_URL``. Can include strftime formatting codes as described `in
the Django documentation`_. By default, set to ``'adminfiles'``.

.. _in the Django documentation: http://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to

ADMINFILES_THUMB_ORDER
----------------------

The ordering that will be applied to thumbnails displayed in the
picker. Expects a tuple of field names, prefixed with ``-`` to
indicate reverse ordering, same as `"ordering" model Meta
attribute`_. The default value is ``('-upload_date')``; thumbnails
ordered by date uploaded, most recent first.

.. _"ordering" model Meta attribute:  http://docs.djangoproject.com/en/dev/ref/models/options/#ordering

ADMINFILES_BROWSER_VIEWS
------------------------

List of dotted paths to file-browsing views to make available in the
filepicker. The default setting includes all the views bundled with
``django-adminfiles``::

    ['adminfiles.views.AllView',
    'adminfiles.views.ImagesView',
    'adminfiles.views.AudioView',
    'adminfiles.views.FilesView',
    'adminfiles.views.FlickrView',
    'adminfiles.views.YouTubeView',
    'adminfiles.views.VimeoView']

The last three may be disabled despite their inclusion in this setting
if their `dependencies`_ are not satisfied or their required settings
are not set.

ADMINFILES_YOUTUBE_USER
-----------------------

Required for use of the Youtube video browser.

ADMINFILES_VIMEO_USER
---------------------

Required for use of the Vimeo video browser.

ADMINFILES_VIMEO_PAGES
----------------------

The Vimeo API returns 20 videos per page; this setting determines the
maximum number of pages to fetch (defaults to 1, Vimeo-imposed maximum of
3).

ADMINFILES_FLICKR_USER
----------------------

Required for use of the Flickr photo browser.

ADMINFILES_FLICKR_API_KEY
-------------------------

Required for use of the Flickr photo browser.

JQUERY_URL
----------

``django-adminfiles`` requires the jQuery Javascript library.  For Django
versions 1.2 or later, ``django-adminfiles`` by default uses the version of
jQuery included with the Django admin.  For older versions, by default
``django-adminfiles`` links to the most recent minor version of jQuery 1.4
available at ajax.googleapis.com (via the URL
``http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js``).

If you wish to use a different version of jQuery, or host it yourself, set
the JQUERY_URL setting.  For example::

    JQUERY_URL = 'jquery.min.js'

This will use the jQuery available at MEDIA_URL/jquery.min.js. Note
that a relative ``JQUERY_URL`` is always relative to ``MEDIA_URL``, it
does not use ``ADMINFILES_MEDIA_URL``.

