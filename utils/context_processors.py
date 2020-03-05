def settings(request):
    from django.conf import settings
    return {'settings': settings}


def random_quote(request):
    from site_info.models import Quote
    return {'quote': Quote.random_quote()}