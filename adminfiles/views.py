import urllib, urlparse, datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.conf import settings
from django.template import RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from adminfiles.models import FileUpload
from adminfiles import settings

class BaseView(object):
    def template_name(self):
        return 'adminfiles/uploader/base.html'
                
    def context(self, request):
        return {'flickr_available': hasattr(settings, 'FLICKR_USER'),
                'youtube_available': hasattr(settings, 'YOUTUBE_USER'),
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
        context = super(YoutubeView, self).context(request)
        context['videos'] = self.videos()
        return context

    def videos(self):
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            import elementtree.ElementTree as ET
        try:
            user = settings.YOUTUBE_USER
            needs_user_setting = False
        except AttributeError:
            raise Http404
        gdata_feed = "http://gdata.youtube.com/feeds/videos?author=%s&orderby=updated" % (user,)
        root = ET.parse(urllib.urlopen(gdata_feed)).getroot()
        videos = []
        for e in root.findall('{http://www.w3.org/2005/Atom}entry'):
            video = {}
            video['title'] = e.findtext('{http://www.w3.org/2005/Atom}title')
            date = e.findtext('{http://www.w3.org/2005/Atom}published').split('T')[0]
            video['upload_date'] = date
            media = e.find('{http://search.yahoo.com/mrss/}group')
            video['description'] = media.findtext('{http://search.yahoo.com/mrss/}description')
            video['thumb'] = media.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url']
            video['image'] = media.findall('{http://search.yahoo.com/mrss/}thumbnail')[-1].attrib['url']
            video['url'] = media.find('{http://search.yahoo.com/mrss/}content').attrib['url']
            videos.append(video)
        return videos

youtube_view = YouTubeView()
@staff_member_required
def youtube(request):
    return youtube_view(request)

class FlickrView(BaseView):
    def template_name(self):
        return 'adminfiles/uploader/flickr.html'
    
    def context(self, request):
        context = super(YoutubeView, self).context(request)
        context['photos'] = self.photos()
        return context

    def photos(self):
        import flickr
        try:
            user = settings.FLICKR_USER
            flickr.API_KEY = settings.FLICKR_API_KEY
        except AttributeError:
            raise Http404
        # Get first 12 photos for the user
        flickr_photos = flickr.people_getPublicPhotos(user, 12, 1)
        photos = []
        #this loop is too slow. needs caching or a better library?
        for f in flickr_photos:
            photo = {}
            photo['url'] = f.getURL('Small', 'source')
            photo['link'] = f.getURL()
            photo['title'] = f._Photo__title
            photo['upload_date'] = datetime.datetime.fromtimestamp(float(f._Photo__dateposted))
            photos.append(photo)
        return photos

flickr_view = FlickrView()
@staff_member_required
def flickr(request):
    return flickr_view(request)
    
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
