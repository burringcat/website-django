from urllib.parse import urljoin
from io import BytesIO
import weasyprint
from django.shortcuts import render, reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.core.files.base import File
from django.template.loader import get_template
from django.http import StreamingHttpResponse
from django.utils.translation import get_language, activate
from utils.utils.misc import md2h5

from .models import PortfolioProject

# Create your views here.
def get_cv_html(lang_code=None):
    if lang_code in settings.LANGUAGES_DICT.keys():
        activate(lang_code)
    lang = get_language() or 'en'
    path = dict(settings.ABOUT_ME_CV_PATHS).get(lang)
    if not path:
        return str()
    with open(path) as f:
        cv_md = f.read()
    context = {
        "pdf_url": f"{urljoin(settings.PRIMARY_HOST_URL, reverse('cv-pdf'))}?lang={lang}",
    }
    custom_context = settings.ABOUT_ME_CV_CONTEXT
    context.update({
    })
    if not context: context = {}
    cv_html = md2h5(cv_md, context=context)
    return cv_html

def cv(request):
    return render(request, 'about_me/cv.html', {
        'cv_html': get_cv_html(),
        'settings': settings,
    })
def iter_cv_pdf(lang_code=None):
    cv_html = get_cv_html(lang_code)
    page_html_template = get_template(
        'about_me/cv_printed.html'
    )
    page_html = page_html_template.render({
        'cv_html': cv_html
    })
    output = BytesIO()
    weasyprint.HTML(string=page_html).write_pdf(target=output)
    output.seek(0)
    while True:
        content = output.read(File.DEFAULT_CHUNK_SIZE)
        if not content:
            break
        yield content
def cv_pdf(request):
    lang = request.GET.get('lang')
    resp =  StreamingHttpResponse(
        iter_cv_pdf(lang)
    )
    resp['Content-Disposition'] = 'attachment; filename=cv.pdf'
    resp['Content-Type'] = 'application/pdf'
    return resp
def about_me(request):
    path = settings.ABOUT_ME_MARKDOWN
    with open(path) as f:
        aboutme_md = f.read()
    aboutme_html = md2h5(aboutme_md)
    return render(request, 'about_me/aboutme.html', {'aboutme_html': aboutme_html})

def portfolio(request):
    portfolio_projects = PortfolioProject.objects.all()
    return render(request, 'about_me/portfolio.html', {'portfolio_projects': portfolio_projects})
