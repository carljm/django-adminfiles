import urllib, urlparse, datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured

from django.contrib.admin.views.decorators import staff_member_required

from adminfiles.models import FileUpload
from adminfiles import settings

class BaseView(object):
    def template_name(self):
        return 'adminfiles/uploader/base.html'
                
    def context(self, request):
        return {'FLICKR_USER': settings.FLICKR_USER,
                'YOUTUBE_USER': settings.YOUTUBE_USER,
                'VIMEO_USER': settings.VIMEO_USER,
                'field_id': request.GET['field'],
                'field_type': request.GET.get('field_type', 'textarea'),
                'ADMINFILES_MEDIA_URL': settings.ADMINFILES_MEDIA_URL,
                'ADMINFILES_REF_START': settings.ADMINFILES_REF_START,
                'ADMINFILES_REF_END': settings.ADMINFILES_REF_END,
                'JQUERY_URL': settings.JQUERY_URL}

    def __call__(self, request):
        return render_to_response(self.template_name(),
                                  self.context(request),
                                  context_instance=RequestContext(request))


class AllView(BaseView):
    def files(self):
        return FileUpload.objects.all()

    def context(self, request):
        context = super(AllView, self).context(request)
        context['files'] = self.files().order_by(
            *settings.ADMINFILES_THUMB_ORDER)
        return context
    
all_view = AllView()
@staff_member_required
def all(request):
    return all_view(request)

class ImagesView(AllView):
    def files(self):
        return super(ImagesView, self).files().filter(content_type='image')

images_view = ImagesView()
@staff_member_required
def images(request):
    return images_view(request)

class FilesView(AllView):
    def files(self):
        not_files = ['video', 'image']
        return super(FilesView, self).files().exclude(content_type__in=not_files)
files_view = FilesView()
@staff_member_required
def files(request):
    return files_view(request)

class YouTubeView(BaseView):
    def template_name(self):
        return 'adminfiles/uploader/youtube.html'
    
    def context(self, request):
        context = super(YouTubeView, self).context(request)
        context['videos'] = self.videos()
        return context

    def videos(self):
        try:
            from gdata.youtube.service import YouTubeService
        except ImportError:
            raise ImproperlyConfigured('The YouTube view requires the "gdata" module')
        try:
            user = settings.YOUTUBE_USER
        except AttributeError:
            raise Http404
        gdata_feed = "http://gdata.youtube.com/feeds/videos?author=%s&orderby=updated" % (user,)
        feed = YouTubeService().GetYouTubeVideoFeed(gdata_feed)
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

youtube_view = YouTubeView()
@staff_member_required
def youtube(request):
    return youtube_view(request)

class FlickrView(BaseView):
    def template_name(self):
        return 'adminfiles/uploader/flickr.html'
    
    def context(self, request):
        context = super(FlickrView, self).context(request)
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
        try:
            import flickrapi
        except ImportError:
            raise ImproperlyConfigured('django-adminfiles requires the "flickrapi" module for accessing Flickr photos')
        user = settings.FLICKR_USER
        flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY)
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

flickr_view = FlickrView()
@staff_member_required
def flickr(request):
    return flickr_view(request)


class VimeoView(BaseView):
    def template_name(self):
        return 'adminfiles/uploader/youtube.html'

    def context(self, request):
        context = super(VimeoView, self).context(request)
        context['videos'] = self.videos()
        return context

    def videos(self):
        import urllib2
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            import elementtree.ElementTree as ET
        url = 'http://vimeo.com/api/v2/%s/videos.xml' % settings.VIMEO_USER
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'django-adminfiles/0.x')
        opener = urllib2.build_opener()
        root = ET.parse(opener.open(request)).getroot()
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

vimeo_view = VimeoView()
@staff_member_required
def vimeo(request):
    return vimeo_view(request)

    
@staff_member_required
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
