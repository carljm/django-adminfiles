import urllib

from django.http import HttpResponse
from django.conf import settings as django_settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from adminfiles.models import FileUpload
from adminfiles import settings

class DisableView(Exception):
    pass

class BaseView(TemplateView):
    template_name = 'adminfiles/uploader/base.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update({
            'browsers': get_enabled_browsers(),
            'field_id': self.request.GET['field'],
            'field_type': self.request.GET.get('field_type', 'textarea'),
            'ADMINFILES_REF_START': settings.ADMINFILES_REF_START,
            'ADMINFILES_REF_END': settings.ADMINFILES_REF_END,
            'JQUERY_URL': settings.JQUERY_URL
        })

        return context

    @classmethod
    def slug(cls):
        """
        Return slug suitable for accessing this view in a URLconf.

        """
        slug = cls.__name__.lower()
        if slug.endswith('view'):
            slug = slug[:-4]
        return slug

    @classmethod
    def link_text(cls):
        """
        Return link text for this view.

        """
        link = cls.__name__
        if link.endswith('View'):
            link = link[:-4]
        return link

    @classmethod
    def url(cls):
        """
        Return URL for this view.

        """
        return reverse('adminfiles_%s' % cls.slug())

    @classmethod
    def check(cls):
        """
        Raise ``DisableView`` if the configuration necessary for this
        view is not active.

        """
        pass


class AllView(BaseView):
    link_text = _('All Uploads')

    def files(self):
        return FileUpload.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        context.update({
            'files': self.files().order_by(*settings.ADMINFILES_THUMB_ORDER)
        })
        return context


class ImagesView(AllView):
    link_text = _('Images')

    def files(self):
        return super(ImagesView, self).files().filter(content_type='image')


class AudioView(AllView):
    link_text = _('Audio')

    def files(self):
        return super(AudioView, self).files().filter(content_type='audio')


class FilesView(AllView):
    link_text = _('Files')

    def files(self):
        not_files = ['video', 'image', 'audio']
        return super(FilesView, self).files().exclude(content_type__in=not_files)

class OEmbedView(BaseView):
    @classmethod
    def check(cls):
        if 'oembed' not in django_settings.INSTALLED_APPS:
            raise DisableView('OEmbed views require django-oembed or djangoembed. '
                              '(http://pypi.python.org/pypi/django-oembed, '
                              'http://pypi.python.org/pypi/djangoembed)')

class YouTubeView(OEmbedView):
    template_name = 'adminfiles/uploader/video.html'

    @classmethod
    def check(cls):
        super(YouTubeView, cls).check()
        try:
            from gdata.youtube.service import YouTubeService
        except ImportError:
            raise DisableView('YouTubeView requires "gdata" library '
                              '(http://pypi.python.org/pypi/gdata)')
        try:
            django_settings.ADMINFILES_YOUTUBE_USER
        except AttributeError:
            raise DisableView('YouTubeView requires '
                              'ADMINFILES_YOUTUBE_USER setting')

    def get_context_data(self, **kwargs):
        context = super(YouTubeView, self).get_context_data(**kwargs)
        context.update({
            'videos': self.videos()
        })
        return context

    def videos(self):
        from gdata.youtube.service import YouTubeService
        feed = YouTubeService().GetYouTubeVideoFeed(
            "http://gdata.youtube.com/feeds/videos?author=%s&orderby=updated"
            % django_settings.ADMINFILES_YOUTUBE_USER)
        videos = []
        for entry in feed.entry:
            videos.append({
                    'title': entry.media.title.text,
                    'upload_date': entry.published.text.split('T')[0],
                    'description': entry.media.description.text,
                    'thumb': entry.media.thumbnail[0].url,
                    'url': entry.media.player.url.split('&')[0],
                    })
        return videos


