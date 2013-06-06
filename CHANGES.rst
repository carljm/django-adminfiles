CHANGES
=======

tip (unreleased)
----------------

- BACKWARDS-INCOMPATIBLE: Django versions prior to 1.4 are no longer tested or supported.

- BACKWARDS-INCOMPATIBLE: Removed the ``ADMINFILES_MEDIA_URL`` setting, use
  ``STATIC_URL`` everywhere for static assets. Thanks Rudolph Froger for the
  nudge.

- Updated to most recent sorl-thumbnail. Thanks Svyatoslav Bulbakha.

- Added Russian translation. Thanks Svyatoslav Bulbakha.

- Added Spanish translation. Thanks Andrés Reyes Monge.

- Updated to use Django 1.3's class-based views. Fixes #10. Thanks Andrés
  Reyes Monge and Ales Zabala Alava.


0.5.1 (2011.03.22)
------------------

- Added support for djangoembed as well as django-oembed.

- Added support for multiple pages of Vimeo results via
  ADMINFILES_VIMEO_PAGES setting (defaults to 1).

- Added German translation. Thanks Jannis Leidel.



0.5.0 (2010.03.09)
------------------

- Added ``as`` template override keyword option

- Added ``render_upload`` filter

- Added YouTube, Flickr, Vimeo browsers

- Added OEmbed support

- Added translation hooks and Polish translation: thanks Ludwik Trammer!

- Added support for linking full set of mime-type icons from stdicon.com.

- Made the JS reference-insertion options configurable.

- BACKWARDS-INCOMPATIBLE: default rendering template is now
  ``adminfiles/render/default.html`` instead of
  ``adminfiles/render.html``.  Image-specific rendering should
  override ``adminfiles/render/image/default.html`` instead of testing
  ``upload.is_image`` in default template.

- Added per-mime-type template rendering

- Upgraded to jQuery 1.4

- Fixed bug where YouTube and Flickr links showed up even when disabled.

- Added sync_upload_refs command


0.3.4 (2009.12.03)
------------------

- Fixed over-eager escaping in render_uploads template tag.


0.3.3 (2009.12.02)
------------------

- Fixed insertion of slugs for non-image files.


0.3.2 (2009.12.02)
------------------

- Fixed setup.py package_data so media and templates are installed from sdist.


0.3.1 (2009.11.25)
------------------

- Fixed setup.py so ``tests`` package is not installed.


0.3.0 (2009.11.23)
------------------

- Initial release as ``django-adminfiles``

- Added docs and test suite

- Added reference parsing & rendering, template filter, signal handling

