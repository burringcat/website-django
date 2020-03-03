from urllib.parse import urljoin
from django.conf import settings
from django.shortcuts import reverse
def country_redirect(request):
    path_check = request.path == reverse('conf')
    header_check = request.META.get('HTTP_COUNTRY_REDIRECT') == 'no'
    cookie_check = request.COOKIES.get('country_redirect') == 'no'
    disable_redirect = path_check or header_check or cookie_check
    if disable_redirect:
        return False, None
    country_code_valid = False
    country_code_in_settings = False
    redirect_target = None
    country_code = request.META.get('COUNTRY', {}).get('code')
    if country_code:
       country_code_valid = True
    for c, target in settings.UTILS_COUNTRY_REDIRECT:
        if country_code in c:
            country_code_in_settings = True
            redirect_target = str(target)
            break
    redirect_target = urljoin(redirect_target, request.get_full_path())
    return country_code_valid and country_code_in_settings, redirect_target
