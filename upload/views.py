from models import FileUpload
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
import urllib, urlparse, datetime

def _render_to_response(request, template, data):
    data['flickr'] = hasattr(settings, 'FLICKR_USER')
    data['youtube'] = hasattr(settings, 'YOU_TUBE_USER')
    return render_to_response(template, data, context_instance=RequestContext(request))

@staff_member_required
def all(request):
    files = FileUpload.objects.all().order_by('-upload_date')
    return _render_to_response(request, 'upload/base.html', {'files': files, 'textarea_id': request.GET['textarea']})

@staff_member_required
def images(request):
    files = FileUpload.objects.filter(content_type = 'image').order_by('-upload_date')
    return _render_to_response(request, 'upload/base.html', {'files': files, 'textarea_id': request.GET['textarea']})

@staff_member_required
def files(request):
    not_files = ['video', 'image']
    files = FileUpload.objects.exclude(content_type__in = not_files).order_by('-upload_date')
    return _render_to_response(request, 'upload/base.html', {'files': files, 'textarea_id': request.GET['textarea']})

@staff_member_required
def youtube(request):
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET
    try:
        user = settings.YOU_TUBE_USER
        needs_user_setting = False
    except AttributeError:
        user = 'NBC'
        needs_user_setting = True
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
    return _render_to_response(request, 'upload/youtube.html', {'videos': videos, 'textarea_id': request.GET['textarea'], 'needs_user_setting': needs_user_setting})

@staff_member_required
def flickr(request):
    import flickr
    try:
        user = settings.FLICKR_USER
        flickr.API_KEY = settings.FLICKR_API_KEY
    except AttributeError:
        return HttpResponse('You need to set <tt>FLICKR_USER</tt> and <tt>FLICKR_API_KEY</tt> in your settings file. <br />&larr; <a href="/uploads/?textarea=%s">Back to all uploads.</a>' % (request.GET['textarea'],))
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
    return _render_to_response(request, 'upload/flickr.html', {'photos': photos, 'textarea_id': request.GET['textarea']})

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
