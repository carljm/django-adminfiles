from django.test import TestCase, Client
from django.conf import settings as django_settings
from django.test.utils import ContextList
from django.test.signals import template_rendered
from django import template
from django.db.models.signals import pre_save

from django.contrib import admin
from django.contrib.auth.models import User

from adminfiles import settings, parse
from adminfiles.utils import render_uploads
from adminfiles.models import FileUpload, FileUploadReference
from adminfiles.listeners import _register_upload_listener, \
    _disconnect_upload_listener
from adminfiles.admin import FilePickerAdmin

from models import Post

class PostAdmin(FilePickerAdmin):
    adminfiles_fields = ('content',)

class FileUploadTestCase(TestCase):
    """
    Test case with a populate() method to save a couple FileUpload instances.

    """
    def populate(self):
        self.animage = FileUpload.objects.create(
            upload='adminfiles/tiny.png',
            title='An image',
            slug='an-image')
        self.somefile = FileUpload.objects.create(
            upload='adminfiles/somefile.txt',
            title='Some file',
            slug='some-file')

class FilePickerTests(FileUploadTestCase):
    def setUp(self):
        self.populate()
        self.client = Client()
        admin.site.register(Post, PostAdmin)
        self.admin = User.objects.create_user('admin', 'admin@example.com',
                                              'testpw')
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.is_active = True
        self.admin.save()
        self.failUnless(self.client.login(username='admin', password='testpw'))
        
    def tearDown(self):
        admin.site.unregister(Post)
        
    def test_picker_class_applied(self):
        response = self.client.get('/admin/tests/post/add/')
        self.assertContains(response, 'name="content" class="vLargeTextField adminfilespicker"')

    def test_picker_loads(self):
        """
        Very basic smoke test for file picker.

        """
        response = self.client.get('/adminfiles/?field=test')
        self.assertContains(response, 'href="/media/adminfiles/tiny.png"')
        self.assertContains(response, 'href="/media/adminfiles/somefile.txt')
            
    def test_images_picker_loads(self):
        response = self.client.get('/adminfiles/images/?field=test')
        self.assertContains(response, 'href="/media/adminfiles/tiny.png"')
        self.assertNotContains(response, 'href="/media/adminfiles/somefile.txt')
            
    def test_files_picker_loads(self):
        response = self.client.get('/adminfiles/files/?field=test')
        self.assertNotContains(response, 'href="/media/adminfiles/tiny.png"')
        self.assertContains(response, 'href="/media/adminfiles/somefile.txt')

    def test_thumb_order(self):
        _old_order = settings.ADMINFILES_THUMB_ORDER
        settings.ADMINFILES_THUMB_ORDER = ('title',)
        
        response = self.client.get('/adminfiles/?field=test')
        image_index = response.content.find('tiny.png')
        file_index = response.content.find('somefile.txt')
        self.failUnless(image_index > 0)
        self.failUnless(image_index < file_index)

        settings.ADMINFILES_THUMB_ORDER = _old_order
            
class SignalTests(FileUploadTestCase):
    """
    Test tracking of uploaded file references, and auto-resave of
    content models when referenced uploaded file changes.

    """
    def setUp(self):
        self._old_use_signals = settings.ADMINFILES_USE_SIGNALS
        settings.ADMINFILES_USE_SIGNALS = True
        if not self._old_use_signals:
            _register_upload_listener()

        PostAdmin(Post, admin.site)

        self.populate()

    def tearDown(self):
        if not self._old_use_signals:
            _disconnect_upload_listener()
        settings.ADMINFILES_USE_SIGNALS = self._old_use_signals

    def test_track_references(self):
        Post.objects.create(title='Some title',
                            content='This has a reference to'
                            '<<<some-file>>>')

        self.assertEquals(FileUploadReference.objects.count(), 1)

    def test_track_multiple_references(self):
        Post.objects.create(title='Some title',
                            content='This has a reference to'
                            '<<<some-file>>> and <<<an-image>>>')

        self.assertEquals(FileUploadReference.objects.count(), 2)

    def test_track_no_dupe_references(self):
        post = Post.objects.create(title='Some title',
                                   content='This has a reference to'
                                   '<<<an-image>>> and <<<an-image>>>')

        post.save()

        self.assertEquals(FileUploadReference.objects.count(), 1)

    def test_update_reference(self):
        post = Post.objects.create(title='Some title',
                                   content='This has a reference to'
                                   '<<<some-file>>>')

        def _render_on_save(sender, instance, **kwargs):
            instance.content = render_uploads(instance.content)
        pre_save.connect(_render_on_save, sender=Post)
                                   
        self.somefile.title = 'A New Title'
        self.somefile.save()

        reloaded_post = Post.objects.get(title='Some title')
        
        self.failUnless('A New Title' in reloaded_post.content)
        
