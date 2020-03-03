import os
import urllib.parse
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt

from utils.decorators import admin_required
from utils.utils.misc import timestamp_str


def index(request):
    return render(request, 'f1l3/index.html')


@csrf_exempt
@admin_required
def admin_browse(request, path='.'):
    os.makedirs(settings.F1L3_ROOT, exist_ok=True)
    system_path = os.path.join(settings.F1L3_ROOT, path)
    is_dir = lambda name: os.path.isdir(os.path.join(system_path, name))
    files = [
        (
            name,
            is_dir(name),
            name if is_dir(name)
            else file_abs_url(os.path.join(path, name))
        )
        for name in os.listdir(system_path)
        ]
    print(files)
    if path != '.':
        files = [('../', True, '..')] + files
    return render(request, 'f1l3/browse.html', {'files': files})


f1l3_abs_url = lambda: urllib.parse.urljoin(
    settings.PRIMARY_HOST_URL,
    settings.F1L3_URL,
)


def file_abs_url(filename):
    return urllib.parse.urljoin(f1l3_abs_url(), filename)

@csrf_exempt
def upload(request):
    redirect_resp = redirect(reverse('f1l3'))
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file is None:
            return redirect_resp
        os.makedirs(settings.F1L3_ROOT, exist_ok=True)
        local_filename = f'{timestamp_str()}-{file.name}'
        file_path = os.path.join(settings.F1L3_ROOT, local_filename)
        with open(file_path, 'wb+') as path:
            for chunk in file.chunks():
                path.write(chunk)
        return render(request, 'f1l3/on_uploaded.html', {
            'url': file_abs_url(local_filename)
        })
    else:
        return redirect_resp

