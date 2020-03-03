from django.db.utils import IntegrityError
from django.utils import timezone
from site_info.models import Visitor
class StatisticsMiddleware:
    # after IP and Country middleware
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.META['IS_IP_ROUTABLE']:
            return response
        country = request.META.get('COUNTRY')
        ip = request.META['IP']
        if not country or not ip:
            return response
        if Visitor.objects.filter(visit_date=timezone.now()).filter(ip=ip).count() != 0:
            return response
        try:
            Visitor.create(country.get('code'), ip, country.get('name'))
        except IntegrityError:
            pass
        except ValueError:
            pass
        return response