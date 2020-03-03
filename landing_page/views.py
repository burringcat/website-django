from django.shortcuts import render
from django.conf import settings
# Create your views here.
def home(request):
    if settings.DEBUG is True:
        print('routing to landing page.')
    return render(request, 'landing_page/index.html')