class TemplateTestCase(TestCase):
    """
    A TestCase that stores information about rendered templates, much
    like the Django test client.

    """
    def store_rendered_template(self, signal, sender, template, context,
                                **kwargs):
        self.templates.append(template)
        self.contexts.append(context)
    
    def setUp(self):
        self.templates = []
        self.contexts = ContextList()
        template_rendered.connect(self.store_rendered_template)

    def tearDown(self):
        template_rendered.disconnect(self.store_rendered_template)

class RenderTests(TemplateTestCase, FileUploadTestCase):
    """
    Test rendering of uploaded file references.

    """
    def setUp(self):
        super(RenderTests, self).setUp()
        self.populate()
    
    def test_render_template_used(self):
        render_uploads('<<<some-file>>>')
        self.assertEquals(self.templates[0].name, 'adminfiles/render.html')

    def test_render_whitespace(self):
        render_uploads('<<< some-file \n>>>')
        self.assertEquals(len(self.templates), 1)
        
    def test_render_amidst_content(self):
        render_uploads('Some test here<<< some-file \n>>>and more here')
        self.assertEquals(len(self.templates), 1)
        
    def test_render_upload_in_context(self):
        render_uploads('<<<some-file>>>')
        self.assertEquals(self.contexts['upload'].upload.name,
                          'adminfiles/somefile.txt')

    def test_render_options_in_context(self):
        render_uploads('<<<some-file:class=left:key=val>>>')
        self.assertEquals(self.contexts['options'], {'class': 'left',
                                                     'key': 'val'})

    def test_render_alternate_markers(self):
        old_start = settings.ADMINFILES_REF_START
        old_end = settings.ADMINFILES_REF_END
        settings.ADMINFILES_REF_START = '[[['
        settings.ADMINFILES_REF_END = ']]]'
        parse.UPLOAD_RE = parse._get_upload_re()

        render_uploads('[[[some-file]]]')
        self.assertEquals(len(self.templates), 1)

        settings.ADMINFILES_REF_START = old_start
        settings.ADMINFILES_REF_END = old_end
        parse.UPLOAD_RE = parse._get_upload_re()

    def test_render_invalid(self):
        old_nf = settings.ADMINFILES_STRING_IF_NOT_FOUND
        settings.ADMINFILES_STRING_IF_NOT_FOUND = u'not found'

        html = render_uploads('<<<invalid-slug>>>')
        self.assertEquals(html, u'not found')

        settings.ADMINFILES_STRING_IF_NOT_FOUND = old_nf

    def test_default_template_renders_image(self):
        html = render_uploads('<<<an-image>>>')
        self.failUnless('<img src="/media/adminfiles/tiny.png"' in html)

    def test_default_template_renders_image_class(self):
        html = render_uploads('<<<an-image:class=some classes>>>')
        self.failUnless('class="some classes"' in html)

    def test_default_template_renders_image_alt(self):
        html = render_uploads('<<<an-image:alt=the alt text>>>')
        self.failUnless('alt="the alt text"' in html)

    def test_default_template_renders_image_title_as_alt(self):
        html = render_uploads('<<<an-image>>>')
        self.failUnless('alt="An image"' in html)

    def test_default_template_renders_link(self):
        html = render_uploads('<<<some-file>>>')
        self.failUnless('<a href="/media/adminfiles/somefile.txt"' in html)
        
    def test_default_template_renders_link_class(self):
        html = render_uploads('<<<some-file:class=other classes>>>')
        self.failUnless('class="other classes"' in html)

    def test_default_template_renders_link_title(self):
        html = render_uploads('<<<some-file>>>')
        self.failUnless('Some file' in html)

    def test_default_template_renders_link_title(self):
        html = render_uploads('<<<some-file:title=Other name>>>')
        self.failUnless('Other name' in html)

    def test_render_template_filter(self):
        tpl = template.Template('{% load adminfiles_tags %}'
                                '{{ post.content|render_uploads }}')
        html = tpl.render(template.Context({
                    'post': Post(title='a post',
                                 content='<<<some-file>>>')}))
        self.assertEquals(self.templates[1].name, 'adminfiles/render.html')

    def test_render_template_filter_alt_template(self):
        tpl = template.Template(
            '{% load adminfiles_tags %}'
            '{{ post.content|render_uploads:"other.html" }}')
        html = tpl.render(template.Context({
                    'post': Post(title='a post',
                                 content='<<<some-file>>>')}))
        self.assertEquals(self.templates[1].name, 'other.html')
        
