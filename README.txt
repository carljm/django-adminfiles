=================
django-adminfiles
=================

A file upload manager and picker for the Django admin. 

Easily upload files and view all uploaded files (with thumbnails for
images) in a picker underneath any content textarea. Click on an image
to add a reference to it into the content area.

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-adminfiles

or get the `in-development version`_::

    pip install django-adminfiles==tip

.. _in-development version: http://bitbucket.org/carljm/django-adminfiles/get/tip.gz#egg=django_adminfiles-tip

Usage
=====

To use django-adminfiles in your Django project:

    1. Add ``'adminfiles'`` to your ``INSTALLED_APPS`` setting.

    2. Make the contents of the ``adminfiles/media/adminfiles``
       directory available at ``MEDIA_URL/adminfiles`` (or
       ``ADMINFILES_MEDIA_URL/adminfiles/``, see
       `ADMINFILES_MEDIA_URL`_).  This can be done by copying the
       files, making a symlink, or through your webserver
       configuration.

    3. Add ``url(r'^adminfiles/', include('adminfiles.urls')`` in your
       root URLconf.

    4. Inherit content model admin options from
       `FilePickerAdmin`_.

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
content field.

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
controlled by a Django template: ``adminfiles/render.html``. 

The default template produces an HTML ``img`` tag for images and a
simple ``a`` link to other file types. It also respects three
key-value options: ``class``, which will be used as the the ``class``
attribute of the ``img`` or ``a`` tag; ``alt``, which will be the
image alt text (images only; if not provided ``upload.title`` is used
for alt text); and ``title``, which will override ``upload.title`` as
the link text of the ``a`` tag (non-images only).

You can easily override this template with your own. The template is
rendered with the following context:

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
in the content with the rendered ``adminfiles/render.html`` template.

The filter also accepts an optional argument: the name of an alternate
template to use for rendering each uploaded file reference. This
allows several different renderings to be used in different
circumstances::

    {{ post.content|render_uploads:"custom_file_render.html" }}

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
``template_name`` argument.

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

JQUERY_URL
----------

``django-adminfiles`` requires the jQuery Javascript library.  By
default, ``django-adminfiles`` links to the most recent minor version
of jQuery 1.3 available at ajax.googleapis.com (via the URL
``http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js``).
If you wish to use a different version of jQuery, or host it yourself,
set the JQUERY_URL setting.  For example::

    JQUERY_URL = 'jquery.min.js'

This will use the jQuery available at MEDIA_URL/jquery.min.js. Note
that a relative ``JQUERY_URL`` is always relative to ``MEDIA_URL``, it
does not use ``ADMINFILES_MEDIA_URL``.

