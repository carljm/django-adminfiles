CHANGES
=======

0.5.1 (2011.03.22)
------------------

- add support for djangoembed as well as django-oembed.

- add support for multiple pages of Vimeo results via ADMINFILES_VIMEO_PAGES
  setting (defaults to 1).

0.5.0 (2010.03.09)
------------------

- add ``as`` template override keyword option

- add ``render_upload`` filter

- add YouTube, Flickr, Vimeo browsers

- add OEmbed support

- add translation hooks and Polish translation: thanks Ludwik Trammer!

- add support for linking full set of mime-type icons from stdicon.com.

- make the JS reference-insertion options configurable.

- BACKWARDS-INCOMPATIBLE: default rendering template is now
  ``adminfiles/render/default.html`` instead of
  ``adminfiles/render.html``.  Image-specific rendering should
  override ``adminfiles/render/image/default.html`` instead of testing
  ``upload.is_image`` in default template.

- add per-mime-type template rendering

- upgrade to jQuery 1.4

- fix bug where YouTube and Flickr links showed up even when disabled.

- add sync_upload_refs command

0.3.4 (2009.12.03)
------------------

- fix over-eager escaping in render_uploads template tag.

0.3.3 (2009.12.02)
------------------

- slugs for non-image files are inserted.

0.3.2 (2009.12.02)
------------------

- fix setup.py package_data so media and templates are installed from sdist.

0.3.1 (2009.11.25)
------------------

- fix setup.py so ``tests`` package is not installed.

0.3.0 (2009.11.23)
------------------

- initial release as ``django-adminfiles``

- added docs and test suite

- added reference parsing & rendering, template filter, signal handling

