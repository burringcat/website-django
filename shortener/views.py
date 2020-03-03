from urllib.parse import urlparse

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import URL


# Create your views here.


def links(request):
    return render(request, 'shortener/links.html', {'public': URL.get_public()})


def shortener(request, action=None):
    if action is None:
        return render(request, 'shortener/index.html')
    if action == 'new_url':
        return new_url(request)
    if action == 'delete_url':
        return delete_url(request)
    return HttpResponseNotFound()


@csrf_exempt
def new_url(request):
    def get_arg(name):
        return request.GET.get(name, request.POST.get(name, ''))
    user = request.user
    url = get_arg('url')
    parsed = urlparse(url)
    url_valid = parsed.scheme and parsed.netloc
    if not (url and url_valid):
        return redirect(reverse('shortener'))
    notes = get_arg('notes')
    is_encrypted = get_arg('is_encrypted') == 'yes'
    if user.is_anonymous:
        access_option = 0
    else:
        try:
            access_option = int(get_arg('access_option'))
        except ValueError:
            access_option = 3 if user.is_superuser else 0
    url = URL.objects.create(
        creator=user if not user.is_anonymous else None,
        url=url,
        notes=notes,
        access_option=access_option
    )
    if is_encrypted:
        url.encrypt()
    return render(request, 'shortener/on_created.html', {'created': url})


@csrf_exempt
def delete_url(request):
    user = request.user
    if user.is_anonymous:
        return HttpResponseForbidden()
    uid = request.POST.get('uid', request.GET.get('uid', ''))
    url = URL.get_url_by_unique_id(uid)
    if url.creater == user:
        url.delete()
    return redirect(reverse('shortener'))


def to(request):
    uid = request.POST.get('uid', request.GET.get('uid', ''))
    url = URL.get_url_by_unique_id(uid)
    if url is None:
        return HttpResponseNotFound()
    if not url.can_access(request.user):
        return HttpResponseForbidden()
    return redirect(url.url)
