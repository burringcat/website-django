from os import listdir
from urllib.parse import urlparse
from random import choice
from mimetypes import guess_type
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render, reverse
from utils.utils.iter_file_content import \
    iter_file_content, iter_file_to_blob_src
from utils.utils.misc import get_site_config



# Create your views here.
def random_background_image(request):
    image_path = settings.UTILS_BACKGROUND_PATH
    file_name = choice(listdir(image_path))
    full_path = image_path + file_name
    mime = guess_type(file_name)[0]
    resp = StreamingHttpResponse(iter_file_content(full_path), content_type=mime)
    resp['cache-control'] = 'no-cache, no-store, must-revalidate'
    resp['pragma'] = 'no-cache'
    resp['expires'] = '0'
    return resp
def site_config(request):
    referer = request.GET.get('referer', '/')
    referer = urlparse(referer).netloc or referer
    resp = redirect(referer)
    sc = get_site_config()
    for conf, val_range, text in sc:
        val = request.POST.get(conf, request.GET.get(conf))
        if val in val_range:
            resp.set_cookie(conf, val)
    return resp
@csrf_exempt
def image_to_blob(request):
    if not request.user or not request.user.is_superuser:
        return HttpResponse(status=403)
    file = request.FILES.get('file')
    return StreamingHttpResponse(iter_file_to_blob_src(file))
def ping(request):
    return HttpResponse("pong")

def utils(request):
    return render(request, 'utils/utils.html', {'settings': settings})

def url_shortener(request):
    return redirect(reverse('shortener'))