class FlickrView(OEmbedView):
    template_name = 'adminfiles/uploader/flickr.html'

    @classmethod
    def check(cls):
        super(FlickrView, cls).check()
        try:
            import flickrapi
        except ImportError:
            raise DisableView('FlickrView requires the "flickrapi" library '
                              '(http://pypi.python.org/pypi/flickrapi)')
        try:
            django_settings.ADMINFILES_FLICKR_USER
            django_settings.ADMINFILES_FLICKR_API_KEY
        except AttributeError:
            raise DisableView('FlickrView requires '
                              'ADMINFILES_FLICKR_USER and '
                              'ADMINFILES_FLICKR_API_KEY settings')

    def get_context_data(self, **kwargs):
        context = super(FlickrView, self).get_context_data(**kwargs)
        page = int(request.GET.get('page', 1))
        base_path = '%s?field=%s&page=' % (request.path, request.GET['field'])
        context['next_page'] = base_path + str(page + 1)
        if page > 1:
            context['prev_page'] = base_path + str(page - 1)
        else:
            context['prev_page'] = None
        context['photos'] = self.photos(page)
        return context

    def photos(self, page=1):
        import flickrapi
        user = django_settings.ADMINFILES_FLICKR_USER
        flickr = flickrapi.FlickrAPI(django_settings.ADMINFILES_FLICKR_API_KEY)
        # Get the user's NSID
        nsid = flickr.people_findByUsername(
            username=user).find('user').attrib['nsid']
        # Get 12 photos for the user
        flickr_photos = flickr.people_getPublicPhotos(
            user_id=nsid, per_page=12, page=page).find('photos').findall('photo')
        photos = []
        for f in flickr_photos:
            photo = {}
            photo['url'] = 'http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s_m.jpg' % f.attrib
            photo['link'] = 'http://www.flickr.com/photos/%s/%s' % (
                nsid, f.attrib['id'])
            photo['title'] = f.attrib['title']
            photos.append(photo)
        return photos


class VimeoView(OEmbedView):
    template_name = 'adminfiles/uploader/video.html'

    @classmethod
    def check(cls):
        super(VimeoView, cls).check()
        try:
            django_settings.ADMINFILES_VIMEO_USER
        except AttributeError:
            raise DisableView('VimeoView requires '
                              'ADMINFILES_VIMEO_USER setting')
        try:
            cls.pages = django_settings.ADMINFILES_VIMEO_PAGES
        except AttributeError:
            cls.pages = 1
        if cls.pages > 3:
            cls.pages = 3

    def get_context_data(self, **kwargs):
        context = super(VimeoView, self).get_context_data(**kwargs)
        context.update({
            'videos':self.videos()
        })
        return context

    def _get_videos(self, url):
        import urllib2
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            import elementtree.ElementTree as ET
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'django-adminfiles/0.x')
        root = ET.parse(urllib2.build_opener().open(request)).getroot()
        videos = []
        for v in root.findall('video'):
            videos.append({
                    'title': v.find('title').text,
                    'upload_date': v.find('upload_date').text.split()[0],
                    'description': v.find('description').text,
                    'thumb': v.find('thumbnail_small').text,
                    'url': v.find('url').text,
                    })
        return videos

    def videos(self):
        url = ('http://vimeo.com/api/v2/%s/videos.xml'
               % django_settings.ADMINFILES_VIMEO_USER)
        videos = self._get_videos(url)
        for page in range(2, self.pages + 1):
            page_url = "%s?page=%s" % (url, page)
            page_videos = self._get_videos(page_url)
            if not page_videos:
                break
            videos += page_videos
        return videos


def download(request):
    '''Saves image from URL and returns ID for use with AJAX script'''
    f = FileUpload()
    f.title = request.GET['title'] or 'untitled'
    f.description = request.GET['description']
    url = urllib.unquote(request.GET['photo'])
    file_content = urllib.urlopen(url).read()
    file_name = url.split('/')[-1]
    f.save_upload_file(file_name, file_content)
    f.save()
    return HttpResponse('%s' % (f.id))


_enabled_browsers_cache = None

def get_enabled_browsers():
    """
    Check the ADMINFILES_BROWSER_VIEWS setting and return a list of
    instantiated browser views that have the necessary
    dependencies/configuration to run.

    """
    global _enabled_browsers_cache
    if _enabled_browsers_cache is not None:
        return _enabled_browsers_cache
    enabled = []
    for browser_path in settings.ADMINFILES_BROWSER_VIEWS:
        try:
            view_class = import_browser(browser_path)
        except ImportError:
            continue
        if not issubclass(view_class, BaseView):
            continue
        browser = view_class
        try:
            browser.check()
        except DisableView:
            continue
        enabled.append(browser)
    _enabled_browsers_cache = enabled
    return enabled

def import_browser(path):
    module, classname = path.rsplit('.', 1)
    return getattr(__import__(module, {}, {}, [classname]), classname)
