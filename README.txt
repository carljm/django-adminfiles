=================
django-adminfiles
=================

A file upload manager and picker for the Django admin. 

Easily upload files and view all uploaded files (with thumbnails for
images) in a picker underneath any content textarea or
select dropdown. Click on an image to add a reference to it into the
content area, or select it in the dropdown.

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

    4. Inherit model admin options from `FileUploadPickerAdmin`_.

FilePickerAdmin
---------------

For each model you'd like to use the ``django-adminfiles`` picker
with, inherit that model's admin options class from
``adminfiles.admin.FilePickerAdmin`` instead of the usual
``django.contrib.admin.ModelAdmin``, and set the ``adminfiles_fields``
attribute to a list/tuple of the names of fields it is used with.

For instance, if you have a ``Post`` model with a ``content``
TextField, and you'd like to insert references into that TextField
from a ``django-adminfiles`` picker::

    from django.contrib import admin

    from adminfiles.admin import FilePickerAdmin

    from myapp.models import Post

    class PostAdmin(FilePickerAdmin):
        adminfiles_fields = ('content',)

    admin.site.register(Post, PostAdmin)

Settings
========

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

