from django.shortcuts import redirect
from django.conf import settings
from utils.utils.rproxy import country_redirect
from utils.utils.misc import get_country
from ipware import get_client_ip
class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def process_request(self, request):
        if settings.DEBUG is True:
            print('processing IP middlewarex')
        ip, is_routable = get_client_ip(request)
        request.META['IP'] = ip
        request.META['IS_IP_ROUTABLE'] = is_routable
    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)
class CountryMiddleware:
    # after IPMiddleware
    def __init__(self, get_response):
        self.get_response = get_response
    def process_request(self, request):
        if settings.DEBUG is True:
            print('processing country middleware')
        if request.META['IS_IP_ROUTABLE']:
            request.META['COUNTRY'] = get_country(request.META['IP'])
    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)
class CountryRedirectMiddleware:
    # after CountryMiddleware
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG is True:
            print('processing country redirect middleware')
        should_redirect, target = country_redirect(request)
        if should_redirect is False:
            response = self.get_response(request)
        else:
            response = redirect(target)
        return response